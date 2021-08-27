import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
from ClockCLass import ConvNet
from ClockDataSet import ClockDataset
# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper-parameters
num_epochs = 200
batch_size = 60
learning_rate = 0.001
momentum = 0.9

train_loader = torch.load("digi_train_loader.pt")

model = ConvNet().to(device)

criterion1 = nn.CrossEntropyLoss()
criterion2 = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum = momentum)

n_total_steps = len(train_loader)
for epoch in range(num_epochs):
    for i, (images, hours, minutes) in enumerate(train_loader):
        images = images.to(device)
        hours = hours.to(device)
        minutes = minutes.to(device)
        
        # Forward pass
        output_hours, output_minutes, avg0, avg1 = model(images)
        torch._assert(output_minutes.size() == minutes.size(), "Size mismatch on minute output")
        loss = criterion1(output_hours, hours) + criterion2(output_minutes, minutes)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print (f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{n_total_steps}], Loss: {loss.item():.4f}, avg0:{avg0:.8f}, avg1:{avg1:.8f}')

print('Finished Training')
PATH = './digital.pth'
torch.save(model.state_dict(), PATH)

