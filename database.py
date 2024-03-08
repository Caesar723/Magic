from sqlalchemy import create_engine, ForeignKey, Column, Integer, String,Table,MetaData,func,and_
from sqlalchemy.orm import relationship,declarative_base

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import text

import bcrypt
import os
import json


from server_function_tool import split_message_deck,Deck_Response



engine = create_engine("mysql+pymysql://root@localhost/Magic_fan_made")

Base = declarative_base()

pack_cards_association = Table('pack_cards', Base.metadata,
    Column('pack_id', Integer, ForeignKey('packs.id')),
    Column('card_id', Integer, ForeignKey('cards.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password_hash = Column(String(255))
    decks = relationship("Deck", backref="user")
    cards = relationship("PlayerCard", backref="user")
    packs = relationship("PlayerPack", backref="user")
    virtual_currency = Column(Integer, default=0)  # 新增：虚拟货币
    

class Deck(Base):
    __tablename__ = 'decks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(255))
    content = Column(String(1024))  # 卡牌ID列表，例如 "1,3,5,7"

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    relative_url=Column(String(255))#cards/Instant/Arcane Insight
    rarity=Column(String(255))
    type_card=Column(String(255))#creature,instant,land,sorcery
    color=Column(String(255))

class PlayerCard(Base):
    __tablename__ = 'player_cards'
    id=Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    card_id = Column(Integer, ForeignKey('cards.id'))
    quantity = Column(Integer)  # 玩家拥有的该卡牌数量

class Pack(Base):
    __tablename__ = 'packs'
    id=Column(Integer, primary_key=True)
    name = Column(String(255))#orginal
    pack_url=Column(String(255))#webpages/image_source/packs/pack_org.jpg
    cards = relationship("Card", secondary=pack_cards_association)


class PlayerPack(Base):
    __tablename__ = 'player_packs'
    id=Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    pack_id = Column(Integer, ForeignKey('packs.id'))
    quantity = Column(Integer)  # 玩家拥有的该卡包数量
    


def reset_table():
    # # 删除所有表
    Base.metadata.drop_all(engine)
    # # 重新创建所有表
    Base.metadata.create_all(engine)

def check_in_data_base_card(session,name,type,rarity):
    print((session.query(Card).filter(and_(Card.name == name,Card.type_card==type)).first() is not None))
    return (session.query(Card).filter(and_(Card.name == name,Card.type_card==type)).first() is not None)

def reset_all_card():
    from server_function_tool import check_color,check_type
    ORGPATH=os.path.dirname(os.path.abspath(__file__))
    Session = sessionmaker(bind=engine)
    directory=f"{ORGPATH}/cards"
    # 创建会话实例
    session = Session()
    types=os.listdir(directory)
    
    if ".DS_Store" in types:
        types.remove(".DS_Store")
    for type in types:#creature Instant land sorcery
        further_path=f"{directory}/{type}"
        cards=os.listdir(further_path)
        
        if ".DS_Store" in cards:
            cards.remove(".DS_Store")

        for card in cards:
            with open(f"{further_path}/{card}/data.json", 'r') as file:
                # 加载JSON文件内容到一个Python字典
                data = json.load(file)
            
            if not check_in_data_base_card(session,data["Name"],type,data["Rarity"]):
                #print(type,card)

                color=check_color(data["Cost"]) if type!="land" else check_type(data["Type"])
                new_card = Card(name=data["Name"], relative_url=f"cards/{type}/{card}",rarity=data["Rarity"],type_card=type,color=color)
                session.add(new_card)
    session.commit()
    session.close()     
            

def reset_packs():
    from packs import Pack_Database
    
    Session = sessionmaker(bind=engine)
    # 创建会话实例
    session = Session()
    classes=Pack_Database.__subclasses__()
    for cla in classes:
        pack=cla()
        #print(3,cla.__name__)
        #print(not (session.query(Pack).filter(Pack.name == cla.__name__).first() is not None),1)
        #print(1)
        if not (session.query(Pack).filter(Pack.name == cla.__name__).first() is not None):
            pack_new=Pack(name=cla.__name__,pack_url=cla.image_url)
            print(pack.collect_cards())
            for url in pack.collect_cards():
                #print(cla())
                card=session.query(Card).filter_by(relative_url=url).first()
                pack_new.cards.append(card)
            #print(pack_new.cards)
            session.add(pack_new)
    session.commit()
    session.close()     
    





class DataBase:

    def __init__(self) -> None:
        self.async_engine = create_async_engine("mysql+aiomysql://root@localhost/Magic_fan_made")
        self.AsyncSessionLocal = sessionmaker(bind=self.async_engine, class_=AsyncSession, expire_on_commit=False)


        

    def hash_password(self,password:str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async def store_users_password_new_player(self,username:str,password:str):
        async with self.AsyncSessionLocal() as session:
            hashed_password = self.hash_password(password)
            new_user = User(username=username, password_hash=hashed_password,virtual_currency=0)
            session.add(new_user)
            await session.commit()
        return "signup successful"
        
    async def check_username_exists(self,desired_username,password):
        #await self.show_all_tables_info()
        async with self.AsyncSessionLocal() as session:
            # 注意：使用 select() 函数而不是直接的表达式
            
            query = select(User).where(User.username == desired_username)
            result = await session.execute(query)
            
            user = result.fetchall()
            
        
        return not user and bcrypt.checkpw(password.encode(), user[0][0].password_hash.encode())
        return not bool(user)

    async def check_password_match(self,username:str,password:str):#username error, passward error,matched
        async with self.AsyncSessionLocal() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalars().first()
        if user:
            if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                return "matched"
            else:
                return "passward error"
        else:
            return "username error"
    

    async def show_all_tables_info(self):
        async with self.AsyncSessionLocal() as session:
            metadata = MetaData()
            metadata.reflect(bind=engine)
            for table_name in metadata.tables:
                table = metadata.tables[table_name]
                query = select(table)
                result = await session.execute(query)
                print(f"Data from table {table_name}:")
                for row in result.fetchall():
                    print("    "+str(row))

    async def add_packs(self,pack_name,username,quantity=1):
        async with self.AsyncSessionLocal() as session:
            async with session.begin():
                query = select(User).where(User.username == username)
                result = await session.execute(query)
                user = result.scalars().first()
                query = select(Pack).where(Pack.name == pack_name)
                result = await session.execute(query)
                pack = result.scalars().first()
                #print(user.id,pack.id)
                new_player_pack = PlayerPack(user_id=user.id, pack_id=pack.id, quantity=quantity)
                session.add(new_player_pack)
                await session.commit()
        return True
    
    async def get_player_packs(self,username):
        async with self.AsyncSessionLocal() as session:  # 使用你的异步session
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            user = result.scalars().first()
            
            query = select(PlayerPack, Pack).join(Pack, PlayerPack.pack_id == Pack.id).where(PlayerPack.user_id == user.id)

            result = await session.execute(query)
            packs = result.all()
        packs_dicts = [{'id': player_pack.id, 'pack_url': pack.pack_url,'name':pack.name,'name_id':pack.id,"quantity":player_pack.quantity} for player_pack, pack in packs]
        # 然后，将列表转换为JSON字符串
        packs_json = json.dumps(packs_dicts)
        return packs_json
    
    async def draw_cards(self,packid,pack_name_id,Common_num,Uncommon_num,Rare_num,Mythic_Rare_num,username):
        
        cards=[]
        rarity_num={
            "Mythic Rare":Mythic_Rare_num,
            "Rare":Rare_num,
            "Uncommon":Uncommon_num,
            "Common":Common_num
        }

        async with self.AsyncSessionLocal() as session:

            await self.delete_pack(session,packid)
            # 构建查询：选择cards，基于pack_cards_association中的pack_id过滤，随机排序，并限制结果数量
            for rarity in rarity_num:
                stmt = select(Card).join(
                    pack_cards_association, Card.id == pack_cards_association.c.card_id,
                    
                ).where(
                    pack_cards_association.c.pack_id == pack_name_id,
                    Card.rarity==rarity
                ).order_by(
                    func.random()  # PostgreSQL的随机排序函数，根据DBMS调整
                ).limit(rarity_num[rarity])

                result = await session.execute(stmt)
                cards += result.scalars().all()
        
        cards_dicts=[]
        for card in cards:
            await self.add_card_to_player(session,username,card)
            cards_dicts.append({'name': card.name, 'rarity': card.rarity,'relative_url':card.relative_url,"type":card.type_card})

        
        return cards_dicts
    
    async def delete_pack(self,session,packid):
        stmt = select(PlayerPack).where(PlayerPack.id == packid)
        result = await session.execute(stmt)
        pack = result.scalars().first()
        if pack:
            if pack.quantity == 1:
                # 如果quantity是1，则删除Pack
                await session.delete(pack)
            else:
                # 如果quantity大于1，则减少quantity的值
                pack.quantity -= 1
                # 更新Pack
                session.add(pack)
            
            await session.commit()
            return f"Pack with id {packid} {'deleted' if pack.quantity == 1 else 'updated'} successfully."
        else:
            return "Pack not found."
        
    async def find_user(self,session,username):
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        element = result.scalars().first()
        return element
    
    async def add_card_to_player(self,session,username,card):
        user= await self.find_user(session,username)
        stmt = select(PlayerCard).where(PlayerCard.user_id == user.id,PlayerCard.card_id==card.id)
        result = await session.execute(stmt)
        playerCard = result.scalars().first()

        if playerCard:
            # 如果元素存在，增加quantity
            if playerCard.quantity>=4 and card.type_card!="land":
                currency_dict={
                    "Common":5,
                    "Uncommon":20,
                    "Rare":100,
                    "Mythic Rare":500,
                }
                user.virtual_currency+=currency_dict[card.rarity]
            else:
                playerCard.quantity += 1
            await session.commit()
            return 'Updated', playerCard,user
        else:
            # 如果元素不存在，创建并添加新元素
            new_card = PlayerCard(user_id=user.id, card_id=card.id,quantity=1)
            session.add(new_card)
            await session.commit()
            return 'Created', new_card

    async def page_cards(self,offset,number,color,type_card,username):#color(black,blue,gold,green,red) type_card(creature,sorcery,Instant,land)
        async with self.AsyncSessionLocal() as session:
            
            stmt = (
                select(PlayerCard,Card)
                .join(Card, PlayerCard.card_id == Card.id)
                .join(User, PlayerCard.user_id == User.id)
                .filter(Card.type_card==type_card ,Card.color==color,User.username==username) 
                .order_by(Card.name) 
                .offset(offset)  # 跳过前两个元素
                .limit(number)  # 选择接下来的6个元素
            )
            result = await session.execute(stmt)
            cards = result.all()
            
            cards_dicts=[]
            for playerCard,card in cards:
                
                cards_dicts.append({'name': card.name, 'rarity': card.rarity,'relative_url':card.relative_url,"type":card.type_card,"quality":playerCard.quantity})

            
            return cards_dicts
                
    async def check_cards_in_player(self,list_deck_cards,username):
        
        async with self.AsyncSessionLocal() as session:
            for card in list_deck_cards:
            
                stmt = (
                    select(PlayerCard)
                    .join(Card, PlayerCard.card_id == Card.id)
                    .join(User, PlayerCard.user_id == User.id)
                    .filter(Card.type_card==card.type_card ,Card.name==card.name,User.username==username) 
                )
                result = await session.execute(stmt)
                finded_card = result.first()[0]
                
                if not (finded_card):
                    return False
                elif finded_card.quantity<card.quantity:
                    return False
        return True

    async def store_deck(self,name,cards,username):
        async with self.AsyncSessionLocal() as session:  
            user=await self.find_user(session,username)
            new_deck = Deck(name=name, user_id=user.id, content=cards)
            session.add(new_deck)
            await session.commit()
        
        return True
    
    async def get_all_decks(self,username):
        async with self.AsyncSessionLocal() as session:  
            user=await self.find_user(session,username)
            stmt = (
                    select(Deck)
                    .filter(Deck.user_id ==user.id) 
                )
            result = await session.execute(stmt)
            decks = result.all()
        result=[Deck_Response(
                    id=deck[0].id
                    ,content=split_message_deck(deck[0].name+(f"|{deck[0].content}" if deck[0].content else ""))
                ) 
            for deck in decks
            ]
        return result
        
    async def delete_decks(self,name,id,username):
        async with self.AsyncSessionLocal() as session: 
            user=await self.find_user(session,username)
            stmt = (
                    select(Deck)
                    .filter(Deck.user_id ==user.id, Deck.name==name,Deck.id==id) 
                ) 
            result = await session.execute(stmt)
            user_to_delete = result.scalars().first()

            if user_to_delete:
                await session.delete(user_to_delete)
                await session.commit()
                return True
            else:
                return False
            
    async def check_deck_real(self,name,id,username):
        async with self.AsyncSessionLocal() as session: 
            user=await self.find_user(session,username)
            stmt = (
                    select(Deck)
                    .filter(Deck.user_id ==user.id, Deck.name==name,Deck.id==id) 
                ) 
            result = await session.execute(stmt)
            deck = result.scalars().first()
            
            if deck:
                return deck.content
            else:
                return False



if __name__=="__main__":
    
    reset_table()
    reset_all_card()
    reset_packs()
    pass