import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
from ClockDataSet import ClockDataset


# dataset has PILImage images of range [0, 1].
# We transform them to Tensors of normalized range [-1, 1]
def create_and_save_dateLoader(csv, root, trainLoaderFileName, testDataLoaderName):
    transform = transforms.Compose(
       [transforms.ToTensor(),
       #Normalize by VGG16's settings
       transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])

    dataset = ClockDataset(csv_file = csv, root_dir = root, transform = transform)
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [600, 120])
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=60,
                                          shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1,
                                         shuffle=False)
    torch.save(train_loader, trainLoaderFileName)
    torch.save(test_loader, testDataLoaderName)


create_and_save_dateLoader("digiClock.csv", "./testData", "digi_train_loader.pt", "digi_test_loader.pt")
create_and_save_dateLoader("analogClock.csv", "./testData", "analog_train_loader.pt", "analog_test_loader.pt")
create_and_save_dateLoader("kidClock.csv", "./testData", "kid_train_loader.pt", "kid_test_loader.pt")

