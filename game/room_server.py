
from game.room import Room
from server_function_tool import Deck_selected

import game.custom_print
class RoomServer:
    

    def __init__(self,database) -> None:
        self.client_room={

        }
        self.queue=[]#set
        self.queue_dict={}

        self.database=database

    def find_player_room(self,player_name:str):
        if player_name in self.client_room:
            return self.client_room[player_name]
        else:
            return "no room found"

    async def create_new_room(self,client_1:tuple,client_2:tuple):
        room=Room([client_1,client_2],self)

        self.client_room[client_1[1]]=room
        self.client_room[client_2[1]]=room

        await room.game_start()


        

    def put_client_to_queue(self,client:tuple):
        self.queue.append(client)
        self.queue_dict[client[1]]=client

    def check_client_in_room(self,client:str):
        return client in self.client_room

    def check_client_in_queue(self,client:str):
        return client in self.queue_dict
    
    def get_room(self,client:str):
        return self.client_room[client]
    
    async def check_matching(self):
        print(self.queue)
        if len(self.queue)>=2:
            print(1)
            client_1=self.queue.pop(0)
            client_2=self.queue.pop(0)

            del self.queue_dict[client_1[1]]
            del self.queue_dict[client_2[1]]

            await self.create_new_room(client_1,client_2)




    async def matching(self,client_detail:tuple):# deck_detail username

        await self.check_matching()
        if self.check_client_in_room(client_detail[1]):
            return {"state":"find!"}

        elif self.check_client_in_queue(client_detail[1]):
            return {"state":"waiting"}

        else:
            self.put_client_to_queue(client_detail)
            return {"state":"waiting"}
        

    def delete_matching(self,client:str):
        if client in self.queue_dict:
            self.queue.remove(self.queue_dict[client])
            del self.queue_dict[client]
            return {"state":"success delete"}
        else:
            return {"state":"not find"}
        
    def get_players_name(self,username:str):
        result={"self":"t","opponent":"tt"}
        if self.check_client_in_room(username):

            room:Room=self.client_room[username]
            for player_name in room.players:
                if player_name==username:
                    result["self"]=player_name
                else:
                    result["opponent"]=player_name
        return result
        
    


    




    

