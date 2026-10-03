from tqdm import tqdm
import torch

def train_step(model, batch, optimizer, device):
    model.train()
    optimizer.zero_grad()
    inputs = batch["input"].to(device)
    labels = batch["labels"].float().unsqueeze(1).to(device)
    _, loss = model(inputs, labels)
    loss.backward()
    optimizer.step()
    return loss.item()

def evaluate(model, test_loader, device):
    model.eval()
    total_loss = 0.0
    progress_bar = tqdm(
        test_loader,
        desc="Evaluating",
        unit="batch",
        leave=False,
        dynamic_ncols=True,
    )
    with torch.no_grad():
        for batch in progress_bar:
            inputs = batch["input"].to(device)
            labels = batch["labels"].float().unsqueeze(1).to(device)
            _, loss = model(inputs, labels)
            total_loss += loss.item()
    return total_loss / len(test_loader)

def train_model(model, train_loader, test_loader, optimizer, scheduler, epochs, device):
    model.to(device)
    training_progress = tqdm(
        total=epochs * len(train_loader),
        desc="Training",
        unit="step",
        dynamic_ncols=True,
    )
    train_losses = []
    eval_losses = []
    epoch_summaries = []
    for epoch in range(1, epochs + 1):
        model.train()
        total_train_loss = 0.0

        for batch in train_loader:
            loss = train_step(model, batch, optimizer, device)
            total_train_loss += loss
            training_progress.update(1)
        train_losses.append(total_train_loss / len(train_loader))

        train_loss = total_train_loss / len(train_loader)
        eval_loss = evaluate(model, test_loader, device)
        eval_losses.append(eval_loss)
        epoch_summaries.append(
            f"Epoch {epoch} / {epochs} | "
            f"train_loss={train_loss:.4f} | test_loss={eval_loss:.4f}"
        )
        if scheduler:
            scheduler.step()
    training_progress.close()
    print("\n".join(epoch_summaries))
    return model, train_losses, eval_losses