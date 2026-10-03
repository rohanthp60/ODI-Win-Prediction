import torch
from torch.utils.data import DataLoader
from data.filter import load_data, filter_with_nation_winners
from data.preprocess import DatasetLoad
from data.dataset import SecondInningsDataset
from models.baseline import BaselineModel
from train import train_model, evaluate

batch_size = 128
epochs = 30
learning_rate = 0.003
mid_dim = 512
gamma = 0.8
dropout = 0
device = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)
print(f"Using device: {device}")

loaded_data = filter_with_nation_winners(load_data())
dataset = DatasetLoad(loaded_data)
_, second_innings = dataset.get_data_non_sequential(train_test_split=True)
train_data, test_data = [SecondInningsDataset(data) for data in second_innings.values()]
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

model = BaselineModel(input_dim=3, mid_dim=mid_dim, dropout=dropout).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=gamma)

model, train_losses, eval_losses = train_model(model, train_loader, test_loader, optimizer, scheduler, epochs, device)
final_train_loss, final_eval_loss = evaluate(model, train_loader, device), evaluate(model, test_loader, device)
print(f"\n\nFinal train loss: {final_train_loss:.4f}, Final eval loss: {final_eval_loss:.4f}")
