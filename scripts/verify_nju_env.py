"""Check NJU Python/native dependencies offline; never download model weights."""

from importlib.metadata import version
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".cache/nju-validation"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache/matplotlib"))
    import torch
    import accelerate
    import graphviz
    import ipykernel
    import matplotlib
    import numpy
    import pytest
    import safetensors
    from tokenizers import Tokenizer, models, pre_tokenizers
    from torchviz import make_dot
    from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedTokenizerFast, Qwen3Config, TextStreamer

    packages = ("torch", "transformers", "tokenizers", "accelerate", "safetensors",
                "torchviz", "graphviz", "pytest", "ipykernel", "numpy", "matplotlib")
    versions = {name: version(name) for name in packages}
    print("Python:", sys.executable, flush=True)
    print(json.dumps(versions, indent=2), flush=True)
    dot_version = subprocess.check_output(["dot", "-V"], stderr=subprocess.STDOUT, text=True).strip()
    print(dot_version, flush=True)

    torch.manual_seed(42)
    # A tiny random Qwen3 tests the architecture and loading APIs, not the real weights.
    config = Qwen3Config(vocab_size=64, hidden_size=32, intermediate_size=64,
                         num_hidden_layers=1, num_attention_heads=4,
                         num_key_value_heads=2, head_dim=8, max_position_embeddings=64,
                         pad_token_id=0, eos_token_id=2)
    model = AutoModelForCausalLM.from_config(config).eval()
    inputs = torch.tensor([[1, 3, 4, 2]])
    output = model(input_ids=inputs, labels=inputs)
    svg = make_dot(output.loss, params=dict(model.named_parameters())).pipe(format="svg")
    assert b"<svg" in svg
    (OUT / "autograd.svg").write_bytes(svg)
    output.loss.backward()
    assert torch.isfinite(output.loss) and any(p.grad is not None for p in model.parameters())

    with tempfile.TemporaryDirectory(dir=OUT) as folder:
        tokenizer = Tokenizer(models.WordLevel({"[PAD]": 0, "[UNK]": 1, "[EOS]": 2,
                                                "hello": 3, "NJU": 4}, unk_token="[UNK]"))
        tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
        fast = PreTrainedTokenizerFast(tokenizer_object=tokenizer, unk_token="[UNK]",
                                      pad_token="[PAD]", eos_token="[EOS]",
                                      model_input_names=["input_ids", "attention_mask"])
        fast.save_pretrained(folder)
        model.save_pretrained(folder, safe_serialization=True)
        loaded_tokenizer = AutoTokenizer.from_pretrained(folder, local_files_only=True)
        assert loaded_tokenizer.encode("hello NJU") == [3, 4]
        loaded = AutoModelForCausalLM.from_pretrained(folder, local_files_only=True,
                                                     device_map="auto", dtype=torch.float32).eval()
        batch = loaded_tokenizer("hello NJU", return_tensors="pt").to(loaded.device)
        with torch.inference_mode():
            generated = loaded.generate(**batch, max_new_tokens=2, do_sample=False)
        assert generated.shape[1] > batch["input_ids"].shape[1]

    result = dict(python=sys.executable, versions=versions, graphviz_native=dot_version,
                  mps_available=torch.backends.mps.is_available(),
                  checks=["imports", "Qwen3 forward/backward", "tokenizer roundtrip",
                          "safetensors save/load", "device_map=auto", "generation", "Graphviz SVG"],
                  pretrained_weights_tested=False)
    (OUT / "environment.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: imports, tiny Qwen3, tokenizer, Accelerate loading, generation, Graphviz.", flush=True)
    print("Real Qwen/Qwen3-0.6B weights are separate and were not downloaded by this check.")


if __name__ == "__main__":
    main()
