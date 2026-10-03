from torch.utils.data import Dataset
import torch

class SecondInningsDataset(Dataset):
    def __init__(self, data, rescale=False):
        self.data = data
        self.rescale_values = {
            "runs": 300,
            "wickets": 10,
            "balls": 300
        }
        self.rescale = rescale

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_item = self.data[idx]
        input_features = torch.tensor([data_item[k] / (self.rescale_values[k] if self.rescale else 1)
                                       for k in ["runs", "wickets", "balls"]], dtype=torch.float32)
        labels = torch.tensor(data_item["labels"])
        return { "input": input_features, "labels": labels }