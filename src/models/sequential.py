import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1):
        super(LSTMModel, self).__init__()
        self.fc_input = nn.Linear(3, input_size)  # Adjust input size to match the LSTM input
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True, num_layers=num_layers)
        self.fc = nn.Linear(hidden_size, 1)
        self.loss_function = nn.BCEWithLogitsLoss(reduction='none')  

    def compute_loss(self, output, labels, loss_mask):
        loss = self.loss_function(output, labels)
        masked_loss = loss * loss_mask
        return masked_loss.sum() / loss_mask.sum()

    def forward(self, innings, loss_mask, labels):
        innings = self.fc_input(innings)
        lstm_out, _ = self.lstm(innings)
        output = self.fc(lstm_out)
        loss = self.compute_loss(output.squeeze(-1), labels, loss_mask)
        return {'loss': loss, 'logits': output.squeeze(-1)}

class LSTMModelWithTeamEmbedding(LSTMModel):
    def __init__(self, input_size, hidden_size, num_layers=1, num_teams=0, embedding_dim=8):
        super(LSTMModelWithTeamEmbedding, self).__init__(input_size, hidden_size, num_layers)
        self.team_embedding = nn.Embedding(num_teams, embedding_dim)
        self.compute_team_features = nn.Linear(2 * embedding_dim, hidden_size)
        self.fc_input = nn.Linear(3 + 2 * embedding_dim, input_size)  # Adjust input size to include team embeddings

    def forward(self, innings, loss_mask, labels):
        batting_team = innings[:, :, -2].long()
        bowling_team = innings[:, :, -1].long()
        batting_emb = self.team_embedding(batting_team)
        bowling_emb = self.team_embedding(bowling_team)
        team_features = torch.cat([batting_emb, bowling_emb], dim=-1)
        team_features = self.compute_team_features(team_features)
        team_features = team_features.permute(1, 0, 2)  # Adjust dimensions to match innings

        state_features = innings[:, :, :-2]

        lstm_out, _ = self.lstm(state_features, ())
        output = self.fc(lstm_out)
        loss = self.compute_loss(output.squeeze(-1), labels, loss_mask)
        return {'loss': loss, 'logits': output.squeeze(-1)}