# coding: utf-8
# ----------------------------------------------------------------------------------
# ChatWork通知　クラス
# 2023/1/27制作
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


class ChatworkNotify:
    def __init__(self, debug_mode=True):
        # Loggerクラスを初期化
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode

        # トークンを.envから取得
        # 通知したい部屋を選定（作成）=> .envにルーム番号を貼り付ける
        load_dotenv()
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

        # ChatWork送信時、データ容量上限は「5M」
        # 写真のサイズと解像度を下げて保存する
        try:
            with Image.open('login_after_take.jpeg') as jpg:
                png = jpg.resize((jpg.width // 2, jpg.height // 2))
                compressed_image = "login_after_take_comp.jpeg"
                
                png.save(compressed_image, "PNG")

            if not os.path.exists(compressed_image):
                raise FileNotFoundError(f"ファイル '{compressed_image}' が見つかりません")

        except FileNotFoundError as e:
            self.logger.error(f"指定の画像が見つかりません: {e}")

        except Exception as e:
            self.logger.error(f"画像処理でエラーが発生しました: {e}")


        url = URL + '/rooms/' + str(self.chatwork_roomid) + '/files'
        headers = { 'X-ChatWorkToken': self.chatwork_notify_token}
        
        # ファイルの形式の選定
        # Content-Typeでの指定が必要=> "image/png"
        try:
            with open(compressed_image, 'rb') as jpeg_bin:
                files = {'file': (compressed_image, jpeg_bin, "image/jpeg")}

                data = {'message': notification_message}

                # chatworkに画像とメッセージを送る
                response = requests.post(url, headers = headers, data=data, files=files)

                if response.status_code == 200:
                    self.logger.info("送信成功")
                else:
                    self.logger.error(f"送信に失敗しました: ステータスコード {response.status_code},{response.text}")

        except FileNotFoundError as e:
            self.logger.error(f"指定の画像が見つかりません: {e}")

        except Exception as e:
            self.logger.error(f"画像送信でエラーが発生: {e}")



        time.sleep(5)

        # 添付した写真を削除
        try:
            if os.path.exists(compressed_image):
                # ファイルを削除
                os.remove(compressed_image)
                self.logger.info(f"'{compressed_image}'を削除しました")
            else:
                self.logger.error(f"削除するファイル'{compressed_image}' が見つかりませんでした。")

        except Exception as e:
            self.logger.error(f"ファイル削除中にエラーが発生しました: {e}")
