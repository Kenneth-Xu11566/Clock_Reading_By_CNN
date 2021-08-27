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
from TransClockDataSet import TransClockDataset
# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyper-parameters
num_epochs = 200
batch_size = 60
learning_rate = 0.001
momentum = 0.9


train_loader = torch.load("trans_digi_train_loader.pt")

#Prepare and Identity to replace the original
class Identity(nn.Module):
    def __init__(self):
        super(Identity, self).__init__()
        
    def forward(self, x):
        return x


#load VGG16 model
convModel = torchvision.models.vgg16(pretrained=True)
for param in convModel.parameters():
    param.requires_grad = False
    
convModel.avgpool = Identity()
convModel.classifier = Identity()
convModel.to(device)

fhm_list = []
for i, (images, hours, minutes) in enumerate(train_loader):
        # origin shape: [4, 3, 32, 32] = 4, 3, 1024
        # input_layer: 3 input channels, 6 output channels, 5 kernel size
        images = images.to(device)
        hours = hours.to(device)
        minutes = minutes.to(device)
        
        outFeatures = convModel(images)
        fhm_list.append([outFeatures, hours, minutes])
        print(len(fhm_list))


newDataSet = TransClockDataset(fhm_list);
new_train_loader = torch.utils.data.DataLoader(newDataSet, batch_size, shuffle=True)

#new_train_loader = torch.load("new_train_loader.pt")
#torch.save(new_train_loader, "new_train_loader.pt")

#Prepare a full connection model that includes the vgg16 conv layers.
class ClockHourMinute(nn.Module):
    def __init__(self):
        super(ClockHourMinute, self).__init__()
        self.hfc1 = nn.Linear(25088, 144)
        self.hfc2 = nn.Linear(144, 12)
        self.mfc1 = nn.Linear(25088, 100)
        self.mfc2 = nn.Linear(100, 1)

    def forward(self, x):
        sum0 = .0
        numel0 = 0
        x = torch.flatten(x,1)
        # full connection for hour
        h = F.relu(self.hfc1(x))

        sum0 += torch.sum(torch.abs(h))
        numel0 += torch.numel(h)

        h = self.hfc2(h)

        sum0 += torch.sum(torch.abs(h))
        numel0 += torch.numel(h)

        # full connection for minute
        m = F.relu(self.mfc1(x))

        sum0 += torch.sum(torch.abs(m))
        numel0 += torch.numel(m)

        m = self.mfc2(m)
        
        sum0 += torch.sum(torch.abs(m))
        numel0 += torch.numel(m)

        avg0 = sum0/numel0
        return (h, m[:,0], avg0)

model=ClockHourMinute()

criterion1 = nn.CrossEntropyLoss()
criterion2 = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum = momentum)

n_total_steps = len(new_train_loader)
for epoch in range(num_epochs):
    for i, (features, hours, minutes) in enumerate(new_train_loader):
        features = features.to(device)
        hours = hours.to(device)
        minutes = minutes.to(device)
        # Forward pass
        output_hours, output_minutes, avg0 = model(features)
        torch._assert(output_minutes.size() == minutes.size(), "Size mismatch on minutes output")
        loss = criterion1(output_hours, hours) + criterion2(output_minutes, minutes)
        
        #loss = criterion2(output_minutes, minutes)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print (f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{n_total_steps}], Loss: {loss.item():.4f}, avg0:{avg0:.8f}')

print('Finished Training')
PATH = './TransDigital.pth'
torch.save(model.state_dict(), PATH)

