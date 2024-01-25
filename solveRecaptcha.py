import sys
import os
from twocaptcha import TwoCaptcha

def solveRecaptcha(sitekey, url):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    # 2captcha APIkeyを設定
    api_key = os.getenv('APIKEY_2CAPTCHA', 'a02d008fb7e4bfd5aa447a9465c6d621')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url)

    except Exception as e:
        sys.exit(e)

    else:
        return result