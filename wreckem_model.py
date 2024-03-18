import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

class SimpleNN(nn.Module):
    def __init__(self, input_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        return x

# Load your dataset
df = pd.read_csv('data.csv')

# Assume the last column is the target and the rest are features
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert to PyTorch tensors
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

model = SimpleNN(input_size=X_train.shape[1])
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 100
for epoch in range(num_epochs):
    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    
    # Backward and optimize
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

with torch.no_grad():
    predictions = model(X_test_tensor)
    predicted_classes = predictions.round()
    accuracy = (predicted_classes.eq(y_test_tensor).sum() / float(y_test_tensor.shape[0])).item()
    print(f'Accuracy: {accuracy:.4f}')

# Convert predictions and actual labels to numpy arrays
predictions_np = predictions.numpy().flatten()  # Convert predictions to a 1D numpy array
y_test_np = y_test_tensor.numpy().flatten()  # Convert actual labels to a 1D numpy array

# Create a DataFrame with predictions and actual labels
results_df = pd.DataFrame({
    'Actual': y_test_np,
    'Predicted': predictions_np
})

# Save the DataFrame to a CSV file
results_df.to_csv('predictions_results.csv', index=False)



