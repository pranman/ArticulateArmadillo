import ctypes
print("cuDNN version:", ctypes.CDLL("cudnn64_8.dll").cudnnGetVersion())

import torch
print("PyTorch CUDA available:", torch.cuda.is_available())
print("Device count:", torch.cuda.device_count())
print("Current device:", torch.cuda.current_device())
print("Device name:", torch.cuda.get_device_name(torch.cuda.current_device()))
