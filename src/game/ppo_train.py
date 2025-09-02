import torch
import torch.distributed
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
import random
import numpy as np
import matplotlib.pyplot as plt
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader



def orthogonal_init(layer, gain=1.0):
    nn.init.orthogonal_(layer.weight, gain=gain)
    nn.init.constant_(layer.bias, 0)


class Act_Net(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.embedding= nn.Embedding(num_embeddings=100, embedding_dim=14)
        
        self.action = nn.Sequential(
            nn.Linear(state_size, 272),
            nn.Tanh(),
            nn.Linear(272, 309),
            nn.Tanh(),
            nn.Linear(309, action_size),
            nn.Softmax(dim=-1)
        )
        #orthogonal_init(self.embedding_card)
        orthogonal_init(self.action[0])
        orthogonal_init(self.action[2])
        orthogonal_init(self.action[4],gain=0.1)
        

    def forward(self,num_state,cards_id):
        #print(cards_id)
        embedding_value=self.embedding(cards_id)
        #print(embedding_value)
        embedding_flatten=embedding_value.reshape(embedding_value.size(0), -1)
        #print(embedding_flatten.shape,num_state.shape)
        
        x = torch.cat((num_state, embedding_flatten), dim=1)

        #print(x.shape)
        action=self.action(x)
        #value=self.value(x)
        dist=torch.distributions.Categorical(action)
        return dist,dist.entropy()
    
    def predict(self,num_state,cards_id):
        
        embedding_value=self.embedding(cards_id)
        #print(cards_id,embedding_value)
        #print(embedding_value)
        embedding_flatten=embedding_value.reshape(embedding_value.size(0), -1)
        #print(embedding_flatten)
        x = torch.cat((num_state, embedding_flatten), dim=1)
        
        #print(x.shape)

        return self.action(x)
    

class Val_Net(nn.Module):
    def __init__(self, state_size):
        super().__init__()
        self.embedding = nn.Embedding(num_embeddings=100, embedding_dim=14)
        self.value=nn.Sequential(
            nn.Linear(state_size, 272),
            nn.Tanh(),
            nn.Linear(272, 309),
            nn.Tanh(),
            nn.Linear(309, 1)
        )
        #orthogonal_init(self.embedding)
        orthogonal_init(self.value[0])
        orthogonal_init(self.value[2])
        orthogonal_init(self.value[4])
    def forward(self,num_state,cards_id):
        
        embedding_value=self.embedding(cards_id)
        
        embedding_flatten=embedding_value.reshape(embedding_value.size(0), -1)
        #print(embedding_flatten.shape,num_state.shape)
        x = torch.cat((num_state, embedding_flatten), dim=1)
        
        value=self.value(x)
        
        return value

class RunningMeanStd:
    def __init__(self, shape):  # shape:the dimension of input data
        self.n = 0
        self.mean = np.zeros(shape)
        self.S = np.zeros(shape)
        self.std = np.sqrt(self.S)

    def update(self, x):
        x = np.array(x)
        self.n += 1
        if self.n == 1:
            self.mean = x
            self.std = x
        else:
            old_mean = self.mean.copy()
            self.mean = old_mean + (x - old_mean) / self.n
            self.S = self.S + (x - old_mean) * (x - self.mean)
            self.std = np.sqrt(self.S / self.n )

class Normalization:#Trick 2—State Normalization
    def __init__(self, shape):
        self.running_ms = RunningMeanStd(shape=shape)

    def __call__(self, x, update=True):
        #print(x)
        # Whether to update the mean and std,during the evaluating,update=Flase
        x=np.array(x)
        if update:  
            self.running_ms.update(x)
        x = (x - self.running_ms.mean) / (self.running_ms.std + 1e-8)
        return x
    

class RewardScaling:#Trick 4—Reward Scaling

    def __init__(self, gamma):
        self.shape = 1  # reward shape=1
        self.gamma = gamma  # discount factor
        self.running_ms = RunningMeanStd(shape=self.shape)
        
        self.R = np.zeros(self.shape)

    def __call__(self, x):
        self.R = self.gamma * self.R + x
        self.running_ms.update(self.R)
        x = x / (self.running_ms.std + 1e-8)  # Only divided std
        return x[0]

    def reset(self):  # When an episode is done,we should reset 'self.R'
        self.R = np.zeros(self.shape)


class Agent_PPO:

    fig, ax = plt.subplots()

    def __init__(self,state_size, action_size,name="Agent",train=True) -> None:
        self.normalization=Normalization(state_size)
        self.reward_scale=RewardScaling(0.99)
        self.gamma=0.99
        self.lambd=0.95
        self.clip_para=0.2
        self.epochs=15
        self.max_step=3000000
        self.total_step=0
        self.lr=3e-6
        self.name=name
        

        self.state_num=[]
        self.state_id=[]
        self.reward=[]
        self.action=[]
        self.next_state_num=[]
        self.next_state_id=[]
        self.done=[]


        
        if torch.backends.mps.is_available():
            print("mps")
            self.device=torch.device("mps")
        elif torch.cuda.is_available():
            print("cuda")
            self.device=torch.device("cuda")
        else:
            print("cpu")
            self.device=torch.device("cpu")
        self.action_size=action_size
        self.model_act=Act_Net(state_size, action_size).to(self.device)
        self.model_val=Val_Net(state_size).to(self.device)
        self.MSEloss=nn.MSELoss()
        self.opti_act=optim.Adam(self.model_act.parameters(),lr=self.lr, eps=1e-5)#Trick 9—Adam Optimizer Epsilon Parameter
        self.opti_val=optim.Adam(self.model_val.parameters(),lr=self.lr, eps=1e-5)
        self.scheduler_action = StepLR(self.opti_act, step_size=50, gamma=0.99)
        self.scheduler_value = StepLR(self.opti_val, step_size=50, gamma=0.99)

        if train:
            self.init_graph()
        else:
            self.model_act.eval()
            self.model_val.eval()

        
    # def lr_decay(self, total_steps):
    #     lr = self.lr * (1 - total_steps / self.max_step)
    #     for p in self.opti.param_groups:
    #         p['lr'] = lr

    def load_pth(self,path_act,path_val):
        with torch.serialization.safe_globals({'Act_Net': Act_Net}):
            self.model_act=torch.load(path_act, map_location=self.device, weights_only=False)
        with torch.serialization.safe_globals({'Val_Net': Val_Net}):
            self.model_val=torch.load(path_val, map_location=self.device, weights_only=False)


    def init_graph(self):
        self.rewards = 0
        self.step=0
        self.rewards_store=[]
        self.best_mean_reward=0
        
        self.line, = self.ax.plot(self.rewards, label=f'Total Rewards per Episode {self.name}',alpha=0.2)
        self.line_mean, =self.ax.plot(self.rewards, label=f'Total mean Rewards {self.name}')
        #self.fill_std =self.ax.fill_between(self.rewards, label='Fill range',alpha=0.2)
        # 设置图表标题和标签
        self.ax.set_title('PPO Training Rewards Over Episodes')
        self.ax.set_xlabel('Episode')
        self.ax.set_ylabel('Total Reward')
        self.ax.legend()
        self.ax.grid(True)

    


    def store(self,state,action,reward,next_state,done):
        reward=self.reward_scale(reward)
        state_num,state_id=state
        next_state_num,next_state_id=next_state
        self.state_num.append(state_num)
        self.state_id.append(state_id)
        self.action.append(action)
        self.reward.append(reward)
        self.next_state_num.append(next_state_num)
        self.next_state_id.append(next_state_id)
        self.done.append(done)

        self.graph_on_step(reward)

    def clean(self):
        self.state_num=[]
        self.state_id=[]
        self.reward=[]
        self.action=[]
        self.next_state_num=[]
        self.next_state_id=[]
        self.done=[]
        self.reward_scale.reset()

    def choose_act(self,num_state,cards_id,mask:torch.Tensor=None):
        #num_state,cards_id=state

        num_state=torch.FloatTensor(num_state).unsqueeze(0).to(self.device)
        cards_id=torch.LongTensor(cards_id).unsqueeze(0).to(self.device)
        with torch.no_grad():
            result=self.model_act.predict(num_state,cards_id)
            if mask is not None and mask.any():
                result[mask==False]=0
        dist=torch.distributions.Categorical(result)
        act=dist.sample().item()
        
        return act
    

    def normalize_adv(self,adv:torch.Tensor):
        return ((adv - adv.mean()) / (adv.std() + 1e-5))

    def advantage_cal(self,delta:torch.Tensor,done:torch.Tensor):
        advantage_list=[]
        advantage=0
        #print(delta.cpu().numpy())
        for reward,done in zip(delta.cpu().numpy()[::-1],done.cpu().numpy()[::-1]):
            if done:
                advantage=0
            advantage=reward+self.lambd*self.gamma*advantage
            # print(advantage)
            # print()
            advantage_list.insert(0,advantage)
        #print(advantage_list)
        return np.array(advantage_list)


    def train(self):
        self.graph_on_rollout_end()
        state_num=torch.FloatTensor(np.array(self.state_num)).to(self.device)
        state_id=torch.LongTensor(np.array(self.state_id)).to(self.device)
        action=torch.LongTensor(np.array(self.action)).unsqueeze(1).to(self.device)
        done=torch.FloatTensor(np.array(self.done)).unsqueeze(1).to(self.device)
        next_state_num=torch.FloatTensor(np.array(self.next_state_num)).to(self.device)
        next_state_id=torch.LongTensor(np.array(self.next_state_id)).to(self.device)
        #print(self.reward)
        # print(state_num,state_id)
        # print(action)
        reward=torch.FloatTensor(np.array(self.reward)).unsqueeze(1).to(self.device)

        
        with torch.no_grad():
            
            a_pro,entropy=self.model_act(state_num,state_id)
            
            
            v=self.model_val(state_num,state_id)
            v_=self.model_val(next_state_num,next_state_id)
            delta=reward+self.gamma*v_*(1-done)-v
            
            advantage=self.advantage_cal(delta,done)
            
            advantage=torch.FloatTensor(advantage).detach().to(self.device)
            rewards=advantage+v

            advantage=self.normalize_adv(advantage)
            
            old_prob_log=a_pro.log_prob(action.squeeze(-1))
            

        dataset = TensorDataset(state_num,state_id, action, done, next_state_num,next_state_id,advantage,old_prob_log,rewards)
        dataloader = DataLoader(dataset, batch_size=128, shuffle=True)
        
        for _ in range(self.epochs):
            for batch in dataloader:
                state_num,state_id, action, done, next_state_num,next_state_id,advantage,old_prob_log,rewards=batch
                a_pro,entropy=self.model_act(state_num,state_id)#Trick 5—Policy Entropy
                v=self.model_val(state_num,state_id)
                
                new_prob_log=a_pro.log_prob(action.squeeze(-1))
                
                
                rate=torch.exp(new_prob_log-old_prob_log.detach()).unsqueeze(1)
                
                surr1=rate*advantage
                surr2=torch.clamp(rate,1-self.clip_para,1+self.clip_para)*advantage
                
                act_loss=-torch.min(surr1,surr2).squeeze(1)-0.01*entropy
                
                self.opti_act.zero_grad()
                

                act_loss.mean().backward()
                torch.nn.utils.clip_grad_norm_(self.model_act.parameters(), 0.5)
                self.opti_act.step()
                self.scheduler_action.step()

                self.opti_val.zero_grad()
                val_loss=F.mse_loss(rewards,v)
                #print(val_loss)
                val_loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model_val.parameters(), 0.5)
                self.opti_val.step()
                self.scheduler_value.step() # Trick 6:learning rate Decay

        
        self.clean()
    
    def graph_on_rollout_end(self) -> None:
        if self.best_mean_reward<self.rewards/self.step:
            self.best_mean_reward=self.rewards/self.step
        torch.save(self.model_act, f'model_complete_act_{self.name}.pth')
        torch.save(self.model_val, f'model_complete_val_{self.name}.pth')
        #print(self.rewards_store,self.rewards)
        self.rewards_store.append(self.rewards)
        print(self.rewards_store,self.rewards)
        self.rewards = 0
        self.step=0
        x,y=range(len(self.rewards_store)), self.rewards_store
        self.line.set_data(x,y)

        width=10
        if len(y)>=width:
            y_mean=np.convolve(y,np.ones(width)/width,mode="valid")
            x_mean=x[:len(y_mean)]
            self.line_mean.set_data(x_mean, y_mean)

       
            print(x,y,y_mean,x_mean)
        self.ax.set_xlim(0, len(self.rewards_store))
        self.ax.set_ylim(min(self.rewards_store) - 5, max(self.rewards_store) + 5)
        plt.savefig('ppo_training_reward.png')
        
    def graph_on_step(self,reward):
        self.step+=1
        self.rewards+=reward





if __name__=="__main__":
    agent=Agent_PPO(6,2)
    print(agent.choose_act([0,0,0,0,0,0]))
    
    
    agent.train()