from typing import Tuple, Optional

import torch
import torch.nn.functional as F


def matmul_with_importance(
    input: torch.Tensor,
    weight: torch.Tensor,
    probs: torch.Tensor,
    grad_output: Optional[torch.Tensor] = None,
    num_heads: int = 1,
    top_p: float = 1.0,
    top_k: Optional[int] = None,
) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[torch.Tensor]]:
    """matmul input and weight and return output (with optional grad_input, grad_weight whenever grad_output is given) 
    where only the important elements of the input tensor can be computed and gathered to the output tensor
    decided by the importance probability tensor, tuned by top_p and top_k
    
    Args:
        input (torch.Tensor): input tensor in the range of [-1, 1], with shape: [batch_size, seq_len, hidden_size]
        weight (torch.Tensor): weight tensor in the range of [-1, 1], with shape: [hidden_size, embed_size]
        probs (torch.Tensor): probability tensor in the range of [0, 1], with shape: [batch_size, seq_len]
        grad_output (Optional[torch.Tensor], optional): gradient for the output tensor, with shape: [t, hidden_size]. Defaults to None.
        num_heads (int): number of heads to split hidden_size
        top_p (float, [0., 1.]): only the elements with the probability equal or higher than top_p are important ones
        top_k (int, [1, ..., seq_len], optional): only the elements with the top_k highest probability are important ones
    
    Returns:
        output (torch.Tensor): output tensor, with shape: [t, num_heads, embed_size]
        grad_input (torch.Tensor, optional): gradient for the input tensor if grad_output is given, otherwise None
        grad_weight (torch.Tensor, optional): gradient for the weight tensor if grad_output is given, otherwise None
    """
    # raise NotImplementedError("TODO: Assignment0 - Task1")
    
    # step 0: 拿到输入与embeddedweight的各个维数
    batch_size, seq_len, hidden_size = input.shape
    _, embed_size = weight.shape
    head_dim = hidden_size //num_heads

    # Step 1: multi-head split
    # torch.split(input, split_size_or_sections, dim=0), the tail of the parameter is the 
    # position that we want to split, and the split_size_or_sections is the size of each split
    A_head = torch.split(input, head_dim, dim=-1)  # A_head: tuple of tensors, each with shape [batch_size, seq_len, head_dim]
    B_head = torch.split(weight, head_dim, dim=0)  # B_head: tuple of tensors, each with shape [head_dim, embed_size]

    # Step 2: compute the importance mask
    # 1. top_p mask, the elements with the probability equal or higher than top_p are important ones
    top_p_mask = probs >= top_p  # shape: [batch_size, seq_len], dtype: bool
    # 2. top_k mask
    if top_k is not None:
        # get the top_k indices along the seq_len dimension
        top_k_indices = torch.topk(probs, k=top_k, dim=-1).indices  # shape: [batch_size, top_k]
        # create a mask with the same shape as probs, initialized to False
        top_k_mask = torch.zeros_like(probs, dtype=torch.bool)  # shape: [batch_size, seq_len], dtype: bool
        # set the top_k indices to True
        top_k_mask.scatter_(-1, top_k_indices, True)  # shape: [batch_size, seq_len], dtype: bool
        # combine the masks
        importance_mask = top_p_mask & top_k_mask  # shape: [batch_size, seq_len], dtype: bool
    else:
        importance_mask = top_p_mask  # shape: [batch_size, seq_len], dtype: bool

    # Step 3: compute the output tensor
    output = torch.zeros(batch_size, num_heads, embed_size, device=input.device, dtype=input.dtype)  # shape: [batch_size, num_heads, embed_size]
    for i in range(num_heads):
        # get the i-th head of A and B
        A_i = A_head[i]  # shape: [batch_size, seq_len, head_dim]
        B_i = B_head[i]  # shape: [head_dim, embed_size]
        # apply the importance mask to A_i
        A_i_masked = A_i * importance_mask.unsqueeze(-1)  # shape: [batch_size, seq_len, head_dim]
        # compute the output for the i-th head
        output[:, i, :] = torch.matmul(A_i_masked.transpose(1, 2), B_i)  # shape: [batch_size, embed_size]

    # Step 4: compute the gradients if grad_output is given
    if grad_output is not None:
        grad_input = torch.zeros_like(input)  # shape: [batch_size, seq_len, hidden_size]
        grad_weight = torch.zeros_like(weight)  # shape: [hidden_size, embed_size]
        for i in range(num_heads):
            # get the i-th head of A and B
            A_i = A_head[i]  # shape: [batch_size, seq_len, head_dim]
            B_i = B_head[i]  # shape: [head_dim, embed_size]
            # apply the importance mask to A_i
            A_i_masked = A_i * importance_mask.unsqueeze(-1)  # shape: [batch_size, seq_len, head_dim]
            # compute the gradient for the i-th head
            grad_input[:, :, i * head_dim:(i + 1) * head_dim] = torch.matmul(grad_output[:, i, :], B_i.transpose(0, 1)) * importance_mask.unsqueeze(-1)  # shape: [batch_size, seq_len, head_dim]
            grad_weight[i * head_dim:(i + 1) * head_dim, :] = torch.matmul(A_i_masked.transpose(1, 2), grad_output[:, i, :])  # shape: [head_dim, embed_size]

    else:
        grad_input = None
        grad_weight = None

    return output, grad_input, grad_weight
