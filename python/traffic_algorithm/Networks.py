import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions.categorical import Categorical

class NeuralNetwork(nn.Module):
    def __init__(self, input_dims, lr, fc_dims=32):
        super(NeuralNetwork, self).__init__()
        self.model = nn.Sequential( # network
            nn.Linear(input_dims, fc_dims),
            nn.Mish(),
            nn.Linear(fc_dims, fc_dims),
            nn.Mish(),
            nn.Linear(fc_dims, fc_dims),
            nn.Mish(),
            nn.Linear(fc_dims, 1)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=lr) # optim
        self.device = torch.device("mps") # declare device
        self.to(self.device) # store class in device
    
    def forward(self, state, train_mode=True): # forward propogation
        if train_mode: # train mode while training
            self.model.train()
        else: # eval mode
            self.model.eval()
        value = self.model(state)
        return value

    def load(self, model_path): # load model
        self.load_state_dict(torch.load(model_path))

    def save_model(self, model_path): # save model
        torch.save(self.model, model_path + "_TrafficControl.pt")