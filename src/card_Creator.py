from openai import OpenAI
import os
import json
import requests
import time
import random
from bs4 import BeautifulSoup
from gpt4_openai import GPT4OpenAI




ORGPATH=os.path.dirname(os.path.abspath(__file__))
FORWARDED_IP = (
    f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
)
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "referrer": "https://www.bing.com/images/create/",
    "origin": "https://www.bing.com",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-forwarded-for": FORWARDED_IP,
    "Cookie":"ipv6=hit=1705612170510&t=4; MUID=30712E4FEB25617305F23D02EA4860FA; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=DC7EF7CD87C5409281E1DE5281099EA6&dmnchg=1; BCP=AD=1&AL=1&SM=1; ANON=A=BFAE77929A299605DC75F6F0FFFFFFFF&E=1d28&W=1; NAP=V=1.9&E=1cce&C=fYRLjJwtv9qKzM-WfWcWatfJ0emQK_WjKm8ZjL-o8sDLrhD-8yrX6A&W=1; PPLState=1; MUIDB=30712E4FEB25617305F23D02EA4860FA; _EDGE_S=SID=222A12E74CCA65843B2E06E14DDF6416; USRLOC=HS=1&ELOC=LAT=53.46526336669922|LON=-2.243683338165283|N=Manchester%2C%20Greater%20Manchester|ELT=4|; _Rwho=u=d; MicrosoftApplicationsTelemetryDeviceId=cef2df7a-5c41-4467-b5b5-7519b6225129; dsc=order=Video; KievRPSSecAuth=FACCBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACLVTH2+LyI24QARLiqK9sLprlLN/M3XlnRnCqUKJNe+Pk32U2bFWsKNE+hlY97M+j/0sdMtvkDkIPVADf4KkSFjeHUs34jfZ4T4FHFkyP6axxtYkKjtqQbM3eV1hRQeauG0etVYJIqe256b5V5/TMEpHYEUmne6MHKLFYvdHiixrLpp6nh9rab7UbgVQLZYSIS6yMj3/hq4HIYns+slok7A4fxa+IeHYamX2ikCxY3Mg2PnVeZHmVE8w+8dpS+JMslYswOcUXJr266WBNQpIl7uD89R96zU352AszktasYBK7AuIMEDcfnI5are3PpSPaPtLugifYFQafhdCPgwEMqx2VcQn+AeBmw3ziwXBzUX2FnJuobv4nBuriV2xUFF5kmc3MxSj5p8tfFGdTsTmn3ozYYHJ/k9KrLCzcEEiMt4i717t8N8S4GVRh5fHd9iEUYU+eZH0aoG5+7KZqZJtugTFtOSE0+Nw536PGKlD4KnbkRMScsxD5+jHz7fCz1DKtvz2S0NADV0EIHV5opRhf6BkpZmH47KCjFec9Kx2SXTjf6dpLs45nWA41uObmOcoHduJJAdCyzNfKxb09sBbNAxOTT1T21VpiU7yNA1DskLnSvGiTJWtWC9oPFo1nho54kObBmTS/vDsUsv2Iir8n/xrSWcEgaec9m+MkSV8lTKlm74hSnF5K9szvj8BbWIWKnURre1obvuco2qjdMf6OW7dkvq4spbFbOGVNQoM7GMHZ4pJ1pAbsUxnSzTQFWzJSNa2r1QK8WqytbILr4N5jbkQ6AhpSogrmRjGOBh00+BYI1d9Ucne2Lw1E18pVS5DjRRyxGgR++PjePMZckbmXIeXrPZ16Wf/mpJoi2+NFc4n6me+qIxDy8eVyuwpMpG+z3Hnn0ydPBa5E2BRn+yyDuI/e/wpEbGH90pAYaYrVQlsEo+U4iBlK5recR+fR5ASIrmr1UEpquKWLIqUVgi0Z0Z1C3r0lQuAMqlklm+MTOaldmQUjo8u+uNl1CAVKxZ8AIrdTg4tHo8uYoACRfKi2NSPbzHfV2vXpEBscN/bWgfDDV5HSBgjmGKM8uG93XPEm60+y+7dOMEoZbmv1Yid6zb2X9jm4cM5DIn/yyVtmhRmNRw9E31AGqHAf4RQHenpmdpmKedopXDQZH6fQXVY2q1bwWLADZTz2Dio/9itsaHiwnMkqF8vpo6U53F7y2wT1yM17ozYer7yY/CT8HOABx8WJfrj82eewACjmSjorDW1h/dth4SERgJg8pAvg/xzGg6JqkDXycpzyAZr495KASwTq/MuBNlUyu7Wn5G2nt+Yf+Vt0sQdkXZQztaYzZ9Dl9A6gEHi0qdsDDl/6tnnEO6nDuFTVpZJe+sQJt0uCGzF6zOVDbCBewcMDuHc6cr3qa30fAFHUxyF0ZcB1M+ZzOmz3MfeeS9XwF0SRamdQuDkZ009Emek97SZvhQAGvv4GgA/paUSCL7j4h5MWXSjmrE=; _U=1wU10riyTES2yXyEMtmIEan3JiUQ2QsfqWoJF_weoCnfoqrZdk6ItXiUx76Yep33ZU0iynt5FuSYwHYiXKFExJPxPmV6XkmsRX3PCinwl5DJKRMTxSFcXfE9VoZ6cBK3aZP0JhR0w1aAFrk9gkYYeCKZZVv00fS3C-QHFj7PTcev2IhCNb1fvv3eubmePcySrba4OWCCM-wtU5Fn0EWF7V2iky9C619eT8BECWLPmJf8; WLS=C=f4df761f959178e8&N=xuanpei; MSFPC=GUID=a7fbd005d88248d18d33af863f499f8d&HASH=a7fb&LV=202307&V=4&LU=1689251038722; WLID=m5VufYHWWuFYRkqaE6hO6U5xjDL4VrvzXxzE8Jf+5uXXB2/FyrJ7mwBXmLJmQ8QEwK3128lsHwE2fGNsgtqpv8Y6sSlVzH8VLizIeHzA78M=; _clck=1843f5z%7C2%7Cfii%7C0%7C1478; _UR=cdxcls=0&QS=0&TQS=0; ipv6=hit=1705598918799&t=4; SRCHHPGUSR=SRCHLANG=en&PV=14.0.0&HV=1705595319&BRW=W&BRH=M&CW=1384&CH=745&SCW=1384&SCH=745&DPR=2.0&UTC=0&DM=0&PRVCW=1470&PRVCH=746&CIBV=1.1467.6&WTS=63840839946; _HPVN=CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNC0wMS0xOFQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjozLCJUb2JuIjowfQ==; SRCHUSR=DOB=20230713&T=1705608569000&TPC=1705595270000&POEX=W; GI_FRE_COOKIE=gi_prompt=5&gi_sc=9&gi_fre=2; _RwBf=mta=0&rc=84&rb=84&gb=0&rg=0&pc=81&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=18&l=2024-01-18T08:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=0001-01-01T16:00:00.0000000-08:00&o=0&p=DALLE&c=ML25P7&t=963&s=2023-07-14T11:58:15.9749894+00:00&ts=2024-01-18T20:44:33.8572854+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=0&lka=0&lkt=0&aad=0&TH=&dci=3&e=mEm-hVfJ2PEIWykBiHpIL0l34qQ1QnG0LVls9__qSz5dEo5U6QTs4Tu6PpQKJJdAx93nPaUnI50hNOe7AB9ZTSa_gJEF9mp-Cd-RdTKdusw&A=; _SS=SID=222A12E74CCA65843B2E06E14DDF6416&R=84&RB=84&GB=0&RG=0&RP=81; _clsk=ppnou2%7C1705610674068%7C17%7C0%7Ct.clarity.ms%2Fcollect"
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


        self.COOKIE='eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..HhzT7kRJqjUSmB0H.upVv8NTPKUygtYdDxyO9xtZP5HpYiLT8eKqsEfrnbOit-oMBfpvOpsJU8P3MCUb-9T31kxhOFn3U8LJg2c-MUuroGI3GqmpV9Z7LSJI9JaYcoc3D26RdLGtZiq3rcdWd_8gFMXanXjCMUFm92V1GO0HZ8IZdhuZ6eutSwsLDLrkOheFcqA0IWuhCJJn7yZ-8vz4fhjERtBJV8kiEq3LCzJINTiecSSRDMHUx-kazymJteIS5Thye0H0qZTRQuc9arB3nJgmS-J9NpiDSsI-bvIWNKw1DYIbma9Qs7Jvte67X0MYuSti9iYZ0WxW76u3ejQ3iK7f4O1bOx3KxsbB3YKJc4dc_iYNGiO8Mky6dWY5QltWTN0SVudGFIbhlB4MyaShd-v8FPUNyNF5zpmkgEW9rz6Xmzvw-VwQVbAncdimCDEzULDPKFoYpFDgmTh-hd5c5gnMrSN4c8I-crOBHZWYnqFLfaPXJ9QQ0hKjWwxWEpBzPs9PwgbufJpAB_OoEdAGmUlJeFVu8P-dONkhyWmguzmQaqb0tmIZtNE_xsyy-IwokyAIl3kqeKy8cM6l1-EFPSOv2eA8YMtBYusLIMj7PFDWl3_jMGY5CE1Idvj9cM3ereYGNp0NfCQbpeUx6ABsU075aFcpiw8SoTX_dIANu92Y6knuGMqL8dYj9yjlSajbpYj6W9kWm-VKf6t4AE6oQjnwUdyoaw2w3v_c_LtvCOzBPmh2gINIq-DJBbBPfaqKvBtBdwiYeTsYrUZwlwYPTYRQ9pNb9pv4Mwsum7XMFytdOJ5EvNAb4colDUn-w_at116hUpbrMY9eBCd67Eez2Yv22OmgJdWs7Kv8mdmChJhyDMyCAsOKgSxUcl_RhoqvjEK2oyP98qUbzSZwUYABLF8hkmYRkGTB8TaWhoKehIw68JP5OZsMocAx5Pn8OEV1KvyWpVNBtc3FvM4WluqS-Ob_3D74_a3PiaEXlCaG3pIKg4W0nUuSUp1t3jSXIVB720kniBmGw3FSnjhQpP06L8O1kL07rBc076rh1M2wizcwoC27AzK0naHvkoM8_O1pt2hQs0urHaxG-EcFAiVZ2gB72qVQtwvlfgQw0oeNWx3-OUU29bXTOky_Hg_s2pXbCIyXTRBHNYYIQ2wwwG7BBu4jE7IkBYWNgvGuJJvMJCzCVAmvD8tZD1XCNyP4MKFs_HSTdX3TOqGoLfv2IuKTJLjtZTxGko1C2kvXq2fYviscu5LlYlCl6Pq5EAh6gtEYhj64RIhemN8mnGNbmCjLOymDmxg6pZ8DrPmrVF1D5eNJfkieehHVyupuGjqCPOQ7zoZ92WshHHOYLwQZNQ7CImTsj82yQab_w48eBJfWjAZUi2bXHtfwwfDf4TwWIAuRflqOu14c9YcudlzjDvnQhLD_JIK1qDMZtB5nESvKB30t8rKJ8TDtI_cmWdpSp0TDWSIhfsJGlUEaiv1q7xnstIfROsrt9jM9UquvNVP0QU7XIJ8E33pVnWpl9UyiYHn21MNneCXJh1gZxMFI5oE6P7aWYitGt2Xs-01pntQ9A5EEbDYNaLfsYyEJNJY7-l3KRkRqnLOxJXrAemwKq4zm-r8aBe5objqTilKYI5oKbXx4VZQpZFKcbi7vK6CTN78v_y1HhNck4OS2mYf7FoaYZV1BkqU9RvYvsi7kiNzGbBclab_4lQ6GQ9Hu0TWSdKFTto5KLrMAo5Y8NVwmjmfDQJpiV9InYrNWZPfaozhe-2kwMB1GvTnZ4acn1FS0TPyj_MGqJCsSUnUdp9zzt-W2MmVIEhINVlRzCCvakrLnLHyh-QKZrksUC1GTfH2ihiKgiwBoxxXevylqkW1xzYughEpJL97W2uD4Ddg3aP_4RBUH5mVzsFxH8XfT9s98RR6sq997pdqiru8B9gd58fkSpv-JSbE4heQESKnw_pbKDCs-QY7SJLs5rm5umSwoDPJFJiqZYQVua4YE1SxKB2WxI2pvYUszPYVSa0-Vb2Oj0QsYwH9fChZItu0jINH0cJESawKfy3PGADKKtpyI3rq76QKZp1GgV8x_YGodT-KY3kgsmZ4NMtkeqxkD7Bd-Z7iQN6csZT1TKm5tOKDDuZnJ5zpFWOaZDdKNqWXKKST9ImYwQV1s_Ec1SstAwfzjyEtlDZ-lhL8r0JLFn1FJFdtdsuu4rOY1imxtu4WUR8_QTqDNUB-nCZCRzORZJCm8cpX85aMeTyM_w05LpSO8Yq4upOR1jvrefIM6jhJPAD9hMtSzHm7UyaNhXgon_18Vaw_2eT6Z-k7m4WQdJ7tbDnvQtX5KbWbwD0aNCEAdWzMT4zLpVxlLIBwjxWxnovzYHmL5GapMc57dl4HrgcM6y8MtX6vJcMm-rIymanyRQJxvDit_kS49qynpkjxqR6hgXBd1Ev39zT98Cxoei3qE1Z8U2RslSOti4KBhaZy4ZygUYek7MEOC_ngd6McXm21YY9LTWaU2PrQuoPdjrcz_2f-EU8Yx12I8NLfnDj0VzfkZFOsebrmEe6isDg-9iArMLczwRONNTdWEUhllcnEKO-XHBY7R8cskno7ar_BsU5t_nk1KeaEbSsQviAhHfnKbwRbrCCJjOgIMuxiLa4fNkpGs8EgWefyPz2v4cLWQ79CI6nt5hu3ZUouUanC6wWMzIat8GebH4Qw6xE7NGFsiFojuXheKXALLolHKTWfijt7PQcF0h6uo6-jR1X4bQVpQOb-RCk_T9VpxyymUqQ5NVL4cF_SadDnNVCNGoJXKBBWky80AM_ovpKX0aPi4dUy1ONtXvREFTDRVGRnOJN2jJXpIc4fGdWTs6k8esAwNFIJHM5tltMFivlzsNreprK7Q5qqNxw3dMZ9F-dcmc10ImJkiLYvzrS4f7ayfbpP9O_Woilaokk_ZGVrYo7ac1eyUoyxBIl-Cfqewo7GAsB1Q9pVdEoDQ13tXO1dtyw9bk07KWtRXm_kVpbN4F.Uqt1r_0SF8tYEJMUwnUhxQ'
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
                                print(contents)
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

        print(response.choices[0].message.content)
        
        successful_flag=self.process_data_gpt(type,response.choices[0].message.content)
        if successful_flag:
            self.save_info_v2(type,response.choices[0].message.content,path)
    def save_info_v2(self,type,content:str,path):
        self.dic_each_arr[type].append({"role": "assistant", "content": content})
        content=content.replace("\n","#")
        with open(path,"a") as file:
            file.write(f"\n{content}")

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


      

  