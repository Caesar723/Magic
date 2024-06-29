import requests
import time
import random
from bs4 import BeautifulSoup

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

def getIG(response):
    soup=BeautifulSoup(response.text, "html.parser")# use BeautifulSoup to analysis html page
    

    ###this code is used to find IG 
    finds=soup.findAll("script", {"type": "text/javascript"})
    
    split_list=((str(finds[1]).split(";")[0]).split(","))
    IG=split_list[7][4:-1]
    ###

    return IG


def getImageUrl(response):#str of  https://th.bing.com/th/id/{}
    text=response.text
    
    if text:
        
        soup=BeautifulSoup(text, "html.parser")# use BeautifulSoup to analysis html page
        div_tag = soup.find("div", {"id": "gir_async"})
        
        img_id=div_tag.get("fir-th")
        url=f"https://th.bing.com/th/id/{img_id}"
        return url
    else:
        return False

def send_task_to_bing_api(prompt:str)->str:#get url if image
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
    
    
    IG=getIG(response_first_get)
    
    
    while Run:
        print("loading....")
        url=f'https://www.bing.com/images/create/async/results/1-{X_EventID}?q={prompt}&IG={IG}&IID=images.as'
        
        HEADERS["Referer"]=url
        response_get_img=requests.get(url,headers=HEADERS)# check whether the img is created
        
        
        img_urls=getImageUrl(response_get_img)
        if img_urls:
            Run=False
        time.sleep(3)
    print()
    print(img_urls)


def download_image(url,path):
    response_get_img=requests.get(url,headers=HEADERS)

    if response_get_img.status_code == 200:
        # 将内容写入文件
        with open(path, 'wb') as file:
            file.write(response_get_img.content)

    
#send_task_to_bing_api("The Verdant Grove Guardian takes the form of a towering, humanoid figure composed of intertwining roots, moss, and vibrant foliage. Its eyes radiate a tranquil, verdant glow, and its presence emanates a soothing aura that revitalizes the surrounding flora and fauna. style:fantasy art")
download_image()


#https://www.bing.com/images/create?q=bird&rt=4&FORM=GENCRE
#https://www.bing.com/images/create?q=bird&rt=4&FORM=GENCRE&id=64b243c800ba4916887356003fc2e787
#https://www.bing.com/images/create/async/results/64b243c800ba4916887356003fc2e787?q=bird&IG=6E792F3064BD48B4A756CB4C3E79CBFC&IID=images.as
#https://www.bing.com/images/create/async/results/64b243c800ba4916887356003fc2e787?q=bird&IG=6E792F3064BD48B4A756CB4C3E79CBFC&IID=images.as