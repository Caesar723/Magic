from game.game_function_tool import ORGPATH


ROGUE_AGENTS_DICT={
    "agent_low_level":{
        "config_lists_monster":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/white/ppo_lstm2.yaml",
                "name":"Explodichick",
                "avatar": '💣',
                "description":"A small explosion-prone chicken that can explode when hit."
            },
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/red/ppo_lstm.yaml",
                "name":"Flame Dragon",
                "avatar": '🐲',
                "description":"An ancient flame dragon that wields the power of blazing fire. Its scales burn like molten lava, and its breath can incinerate everything in its path. Legends say only the bravest warriors dare to challenge it."
            },
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/green/ppo_lstm6.yaml",
                "name":"Mukaso, the Thousand-Fanged Serpent",
                "avatar": '🐍',
                "description":"A thousand-fanged serpent that can shoot fireballs and poison darts."
            }
        ],
        "config_lists_boss":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/green/ppo_lstm6.yaml",
                "name":"Mukaso, the Thousand-Fanged Serpent",
                "avatar": '🐍',
                "description":"A thousand-fanged serpent that can shoot fireballs and poison darts."
            },
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/red/ppo_lstm.yaml",
                "name":"Flame Dragon",
                "avatar": '🐲',
                "description":"An ancient flame dragon that wields the power of blazing fire. Its scales burn like molten lava, and its breath can incinerate everything in its path. Legends say only the bravest warriors dare to challenge it."
            }
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
            },
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/green/ppo_lstm6.yaml",
                "name":"Mukaso, the Thousand-Fanged Serpent",
                "avatar": '🐍',
                "description":"A thousand-fanged serpent that can shoot fireballs and poison darts."
            }
        ],
        "config_lists_boss":[
            
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/angle/ppo_lstm6.yaml",
                "name":"Adjudicator",
                "avatar": '⚖️',
                "description":"A divine judge who weighs the souls of mortals and delivers righteous judgment upon the wicked."
            },
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/red/ppo_lstm.yaml",
                "name":"Flame Dragon",
                "avatar": '🐲',
                "description":"An ancient flame dragon that wields the power of blazing fire. Its scales burn like molten lava, and its breath can incinerate everything in its path. Legends say only the bravest warriors dare to challenge it."
            }
        ],
        "monster_max_life":25,
        "boss_max_life":50,

        "win_price_min":5,
        "win_price_max":20,
        "boss_win_price_min":20,
        "boss_win_price_max":40,
    },
    "agent_high_level":{
        "config_lists_monster":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/angle/ppo_lstm6.yaml",
                "name":"Adjudicator",
                "avatar": '⚖️',
                "description":"A divine judge who weighs the souls of mortals and delivers righteous judgment upon the wicked."
            },
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/red/ppo_lstm.yaml",
                "name":"Flame Dragon",
                "avatar": '🐲',
                "description":"An ancient flame dragon that wields the power of blazing fire. Its scales burn like molten lava, and its breath can incinerate everything in its path. Legends say only the bravest warriors dare to challenge it."
            }
        ],
        "config_lists_boss":[
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/green/ppo_lstm6.yaml",
                "name":"Mukaso, the Thousand-Fanged Serpent",
                "avatar": '🐍',
                "description":"A thousand-fanged serpent that can shoot fireballs and poison darts."
            },
            {
                "config_path":f"{ORGPATH}/game/rlearning/weights/red/ppo_lstm.yaml",
                "name":"Flame Dragon",
                "avatar": '🐲',
                "description":"An ancient flame dragon that wields the power of blazing fire. Its scales burn like molten lava, and its breath can incinerate everything in its path. Legends say only the bravest warriors dare to challenge it."
            }
        ],
        "monster_max_life":40,
        "boss_max_life":80,

        "win_price_min":20,
        "win_price_max":40,
        "boss_win_price_min":40,
        "boss_win_price_max":80,
    },
}



ROGUE_TREASURE_DICT={
    "low_level":{
        "treasure_list":[
            
            
            
            
            "pytreasures.Boots_of_the_Swift_Strider.model.Boots_of_the_Swift_Strider",
            
            
            
            "pytreasures.Cursed_Coin_of_Misfortune.model.Cursed_Coin_of_Misfortune",
            
            "pytreasures.Lucky_Charm_of_the_Trickster.model.Lucky_Charm_of_the_Trickster",
            
            "pytreasures.Mirror_of_Misdirection.model.Mirror_of_Misdirection",
            
            "pytreasures.Shield_of_the_Trickster.model.Shield_of_the_Trickster",
            "pytreasures.Spectral_Lantern.model.Spectral_Lantern",
        ],
        "win_appear_percent":0.1,
        
    },
    "middle_level":{
        "treasure_list":[
            "pytreasures.Endless_Grimoire.model.Endless_Grimoire",
            "pytreasures.Amulet_of_the_Time_Weaver.model.Amulet_of_the_Time_Weaver",
            
            "pytreasures.Boots_of_Blinding_Speed.model.Boots_of_Blinding_Speed",
            "pytreasures.Boots_of_the_Swift_Strider.model.Boots_of_the_Swift_Strider",
            "pytreasures.Boots_of_the_Time_Traveler.model.Boots_of_the_Time_Traveler",
            
            
            "pytreasures.Cursed_Coin_of_Misfortune.model.Cursed_Coin_of_Misfortune",
            
            "pytreasures.Lucky_Charm_of_the_Trickster.model.Lucky_Charm_of_the_Trickster",
            "pytreasures.Lucky_Clover_Pin.model.Lucky_Clover_Pin",
            "pytreasures.Mirror_of_Misdirection.model.Mirror_of_Misdirection",
            
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
            
            
            "game.rogue.events.Ancient_Stele.Ancient_Stele",

            
            "game.rogue.events.Cracked_Statue.Cracked_Statue",
            
            "game.rogue.events.Cursed_Obsidian_Altar.Cursed_Obsidian_Altar",
            "game.rogue.events.Eternal_Singing_Statue.Eternal_Singing_Statue",
            
            "game.rogue.events.Mysterious_Ancient_Temple.Mysterious_Ancient_Temple",

            
            
            "game.rogue.events.Shattered_Mirror.Shattered_Mirror",
            
            "game.rogue.events.Whispering_Tome.Whispering_Tome",
            
            
            
            
            "game.rogue.events.Withered_Bloom.Withered_Bloom",
            
        ],
    },
    "middle_level":{
        "event_list":[
            "game.rogue.events.Ancient_Stele.Ancient_Stele",
            "game.rogue.events.Cracked_Statue.Cracked_Statue",
            "game.rogue.events.Cursed_Obsidian_Altar.Cursed_Obsidian_Altar",
            "game.rogue.events.Eternal_Singing_Statue.Eternal_Singing_Statue",
            "game.rogue.events.Poisoned_Darts_Trap.Poisoned_Darts_Trap",
            "game.rogue.events.Shattered_Mirror.Shattered_Mirror",
            "game.rogue.events.Spirit_of_the_Bloom.Spirit_of_the_Bloom",
            "game.rogue.events.Whispering_Flame.Whispering_Flame",
            "game.rogue.events.Whispering_Tome.Whispering_Tome",
            "game.rogue.events.Withered_Bloom.Withered_Bloom",
            
        ],
    },
    "high_level":{
        "event_list":[
            "game.rogue.events.Altar_of_the_Burning_Sun.Altar_of_the_Burning_Sun",
            "game.rogue.events.Ancient_Throne.Ancient_Throne",
            "game.rogue.events.Cursed_Inscription.Cursed_Inscription",
            "game.rogue.events.Forgotten_Pact.Forgotten_Pact",
            "game.rogue.events.Runic_Chamber.Runic_Chamber",
            "game.rogue.events.Spirit_of_the_Bloom.Spirit_of_the_Bloom",
            "game.rogue.events.Stellar_Altar.Stellar_Altar",
            "game.rogue.events.Void_Rift.Void_Rift",
        ],
    },
}

ROGUE_CARD_BATCH_DICT={
    "low_level":{
        "card_batch_list":[
            "game.rogue.card_batch.Break_the_Hourglass.Break_the_Hourglass",
            "game.rogue.card_batch.Carry_Beyond.Carry_Beyond",
            "game.rogue.card_batch.Channel_Mana.Channel_Mana",
            
            "game.rogue.card_batch.Land_Black.Land_Black",
            "game.rogue.card_batch.Land_Blue.Land_Blue",
            "game.rogue.card_batch.Land_Green.Land_Green",
            "game.rogue.card_batch.Land_Red.Land_Red",
            "game.rogue.card_batch.Land_White.Land_White",
            "game.rogue.card_batch.Primal_Interruption.Primal_Interruption",
            "game.rogue.card_batch.Roar_of_Domination.Roar_of_Domination",
            "game.rogue.card_batch.Tidal_Revelation.Tidal_Revelation",
            "game.rogue.card_batch.Turn_Blows_to_Power.Turn_Blows_to_Power",
        ],
    },
    "middle_level":{
        "card_batch_list":[
            "game.rogue.card_batch.Break_the_Hourglass.Break_the_Hourglass",
            "game.rogue.card_batch.Carry_Beyond.Carry_Beyond",
            "game.rogue.card_batch.Channel_Mana.Channel_Mana",
            
            "game.rogue.card_batch.Land_Black.Land_Black",
            "game.rogue.card_batch.Land_Blue.Land_Blue",
            "game.rogue.card_batch.Land_Green.Land_Green",
            "game.rogue.card_batch.Land_Red.Land_Red",
            "game.rogue.card_batch.Land_White.Land_White",
            "game.rogue.card_batch.Primal_Interruption.Primal_Interruption",
            "game.rogue.card_batch.Roar_of_Domination.Roar_of_Domination",
            "game.rogue.card_batch.Tidal_Revelation.Tidal_Revelation",
            "game.rogue.card_batch.Turn_Blows_to_Power.Turn_Blows_to_Power",
        ],
    },
    "high_level":{
        "card_batch_list":[
            "game.rogue.card_batch.Break_the_Hourglass.Break_the_Hourglass",
            "game.rogue.card_batch.Carry_Beyond.Carry_Beyond",
            "game.rogue.card_batch.Channel_Mana.Channel_Mana",
            "game.rogue.card_batch.Crush_All.Crush_All",
            "game.rogue.card_batch.Land_Black.Land_Black",
            "game.rogue.card_batch.Land_Blue.Land_Blue",
            "game.rogue.card_batch.Land_Green.Land_Green",
            "game.rogue.card_batch.Land_Red.Land_Red",
            "game.rogue.card_batch.Land_White.Land_White",
            "game.rogue.card_batch.Primal_Interruption.Primal_Interruption",
            "game.rogue.card_batch.Roar_of_Domination.Roar_of_Domination",
            "game.rogue.card_batch.Tidal_Revelation.Tidal_Revelation",
            "game.rogue.card_batch.Turn_Blows_to_Power.Turn_Blows_to_Power",
        ],
    },
}