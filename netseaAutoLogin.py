# ----------------------------------------------------------------------------------
# netsea自動ログイン
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

netsea_auto_login = AutoLogin()

# netseaにログイン
netsea_auto_login.login(
    "https://www.netsea.jp/login",  # URL
    "info@abitora.jp",  # ID
    "Abitra2577",  # password
    "//input[@name='login_id']",  # IDの検索する要素
    "//input[@name='password']",  # パスの検索する要素
    "//button[@name='submit']",  # クリックするボタン検索する要素
    "//a[contains(@href, 'cart') and .//i[contains(@class, 'fa-shopping-cart')]]"  # カートの有無でログイン確認
    )

