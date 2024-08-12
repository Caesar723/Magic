import torch



from game.type_action.actions import List_Action_Processor
from game.ppo_train import Agent_PPO
from game.agent import Agent_Player_Red


class Agent_Train_Red(Agent_Player_Red):

    def __init__(self, name: str, action_stroe: List_Action_Processor,agent:Agent_PPO) -> None:
        super().__init__(name, action_stroe)
        self.agent=agent
        #self.data_counter=0
        


   
    
    def store_data(self,state,action,reward,next_state,done):
        self.agent.store(state,action,reward,next_state,done)
        if len(self.agent.reward)>=1024:
            print("____________________update agent____________________")
            self.update()
            


    def update(self):
        self.agent.train()

    