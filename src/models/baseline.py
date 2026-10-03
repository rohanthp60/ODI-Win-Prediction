import torch.nn as nn

class BaselineModel(nn.Module):
    def __init__(self, input_dim, mid_dim=16, dropout=0):
        super(BaselineModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, mid_dim // 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mid_dim // 4, mid_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mid_dim, mid_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mid_dim, mid_dim // 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(mid_dim // 4, 1),
        )

    def compute_loss(self, pred, labels):
        criterion = nn.BCEWithLogitsLoss()
        return criterion(pred, labels)
    
    def forward(self, x, y):
        pred = self.fc(x)
        loss = self.compute_loss(pred, y)
        return pred, loss
    