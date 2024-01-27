# ----------------------------------------------------------------------------------
# SUPER DELIVERY　自動ログイン
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

superdelivery_auto_login = AutoLogin(debug_mode=True)

# superdeliveryにログイン
superdelivery_auto_login.login(
    "https://www.superdelivery.com/p/do/clickMemberLogin",  # URL
    "info@abitora.jp",  # ID
    "Abitra2577",  # password
    "//input[@name='identification']",  # IDの検索する要素
    "//input[@name='password']",  # パスの検索する要素
    "//input[@type='submit' and @value='ログイン']",  # クリックするボタン検索する要素
    "//a[contains(@href, '/p/do/shoppingCart') and .//p[contains(text(), 'カートを見る')]]"  # カートの有無でログイン確認
    )


