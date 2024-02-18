import torch  # 如正常则静默
from torch.backends import cudnn  # 如正常则静默

a = torch.Tensor([1.])  # 如正常则静默
# 如正常则返回"tensor([ 1.], device='cuda:0')"
print(a.cuda())
# 如正常则返回 "True"
print(cudnn.is_acceptable(a.cuda()))
