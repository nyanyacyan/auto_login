# ----------------------------------------------------------------------------------
# 卸売ドットコム自動ログイン
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
from autoLoginHeadless import AutoLogin
import logging


oroshiuri_auto_login = AutoLogin()

# oroshiuriにログイン
oroshiuri_auto_login.login(
    "https://oroshi-uri.com/login.php",  # URL
    "info@abitora.jp",  # ID
    "Abitra2577",  # password
    "//input[@name='loginEmail']",  # IDの検索する要素
    "//input[@name='loginPassword']",  # パスの検索する要素
    "//input[@name='login']",  # クリックするボタン検索する要素
    "//a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"  # カートの有無でログイン確認
    )

