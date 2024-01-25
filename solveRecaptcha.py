import sys
import os
from twocaptcha import TwoCaptcha
from infoLogger import Logger

def solveRecaptcha(sitekey, url):
    logger = Logger().get_logger()

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    

    api_key = os.getenv('APIKEY_2CAPTCHA', 'a02d008fb7e4bfd5aa447a9465c6d621')

    solver = TwoCaptcha(api_key)

    try:
        logger.info('関数処理スタート')
        result = solver.recaptcha(
            sitekey=sitekey,
            url=url)
        logger.info('関数処理完了')

    except Exception as e:
        sys.exit(e)

    else:
        return result