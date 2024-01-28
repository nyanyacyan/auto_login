# coding: utf-8
# ----------------------------------------------------------------------------------
# Slack通知　クラス
# 2023/1/28制作
# 仮想環境 / source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# requests==2.31.0
# pillow==10.2.0

# ----------------------------------------------------------------------------------
import os
import time
import requests
from PIL import Image
from dotenv import load_dotenv

# モジュール
from debugLogger import Logger


class SlackNotify:
    def __init__(self, debug_mode=True):
        # Loggerクラスを初期化
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        # トークンを.envから取得
        # 通知したい部屋を選定（作成）=> .envにルーム番号を貼り付ける
        load_dotenv()
        self.slack_notify_token = os.getenv('SLACK_NOTIFY_TOKEN')
        self.slack_channel = os.getenv('SLACK_CHANNEL')


    def chatwork_notify(self, notification_message):
        """
        "chatwork Notify"からラインメッセージのみ通知する
        """
        URL = 'https://api.chatwork.com/v2'

        url = URL + '/rooms/' + str(self.chatwork_roomid) + '/messages'


        headers = { 'X-ChatWorkToken': self.chatwork_notify_token}
        params = {'body': {notification_message}}

        response = requests.post(url, headers = headers, params=params)

        if response.status_code == 200:
            self.logger.info("送信成功")
        else:
            self.logger.error(f"送信に失敗しました: ステータスコード {response.status_code},{response.text}")



    def chatwork_image_notify(self, notification_message):
        """
        "Chatwork Notify"からメッセージ + 画像添付 + 送信後、リサイズ画像削除
        """
        URL = 'https://api.chatwork.com/v2'


        # ディレクトリにある画像ファイルを指定する（ファイルもOK）
        image_file = 'screenshot_after_compressed.png'

        url = URL + '/rooms/' + str(self.chatwork_roomid) + '/files'
        jpeg_bin = open(image_file, 'rb')
        headers = { 'X-ChatWorkToken': self.chatwork_notify_token}
        
        # ファイルの形式の選定
        # Content-Typeでの指定が必要=> "image/png"
        files = {'file': (image_file, jpeg_bin, "image/png")}

        data = {'message': notification_message}

        # chatworkに画像とメッセージを送る
        response = requests.post(url, headers = headers, files=files, data=data)

        if response.status_code == 200:
            self.logger.info("送信成功")
        else:
            self.logger.error(f"送信に失敗しました: ステータスコード {response.status_code},{response.text}")

        time.sleep(5)

        # 添付した写真を削除
        try:
            if os.path.exists(compressed_image_path):
                # ファイルを削除
                os.remove(compressed_image_path)
                self.logger.info(f"'{compressed_image_path}'を削除しました")
            else:
                self.logger.error(f"削除するファイル'{compressed_image_path}' が見つかりませんでした。")

        except Exception as e:
            self.logger.error(f"ファイル削除中にエラーが発生しました: {e}")
