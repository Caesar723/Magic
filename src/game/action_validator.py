from typing import TYPE_CHECKING

from game.type_cards.creature import Creature
from game.type_cards.instant import Instant
from game.type_cards.land import Land
from game.type_cards.sorcery import Sorcery

if TYPE_CHECKING:
    from game.card import Card
    from game.player import Player
    from game.room import Room


def _validation_result(result,default_reason:str)->tuple[bool,str]:
    """Normalize bool and tuple validation results."""
    if isinstance(result,(tuple,list)):
        valid=bool(result[0]) if result else False
        reason=str(result[1]) if len(result)>1 and not valid else ""
        return valid,reason or ("" if valid else default_reason)
    valid=bool(result)
    return valid,"" if valid else default_reason


def _get_card_index(player:"Player",index:int,area:str):
    if index<0:
        return False
    return player.get_card_index(index,area)


def get_card_select_range(card:"Card")->str:
    instance_dict={
        Creature:"when_enter_battlefield",
        Instant:"card_ability",
        Land:"when_enter_landarea",
        Sorcery:"card_ability"
    }
    for cls,ability_name in instance_dict.items():
        if isinstance(card,cls):
            ability=getattr(card,ability_name,None)
            return getattr(ability,"select_range","")
    return ""


def _has_valid_target(player:"Player",select_range:str)->bool:
    if select_range.startswith("select|"):
        try:
            return int(select_range.split("|",1)[1])>0
        except ValueError:
            return False
    target_groups={
        "all_roles":[player.battlefield,player.opponent.battlefield,[player.opponent],[player]],
        "opponent_roles":[player.opponent.battlefield,[player.opponent]],
        "your_roles":[player.battlefield,[player]],
        "all_creatures":[player.battlefield,player.opponent.battlefield],
        "opponent_creatures":[player.opponent.battlefield],
        "your_creatures":[player.battlefield],
        "all_lands":[player.land_area,player.opponent.land_area],
        "opponent_lands":[player.opponent.land_area],
        "your_lands":[player.land_area]
    }
    if select_range not in target_groups:
        return False
    for targets in target_groups[select_range]:
        for target in targets:
            if not hasattr(target,"get_flag") or not target.get_flag("Hexproof") or target.player==player:
                return True
    return False


def validate_end_step(room:"Room",player:"Player")->tuple[bool,str]:
    if player!=room.active_player:
        return False,"You must do it in your turn"
    if room.get_flag("bullet_time"):
        return False,"You can't end the turn in bullet time"
    if room.get_flag("attacker_defenders"):
        return False,"You must finish the attack first"
    return True,""


def validate_end_bullet(room:"Room",player:"Player")->tuple[bool,str]:
    if not room.get_flag("bullet_time"):
        return False,"Not in bullet time"
    key=f"{player.name}_bullet_time_flag"
    if room.get_flag(key):
        return False,"Player has already ended bullet time"
    return True,""


def validate_select_attacker(room:"Room",player:"Player",card:"Card")->tuple[bool,str]:
    if not isinstance(card,Creature) or card not in player.battlefield:
        return False,"Creature is not on the battlefield"
    if player!=room.active_player:
        return False,"You must attack in your turn"
    if room.get_flag("bullet_time") or room.get_flag("attacker_defenders"):
        return False,"You can't select an attacker now"
    if card.get_flag("summoning_sickness") and not card.get_flag("haste"):
        return False,"Creature has summoning sickness"
    if card.get_flag("tap"):
        return False,"Creature is tapped"
    if card.get_counter_from_dict("attack_counter")<=0:
        return False,"Creature can't attack"
    return True,""


def validate_select_defender(room:"Room",player:"Player",card:"Card")->tuple[bool,str]:
    attacker=room.attacker
    if not isinstance(card,Creature) or card not in player.battlefield:
        return False,"Creature is not on the battlefield"
    if player!=room.non_active_player:
        return False,"You are not the defending player"
    if not room.get_flag("attacker_defenders") or attacker is None:
        return False,"There is no attacker"
    if card.get_flag("tap"):
        return False,"Creature is tapped"
    if attacker.get_flag("flying") and not (card.get_flag("flying") or card.get_flag("reach")):
        return False,"Creature can't block flying"
    if not room.check_landwalk(attacker,player):
        return False,"Creature can't block landwalk"
    if attacker.get_flag("unblockable"):
        return False,"Attacker is unblockable"
    return True,""


def validate_select_content(room:"Room",player:"Player",card:"Card",select_content:str)->tuple[bool,str]:
    select_range=get_card_select_range(card) or getattr(card,"select_range","")
    if not select_range:
        return True,""
    if not select_content:
        return (True,"") if _has_valid_target(player,select_range) else (False,"This card has no valid target")
    parameters=select_content.split("|")
    if len(parameters)<3 or parameters[0]!=player.name:
        return False,"Invalid target message"
    if parameters[1]=="cancel":
        return False,"Selection cancelled"
    if parameters[1]=="cards":
        if not select_range.startswith("select|"):
            return False,"Invalid card selection"
        try:
            option=int(parameters[2])
            option_count=int(select_range.split("|",1)[1])
        except (TypeError,ValueError):
            return False,"Invalid card selection"
        return (True,"") if 1<=option<=option_count else (False,"Card selection is out of range")
    if parameters[1]!="field" or len(parameters)<4:
        return False,"Invalid target message"
    field_dict={
        "self_battlefield":player.battlefield,
        "opponent_battlefield":player.opponent.battlefield,
        "self_landfield":player.land_area,
        "opponent_landfield":player.opponent.land_area
    }
    player_dict={"self":player,"oppo":player.opponent}
    target_type=parameters[2]
    if target_type in player_dict:
        target=player_dict[target_type]
    elif target_type in field_dict:
        try:
            target_index=int(parameters[3])
            if target_index<0:
                return False,"Target is out of range"
            target=field_dict[target_type][target_index]
        except (TypeError,ValueError,IndexError):
            return False,"Target is out of range"
    else:
        return False,"Unknown target type"
    valid_targets={
        "all_roles":[player.battlefield,player.opponent.battlefield,player.opponent,player],
        "opponent_roles":[player.opponent.battlefield,player.opponent],
        "your_roles":[player.battlefield,player],
        "all_creatures":[player.battlefield,player.opponent.battlefield],
        "opponent_creatures":[player.opponent.battlefield],
        "your_creatures":[player.battlefield],
        "all_lands":[player.land_area,player.opponent.land_area],
        "opponent_lands":[player.opponent.land_area],
        "your_lands":[player.land_area]
    }
    if select_range not in valid_targets:
        return False,"Unknown select range"
    for targets in valid_targets[select_range]:
        if target is targets:
            return True,""
        if isinstance(targets,list) and target in targets:
            if target.get_flag("Hexproof") and target.player!=player:
                return False,"Target has Hexproof"
            return True,""
    return False,"Target is not valid"


def validate_play_card(room:"Room",player:"Player",card:"Card",select_content:str="")->tuple[bool,str]:
    if card not in player.hand:
        return False,"Card is not in hand"
    if room.get_flag("bullet_time"):
        if not isinstance(card,Instant) and not card.get_flag("Flash"):
            return False,"You can't play this card in bullet time"
    elif player!=room.active_player:
        return False,"You must play this card in your turn"
    valid,reason=_validation_result(card.check_can_use(player),"Card can't be used")
    if not valid:
        return False,reason
    return validate_select_content(room,player,card,select_content)


def validate_activate_ability(room:"Room",player:"Player",card:"Card",area:str)->tuple[bool,str]:
    if area!="land_area" or not isinstance(card,Land) or card not in player.land_area:
        return False,"Land is not in the land area"
    if card.get_flag("tap"):
        return False,"Land is already tapped"
    check_ability=getattr(card,"check_ability_can_be_used",None)
    if check_ability is None:
        return False,"Card has no activatable ability"
    return _validation_result(check_ability(player,player.opponent),"Ability can't be activated")


def validate_player_action(room:"Room",message:str)->tuple[bool,str]:
    try:
        base_message,select_content=(message.split("||",1)+[""])[:2]
        username,action_type,content=base_message.split("|")
        player=room.players.get(username)
        if player is None:
            return False,"Unknown player"
        if action_type=="end_step":
            return validate_end_step(room,player)
        if action_type=="end_bullet":
            return validate_end_bullet(room,player)
        if action_type=="select_attacker":
            card=_get_card_index(player,int(content),"battlefield")
            return validate_select_attacker(room,player,card)
        if action_type=="select_defender":
            card=_get_card_index(player,int(content),"battlefield")
            return validate_select_defender(room,player,card)
        if action_type=="play_card":
            card=_get_card_index(player,int(content),"hand")
            if not card:
                return False,"No card"
            select_content=select_content or getattr(player,"select_content","")
            return validate_play_card(room,player,card,select_content)
        if action_type=="activate_ability":
            area,index=content.split(";",1)
            card=_get_card_index(player,int(index),area)
            return validate_activate_ability(room,player,card,area)
        return False,"Unsupported action"
    except (AttributeError,IndexError,KeyError,TypeError,ValueError):
        return False,"Invalid action message"
