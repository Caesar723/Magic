from openai import OpenAI
import os
import json
import requests
import time
import random
from bs4 import BeautifulSoup
from gpt4_openai import GPT4OpenAI

from PIL import Image


ORGPATH=os.path.dirname(os.path.abspath(__file__))
FORWARDED_IP = (
    f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
)
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "cache-control": "max-age=0",
    #"content-type": "application/x-www-form-urlencoded",
    # "referrer": "https://www.bing.com/images/create/",
    # "origin": "https://www.bing.com",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "x-forwarded-for": FORWARDED_IP,
    "Cookie":'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..smb78KtJb-1csLSF.Grx_RsQIJCDwsmF3Wn5c8ClgFPcrCSXdfDjEbQR-VwvlE69AF-jtAHyjh7JlYyXPndHNsKp_WLnBtGaKqwnKuTbPrS4evjcqSXB0e9WHKWB9AfyG8-OZ4v0WxNAyLoxk2wtryGM3I5E8X8TB-d52npB9JVz1rw_aD44uXKxAHsi_cdvTXBynpRhO2OIQdcHjtBlad2qeo2ZYEdZclXZYX5x-hBm79BlO4y58b8QyJIWgfC0SJOnqaFBBVCJ6l7IewdYfONLwSdqIHn-mk_QVCcquRs_aRIOQxFEQ5G9B1Tyayn7P9aHH9zqVvjmHv5b_bY6JUKGUDpoYYBg7AZIlCmyD8EZpC5HYeFyK0xEhca5T_rLKkOKQnqUYuB5XJZ6FGgDt5T_xMWfQeMvQicS2nLFOfwU7PqHf-auMttVCKAYBvoBM5qN4r-XVuMSmukDLE5ZRRRRuZ38KCfVXdC_AJiR1dSYYyQpumAQ6lvUz1Mzf7pj3bxcgf9Aq6yv3xTwbXtsme2W6Ab1ePVoY8IhJb5_1_EIuZNlVcxe_4q53HT6bTxmEPY74LRXJm1Gs2h9bBfqSLCLdhE3WRAXZub_Ca2JDyYUpK3nkPW1yt_14jDBzpDNl-Fb81ee1PI4QcRmmjlIOM2VQGWUMFq0cAV81HFTqF4EzK7rGzB_1fF5u7w2KuIKG65tHJfjLzGVhbCYb8jHmMH9KP9hwE4jrNwPG43eTw7jwIW9qkEMOFfJCOjRUDMkJ_-ZghbWW_Ep1g093AWh9YCxFo5Sn1VzKpNa_QdhvtTLWOQmXbffNz4kff54uKoUdeyGs4Glf2tel3rQUhgQdRm0BuDSPrWCVMMXMcIYjDeuNKOWlxxr9CNjgtgIEJSNuURaF3S67TXUxLIbZiH303unPCIzHlqZsRn411Dp9P6Fi0n-wHKEhWEXWUKoVBj1ZUzCh2_xEzuFEDCOGwxYipgcTYoOqxAh14XrgAjUo5zNU0fe_l0aGnhdsb53emF_XdeWEIEPYm_EMnP1zzsqFn1yZkjN2LmZHYI7TgnnxfmydSBTCf9Tnvv5-DQAnJlfAdRjapvw5CDC99AP3dd0AVh6GoUkjecdP_jBl7WwE9YfQmHxo7LJ33l0LRQ9VHUsc5Vnxx1ipXVwD06rPr3TD7URwg-5l9_IogPnZRQd0BV-H3UF5G7a1DbUzoqcIhGqTWm_YzQ9TQKMkEOJ6Gx73eNi3BRvaqmPfIUdjyqmD-RNazmQ7G6W_K_tNOemRW6Vbi4hZUsltkwcaagvxiolKTN-aMS8dzLNEUIZvYXRZ-k-M6sx3hcmODfHwyNFab_sLjvpWw-DTBUt616Oc6hDcv4CkG5pU6tbBqupJ8xx_tmNbxr4aclOj83C1h_uXJMSFn4JVkf9XGHzpB5gYigEYM8rDG8fqV49ISZkEM3SlIhXMc-N0eCcHnReeqAJK_-nuiqjshKugBjeVp2XkllInPXfYpvWyPRYxak2LolwSqN4DDhN2m1lsa1jmZcBeqx2AWpi3B7Fat4N21A_zH_A1kiUOTX6mSgHtamtmNuFAevrRo7PvTXx4lqLVzq1bnrEbvM6unf-qvhJ0g-hkJ9n4BM0zo3IQtZG2rRf3uaTEbovy0k48YSsIjXQQY1mdMgCEzGYUMfnl6-v8sqGqdzlYUpWxke87-m-gazT-TmVAevAP5H0tqDmFXq2fwam8wu9TVVZDsg2VMH1XmStGkM-fhXr_Ch0ksTvLBeXL-yjKHyJQlccMaySR6p0UBnhJRDO8Mj5c8pgfa2cD8WIKDH_QIgQohahDjEkpGKaKnJZHM6LoxOirVCsbF7_iLUBXrRG0P-IGJ743EerY5UfxxfytWqgZ2SwMUt5Swe1oSH0aSgALPPNQBvCTDo06_GRjxdAFFyCl_KuLfPyR0ACtcW88MuPy7aIB7uvkFSgJGPBC9gBORipT8c1QkEq-qx6AIO12XnEpmmYuKA5dRtg2KjtBtK7zLsCg0zzdsKwxYdkroLfkZTS7aDeJ4J0lA4pqsINQ32zMdtYTAkayAKFwo45gF0bcOd9BBGHUk64GtgO0nq_K0hdFwPEnOXEd9kPjBcnyRxHWwdqf8CbphkufYmi1r880RZyFmwvved9FOSiGfnudYLsz_Z1ikQ4WEMkUMlDaF_jQw5EW2iFE9EUnR1Z2K9ssMaeHCe7XHuFxOksV3kjOK1L9FItF9xIpvHPfrkWTLOdKKUS_Bc9FuwB9AxDVvTab8ka_2RBe8ZsB5QQxpQBSf3YOmhsX7JV89qxDm7ZGA9Z5-Dih7sOi1hC1z3tqJJ3xkgu9YqHbegf0j9Uh50EuH1D6zgBGv0Bbwh6ddfn7KVSOenEKMsMrsn7RVcBj9u2Pzc0DBzfDJVwwN-pIfBHBd2LD3o8buuG926mvepALLso3BXwY9JXRzRyx2tXz1fWAVG7EG0I2vQDBT9ijsNFdP9oIiHhQJ0WZ2OA6egpGwRXgOySj56U2ZFbIIM4C4o0vP9-CnSs-M3JLQrpN78bTljVnqSIuSvl_jSZoQUnGf5nSUH8BsLKNW-dQ8LDO3p8CUYsw7Jw1ZTR9_qanIrW-QPsORXmko9_raciA5UanLfxqNvW81W0VEGKOGcWSLkvB_nu-cAH76HDTjHRk8HobM1k9ks-qmV_mUY8Lrb0SJH_TqFc0c4_a7beSGzwlUGiPQzaGbyiN21CrRPMN1IqXsbHzbKhB0pha2XQ_7OQtZWLbDhOiLZve-JlwSCz8ZWCrNmBf0Alw0JrJkzXuP4az8_XMqEyORMoTvQQnJhSSo8pFMaIctVseyk6FfsPSiT9wIU-RkhWtawNYvUWb2URtTqdSESeZostHPXg8onisBLHgFcfW_uhtGfr7H0wzCyOoUOCtbprR8rzo2A4KdKcc--fDXaDrGZlsywSv9l8.i-GggIi4qzfajgBSgy43gw'
}

 
class Card_Creater:
    
    #cost:U:blue,B:black,W:white,R:red,G:green
    def __init__(self) -> None:
        self.dic_type_path={"Creature":"card_info/creature.txt","Land":"card_info/land.txt","Sorcery":"card_info/sorcery.txt","Instant":"card_info/Instant.txt"}
        self.dic_cards_path={"Creature":"cards/creature","Land":"cards/land","Sorcery":"cards/sorcery","Instant":"cards/Instant"}
        
        self.client = OpenAI(api_key="sk-BXIUJfFqAg1XqqTW7o5tQK9YyhyPQbwdNt9sMm4RIZuiStaW",base_url="https://api.chatanywhere.tech")
        self.messages_Creature=[
                {"role": "system", "content": "Activate GPT-3.5-turbo assistant, set to Magic: The Gathering Creature card design mode. Each cards are different."},
                {"role": "user", "content": "Please design a new Creature card for Magic: The Gathering."},
                {"role": "assistant", "content": "Name: [Name]\nRarity: [Common/Uncommon/Rare/Mythic Rare]\nType: [Human/Skeleton/Beast/Angel/Goblin/Demon/Artifact Creature/Elemental/etc.]\nPower/Toughness: [Value]\nCost: [Mana Cost]\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance]."}
            ]
        self.messages_Land=[
                {"role": "system", "content": "Activate GPT-3.5-turbo assistant, set to Magic: The Gathering Land card design mode. Each cards are different."},
                {"role": "user", "content": "Please design a new Land card for Magic: The Gathering."},
                {"role": "assistant", "content": "Name: [Name]\nRarity: [Common/Uncommon/Rare/Mythic Rare]\nType: [Water/Light/Dark/Fire/Forest]\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance]."}
            ]
        self.messages_Sorcery=[
                {"role": "system", "content": "Activate GPT-3.5-turbo assistant, set to Magic: The Gathering Sorcery card design mode. Each cards are different."},
                {"role": "user", "content": "Please design a new Sorcery card for Magic: The Gathering."},
                {"role": "assistant", "content": "Name: [Name]\nRarity: [Common/Uncommon/Rare/Mythic Rare]\nCost: [Mana Cost]\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance]."}
            ]
        self.messages_Instant=[
                {"role": "system", "content": "Activate GPT-3.5-turbo assistant, set to Magic: The Gathering Instant card design mode. Each cards are different.The number of cards of each type needs to be equal (B/U/G/R/W), with more fees and less fees"},
                {"role": "user", "content": "Please design a new Instant card for Magic: The Gathering."},
                {"role": "assistant", "content": "Name: [Name]\nRarity: [Common/Uncommon/Rare/Mythic Rare]\nCost: [Mana Cost]\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance]."}
            ]
        #self.load_info()
        self.dic_each_arr={"Creature":self.messages_Creature,"Land":self.messages_Land,"Sorcery":self.messages_Sorcery,"Instant":self.messages_Instant}


        self.COOKIE='eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..mF66w6nHIdDFdJvJ.7PCw_qeXMaqzco3W7PX2N4y5ShXg5EvCxK8x-m-XywwxjboWY__5je4lPUe8WZDK__AfKspLDNXVeh6fpuGHgn_5ocuKFLKvqsVPja9YL-4XnPfk3xA8wKwr3hlEeBz49JUhO1G83QSKAwPmcUPYx_yxfjuuJ4byMxZP7zHIz1pGJADywnoyEGY7Q1BLZfrUkPyiZ2h_55bDjqx7Kwp3F-EapFtRh3hXvo7Da2784kfphw7_bxXqHKKE6gx0RLHvViNxLvtRXeMcWrNUxE0PQ1bdz3V_pZXju9ZZ0lpWpoIJQogJjtLQWIVuD_SXKER903ZTv6dwkInmdEyYTNDTIBueW-i7ziAoHvhDkUCpuVIQm5EBfWA5Pj3pEb7SUCqOgT02GzYlG7b3Jp9TpI62J2MeM14cm0Agy5OW-Z51FrOXHtLKEN9XVrkrOUyMCq7vCqeyUAhFQobA4rdqf_cev0wgZRxdCTeXKMcSYeoQj8mT3XfICH3tNRGu72fCOJDKoNSUz3I_cp63FD-MBFic7SHAPdK7_mDDSM8x-JLVDf6HOAJirEoc8Zk6BpkTy1wIpYvTiZRepsnrRykxGWHRAqdbyQhLsvpiW-FMFyXZVH_tLAjqlYwXIhooDb2L1sudOXuS6Qbdy-xD8zeiHEwEeD7H_dnaYtjUiFE6EEGNDceqgPR7M26G78WbbHhTFPer1hAyWvUWbC9fq_Bi51-oOvAdsfFmdrk3HugwNwujbfvV8Q213EKPZ9s2v7ht9Wp2f1rnTNSFV7Hn1KwgY42xBWKa-jVO5LDK60EzP6DQVBSbXESMVYTR5SIWy1qb7JZ22Fk0YTGO_jM3cVs9qFi0FoQZyqat_5whNyjQAk08GbOciF57UGdSuxSqQPebo5_gg4IbUedEhNE_d9NtOj-fgZZPcYdwQtZuSClanOtYqQA7nlY0REuKZpi98wq9q_YvBDig2RRTQGwasKzebMKwh0f3tdN1zJ1FUJZqYVZNqclJfn03SECYtactxN1DEeEZSisE4XvwrP_GLhwnmePKxSIEzslfz8z3RqpT2MXxRE-XkWM8axoz2hGgkVVpS7txusPFoB3DtB5kqZFnBOpSp6DVVJSv5s5kJznyDfamhIuznU6rCNRXzLH6DI2-1WZH1YY5R2m5t3rjI-2Et-QmCBQFsQz5WN-7XE3RvjbBPe_69zsz6gVD-iHxCfL-tSZasHPoKKBauKQTu2uaVJDnq4QGEfxHk__oYpGNXLFKaqf6Mj2uSN_wEjAeDDd2ekL3o8BeWqS9HqTVk2Yr0-fBKYP3Mf3nV-CSbwKq8LsUeteUkMvVEy6S-x2XneLyKg4HPZszWMCvOEkojJmS5iVNTtVOX3_Dd3JPtsfdf1MgmcqIFHI2MWSXQ-ipNbsaV_7LdxaYYKki7LPMo2sZovYNOzYLEKHeWoWz2EWOyvvi1XF0ec4U-rAkmW8dSYWUtOFIn6-d_cn0clUtvusFtoIqMXIxfWIvr1ORx45YlNlPSG6jmTcmK023yxyMgN3kW3AR0NyBidsKMyea1GHwTYWOQkHZm9_jcICC3HPhAAX3miW_BlSbjoT3V-KsJP0kDE8zrdgdYHh-DAXv2L8iGANrpoqJY63nWX3zvz8aRyqY8SzfzEvHf-70NFemnXudIvefO87HpOcAcBQgx__wc4Ai71Fca5EtVL9zB0vqpPTNUnYGPBnkNqpdepVV0uDvaJFW4sQUkoBi6-4Ut2X7NB4z3QTXut-eC5KXTEm3PrcLHR6IwXSvVZ6HZAOnHsbRuej9FlsgUMrp4q4tB11MMG8uy8AMmwnnI1WL3TZZnt3BGCFw8bGzcQn6YIeytaO6O-v6CnHlVmoeG6pL_HmfIbVY_qE6ok-ucFzX2bJbh-wpgmF-wjlAnX0tOQSxX3Um9BvpaygLt2xymoObFWlmG0a7X-_TN5tMBFoOlXqvP9Gh0KDa_-9ZaELqXwz8ZmzsvDf-Q9_dftc8mcNIAl9PZG-KxOltnOg1dBPlwx7LbyoaKLydsKpWAPJuKY2oerA6K2umq2u8X7mLTDD7yHv31jD-1sySP5r6DDufUKsvKMs-fZa9NlxYGNOnTUUKESICi_Dm8KotuUhGQjfkHIhqxkpiPFLX88SQj-kXXdXuprX4f0Jq1lxcSrc0-qfELeno4cQ0KII4vaF7UJGUVkINpTyFO6jYkxlqPPrRfsry4fFHfbkmBrIlPNye94bhL85LrR3BySDaB9wiblQ4rtzXz2oJInJ4Sd5MuZaLUZ2szBccClXdYybhnv0PrllZXacJoHji35atcB9C3PE8R3TAQJrWijM0S0qX86p5C1cdgkRfkKmjhgZgrs4BGCR9OI-6v3OR-3nXCabQdNM4R0N9UFFczUT3DtLolK3biInvGR_x9_4m7wjfT5tgVtZhvrUejs_brL1IYwMk8BARH7qnayqUo5o8GN6CrXonrd-jxojOwMMZ7WI4MbRlfSTgfZDc4pbxYluL57wLau2aeplZJM4jLZUCX16BZZsStviSM0FwhtIgHJsPnb_WWmCsU8S_Bc_N3IXxeY0DPg_insHh6rkxEbC4nzPaLTuGdnUT97bIkJtLP1UyZPMvvYEH14zpNaW9bgoimN77PXwJLRZLnTLmPmQ0pNzyXeGMZS9ZJk3njF81F_ZmoLOXoneBEKkCftLBUGoxOcLO1XeZlsGEvw7jvuq6cv64hEDRn8yN0FQKdFjDJLxJgIN6qTCjRLukt-JrNXSqrsU6CIK7pbKDrG-3He86AILntmkNGpnrPpeBcJwTJ3x4SUEJ4ivZZWL2ymgcujTidK_xIRGT7aetFGyl0hmnPK5G1KgvV1lnN1BZr6USQ1V1SoImKFyT241eklbMuLINov5yFseszIjmy8351O3ANGZI3HK9ZAXHWiHIE5Vkabg.L8XnAZXmIdV9YJTL1ICW6w'
        self.llm = GPT4OpenAI(token=self.COOKIE, headless=False,
                        model='gpt-4' # DALL-E 3 only works with gpt-4
                        )

        

    #
    def create_Creature(self):
        #print(self.messages_Creature)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages_Creature

        )

        print(response.choices[0].message.content)
        successful_flag=self.process_data_gpt("Creature",response.choices[0].message.content)
        if successful_flag:
            self.save_info("Creature",response.choices[0].message.content)
            
        

    def create_Land(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages_Land

        )

        print(response.choices[0].message.content)
        successful_flag=self.process_data_gpt("Land",response.choices[0].message.content)
        if successful_flag:
            self.save_info("Land",response.choices[0].message.content)
        

    def create_Sorcery(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages_Sorcery

        )

        print(response.choices[0].message.content)
        successful_flag=self.process_data_gpt("Sorcery",response.choices[0].message.content)
        if successful_flag:
            self.save_info("Sorcery",response.choices[0].message.content)
        

    def create_Instant(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages_Instant

        )

        print(response.choices[0].message.content)
        
        successful_flag=self.process_data_gpt("Instant",response.choices[0].message.content)
        if successful_flag:
            self.save_info("Instant",response.choices[0].message.content)

        

    def save_info(self,type,content:str):
        self.dic_each_arr[type].append({"role": "assistant", "content": content})
        content=content.replace("\n","#")
        with open(f"{ORGPATH}/{self.dic_type_path[type]}","a") as file:
            file.write(f"{content}\n")
        print("save successfully ",f"{ORGPATH}/{self.dic_type_path[type]}")

    def load_info(self):
        self.load("Creature",self.messages_Creature)
        self.load("Land",self.messages_Land)
        self.load("Sorcery",self.messages_Sorcery)
        self.load("Instant",self.messages_Instant)

    def load(self,type,dict_message:list):
        with open(f"{ORGPATH}/{self.dic_type_path[type]}","r") as file:
            all_message=file.read()
        messages=all_message.split("\n")
        for message in messages:
            if message:
                message=message.replace("#","\n")
                dict_message.append({"role": "assistant", "content": f"{message}"})
        

    def process_data_gpt(self,type,content:str):
        data={}
        name=""
        prompt=""
        for line in content.split("\n"):
            splited=line.split(": ")
            title,message=splited[0],': '.join(splited[1:])
            if title=="Power/Toughness":
                Power_Toughness=message.split("/")
                data["Power"],data["Toughness"]=int(Power_Toughness[0]),int(Power_Toughness[1])
            else:
                data[title]=message
            if title=="Name":
                name=message
            elif title=="Appearance Description":
                prompt=message

        folder_name=f"{ORGPATH}/{self.dic_cards_path[type]}/{name}"
        if not os.path.exists(folder_name):
            
            data_img=self.create_image_case2(prompt)
            os.mkdir(folder_name)
            self.download_image(data_img,f'{folder_name}/image.jpg')
            with open(f'{folder_name}/data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("save successfully")
            print()
            return True
        else:
            print("error occur")
            print()
            return False

    def get_image_url_from_message(self,prompt:str)->str:#get url if image
        prompt=prompt.replace(" ","+")
        Run=True# the controel of while loop when the response of response_get_img have text it become False
        url_encoded_prompt = requests.utils.quote(prompt)
        payload = f"q={url_encoded_prompt}&qs=ds"
        

        response_first_post = requests.post(f'https://www.bing.com/images/create?q={prompt}&rt=4&FORM=GENCRE',
                                headers=HEADERS,
                                allow_redirects=False,
                                data=payload)#post to server in order to get response header
        
        
        X_EventID=response_first_post.headers["X-EventID"]#response header
        

        response_first_get = requests.post(f'https://www.bing.com/images/create?q={prompt}&rt=4&FORM=GENCRE&id={X_EventID}',
                                headers=HEADERS,
                                allow_redirects=False,
                                data=payload)#in order to get IG
        
        
        IG=self.getIG(response_first_get)
        
        print()
        while Run:
            
            print("loading....")
            url=f'https://www.bing.com/images/create/async/results/1-{X_EventID}?q={prompt}&IG={IG}&IID=images.as'
            
            HEADERS["Referer"]=url
            response_get_img=requests.get(url,headers=HEADERS)# check whether the img is created
            
            
            img_urls=self.getImageUrl(response_get_img)
            if img_urls:
                Run=False
            time.sleep(3)
        print("image created:"+img_urls)
        print()
        return img_urls

    def getIG(self,response):
        soup=BeautifulSoup(response.text, "html.parser")# use BeautifulSoup to analysis html page
        

        ###this code is used to find IG 
        finds=soup.findAll("script", {"type": "text/javascript"})
        
        split_list=((str(finds[1]).split(";")[0]).split(","))
        IG=split_list[7][4:-1]
        ###

        return IG


    def getImageUrl(self,response):#str of  https://th.bing.com/th/id/{}
        text=response.text
        
        if text:
            
            soup=BeautifulSoup(text, "html.parser")# use BeautifulSoup to analysis html page
            div_tag = soup.find("div", {"id": "gir_async"})
            
            img_id=div_tag.get("fir-th")
            url=f"https://th.bing.com/th/id/{img_id}"
            return url
        else:
            return False
        
    def download_image(self,data,path):
            with open(path, 'wb') as file:
                file.write(data)

    def create_image_case1(self,prompt):#data
        url=self.get_image_url_from_message(prompt)
        response_get_img=requests.get(url,headers=HEADERS)
        if response_get_img.status_code == 200:
            return response_get_img.content
        else:
            raise

    def create_image_case2(self,prompt):
        img_bytes = self.llm.generate_image(f"Generate an image of {prompt} style:fantasy art")
        return img_bytes
    
    def initinal_card_info(self):
        colors=["U","W","G","R","B"]
        
        type_land={
            "U":'Water',
            "W":'Light',
            "G":'Forest',
            "R":'Fire',
            "B":'Dark'
        }
        Raritys=["Common","Uncommon","Rare","Mythic Rare"]
        user_con="Please design a new {} card for Magic: The Gathering. Each cards are different. The Cost must be ?{} (? should be integer or no ?). The Rarity must be {}"
        Land_con="Please design a new {} card for Magic: The Gathering. Each cards are different. The Rarity must be {}. The Type must be {}."
        content_type={
              "Creature":"Name: [Name]\nRarity: {}\nType: [Human/Skeleton/Beast/Angel/Goblin/Demon/Artifact Creature/Elemental/etc.]\nPower/Toughness: [Value]\nCost: 1{}\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance].",
              "Land":"Name: [Name]\nRarity: {}\nType: [Water/Light/Dark/Fire/Forest]\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance].",
              "Sorcery":"Name: [Name]\nRarity: {}\nCost: 1{}\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance].",
              "Instant":"Name: [Name]\nRarity: {}\nCost: 1{}\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance]."

        }
        for i in range(5):
            for color in colors:
                for Rarity in Raritys:
                    for type in content_type:
                        if type!='Land':
                            cost=color*(i+1)
                            name=f"{type}{Rarity}{cost}"
                            with open(f"{ORGPATH}/card_info_2/{name}.txt",'w') as file:
                                text_1=user_con.format(type,cost,Rarity)
                                text_2=content_type[type].format(Rarity,cost)
                                text_2=text_2.replace("\n",'#')
                                file.write(f"{text_1}\n{text_2}")
                        else:
                            name=f"{type}{Rarity}{type_land[color]}"
                            with open(f"{ORGPATH}/card_info_2/{name}.txt",'w') as file:
                                text_1=Land_con.format(type,Rarity,type_land[color])
                                text_2=content_type[type].format(Rarity)
                                text_2=text_2.replace("\n",'#')
                                file.write(f"{text_1}\n{text_2}")
        return 
    
    def start_create_prompt(self):
        colors=["U","W","G","R","B"]
        
        type_land={
            "U":'Water',
            "W":'Light',
            "G":'Forest',
            "R":'Fire',
            "B":'Dark'
        }
        Raritys=["Common","Uncommon","Rare","Mythic Rare"]
        user_con="Please design a new {} card for Magic: The Gathering. Each cards are different. The Cost must be x{}(x can be any number :1~5 ). The Rarity must be {}"
        Land_con="Please design a new {} card for Magic: The Gathering. Each cards are different. The Rarity must be {}. The Type must be {}."
        content_type={
              "Creature":"Name: [Name]\nRarity: {}\nType: [Human/Skeleton/Beast/Angel/Goblin/Demon/Artifact Creature/Elemental/etc.]\nPower/Toughness: [Value]\nCost: 1{}\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance].",
              "Land":"Name: [Name]\nRarity: {}\nType: [Water/Light/Dark/Fire/Forest]\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance].",
              "Sorcery":"Name: [Name]\nRarity: {}\nCost: 1{}\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance].",
              "Instant":"Name: [Name]\nRarity: {}\nCost: 1{}\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance]."

        }
        max_val=self.find_max_line()
        print(max_val)
        for i in range(5):
            for color in colors:
                for Rarity in Raritys:
                    for type in content_type:
                        if type!='Land':
                            cost=color*(i+1)
                            name=f"{type}{Rarity}{cost}"
                            path=f"{ORGPATH}/card_info_2/{name}.txt"
                            with open(path,'r') as file:
                                text=file.read()
                            if max_val[1] or max_val[0]>len(text.split("\n")):
                                contents=self.reorganise_content(text)
                                self.process_respond_mess(type,contents,path)
                                #print(contents)
                        else:pass
        for color in colors:
            for Rarity in Raritys:
                for type in content_type:
                    if type=='Land':
                        name=f"{type}{Rarity}{type_land[color]}"
                        path=f"{ORGPATH}/card_info_2/{name}.txt"
                        with open(path,'r') as file:
                            text=file.read()
                        if max_val[1] or max_val[0]>len(text.split("\n")):
                            contents=self.reorganise_content(text)
                            self.process_respond_mess(type,contents,path)
                            
                    pass
    def process_respond_mess(self,type,message,path):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message

        )
        print("*"*100)
        print("这是输入的内容",message)
        print("*"*100)
        print("这是输出的内容",response.choices)
        print("*"*100)
        return
        
        successful_flag=self.process_data_gpt(type,response.choices[0].message.content)
        if successful_flag:
            self.save_info_v2(type,response.choices[0].message.content,path)
    def save_info_v2(self,type,content:str,path):
        self.dic_each_arr[type].append({"role": "assistant", "content": content})
        content=content.replace("\n","#")
        with open(path,"a") as file:
            file.write(f"\n{content}")

    def process_data_hand_make(self,content:dict):
        json_list=content
        path=f"{ORGPATH}/card_info/other_cards.txt"
        for key in json_list:
            name,type=key.split("|")
            successful_flag=self.process_data_gpt(type,json_list[key])
            if successful_flag:
                self.save_info_v2(type,json_list[key],path)
        
       

    def find_max_line(self):
        colors=["U","W","G","R","B"]
        type_land={
            "U":'Water',
            "W":'Light',
            "G":'Forest',
            "R":'Fire',
            "B":'Dark'
        }
        
        Raritys=["Common","Uncommon","Rare","Mythic Rare"]
        content_type={
              "Creature":"Name: [Name]\nRarity: {}\nType: [Human/Skeleton/Beast/Angel/Goblin/Demon/Artifact Creature/Elemental/etc.]\nPower/Toughness: [Value]\nCost: {}\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance].",
              "Land":"Name: [Name]\nRarity: {}\nType: [Water/Light/Dark/Fire/Forest]\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance].",
              "Sorcery":"Name: [Name]\nRarity: {}\nCost: {}\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance].",
              "Instant":"Name: [Name]\nRarity: {}\nCost: {}\nStory Background: [Story Background]\nAbility: [Ability Description]\nAppearance Description: [Detailed Description of Appearance]."

        }
        max_value=0
        min_value=999
        for i in range(5):
            for color in colors:
                for Rarity in Raritys:
                    for type in content_type:
                        if type!='Land':
                            cost=color*(i+1)
                            name=f"{type}{Rarity}{cost}"
                            url=f"{ORGPATH}/card_info_2/{name}.txt"
                            with open(url,'r') as file:
                                length=len(file.read().split("\n"))
                                max_value=max(max_value,length)
                                min_value=min(length,min_value)
                        
        for color in colors:
            for Rarity in Raritys:
                for type in content_type:
                    if type=='Land':
                        name=f"{type}{Rarity}{type_land[color]}"
                        url=f"{ORGPATH}/card_info_2/{name}.txt"
                        with open(url,'r') as file:
                            length=len(file.read().split("\n"))
                            max_value=max(max_value,length)
                            min_value=min(length,min_value)

        if max_value==min_value:
            return (max_value,1)
        else:
            return (max_value,0)


    def reorganise_content(self,text):
        arr=text.split("\n")
        two_text=arr[:2]
        other=arr[2:]
        #print(other,two_text)

        contents=[
                {"role": "system", "content": "Activate GPT-3.5-turbo assistant, set to Magic: The Gathering Instant card design mode. Each cards are different."},
                {"role": "user", "content": two_text[0]},
                {"role": "assistant", "content": two_text[1]}
            ]
        for content in other:
            new_con=content.replace('#','\n')
            dic={"role": "assistant","content":new_con}
            contents.append(dic)
        return contents


    def change_format(self,path):
        with Image.open(path) as img:
            print(path)
            img.convert('RGB').save(path, 'JPEG')
        

    def change_format_all(self):
        for key in self.dic_cards_path:
            for file in os.listdir(f"{ORGPATH}/{self.dic_cards_path[key]}"):
                path=f"{ORGPATH}/{self.dic_cards_path[key]}/{file}/image.jpg"
                
                if file!=".DS_Store":
                    self.change_format(path)
    

    
card_creator=Card_Creater()
#print(ORGPATH)
#card_creator.initinal_card_info()
card_creator.start_create_prompt()
# for i in range(4):
#     card_creator.create_Instant()

# for i in range(40):
#     try:
#         card_creator.create_Creature()
#     except Exception as e:
#         print(e)
#         print("create unsuccessfully")

# for i in range(4):
#     try:
#         card_creator.create_Sorcery()
#     except :
#         print("create unsuccessfully")

# for i in range(4):
#     try:
#         card_creator.create_Land()
#     except :
#         print("create unsuccessfully")

content={

  "Warlock's Dark Pact|Instant": "Name: Warlock's Dark Pact\nRarity: Rare\nType: Instant\nCost: 2B\nStory Background: Warlocks make dark bargains, drawing upon forbidden powers to curse their enemies and twist their magic.\nAbility: Counter target spell. Its controller loses life equal to its mana cost.\nAppearance Description: A sinister shadow envelops the battlefield, draining life from the opponent as the spell is consumed by darkness.",
  
  "Warrior's Forced Challenge|Instant": "Name: Warrior's Forced Challenge\nRarity: Uncommon\nType: Instant\nCost: 2R\nStory Background: Warriors are always ready for a fight, even using their strength to force enemies into battle.\nAbility: Counter target creature spell. Another target creature fights a creature you control.\nAppearance Description: The warrior roars a challenge, compelling the creatures to engage in brutal combat.",
  
  "Ranger's Sniping Shot|Instant": "Name: Ranger's Sniping Shot\nRarity: Rare\nType: Instant\nCost: 1G\nStory Background: Rangers strike from a distance, disrupting enemy plans with precise and deadly aim.\nAbility: Counter target spell. If that spell is a creature spell, deal damage to its controller equal to that creature's power.\nAppearance Description: An arrow, glowing with magical energy, strikes the target spell, causing it to explode in a shower of sparks.",
  
  "Wizard's Time Warp|Instant": "Name: Wizard's Time Warp\nRarity: Mythic Rare\nType: Instant\nCost: 3U\nStory Background: Wizards manipulate time and space, bending the flow of magic to their will and disrupting enemy strategies.\nAbility: Counter target spell. Its controller skips their next draw step.\nAppearance Description: A swirling vortex of time opens, sucking the spell into its depths and leaving the opponent momentarily disoriented.",
  
  "Monk's Inner Rebound|Instant": "Name: Monk's Inner Rebound\nRarity: Uncommon\nType: Instant\nCost: 1W\nStory Background: Monks reflect harmful magic back to its source, using their inner strength and discipline.\nAbility: Counter target noncreature spell. Redirect its effects back to its caster.\nAppearance Description: The monk stands calm and focused as the incoming spell rebounds, turning its energy against its originator.",
  
  "Necromancer's Soul Seize|Instant": "Name: Necromancer's Soul Seize\nRarity: Rare\nType: Instant\nCost: 2B\nStory Background: Necromancers harness dark magic to disrupt enemy creatures, trading souls to reclaim lost power.\nAbility: Counter target creature spell. If the spell is countered this way, exile a card from your library, then return a card of the same type from your graveyard to your hand.\nAppearance Description: Dark tendrils of energy reach out, seizing the soul of the target creature as a spectral hand retrieves a forgotten relic.",
  
  "Alchemist's Chaotic Blend|Instant": "Name: Alchemist's Chaotic Blend\nRarity: Rare\nType: Instant\nCost: 3R\nStory Background: Alchemists thrive on unpredictability, mixing volatile concoctions to create powerful, chaotic effects.\nAbility: Counter target spell. Then reveal a random card from your library and cast it without paying its mana cost.\nAppearance Description: A swirling mixture of colors and energies bursts from the alchemist's vial, consuming the target spell and transforming it into something unexpected.",
  
  "Paladin's Judging Light|Instant": "Name: Paladin's Judging Light\nRarity: Uncommon\nType: Instant\nCost: 2W\nStory Background: Paladins wield holy light to judge the wicked, punishing those who dare oppose their righteous cause.\nAbility: Counter target spell. Its controller takes light damage equal to its mana cost.\nAppearance Description: A blinding beam of light descends from the heavens, striking the spell and its caster with divine judgment.",
  
  "Witch's Curse Counter|Instant": "Name: Witch's Curse Counter\nRarity: Rare\nType: Instant\nCost: 2B\nStory Background: Witches weave dark curses, turning enemy spells against their owners and afflicting them with deadly hexes.\nAbility: Counter target spell. Then, its controller gains a curse for three turns, reducing their strength and stamina by half.\nAppearance Description: A cauldron bubbles as dark smoke rises, swirling around the target spell and inflicting a withering curse on its caster.",
  
  "Mechanist's Disruption Device|Instant": "Name: Mechanist's Disruption Device\nRarity: Uncommon\nType: Instant\nCost: 3U\nStory Background: Mechanists use advanced technology to disrupt enemy magic, creating duplicates of their mechanical creations in the process.\nAbility: Counter target spell. Then, create a token that's a copy of each artifact creature you control.\nAppearance Description: A mechanical device whirs and clicks as it emits a pulse of energy, disrupting the spell and replicating the mechanist's creations.",
  
  "Summoner's Arcane Acquisition|Instant": "Name: Summoner's Arcane Acquisition\nRarity: Rare\nType: Instant\nCost: 2G\nStory Background: Summoners channel arcane energies to intercept enemy spells, transforming them into powerful elemental beings.\nAbility: Counter target spell. If the spell is countered this way, create an Elemental creature token with power and toughness equal to that spell's mana cost.\nAppearance Description: Arcane runes glow as the summoner conjures an elemental spirit, drawing power from the defeated spell."
}





#card_creator.process_data_hand_make(content)
#card_creator.change_format_all()
  