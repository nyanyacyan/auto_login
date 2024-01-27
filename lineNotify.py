# coding: utf-8
# ----------------------------------------------------------------------------------
# ライン通知　クラス
# 2023/1/26制作
# 仮想環境 / source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# requests==2.31.0
# pillow==10.2.0

# ----------------------------------------------------------------------------------

import os
import requests
from dotenv import load_dotenv

# モジュール
from infoLogger import Logger

class LineNotify:
    def __init__(self):
        load_dotenv()
        self.logger = Logger().get_logger()
        # 作成したトークンを挿入
        # LINE通知したい人を選定してトークン作成=> ここに貼り付ける
        self.line_notify_token = os.getenv('LINE_NOTIFY_TOKEN')

    def line_notify(self, notification_message):
        """
        "Line Notify"からラインメッセージのみ通知する
        """
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        data = {'message': {notification_message}}

        response = requests.post(line_notify_api, headers = headers, data=data)

        if response.status_code == 200:
            self.logger.info("送信成功")
        else:
            self.logger.error(f"送信に失敗しました: ステータスコード {response.status_code},{response.text}")


    def line_image_notify(self, notification_message):
        """
        "Line Notify"からラインメッセージ + 画像通知する
        """
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        data = {'message': {notification_message}}
        

        # 画像ファイルを指定する（png or jpeg）
        image_file = 'screenshot_after.png'

        # バイナリデータで読み込む
        # バイナリデータは「0」「1」で構成された機械語に直したデータのこと
        binary = open(image_file, mode= 'rb')

        # 指定の辞書型にする
        image_dic = {'imageFile': binary}

        # LINEに画像とメッセージを送る
        response = requests.post(line_notify_api, headers = headers, data=data, files=image_dic)

        if response.status_code == 200:
            self.logger.info("送信成功")
        else:
            self.logger.error(f"送信に失敗しました: ステータスコード {response.status_code},{response.text}")



