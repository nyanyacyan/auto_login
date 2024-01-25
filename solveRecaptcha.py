# ----------------------------------------------------------------------------------
# recaptcha回避　クラス
# 2023/1/20制作
# 仮想環境 / source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# selenium==4.1
# headlessモード
# Chromedriver==ChromeDriverManager


#---流れ--
# ２captchaからトークン取得→ トークンをtextareaに入力→ ログイン
# ----------------------------------------------------------------------------------

import sys
import os
from selenium.common.exceptions import NoSuchElementException
from infoLogger import Logger
from twocaptcha import TwoCaptcha


class SolverRecaptcha:
    def __init__(self, chrome_driver):
        self.logger = Logger().get_logger()
        self.chrome = chrome_driver

        # 2captcha APIkeyを設定
        self.api_key = os.getenv('APIKEY_2CAPTCHA', 'a02d008fb7e4bfd5aa447a9465c6d621')

    def solveRecaptcha(self, sitekey, url):
        solver = TwoCaptcha(self.api_key)

        try:
            result = solver.recaptcha(
                sitekey=sitekey,
                url=url)

        except Exception as e:
            sys.exit(e)

        else:
            return result
        

    def handle_recaptcha(self, current_url):
        try:
            self.logger.info("display:noneを削除開始")

            # display:noneを[""](空欄)に書き換え
            self.chrome.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')

            # 現在のdisplayプロパティ内の値を抽出
            style = self.chrome.execute_script('return document.getElementById("g-recaptcha-response").style.display')

            self.logger.info(style)

            if style == "":
                self.logger.info("display:noneの削除に成功しました")
            else:
                self.logger.info("display:noneの削除に失敗してます")
                return

        except NoSuchElementException as e:
            print(f"要素が見つからない: {e}")

        except Exception as e:
            self.logger.error(f"display:noneを削除中にエラーが発生しました: {e}")
            return


        # data-sitekeyを検索
        recaptcha_element = self.chrome.find_element_by_css_selector('[data-sitekey]')

        # sitekeyの値を抽出
        data_sitekey_value = recaptcha_element.get_attribute('data-sitekey')

        self.logger.info(f"data_sitekey_value: {data_sitekey_value}")
        self.logger.info(f"current_url: {current_url}")

        self.logger.info("2captcha開始")

        result = self.solveRecaptcha(
            data_sitekey_value,
            current_url
        )

        try:
            # レスポンスがあった中のトークン部分を抽出
            code = result['code']

        except Exception as e:
            self.logger.error(f"エラーが発生しました: {e}")
            return

        try:
            # トークンをtextareaに入力
            textarea = self.chrome.find_element_by_id('g-recaptcha-response')
            self.chrome.execute_script(f'arguments[0].value = "{code}";', textarea)

            # textareaの値を取得
            textarea_value = self.chrome.execute_script('return document.getElementById("g-recaptcha-response").value;')

            if code == textarea_value:
                self.logger.info("textareaにトークン入力完了")

        except Exception as e:
            self.logger.error(f"トークンの入力に失敗: {e}")
            return
