# ----------------------------------------------------------------------------------
# ChatWork通知　クラス
# 2023/1/27制作
# 仮想環境 / source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10

# ----------------------------------------------------------------------------------
import os
import requests
from dotenv import load_dotenv

class ChatworkNotify:
    def __init__(self):
        load_dotenv()
        # 作成したトークンを挿入
        # LINE通知したい人を選定してトークン作成=> ここに貼り付ける
        self.chatwork_notify_token = os.getenv('CHATWORK_NOTIFY_TOKEN')
        self.chatwork_roomid = os.getenv('CHATWORK_ROOMID')


    def chatwork_notify(self, notification_message):
        """
        "chatwork Notify"からラインメッセージのみ通知する
        """
        URL = 'https://api.chatwork.com/v2'

        url = URL + '/rooms/' + str(self.chatwork_roomid) + '/messages'


        headers = { 'X-ChatWorkToken': self.chatwork_notify_token}
        params = {'body': {notification_message}}
        requests.post(url, headers = headers, params=params)
