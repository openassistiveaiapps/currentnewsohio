import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import random

# ========================
# STEP 1: Load MNIST Data
# ========================
transform = transforms.ToTensor()

train_dataset = datasets.MNIST(
    root="data",
    train=True,
    transform=transform,
    download=True
)
test_dataset = datasets.MNIST(
    root="data",
    train=False,
    transform=transform,
    download=True
)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

print(f"Train size: {len(train_dataset)}, Test size: {len(test_dataset)}")

# ========================
# STEP 2: Visualize Samples
# ========================
images, labels = next(iter(train_loader))
plt.figure(figsize=(10,2))
for i in range(6):
    plt.subplot(1,6,i+1)
    plt.imshow(images[i].squeeze(), cmap='gray')
    plt.title(f"Label: {labels[i]}")
    plt.axis('off')
plt.show()

# ========================
# STEP 3: Define Neural Network
# ========================
class NeuralNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.flatten(x)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = NeuralNet()
print(model)

# ========================
# STEP 4: Loss and Optimizer
# ========================
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# ========================
# STEP 5: Training Loop
# ========================
epochs = 5
for epoch in range(epochs):
    total_loss = 0
    for images, labels in train_loader:
        outputs = model(images)
        loss = loss_fn(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    avg_loss = total_loss / len(train_loader)
    print(f"Epoch [{epoch+1}/{epochs}] - Loss: {avg_loss:.4f}")

# ========================
# STEP 6: Evaluation
# ========================
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total
print(f"Test Accuracy: {accuracy:.2f}%")

# ========================
# STEP 7: Test on Single Image
# ========================
idx = random.randint(0, len(test_dataset)-1)
img, label = test_dataset[idx]
with torch.no_grad():
    output = model(img.unsqueeze(0))
    pred = output.argmax(1).item()

plt.imshow(img.squeeze(), cmap='gray')
plt.title(f"Predicted: {pred}, Actual: {label}")
plt.axis('off')
plt.show()
