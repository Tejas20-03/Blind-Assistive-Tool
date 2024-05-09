import cv2
import torch
from PIL import Image
from torchvision import transforms
from torchvision import models

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
cap.set(cv2.CAP_PROP_FPS, 36)

ret, image = cap.read()
# convert opencv output from BGR to RGB
image = image[:, :, [2, 1, 0]]


preprocess = transforms.Compose([
    # convert the frame to a CHW torch tensor for training
    transforms.ToTensor(),
    # normalize the colors to the range that mobilenet_v2/3 expect
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
input_tensor = preprocess(image)
# The model can handle multiple images simultaneously so we need to add an
# empty dimension for the batch.
# [3, 224, 224] -> [1, 3, 224, 224]
input_batch = input_tensor.unsqueeze(0)

torch.backends.quantized.engine = 'qnnpack'

net = models.quantization.mobilenet_v2(pretrained=True, quantize=True)

net = torch.jit.script(net)