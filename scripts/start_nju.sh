#!/bin/bash
# Start the shared environment with the local NJU model paths configured.
set -euo pipefail
NJU_PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$NJU_PROJECT_ROOT"
if [[ ! -x .venv/bin/python ]]; then
  echo '缺少 .venv，请按 docs/setup/README.md 创建环境；NJU 运行说明见 library/nju-llm-2026/README.md。' >&2
  exit 1
fi
export LECTURE4_MODEL_PATH="$NJU_PROJECT_ROOT/.cache/llm-course/qwen3-tokenizer"
export LECTURE4_TOKENIZER_PATH="$LECTURE4_MODEL_PATH"
if [[ ! -f "$LECTURE4_MODEL_PATH/model.safetensors" ]]; then
  echo '请先运行 .venv/bin/python scripts/download_nju_model.py 下载模型。' >&2
  exit 1
fi
export HF_HOME="$NJU_PROJECT_ROOT/.cache/huggingface"
export PATH="$NJU_PROJECT_ROOT/.venv/bin:$PATH"
exec .venv/bin/python -m jupyter lab "$@"
