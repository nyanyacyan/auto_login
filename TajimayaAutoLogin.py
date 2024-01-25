# ----------------------------------------------------------------------------------
# Tajimaya　自動ログイン
# 2023/1/20制作
# 仮想環境 / source autologin-v1/bin/activate
# reCAPTCHA有り


#---バージョン---
# Python==3.8.10
# selenium==4.1
# headlessモード
# Chromedriver==ChromeDriverManager


#---流れ--
# ID入力=> パス入力=> クリック
# ----------------------------------------------------------------------------------
from autoLoginHeadless import AutoLogin

superdelivery_auto_login = AutoLogin()

# superdeliveryにログイン
superdelivery_auto_login.login(
    "https://www.tajimaya-oroshi.net/login.php",  # URL
    "info@abitora.jp",  # ID
    "Abitra2577",  # password
    "//input[@name='loginEmail']",  # IDの検索する要素
    "//input[@name='loginPassword']",  # パスの検索する要素
    "//input[@type='submit']",  # クリックするボタン検索する要素
    "//a[contains(@href, 'cart') and .//em[contains(@class, 'material-icons')]]"  # カートの有無でログイン確認
    )

