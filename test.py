
from game.card import Card
from game.type_cards.creature import Creature
from pycards import *
from game.game_function_tool import get_cards_diction


diction=get_cards_diction()
card:Card=diction["Call to Unity_Sorcery"]()
print(card.rarity)
# print(Mistweaver_Drake.__bases__)
# a=Mistweaver_Drake()
# print(a.name)
# print(Mistweaver_Drake())
# print(Creature.__subclasses__())
