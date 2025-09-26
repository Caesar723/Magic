from game.game_function_tool import ORGPATH


ROGUE_AGENTS_DICT={
    "agent_low_level":{
        "config_lists_monster":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/white/ppo_lstm2.yaml",
                "name":"Explodichick",
                "avatar": '💣',
                "description":"A small explosion-prone chicken that can explode when hit."
            }
        ],
        "config_lists_boss":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/white/ppo_lstm2.yaml",
                "name":"Mukaso, the Thousand-Fanged Serpent",
                "avatar": '🐍',
                "description":"A thousand-fanged serpent that can shoot fireballs and poison darts."
            },
        ],
        "monster_max_life":10,
        "boss_max_life":30,

        "win_price_min":2,
        "win_price_max":10,
        "boss_win_price_min":10,
        "boss_win_price_max":20,
    },
    "agent_middle_level":{
        "config_lists_monster":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/white/ppo_lstm2.yaml",
                "name":"Explodichick",
                "avatar": '💣',
                "description":"A small explosion-prone chicken that can explode when hit."
            }
        ],
        "config_lists_boss":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/white/ppo_lstm2.yaml",
                "name":"Mukaso, the Thousand-Fanged Serpent",
                "avatar": '🐍',
                "description":"A thousand-fanged serpent that can shoot fireballs and poison darts."
            },
        ],
        "monster_max_life":20,
        "boss_max_life":40,

        "win_price_min":5,
        "win_price_max":20,
        "boss_win_price_min":20,
        "boss_win_price_max":40,
    },
    "agent_high_level":{
        "config_lists_monster":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/white/ppo_lstm2.yaml",
                "name":"Explodichick",
                "avatar": '💣',
                "description":"A small explosion-prone chicken that can explode when hit."
            }
        ],
        "config_lists_boss":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/white/ppo_lstm2.yaml",
                "name":"Mukaso, the Thousand-Fanged Serpent",
                "avatar": '🐍',
                "description":"A thousand-fanged serpent that can shoot fireballs and poison darts."
            },
        ],
        "monster_max_life":30,
        "boss_max_life":60,

        "win_price_min":20,
        "win_price_max":40,
        "boss_win_price_min":40,
        "boss_win_price_max":80,
    },
}



ROGUE_TREASURE_DICT={
    "low_level":{
        "treasure_list":[
            "pytreasures.Endless_Grimoire.model.Endless_Grimoire",
            "pytreasures.Amulet_of_the_Time_Weaver.model.Amulet_of_the_Time_Weaver",
            "pytreasures.Boots_of_Blazing_Speed.model.Boots_of_Blazing_Speed",
            "pytreasures.Boots_of_Blinding_Speed.model.Boots_of_Blinding_Speed",
            "pytreasures.Boots_of_the_Swift_Strider.model.Boots_of_the_Swift_Strider",
            "pytreasures.Boots_of_the_Time_Traveler.model.Boots_of_the_Time_Traveler",
            "pytreasures.Chrono-Sand_Hourglass.model.Chrono_Sand_Hourglass",
            "pytreasures.Cloak_of_the_Shadow_Thief.model.Cloak_of_the_Shadow_Thief",
            "pytreasures.Cursed_Coin_of_Misfortune.model.Cursed_Coin_of_Misfortune",
            "pytreasures.Lucky_Charm_of_the_Mischievous_Sprite.model.Lucky_Charm_of_the_Mischievous_Sprite",
            "pytreasures.Lucky_Charm_of_the_Trickster.model.Lucky_Charm_of_the_Trickster",
            "pytreasures.Lucky_Clover_Pin.model.Lucky_Clover_Pin",
            "pytreasures.Mirror_of_Misdirection.model.Mirror_of_Misdirection",
            "pytreasures.Mirror_of_Reflection.model.Mirror_of_Reflection",
            "pytreasures.Shield_of_the_Trickster.model.Shield_of_the_Trickster",
            "pytreasures.Spectral_Lantern.model.Spectral_Lantern",
        ],
        "win_appear_percent":0.1,
        
    },
    "middle_level":{
        "treasure_list":[
            "pytreasures.Endless_Grimoire.model.Endless_Grimoire",
            "pytreasures.Amulet_of_the_Time_Weaver.model.Amulet_of_the_Time_Weaver",
            "pytreasures.Boots_of_Blazing_Speed.model.Boots_of_Blazing_Speed",
            "pytreasures.Boots_of_Blinding_Speed.model.Boots_of_Blinding_Speed",
            "pytreasures.Boots_of_the_Swift_Strider.model.Boots_of_the_Swift_Strider",
            "pytreasures.Boots_of_the_Time_Traveler.model.Boots_of_the_Time_Traveler",
            "pytreasures.Chrono-Sand_Hourglass.model.Chrono_Sand_Hourglass",
            "pytreasures.Cloak_of_the_Shadow_Thief.model.Cloak_of_the_Shadow_Thief",
            "pytreasures.Cursed_Coin_of_Misfortune.model.Cursed_Coin_of_Misfortune",
            "pytreasures.Lucky_Charm_of_the_Mischievous_Sprite.model.Lucky_Charm_of_the_Mischievous_Sprite",
            "pytreasures.Lucky_Charm_of_the_Trickster.model.Lucky_Charm_of_the_Trickster",
            "pytreasures.Lucky_Clover_Pin.model.Lucky_Clover_Pin",
            "pytreasures.Mirror_of_Misdirection.model.Mirror_of_Misdirection",
            "pytreasures.Mirror_of_Reflection.model.Mirror_of_Reflection",
            "pytreasures.Shield_of_the_Trickster.model.Shield_of_the_Trickster",
            "pytreasures.Spectral_Lantern.model.Spectral_Lantern",
        ],
        "win_appear_percent":0.2,
    },
    "high_level":{
        "treasure_list":[
            "pytreasures.Endless_Grimoire.model.Endless_Grimoire",
            "pytreasures.Amulet_of_the_Time_Weaver.model.Amulet_of_the_Time_Weaver",
            "pytreasures.Boots_of_Blazing_Speed.model.Boots_of_Blazing_Speed",
            "pytreasures.Boots_of_Blinding_Speed.model.Boots_of_Blinding_Speed",
            "pytreasures.Boots_of_the_Swift_Strider.model.Boots_of_the_Swift_Strider",
            "pytreasures.Boots_of_the_Time_Traveler.model.Boots_of_the_Time_Traveler",
            "pytreasures.Chrono-Sand_Hourglass.model.Chrono_Sand_Hourglass",
            "pytreasures.Cloak_of_the_Shadow_Thief.model.Cloak_of_the_Shadow_Thief",
            "pytreasures.Cursed_Coin_of_Misfortune.model.Cursed_Coin_of_Misfortune",
            "pytreasures.Lucky_Charm_of_the_Mischievous_Sprite.model.Lucky_Charm_of_the_Mischievous_Sprite",
            "pytreasures.Lucky_Charm_of_the_Trickster.model.Lucky_Charm_of_the_Trickster",
            "pytreasures.Lucky_Clover_Pin.model.Lucky_Clover_Pin",
            "pytreasures.Mirror_of_Misdirection.model.Mirror_of_Misdirection",
            "pytreasures.Mirror_of_Reflection.model.Mirror_of_Reflection",
            "pytreasures.Shield_of_the_Trickster.model.Shield_of_the_Trickster",
            "pytreasures.Spectral_Lantern.model.Spectral_Lantern",
        ],
        "win_appear_percent":0.4,
    },
}


ROGUE_EVENT_DICT={
    "low_level":{
        "event_list":[
            "game.rogue.events.Mysterious_Ancient_Temple.Mysterious_Ancient_Temple",
            
        ],
    },
    "middle_level":{
        "event_list":[
            "game.rogue.events.Mysterious_Ancient_Temple.Mysterious_Ancient_Temple",
            
        ],
    },
    "high_level":{
        "event_list":[
            "game.rogue.events.Mysterious_Ancient_Temple.Mysterious_Ancient_Temple",
            
        ],
    },
}