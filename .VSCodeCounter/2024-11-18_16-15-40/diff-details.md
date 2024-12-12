# Diff Details

Date : 2024-11-18 16:15:40

Directory /Users/xuanpeichen/Desktop/code/python/openai

Total : 136 files,  3407 codes, 369 comments, 739 blanks, all 4515 lines

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [README.md](/README.md) | Markdown | 32 | 0 | 13 | 45 |
| [custom_startup.sh](/custom_startup.sh) | Shell Script | 7 | 4 | 4 | 15 |
| [init.sh](/init.sh) | Shell Script | 0 | 12 | 3 | 15 |
| [src/card_Creator.py](/src/card_Creator.py) | Python | 15 | 2 | -3 | 14 |
| [src/card_python_creator.py](/src/card_python_creator.py) | Python | 30 | 9 | 7 | 46 |
| [src/cards/creature/Blazeheart Berserker  /data.json](/src/cards/creature/Blazeheart%20Berserker%20%20/data.json) | JSON | -11 | 0 | 0 | -11 |
| [src/cards/creature/Blazeheart Berserker/data.json](/src/cards/creature/Blazeheart%20Berserker/data.json) | JSON | 11 | 0 | 0 | 11 |
| [src/cards/creature/Emberheart Berserker  /data.json](/src/cards/creature/Emberheart%20Berserker%20%20/data.json) | JSON | -11 | 0 | 0 | -11 |
| [src/cards/creature/Emberheart Berserker/data.json](/src/cards/creature/Emberheart%20Berserker/data.json) | JSON | 11 | 0 | 0 | 11 |
| [src/cards/creature/Guardian of the Grove  /data.json](/src/cards/creature/Guardian%20of%20the%20Grove%20%20/data.json) | JSON | -11 | 0 | 0 | -11 |
| [src/cards/creature/Guardian of the Grove/data.json](/src/cards/creature/Guardian%20of%20the%20Grove/data.json) | JSON | 11 | 0 | 0 | 11 |
| [src/cards/creature/Night Stalker  /data.json](/src/cards/creature/Night%20Stalker%20%20/data.json) | JSON | -11 | 0 | 0 | -11 |
| [src/cards/creature/Night Stalker/data.json](/src/cards/creature/Night%20Stalker/data.json) | JSON | 11 | 0 | 0 | 11 |
| [src/cards/creature/Ralgar, the Inferno King  /data.json](/src/cards/creature/Ralgar,%20the%20Inferno%20King%20%20/data.json) | JSON | -11 | 0 | 0 | -11 |
| [src/cards/creature/Ralgar, the Inferno King/data.json](/src/cards/creature/Ralgar,%20the%20Inferno%20King/data.json) | JSON | 11 | 0 | 0 | 11 |
| [src/cards/sorcery/Flamestrike Surge  /data.json](/src/cards/sorcery/Flamestrike%20Surge%20%20/data.json) | JSON | -8 | 0 | 0 | -8 |
| [src/cards/sorcery/Flamestrike Surge/data.json](/src/cards/sorcery/Flamestrike%20Surge/data.json) | JSON | 8 | 0 | 0 | 8 |
| [src/clean_space.py](/src/clean_space.py) | Python | 3 | 0 | 1 | 4 |
| [src/database.py](/src/database.py) | Python | 13 | 3 | 4 | 20 |
| [src/game/buffs.py](/src/game/buffs.py) | Python | 91 | 3 | 18 | 112 |
| [src/game/card.py](/src/game/card.py) | Python | 8 | 0 | 4 | 12 |
| [src/game/game_function_tool.py](/src/game/game_function_tool.py) | Python | 8 | 2 | 9 | 19 |
| [src/game/player.py](/src/game/player.py) | Python | 14 | 4 | 2 | 20 |
| [src/game/player_agent_room.py](/src/game/player_agent_room.py) | Python | 3 | 2 | 2 | 7 |
| [src/game/room.py](/src/game/room.py) | Python | 48 | 6 | 17 | 71 |
| [src/game/room_server.py](/src/game/room_server.py) | Python | 7 | 0 | 2 | 9 |
| [src/game/type_cards/creature.py](/src/game/type_cards/creature.py) | Python | 17 | 0 | 5 | 22 |
| [src/game/type_cards/instant.py](/src/game/type_cards/instant.py) | Python | 13 | 0 | 3 | 16 |
| [src/game/type_cards/land.py](/src/game/type_cards/land.py) | Python | -1 | 1 | 0 | 0 |
| [src/game/type_cards/sorcery.py](/src/game/type_cards/sorcery.py) | Python | 13 | 0 | 2 | 15 |
| [src/merge_cards.py](/src/merge_cards.py) | Python | 150 | 10 | 19 | 179 |
| [src/pycards/Instant/Alchemist_s_Chaotic_Blend/model.py](/src/pycards/Instant/Alchemist_s_Chaotic_Blend/model.py) | Python | 11 | 0 | -2 | 9 |
| [src/pycards/Instant/Divine_Sanctuary/model.py](/src/pycards/Instant/Divine_Sanctuary/model.py) | Python | 36 | 0 | 8 | 44 |
| [src/pycards/Instant/Ephemeral_Insight/model.py](/src/pycards/Instant/Ephemeral_Insight/model.py) | Python | 10 | 0 | 0 | 10 |
| [src/pycards/Instant/Honorable_Protection/model.py](/src/pycards/Instant/Honorable_Protection/model.py) | Python | 10 | 0 | -3 | 7 |
| [src/pycards/Instant/Mage_s_Veto/model.py](/src/pycards/Instant/Mage_s_Veto/model.py) | Python | 9 | 0 | 0 | 9 |
| [src/pycards/Instant/Mechanist_s_Disruption_Device/model.py](/src/pycards/Instant/Mechanist_s_Disruption_Device/model.py) | Python | 13 | 0 | 9 | 22 |
| [src/pycards/Instant/Monk_s_Inner_Rebound/model.py](/src/pycards/Instant/Monk_s_Inner_Rebound/model.py) | Python | 8 | 0 | 5 | 13 |
| [src/pycards/Instant/Mystic_Convergence/model.py](/src/pycards/Instant/Mystic_Convergence/model.py) | Python | 20 | 1 | 5 | 26 |
| [src/pycards/Instant/Mystic_Insight/model.py](/src/pycards/Instant/Mystic_Insight/model.py) | Python | 4 | 0 | -1 | 3 |
| [src/pycards/Instant/Necromancer_s_Soul_Seize/model.py](/src/pycards/Instant/Necromancer_s_Soul_Seize/model.py) | Python | 22 | 0 | 5 | 27 |
| [src/pycards/Instant/Paladin_s_Judging_Light/model.py](/src/pycards/Instant/Paladin_s_Judging_Light/model.py) | Python | 5 | 0 | -1 | 4 |
| [src/pycards/Instant/Phantom_Shield/model.py](/src/pycards/Instant/Phantom_Shield/model.py) | Python | 23 | 0 | 1 | 24 |
| [src/pycards/Instant/Priest_s_Divine_Binding/model.py](/src/pycards/Instant/Priest_s_Divine_Binding/model.py) | Python | 6 | 0 | 3 | 9 |
| [src/pycards/Instant/Primal_Surge/model.py](/src/pycards/Instant/Primal_Surge/model.py) | Python | 12 | 0 | 1 | 13 |
| [src/pycards/Instant/Ranger_s_Sniping_Shot/model.py](/src/pycards/Instant/Ranger_s_Sniping_Shot/model.py) | Python | 7 | 0 | -1 | 6 |
| [src/pycards/Instant/Roar_of_the_Behemoth/model.py](/src/pycards/Instant/Roar_of_the_Behemoth/model.py) | Python | 29 | 0 | 4 | 33 |
| [src/pycards/Instant/Rogue_s_Trickery/model.py](/src/pycards/Instant/Rogue_s_Trickery/model.py) | Python | 4 | 0 | 1 | 5 |
| [src/pycards/Instant/Summoner_s_Arcane_Acquisition/model.py](/src/pycards/Instant/Summoner_s_Arcane_Acquisition/model.py) | Python | 23 | 0 | 2 | 25 |
| [src/pycards/Instant/Time_Reversal/model.py](/src/pycards/Instant/Time_Reversal/model.py) | Python | 9 | 0 | 4 | 13 |
| [src/pycards/Instant/Timeless_Intervention/model.py](/src/pycards/Instant/Timeless_Intervention/model.py) | Python | 19 | 0 | 2 | 21 |
| [src/pycards/Instant/Titan_s_Strength/model.py](/src/pycards/Instant/Titan_s_Strength/model.py) | Python | 11 | 0 | 1 | 12 |
| [src/pycards/Instant/Veil_of_Serenity/model.py](/src/pycards/Instant/Veil_of_Serenity/model.py) | Python | 4 | 0 | -1 | 3 |
| [src/pycards/Instant/Vengeful_Wrath/model.py](/src/pycards/Instant/Vengeful_Wrath/model.py) | Python | 13 | 0 | 4 | 17 |
| [src/pycards/Instant/Verdant_Growth/model.py](/src/pycards/Instant/Verdant_Growth/model.py) | Python | 11 | 0 | 0 | 11 |
| [src/pycards/Instant/Warlock_s_Dark_Pact/model.py](/src/pycards/Instant/Warlock_s_Dark_Pact/model.py) | Python | 5 | 0 | 1 | 6 |
| [src/pycards/Instant/Warrior_s_Forced_Challenge/model.py](/src/pycards/Instant/Warrior_s_Forced_Challenge/model.py) | Python | 8 | 0 | 2 | 10 |
| [src/pycards/Instant/Witch_s_Curse_Counter/model.py](/src/pycards/Instant/Witch_s_Curse_Counter/model.py) | Python | 31 | 0 | 4 | 35 |
| [src/pycards/Instant/Wizard_s_Time_Warp/model.py](/src/pycards/Instant/Wizard_s_Time_Warp/model.py) | Python | 7 | 0 | 1 | 8 |
| [src/pycards/creature/Aetherweaver/model.py](/src/pycards/creature/Aetherweaver/model.py) | Python | 19 | 0 | 0 | 19 |
| [src/pycards/creature/Angelic_Protector/model.py](/src/pycards/creature/Angelic_Protector/model.py) | Python | 6 | 0 | -1 | 5 |
| [src/pycards/creature/Avacyn__Guardian_of_Hope/model.py](/src/pycards/creature/Avacyn__Guardian_of_Hope/model.py) | Python | 8 | 0 | -1 | 7 |
| [src/pycards/creature/Blightsteel_Colossus/model.py](/src/pycards/creature/Blightsteel_Colossus/model.py) | Python | 6 | 0 | 1 | 7 |
| [src/pycards/creature/Celestial_Guardian/model.py](/src/pycards/creature/Celestial_Guardian/model.py) | Python | 2 | 0 | -1 | 1 |
| [src/pycards/creature/Celestial_Herald/model.py](/src/pycards/creature/Celestial_Herald/model.py) | Python | 15 | 0 | 3 | 18 |
| [src/pycards/creature/Celestial_Sentinel/model.py](/src/pycards/creature/Celestial_Sentinel/model.py) | Python | 2 | 0 | -1 | 1 |
| [src/pycards/creature/Celestial_Seraph/model.py](/src/pycards/creature/Celestial_Seraph/model.py) | Python | 12 | 0 | 3 | 15 |
| [src/pycards/creature/Celestial_Skyweaver/model.py](/src/pycards/creature/Celestial_Skyweaver/model.py) | Python | 15 | 0 | 0 | 15 |
| [src/pycards/creature/Chronostrider/model.py](/src/pycards/creature/Chronostrider/model.py) | Python | 5 | 0 | 0 | 5 |
| [src/pycards/creature/Dragon_Lord/model.py](/src/pycards/creature/Dragon_Lord/model.py) | Python | 26 | 0 | 4 | 30 |
| [src/pycards/creature/Dreamweaver_Archivist/model.py](/src/pycards/creature/Dreamweaver_Archivist/model.py) | Python | 13 | 0 | 3 | 16 |
| [src/pycards/creature/Elite_Squire/model.py](/src/pycards/creature/Elite_Squire/model.py) | Python | 1 | 0 | -1 | 0 |
| [src/pycards/creature/Essence_Channeler/model.py](/src/pycards/creature/Essence_Channeler/model.py) | Python | 5 | 0 | 1 | 6 |
| [src/pycards/creature/Grove_Guardian/model.py](/src/pycards/creature/Grove_Guardian/model.py) | Python | 2 | 0 | 1 | 3 |
| [src/pycards/creature/Harbinger_of_the_Eternal_Tides/model.py](/src/pycards/creature/Harbinger_of_the_Eternal_Tides/model.py) | Python | 7 | 0 | 1 | 8 |
| [src/pycards/creature/Ironclad_Crusader/model.py](/src/pycards/creature/Ironclad_Crusader/model.py) | Python | 9 | 0 | 0 | 9 |
| [src/pycards/creature/Kothar_the_Soul_Reaper/model.py](/src/pycards/creature/Kothar_the_Soul_Reaper/model.py) | Python | 11 | 0 | -2 | 9 |
| [src/pycards/creature/Luminous_Guardian/model.py](/src/pycards/creature/Luminous_Guardian/model.py) | Python | 13 | 0 | 2 | 15 |
| [src/pycards/creature/Mindshaper_Sphinx/model.py](/src/pycards/creature/Mindshaper_Sphinx/model.py) | Python | 5 | 0 | 0 | 5 |
| [src/pycards/creature/Mist_Djinn/model.py](/src/pycards/creature/Mist_Djinn/model.py) | Python | 2 | 0 | -1 | 1 |
| [src/pycards/creature/Mystic_Tidecaller/model.py](/src/pycards/creature/Mystic_Tidecaller/model.py) | Python | 6 | 0 | 0 | 6 |
| [src/pycards/creature/Night_Stalker__/model.py](/src/pycards/creature/Night_Stalker__/model.py) | Python | 1 | 0 | 3 | 4 |
| [src/pycards/creature/Nighthaunt_Assassin/model.py](/src/pycards/creature/Nighthaunt_Assassin/model.py) | Python | 10 | 0 | 1 | 11 |
| [src/pycards/creature/Nyxborn_Serpent/model.py](/src/pycards/creature/Nyxborn_Serpent/model.py) | Python | 6 | 0 | -2 | 4 |
| [src/pycards/creature/Oblivion_Devourer/model.py](/src/pycards/creature/Oblivion_Devourer/model.py) | Python | 19 | 0 | 2 | 21 |
| [src/pycards/creature/Pious_Courser/model.py](/src/pycards/creature/Pious_Courser/model.py) | Python | 3 | 0 | -3 | 0 |
| [src/pycards/creature/Radiant_Angel/model.py](/src/pycards/creature/Radiant_Angel/model.py) | Python | 19 | 0 | -1 | 18 |
| [src/pycards/creature/Ravaging_Ghoul/model.py](/src/pycards/creature/Ravaging_Ghoul/model.py) | Python | 3 | 0 | -2 | 1 |
| [src/pycards/creature/Sage_of_the_Ancient_Grove/model.py](/src/pycards/creature/Sage_of_the_Ancient_Grove/model.py) | Python | 14 | 0 | -1 | 13 |
| [src/pycards/creature/Seraph_of_the_Eternal_Flame/model.py](/src/pycards/creature/Seraph_of_the_Eternal_Flame/model.py) | Python | 6 | 0 | 1 | 7 |
| [src/pycards/creature/Shadowtide_Leviathan/model.py](/src/pycards/creature/Shadowtide_Leviathan/model.py) | Python | 7 | 0 | -1 | 6 |
| [src/pycards/creature/Spectral_Harbinger/model.py](/src/pycards/creature/Spectral_Harbinger/model.py) | Python | 8 | 0 | 2 | 10 |
| [src/pycards/creature/Sunlit_Priestess/model.py](/src/pycards/creature/Sunlit_Priestess/model.py) | Python | 3 | 0 | -1 | 2 |
| [src/pycards/creature/Sylvan_Harmonist/model.py](/src/pycards/creature/Sylvan_Harmonist/model.py) | Python | 15 | 0 | -3 | 12 |
| [src/pycards/creature/Sylvan_Warden/model.py](/src/pycards/creature/Sylvan_Warden/model.py) | Python | 20 | 0 | 3 | 23 |
| [src/pycards/creature/Temporal_Traveler/model.py](/src/pycards/creature/Temporal_Traveler/model.py) | Python | 15 | 1 | 1 | 17 |
| [src/pycards/creature/Thalassian_Tidecaller/model.py](/src/pycards/creature/Thalassian_Tidecaller/model.py) | Python | 3 | 0 | 1 | 4 |
| [src/pycards/creature/Thornroot_Druid/model.py](/src/pycards/creature/Thornroot_Druid/model.py) | Python | 14 | 0 | -1 | 13 |
| [src/pycards/creature/Thornwood_Guardian/model.py](/src/pycards/creature/Thornwood_Guardian/model.py) | Python | 2 | 0 | 0 | 2 |
| [src/pycards/creature/Thornwood_Sentinel/model.py](/src/pycards/creature/Thornwood_Sentinel/model.py) | Python | 1 | 0 | -1 | 0 |
| [src/pycards/creature/Thunderclap_Behemoth/model.py](/src/pycards/creature/Thunderclap_Behemoth/model.py) | Python | 9 | 1 | 0 | 10 |
| [src/pycards/creature/Thundering_Behemoth/model.py](/src/pycards/creature/Thundering_Behemoth/model.py) | Python | 8 | 0 | 1 | 9 |
| [src/pycards/creature/Tidal_Sprite/model.py](/src/pycards/creature/Tidal_Sprite/model.py) | Python | 1 | 0 | 2 | 3 |
| [src/pycards/creature/Verdant_Titan/model.py](/src/pycards/creature/Verdant_Titan/model.py) | Python | 23 | 0 | 2 | 25 |
| [src/pycards/creature/Verdant_Wyrm/model.py](/src/pycards/creature/Verdant_Wyrm/model.py) | Python | 16 | 0 | -2 | 14 |
| [src/pycards/creature/Voidwisp_Harbinger/model.py](/src/pycards/creature/Voidwisp_Harbinger/model.py) | Python | 5 | 0 | 0 | 5 |
| [src/pycards/creature/Vorinclex__Apex_of_Mutation/model.py](/src/pycards/creature/Vorinclex__Apex_of_Mutation/model.py) | Python | 26 | 0 | 2 | 28 |
| [src/pycards/sorcery/Judgment_Day/model.py](/src/pycards/sorcery/Judgment_Day/model.py) | Python | 16 | 0 | -3 | 13 |
| [src/pycards/sorcery/Soul_Transfer/model.py](/src/pycards/sorcery/Soul_Transfer/model.py) | Python | 3 | 0 | 1 | 4 |
| [src/server.py](/src/server.py) | Python | 12 | 3 | 2 | 17 |
| [src/server_start.py](/src/server_start.py) | Python | 2 | -2 | 0 | 0 |
| [src/webpages/card.js](/src/webpages/card.js) | JavaScript | -1 | 1 | 0 | 0 |
| [src/webpages/deckpage/deck.html](/src/webpages/deckpage/deck.html) | HTML | 1 | 0 | 0 | 1 |
| [src/webpages/draw_card/draw.html](/src/webpages/draw_card/draw.html) | HTML | 1 | 0 | 0 | 1 |
| [src/webpages/gaming_page/action_bar.js](/src/webpages/gaming_page/action_bar.js) | JavaScript | -2 | 2 | 0 | 0 |
| [src/webpages/gaming_page/animation.js](/src/webpages/gaming_page/animation.js) | JavaScript | 3 | 21 | 0 | 24 |
| [src/webpages/gaming_page/button.js](/src/webpages/gaming_page/button.js) | JavaScript | 157 | 11 | 51 | 219 |
| [src/webpages/gaming_page/card_battle.js](/src/webpages/gaming_page/card_battle.js) | JavaScript | -14 | 14 | 0 | 0 |
| [src/webpages/gaming_page/card_battle_main.js](/src/webpages/gaming_page/card_battle_main.js) | JavaScript | -4 | 4 | 0 | 0 |
| [src/webpages/gaming_page/card_hand.js](/src/webpages/gaming_page/card_hand.js) | JavaScript | -1 | 1 | 0 | 0 |
| [src/webpages/gaming_page/card_hand_main.js](/src/webpages/gaming_page/card_hand_main.js) | JavaScript | -1 | 1 | 0 | 0 |
| [src/webpages/gaming_page/gaming.css](/src/webpages/gaming_page/gaming.css) | CSS | 13 | 0 | 1 | 14 |
| [src/webpages/gaming_page/gaming.html](/src/webpages/gaming_page/gaming.html) | HTML | 3 | 0 | 0 | 3 |
| [src/webpages/gaming_page/gaming.js](/src/webpages/gaming_page/gaming.js) | JavaScript | -141 | 180 | 11 | 50 |
| [src/webpages/gaming_page/message_processor.js](/src/webpages/gaming_page/message_processor.js) | JavaScript | -1 | 9 | 2 | 10 |
| [src/webpages/gaming_page/selection_page.js](/src/webpages/gaming_page/selection_page.js) | JavaScript | 5 | 0 | 2 | 7 |
| [src/webpages/gaming_page/special_effects.js](/src/webpages/gaming_page/special_effects.js) | JavaScript | 2 | 1 | 1 | 4 |
| [src/webpages/homepage/book.css](/src/webpages/homepage/book.css) | CSS | 190 | 3 | 18 | 211 |
| [src/webpages/homepage/book.js](/src/webpages/homepage/book.js) | JavaScript | 381 | 12 | 36 | 429 |
| [src/webpages/homepage/home.js](/src/webpages/homepage/home.js) | JavaScript | 33 | 0 | 9 | 42 |
| [src/webpages/homepage/protectpage.html](/src/webpages/homepage/protectpage.html) | HTML | 3 | 0 | 3 | 6 |
| [src/webpages/homepage/style.css](/src/webpages/homepage/style.css) | CSS | 10 | 0 | 1 | 11 |
| [src/webpages/loginpage/login.html](/src/webpages/loginpage/login.html) | HTML | 6 | 0 | 0 | 6 |
| [src/webpages/loginpage/login.js](/src/webpages/loginpage/login.js) | JavaScript | 0 | 0 | 2 | 2 |
| [src/webpages/tech_doc/content.html](/src/webpages/tech_doc/content.html) | HTML | 22 | 0 | 7 | 29 |
| [src/webpages/tech_doc/content_En.html](/src/webpages/tech_doc/content_En.html) | HTML | 1,421 | 47 | 415 | 1,883 |

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details