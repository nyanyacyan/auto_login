# coding: utf-8
# ----------------------------------------------------------------------------------
# slack通知　クラス
# 2023/1/27制作
# 仮想環境 / source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# requests==2.31.0
# pillow==10.2.0

# ----------------------------------------------------------------------------------
import os
import requests
from dotenv import load_dotenv

class SlackNotify:
    def __init__(self):
        load_dotenv()
        # 作成したトークンを挿入
        # LINE通知したい人を選定してトークン作成=> ここに貼り付ける
        self.line_notify_token = os.getenv('SLACK_NOTIFY_TOKEN')