import torch, random
import torch.nn as LayerOfFear
import numpy as np

# PyTorch (torch) version = 2.1.2+cu118

flag = "gemastik{REDACTED}"

def convert(ip):
	flag = [float(ord(i)) for i in ip]
	normalized = torch.tensor([flag], dtype=torch.float32)
	return normalized

def wb(_in,_out):
	weight = np.round(np.random.uniform(-1, 1, (_out, _in)).astype(np.float32),2)
	bias = np.round(np.random.uniform(-1, 1, _out).astype(np.float32),2)
	return torch.from_numpy(weight), torch.from_numpy(bias)

np.random.seed(0x2024)
sigma = LayerOfFear.Sequential(
	LayerOfFear.Linear(34, 496),
	LayerOfFear.Linear(496, 128),
	LayerOfFear.Linear(128, 24)
)

layer_shapes = [(34, 496), (496, 128), (128, 24)]

for i, (input_dim, output_dim) in enumerate(layer_shapes):
	weight, bias = wb(input_dim, output_dim)
	sigma[i].weight.data = weight
	sigma[i].bias.data = bias
 
print([i.detach().numpy().tolist() for i in sigma(convert(flag))[0]])
# Output:
# [4366.66357421875, 32835.87890625, -9967.134765625, 63776.640625, 8547.775390625, 12823.4013671875, 28502.36328125, 5493.84423828125, -38881.9609375, -51316.02734375, 8324.1591796875, -26985.572265625, -28508.75, -18546.349609375, -5972.76904296875, 10322.6025390625, -7311.9833984375, -10486.3115234375, -6370.478515625, 18390.52734375, 41471.14453125, -34282.4921875, -1481.2928466796875, -51079.13671875]