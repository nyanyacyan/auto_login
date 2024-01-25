# ----------------------------------------------------------------------------------
# 自動ログインクラス
# 2023/1/20制作
# source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# selenium==4.1
# headlessモード
# Chromedriver==ChromeDriverManager


#---流れ--
# ID入力=> パス入力=> クリック
# ----------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from infoLogger import Logger
from solveRecaptcha import solveRecaptcha


class AutoLogin:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())

        self.chrome = webdriver.Chrome(service=service, options=chrome_options)

        self.logger = Logger().get_logger()



    
    def login(self, login_url, userid, password, userid_xpath, password_xpath, login_button_xpath, cart_element_xpath):
        self.chrome.get(login_url)

        current_url = self.chrome.current_url

        self.logger.info(current_url)

        self.chrome.save_screenshot("screenshot_before.png")  # ログイン前のスクショ

        try:
            # userid_xpathが出てくるまで待機
            WebDriverWait(self.chrome, 10).until(EC.presence_of_element_located((By.XPATH, userid_xpath)))
            self.logger.info("入力開始")
        
        except TimeoutException as e:
            print(f"タイムアウトエラー:{e}")


        try:
            userid_field = self.chrome.find_element_by_xpath(userid_xpath)
            userid_field.send_keys(userid)
            # self.logger.info("ID入力完了")

            password_field = self.chrome.find_element_by_xpath(password_xpath)
            password_field.send_keys(password)
            # self.logger.info("パスワード入力完了")


        except NoSuchElementException as e:
            print(f"要素が見つからない: {e}")

        # ページが完全に読み込まれるまで待機
        WebDriverWait(self.chrome, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        self.logger.info("ページは完全に表示されてる")


        try:
            self.logger.info("display:noneを削除開始")

            self.chrome.execute_script('var element=document.getElementById("g-recaptcha-response"); element.style.display="";')

            style = self.chrome.execute_script('return document.getElementById("g-recaptcha-response").style.display')

            self.logger.info(style)


        except NoSuchElementException as e:
            print(f"要素が見つからない: {e}")

        except Exception as e:
            self.logger.error(f"display:noneを削除中にエラーが発生しました: {e}")

        try:
            recaptcha_element = self.chrome.find_element_by_css_selector('[data-sitekey]')

            self.logger.info("reCAPTCHAが検出されました")
            data_sitekey_value = recaptcha_element.get_attribute('data-sitekey')

            self.logger.info(f"data_sitekey_value: {data_sitekey_value}")
            self.logger.info(f"current_url: {current_url}")

            self.logger.info("2captcha開始")

            result = solveRecaptcha(
                data_sitekey_value,
                current_url
            )

            try:
                code = result['code']

            except Exception as e:
                self.logger.error(f"エラーが発生しました: {e}")

            try:
                # 解除コードを所定のtextareaに入力
                textarea = self.chrome.find_element_by_id('g-recaptcha-response')
                self.chrome.execute_script(f'arguments[0].value = "{code}";', textarea)

                # テキストエリアの値を取得
                textarea_value = self.chrome.execute_script('return document.getElementById("g-recaptcha-response").value;')

                # 値を出力
                self.logger.info(F"テキストエリアの値:{textarea_value}")

            except Exception as e:
                self.logger.error(f"WebDriverWait中にエラーが発生しました: {e}")


            self.logger.info("クリック開始")

            # ログインボタン要素を見つける
            login_button = self.chrome.find_element_by_id("recaptcha-submit")


            # ボタンが無効化されているか確認し、無効化されていれば有効にする
            self.chrome.execute_script("document.getElementById('recaptcha-submit').disabled = false;")

            # ボタンをクリックする
            login_button.click()


        except NoSuchElementException:
            self.logger.info("reCAPTCHA、なし")

            login_button = self.chrome.find_element_by_xpath(login_button_xpath)
            self.chrome.execute_script("arguments[0].click();", login_button)
            self.logger.info("クリック完了")


        # ページ読み込み待機
        try:
            # ログインした後のページ読み込みの完了確認
            WebDriverWait(self.chrome, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            self.logger.info("ログインページ読み込み完了")
            self.chrome.save_screenshot("screenshot_after.png")  # ログイン後のスクショ

        except TimeoutException as e:
            print(f"タイムアウトエラー:{e}")

        # ログイン完了確認
        try:
            self.chrome.find_element_by_xpath(cart_element_xpath)
            self.logger.info("ログイン完了")

        except NoSuchElementException:
            self.logger.info(f"カートの確認が取れませんでした")