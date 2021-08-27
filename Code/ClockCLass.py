import torch
import torch.nn as nn
import torch.nn.functional as F
class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 50, 5, 2)
        self.pool1 = nn.MaxPool2d(2,2)
        self.conv2 = nn.Conv2d(50, 100, 3)
        self.pool2 = nn.MaxPool2d(2,1)
        self.conv3 = nn.Conv2d(100,150,3)
        self.pool3 = self.pool2
        self.conv4 = nn.Conv2d(150,200,3)
        self.pool4 = self.pool3
        self.conv5 = nn.Conv2d(200,300,3)
        self.dropout = nn.Dropout(0.4)
        self.hfc1 = nn.Linear(300 * 28 * 28, 144)
        self.hfc2 = nn.Linear(144, 12)
        self.mfc1 = nn.Linear(300*28*28, 100)
        self.mfc2 = nn.Linear(100, 1)
        

    def forward(self, x):
        sum0 = .0
        sum1 = .0
        numel0 = 0
        numel1 = 0
        # convolution
        x = F.relu(self.conv1(x))
        x = self.pool1(x)

        sum0 += torch.sum(torch.abs(x))
        numel0 += torch.numel(x)

        x = F.relu(self.conv2(x))
        x = self.pool2(x)

        sum0 += torch.sum(torch.abs(x))
        numel0 += torch.numel(x)

        x = F.relu(self.conv3(x))
        x = self.pool3(x)

        sum0 += torch.sum(torch.abs(x))
        numel0 += torch.numel(x)

        x = F.relu(self.conv4(x))
        x = self.pool4(x)

        sum0 += torch.sum(torch.abs(x))
        numel0 += torch.numel(x)

        x = F.relu(self.conv5(x))

        sum0 += torch.sum(torch.abs(x))
        numel0 += torch.numel(x)

        x = self.dropout(x)

        sum0 += torch.sum(torch.abs(x))
        numel0 += torch.numel(x)

        x = torch.flatten(x,1)

        # full connection for hour
        h = F.relu(self.hfc1(x))

        sum0 += torch.sum(torch.abs(h))
        numel0 += torch.numel(h)
        sum1 += torch.sum(torch.abs(h))
        numel1 += torch.numel(h)

        h = self.hfc2(h)

        sum0 += torch.sum(torch.abs(h))
        numel0 += torch.numel(h)
        sum1 += torch.sum(torch.abs(h))
        numel1 += torch.numel(h)

        # full connection for minute
        m = F.relu(self.mfc1(x))

        sum0 += torch.sum(torch.abs(m))
        numel0 += torch.numel(m)
        sum1 += torch.sum(torch.abs(m))
        numel1 += torch.numel(m)

        m = self.mfc2(m)
        
        sum0 += torch.sum(torch.abs(m))
        numel0 += torch.numel(m)
        sum1 += torch.sum(torch.abs(m))
        numel1 += torch.numel(m)

        avg0 = sum0/numel0
        avg1 = sum1/numel1
     
        return (h, m[:,0], avg0, avg1)
