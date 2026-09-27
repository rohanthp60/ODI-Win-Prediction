import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.state_projector = nn.Linear(3, 16)
        self.state_ffn = nn.Sequential(
            nn.Linear(16, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )
        self.loss_fn = nn.BCEWithLogitsLoss()

    def forward(self, runs, wickets, balls, labels):
        x = torch.stack([runs, wickets, balls], dim=1).float()
        x = self.state_projector(x)
        x = self.state_ffn(x)

        logits = x.squeeze(1)
        loss = self.loss_fn(logits, labels.float())
        return {"loss": loss, "logits": logits}

class SimpleModelWithTeamEmbedding(SimpleModel):
    def __init__(self, num_teams):
        super().__init__()
        self.team_embedding = nn.Embedding(num_teams, 8)
        self.ffn = nn.Sequential(
            nn.Linear(16 + 16, 64),  # 3 state features + 16 team embedding features
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, batting_team, bowling_team, runs, wickets, balls, labels):
        batting_emb = self.team_embedding(batting_team)
        bowling_emb = self.team_embedding(bowling_team)
        team_features = torch.cat([batting_emb, bowling_emb], dim=1)

        x = torch.stack([runs, wickets, balls], dim=1).float()
        x = self.state_projector(x.float())
        x = torch.cat([x, team_features], dim=1)  # Concatenate team embeddings with state features
        x = self.ffn(x)

        logits = x.squeeze(1)
        loss = self.loss_fn(logits, labels.float())
        return {"loss": loss, "logits": logits}