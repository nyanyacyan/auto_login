# coding: utf-8
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

# モジュール
from debugLogger import Logger
from solveRecaptcha import SolverRecaptcha
from lineNotify import LineNotify
from chatworkNotify import ChatworkNotify


class AutoLogin:
    def __init__(self, debug_mode=True):
        # Loggerクラスを初期化
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1680,780")

        service = Service(ChromeDriverManager().install())
        self.chrome = webdriver.Chrome(service=service, options=chrome_options)


        # SolverRecaptchaクラスを初期化
        self.recaptcha_solver = SolverRecaptcha(self.chrome)

        # LineNotifyクラスを初期化
        self.line_notify = LineNotify()

        # ChatworkNotifyクラスを初期化
        self.chatwork_notify = ChatworkNotify()


    def take_screenshot(self, filename):
        """
        デバッグモード時にログイン前後にスクショを撮る
        """
        if self.debug_mode:
            # 拡張子選択 {.bmp or .png or .jpg(.jpeg)}
            filename_with_extension = filename + ".jpg"
            self.chrome.save_screenshot(filename_with_extension)
            self.logger.debug(f"スクリーンショットを保存しました: {filename_with_extension}")



    def login(self, login_url, userid, password, userid_xpath, password_xpath, login_button_xpath, cart_element_xpath):
        self.chrome.get(login_url)

        # 現在のURL
        current_url = self.chrome.current_url
        self.logger.debug(current_url)

        # ログイン画面のスクショ
        self.take_screenshot("login_before_take")

        # userid_xpathが出てくるまで待機
        try:
            WebDriverWait(self.chrome, 10).until(EC.presence_of_element_located((By.XPATH, userid_xpath)))
            self.logger.debug("入力開始")
        
        except TimeoutException as e:
            print(f"タイムアウトエラー:{e}")

        # IDとパスを入力
        try:
            userid_field = self.chrome.find_element_by_xpath(userid_xpath)
            userid_field.send_keys(userid)
            self.logger.debug("ID入力完了")

            password_field = self.chrome.find_element_by_xpath(password_xpath)
            password_field.send_keys(password)
            self.logger.debug("パスワード入力完了")

        except NoSuchElementException as e:
            print(f"要素が見つからない: {e}")


        # ページが完全に読み込まれるまで待機
        WebDriverWait(self.chrome, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        self.logger.debug("ページは完全に表示されてる")

        # reCAPTCHA検知
        try:
            # sitekeyを検索
            self.chrome.find_element_by_css_selector('[data-sitekey]')
            self.logger.info("reCAPTCHAが検出されました")


            # solveRecaptchaファイルを実行
            try:
                self.recaptcha_solver.handle_recaptcha(current_url)
                self.logger.info("reCAPTCHA処理、完了")

            except Exception as e:
                self.logger.error("reCAPTCHA処理に失敗しました")
                # ログイン失敗をライン通知
                self.line_notify.line_notify("ログインが正しくできませんでした")


            self.logger.debug("クリック開始")

            # ログインボタン要素を見つける
            login_button = self.chrome.find_element_by_id("recaptcha-submit")

            # ボタンが無効化されているか確認し、無効化されていれば有効にする
            self.chrome.execute_script("document.getElementById('recaptcha-submit').disabled = false;")

            # ボタンをクリックする
            login_button.click()

        # recaptchaなし
        except NoSuchElementException:
            self.logger.info("reCAPTCHA、なし")

            login_button = self.chrome.find_element_by_xpath(login_button_xpath)
            self.chrome.execute_script("arguments[0].click();", login_button)
            self.logger.debug("クリック完了")


        # ページ読み込み待機
        try:
            # ログインした後のページ読み込みの完了確認
            WebDriverWait(self.chrome, 10).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            self.logger.debug("ログインページ読み込み完了")

            # ログイン画面のスクショ
            self.take_screenshot("login_after_take")

        except Exception as e:
            self.logger.error(f"handle_recaptcha を実行中にエラーが発生しました: {e}")

        # ログイン完了確認
        try:
            self.chrome.find_element_by_xpath(cart_element_xpath)
            self.logger.info("ログイン完了")
            self.line_notify.line_image_notify("ログインが完了しました。")


        except NoSuchElementException:
            self.logger.info(f"カートの確認が取れませんでした")
            self.line_notify.line_notify("ログイン失敗してしまいました")