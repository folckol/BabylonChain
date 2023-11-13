import base64
import datetime
import pickle
import random
import ssl
import string
import time
import traceback

import capmonster_python
import cloudscraper
import requests
import warnings

import ua_generator
from capmonster_python import RecaptchaV2Task, RecaptchaV3Task

from utils.logger import logger

warnings.filterwarnings("ignore", category=DeprecationWarning)



class BabylonChainModel:

    def __init__(self, email, proxy, capmonster, refCode = None):

        self.email = email
        self.refCode = refCode
        self.capmonster = capmonster

        self.ua = self.generate_user_agent

        self.email = email
        self.session = self._make_scraper
        self.proxy = proxy
        self.session.proxies = {"http": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}",
                                "https": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"}
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.session.headers.update({"user-agent": self.ua,
                                     "Accept": "application/json, text/plain, */*",
                                     "Accept-Encoding": "gzip, deflate, br",
                                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                                    "Content-Type": "application/json",
                                    "Origin": "https://waitlist.babylonchain.io",
                                    "Referer": "https://waitlist.babylonchain.io/",
                                    "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                                    "Sec-Ch-Ua-Mobile": "?0",
                                    "Sec-Ch-Ua-Platform":'"Windows"',
                                    "Sec-Fetch-Dest":"empty",
                                    "Sec-Fetch-Mode":"cors",
                                    "Sec-Fetch-Site": "same-site"})

    def Registration(self):

        payload = {"email":self.email,
                   "referee_code": self.refCode,
                   "token": self.SolvedCaptchaToken}

        print(payload)
        with self.session.post("https://waitlist-backend.testnet.babylonchain.io/v1/waitlist-user", json=payload) as response:
            print(response.text)
            return response.json()['referral_code']

    @property
    def SolvedCaptchaToken(self) -> str:

        capmonster = RecaptchaV2Task(self.capmonster)
        task_id = capmonster.create_task("https://waitlist.babylonchain.io/", "6LdLBhkoAAAAAGk3DTcYC78IXN1S8ZaHs2IsB4f0")
        result = capmonster.join_task_result(task_id)

        return result.get("gRecaptchaResponse")

    @property
    def generate_user_agent(self) -> str:
        return ua_generator.generate(platform="windows").text

    @property
    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )



if __name__ == '__main__':

    print(' ___________________________________________________________________\n'
          '|                       Rescue Alpha Soft                           |\n'
          '|                   Telegram - @rescue_alpha                        |\n'
          '|                   Discord - discord.gg/438gwCx5hw                 |\n'
          '|___________________________________________________________________|\n\n\n')

    proxies = []
    emails = []

    refCount = ''
    capmonsterKey = ''
    refCode = None
    delayAccs = (10, 30)


    try:
        with open('config', 'r', encoding='utf-8') as file:
            for i in file:
                if 'capmonsterKey=' in i.rstrip():
                    capmonsterKey = str(i.rstrip().split('capmonsterKey=')[-1].split('-')[0])
                if 'refCount=' in i.rstrip():
                    refCount = (int(i.rstrip().split('refCount=')[-1].split('-')[0]), int(i.rstrip().split('refCount=')[-1].split('-')[1]))
                if 'refCode=' in i.rstrip():
                    refCode = str(i.rstrip().split('refCode=')[-1].split('-')[0])
                if 'delayAccs=' in i.rstrip():
                    delayAccs = (int(i.rstrip().split('delayAccs=')[-1].split('-')[0]),
                                int(i.rstrip().split('delayAccs=')[-1].split('-')[1]))

    except:
        # traceback.print_exc()
        print('Вы неправильно настроили конфигуратор, повторите попытку')
        input()
        exit(0)


    with open('InputData/Emails.txt', 'r') as file:
        for i in file:
            emails.append(i.rstrip().split(':')[0])
    with open('InputData/Proxies.txt', 'r') as file:
        for i in file:
            proxies.append(i.rstrip())

    mainRefCode = refCode
    if mainRefCode == '':
        mainRefCode = None

    localRefCode = None
    startRefCount = 0
    randomRefCount = None

    count = 0
    while count < len(emails):

        try:

            if localRefCode == None:
                randomRefCount = random.randint(refCount[0], refCount[1])
                startRefCount = 0

            result = BabylonChainModel(email = emails[count],
                                        proxy = proxies[count],
                                        capmonster = capmonsterKey,
                                        refCode = localRefCode if localRefCode != None else mainRefCode if mainRefCode != None else "").Registration()

            if localRefCode == None:
                localRefCode = result
                logger.success(f'{count} | Зарегистрирован рефовод. Код - {localRefCode}')
            else:

                startRefCount += 1
                logger.success(f'{count} | Реферал {startRefCount}/{randomRefCount} зарегистрирован')

            if startRefCount == randomRefCount:
                localRefCode = None

        except Exception as e:

            traceback.print_exc()
            logger.error(f'{count} | Ошибка - {str(e)}')

        time.sleep(random.randint(delayAccs[0], delayAccs[1]))
        logger.debug('')

        count += 1

    input('Скрипт завершил работу...')


