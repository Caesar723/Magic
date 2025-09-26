
from gpt4_openai import GPT4OpenAI
from openai import OpenAI
from PIL import Image
import random
import os


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

prompt="""

You are a Hearthstone designer tasked with creating brand-new Treasures. Each Treasure must have a unique and creative special ability, never repeating (e.g., “Double your Health this game,” or “Whenever you play a card, draw a card”).

Please generate each Treasure in the following format:

Name:[Treasure’s Name]\nContent:[A one-sentence summary of the Treasure’s main function]\nBackground:[A short fantasy-style backstory of the Treasure]\nAppearance Description:[A vivid and detailed description of the Treasure’s physical appearance, including colors, magical effects, and materials]\n


Requirements:

Each line must saparate by only one "\n"

Every Treasure must be unique and not repeated.

Abilities should be creative, powerful, or whimsical, fitting the fantasy and humorous style of Hearthstone.

Appearance descriptions must be detailed and imaginative.

Keep the style consistent with Hearthstone’s magical, quirky flavor.
"""


class Treasure_Creator:
    def __init__(self):
        self.COOKIE='eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..dxqXb-v0lmFCYhi9.IfJc3sgH9EZiXKE4iuiZ8crlvg2ntN6Kp7KRxTXmR3t4Ldxquu0MqaqoAfc-2helc7n_O9ATnoBEb_MxEurx8geLm2RxXR2F6vq7zIxFGMhiQF-B8boGM1UrJfqLSi_SgDctzVvLnpChiLHqJYTv6heW0MVikcBFO95-on7JZfxz00i-ocuNKhUwA2GiE3sek3qM6P0FqTno_lcW3zYbkWrwKVTfVI4NSfss9IlG-bsHQpyr7mhobPkMkr5KEbUaeg32SwULshQ2_mTeyY6iJkU8BVp4QT6cstSrDYEWVtJJAopPNX6mS2ncBWP3FPVcKP7dyyv4Bim6zI2kotPrcOZfixUaelJBnUVx9lUFnKzWTGNvAkaqBuo3skjkBlaveje0ZrKLEWwHSa-tg3b1HqrEQxkZ8fYbkanKsdpjK64Xs7XZf9EFBnkBKABeDqq_2rVyF55JFOk89kL35cRtDyXriV3Ypj7T8Jiyd0hGWJu4_NXM7L0RsQZvl71q8cg59Tptq_4mJQgXHQGwiFUVDZmMtK5QaKLN1-CiTsDO7J0-ct_C-1StqiN3WevocJDVn1cgPeUsoUdIaHVaEvkkQ-W7pySK6dkzI2_o8Afygs6UcY4y3FbOLjPVvUxbVVWDsc_03kJnh2K0M8Ca3rm0yagXBlZ7Q__LREoCusnNpQfFAY_M1Ug1HvnIN0YDQaCPfpZ_Aj0zPl4kdQv8ryh1PxO7gXwuAJkE5-L9oC0EeJS5iOyqy3UklY-lu3lwm7Cbr_ywDd948paZ7eRgdmZLFHGxhyVgTJXvKzyb8ByqbEpu5-WBTdgo84zih9mH2R9dRDIhnu2xNbKQERsploAAzavhQH_XAPwMPjLce1pEWH0uQ9knygNLRsgGOqbzI_CYm59BEAO1gIw-046DBp98j4VbSOhLYjqAHklbhFUnhkubk8NqEN6zhMkXGJywON5c8VokQyaEUaZxfu7CxKhrG0DEKhiZrjYpqE7JnsqZ2f5yGTjwwF8UML0CqonFDi76wRWHYyJvH1bPUNUu1fh1B_NOUZpEIs9hwjbtWDBmk6wU4mbViLv4e3a4MJb6fbUx13pORTRbc9yrlhdqpavRvi_gbQ2OjyeM87RMO8CxjzOZY_NYFIUPwq5bW1U6I79J20BsEVodYiCmdfSCI8vKxnzsvj2KT-HT5pZMUgPljDEfvOowVpeTqJSqlnq6DYym5GO8M-IhcAex59uSCfDjRqrMp_sqq5ryiXtPI-aQnYxfBZoCyA73Rz5Zd5mOOCO5bou3LPBhRYYCsbo0QdYvFmyY5Dde7bjGhCbyaU3NlrhBk4X5PVWU9Ew1H3ribcJ2MUT3D9i1Sqtk6Abv8alLj78IMuyPUUAiZw82-Z7se0LktoL8ZQb2zCCl2fervLx4IMJ-FW4WuOLBgq7VO_HR-0fL2As1bzVKl1B30DBV2uPYKRK4NVUbkFAV6p6RamVfiTDYzSVOG5J9SPJ8CqXzjY6EOnf5yjPJGG8HbMfVbtUUvDg7Ito9DD_u3rNeXyUb5SiQs8G5pNfOs1x-nsEOH3YUHEWdDAXcQplCZxpMUoN2WarthW_oL_58XEyHAHhW3VPH3DmkMa5ir76WZ2W9z-BRUEVKKCMf8KCzWJtcsylNBXPTo0PdE3M5NpG8hxslgwMMuNMPU5IGt0nNeECWHW4wR9yOvzC8iCHKjG8ly84VALcun6BCn4YGo1iMiYLP3FWRXf-y8tQzCkfgfHdzwRarNsh_A7kqsGrv98VpMs0xohzmNLXvQVAlIPl9gC0pSURR3E4Ef21Krw0qAAD2UUFrgnsqQdvrrisxzONcilgfLMpJ6shJMLAiSI6qpH_wG6VMKeqMaXhj54JMw0j2qRHEBPIh73fCYN23RcDBwMw9YoNmZ4J7g865CTuVNPxkWfFl01KF35sOm7aTDrMRNUCipHthMi5eITigdXE5AhEpBwz1c0Q0yO9bboNku9XOlbofE_fG26I5rDWmWipbgtOLmPJJI4sa71pKEXpvJ_vYLv6Gny3fJ3c5EtYYsUKNoH6X6sGvhMF35g9vMCQQTtzNiLnlArqfW0EabpW7D8BfF3cAQczXbsWfDwDByrDeqxcdEgWztSMnyRgb23yTF_EpgO3-vPbKLYtYuJLYl4GLbkp8bzAV48QO2cYvGg_2xv-tYnp2bmeirJxUOaqulp3_cwSkfaGsBc_0TJnuTPH09aiTFz-t5DWUIcCrylCdfugzvRUE5qBPv6WiP8guxS4wrZR_Whd9C4EhscdyCXOn0rTtr2qaXitnaX7E0b-clJdqW5JyXnptOn3tP_y6BgO__amqLmeB8jI2ylfBspPDLNCfU573Z2GCSwcnxWLhhQDhoGSdnKVMq5xk24RrdXMEo7qp9h1iCGhz3tG_YDX-Un2VkWy7NlUcAhlKK0Akr5kP9mAq2hxv6FDA53GmdJFW6t29Z_ARzQKGHuKz0Thtk0YCORmEwqw8W5ydjSEQY__dM8HOoZNb07xR0a4C-bumhYyQoLggF9nOE7HiIwdKQ_9U0fEyxDPzE79uoR8BJvvOxguH9Hlz8fVhTFWU4d1R22pgF7MI0ecD85KW33YGwDsbExbYkuQN21K7njroXhqYV6A-r2mHA8PgZkqNug4C4y-6hKerkPXL26rc67Q9hgd91kHxS5C0Um1Axu9gz5J5CPJCitEGVL6Irl340GEdTZ5MNZ19WZgHfzLKw8QnnBPdCmOk2rdc8-g6eU9-FJUhDuxaUFxzys1LxyoT3GvpiFroDMyPkltX8dBz1VHGehA4xa5XxWW2JRVn0AQJYaME-tQUhYsNmdduCLdVogiMDtN3Y4jsL32S6wpAPNH4S-ucJc7WHa2uI1i9zhhWzoXeNf5Td3ZSm3PsnVIddTr2mnKTUH2OEnURyZYqdPvVpxzbmAgQlGbNCFFoi_qFwHnfg7pAmpyfgmZOjeScIHWg0sOSdp9tmIWTMRkhQgWsvHU4z5krBtC_XH2EbZi7uR1_sjR-Njyp_02J95rWA2j_1rbHptNKceuIZ9k915o-XXg1FQ_P4FDkPx5TNyPSmBTatWinyeWAhPaU15RjD2EXxoU-MRznwJHhd6YZlnIdcSMlhd1LaolR3GzDLZyjGWzTevmAzHtRRS4-U4YBcwOPbJ3EpLpU4NXgZBNgZUCWr1qZvr9flYt7A_uPbeUaot-NZVBa-uV9L2T54xjZvtZnNuJxDreJn3u1b1K2L4J6qeh1CxI9OtmfoFQxwM7wN6JcQz7ATobdcFKRVmNkgs9hIHGmcEMFWsBfCOTvogscsbeyVcuDNcZUnU_WykXPtMrxu9zME5q2XH0VNLqUpeO56tk010ViT8FAJ06b7s8i7nSUCFOX6vnS0AW3BH4YCw5_y1fHbmOE_z4uXYtX3AnIAfSCYqtxtYcEoSCbU9MxQOUPx3VTpol1Ji7LIl1QGhM9j-KibuGQlkxQJ6rMTaW4oOChjTCPSI3NJr8jmPilcjTU.ueBdoy79_hpow4Ehg2C_Rw'
        self.client = OpenAI(api_key="sk-ao0HCUufUuNrfPzF76B4556483534dE2933fE8C4E46485Dc",base_url="https://free.v36.cm/v1")
        self.llm = GPT4OpenAI(token=self.COOKIE, headless=False,
                        model='gpt-5' # DALL-E 3 only works with gpt-4
                        )
        self.messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Please generate a new Treasure."},
            {"role": "assistant", "content": "Name: Endless Grimoire\nContent: Whenever you cast a sorcery or instant, draw a card.\nBackground: A spellbook that never runs out.\nAppearance Description: A vivid and detailed description of the Treasure’s physical appearance, including colors, magical effects, and materials"},
            {"role": "user", "content": "Please generate a new Treasure."},
        ]
    def create_treasure_message(self):
        
        response=self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.8
        )

        message=response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": message})
        self.messages.append({"role": "user", "content": "Please generate a new Treasure."})
        self.process_message(message)

    def process_message(self,response:str):
        try:
            p1=[string.split(":")[1].strip() for string in response.split("\n")]
            diction={
                "name":p1[0],
                "content":p1[1],
                "background":p1[2],
                "appearance description":p1[3]
            }
            try:
                image_byte=self.get_treasure_image(diction["appearance description"])
                self.initinal_file_folder(diction,image_byte)
            except Exception as e:
                print(e)
            

        except Exception as e:
            print(e)

    def initinal_file_folder(self,diction,image_byte):
        folder_name=diction["name"].replace(" ","_")
        image_path=f"{ORGPATH}/treasures/{folder_name}"
        py_path=f"{ORGPATH}/pytreasures/{folder_name}"
        os.makedirs(image_path)
        with open(f"{image_path}/image.png","wb") as fimg:
            fimg.write(image_byte)
        os.makedirs(py_path)
        with open(f"{py_path}/model.py","w") as fpy:
            fpy.write(self.creature_treature_frame(diction))

    def creature_treature_frame(self,diction):
        name=diction["name"]
        class_name=name.replace(" ","_")
        content=diction["content"]
        price=0
        background=diction["background"]
        image_path=f"treasures/{class_name}/image.png"
        
        treature_frame=f"""
from typing import TYPE_CHECKING
import types
if TYPE_CHECKING:
    from game.player import Player

from game.treasure import Treasure



class {class_name}(Treasure):
    name="{name}"
    content="{content}"
    price={price}
    background="{background}"
    image_path="{image_path}"

    def change_function(self,player:"Player"):
        pass
"""
        return treature_frame


    def get_treasure_image(self,appearance_description):
        prompt=f"Generate an image of {appearance_description} style:fantasy art, transparent background and png format, 1:1 image aspect"
        img_bytes = self.llm.generate_image(prompt)
        # with open("test.png","wb") as f:
        #     f.write(img_bytes)
        return img_bytes

if __name__ == "__main__":
    treasure_creator = Treasure_Creator()
    for i in range(10):
        treasure_creator.create_treasure_message()
    #treasure_creator.get_treasure_image("The Whispers of the Ancients Treasure appears as a collection of small, shimmering stones in various shades of ancient gold, deep emerald, and sapphire blue, each exuding a faint ethereal glow. As the stones hover in the air, faint whispers in an ancient language can be heard emanating from them.")