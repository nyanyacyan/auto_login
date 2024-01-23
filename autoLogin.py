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
from twocaptcha import TwoCaptcha
from infoLogger import Logger


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

        solver = TwoCaptcha("a02d008fb7e4bfd5aa447a9465c6d621")

        self.chrome.save_screenshot("screenshot_before.png")  # ログイン後のスクショ

        try:
            # userid_xpathが出てくるまで待機
            WebDriverWait(self.chrome, 10).until(EC.presence_of_element_located((By.XPATH, userid_xpath)))
            self.logger.info("入力開始")
        
        except TimeoutException as e:
            print(f"タイムアウトエラー:{e}")


        try:
            userid_field = self.chrome.find_element_by_xpath(userid_xpath)
            userid_field.send_keys(userid)
            self.logger.info("ID入力完了")

            password_field = self.chrome.find_element_by_xpath(password_xpath)
            password_field.send_keys(password)
            self.logger.info("パスワード入力完了")


        except NoSuchElementException as e:
            print(f"要素が見つからない: {e}")

        try:
            recaptcha_element = self.chrome.find_elements_by_css_selector("[data-sitekey]")
            if len(elements) > 0:
                print("要素が存在します。")
            else:
                print("要素が存在しません。")
                self.logger.info("reCAPTCHAが検出されました")
                data_sitekey = recaptcha_element.get_attribute("data-sitekey")

                # 2Captchaで解除コードを取得
                response = solver.recaptcha(sitekey=data_sitekey, url=current_url)
                code = response['code']

                # 解除コードを所定のtextareaに入力
                textarea = self.chrome.find_element_by_id('g-recaptcha-response')
                self.chrome.execute_script(f'arguments[0].value = "{code}";', textarea)
        except:
            self.logger.info("reCAPTCHA、なし")

            login_button = self.chrome.find_element_by_xpath(login_button_xpath)
            login_button.click()
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