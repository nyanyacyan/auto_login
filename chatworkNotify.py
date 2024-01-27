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
from infoLogger import Logger


class ChatworkNotify:
    def __init__(self):
        load_dotenv()
        self.logger = Logger().get_logger()
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

    def chatwork_image_notify(self, notification_message):
        """
        "Chatwork Notify"からメッセージ + 画像添付 + 送信後、リサイズ画像削除
        """
        URL = 'https://api.chatwork.com/v2'

        # ChatWork送信時、データ容量上限は「5M」
        # 写真のサイズと解像度を下げて保存する
        try:
            png = Image.open('screenshot_after.png')
            png = png.resize((png.width // 2, png.height // 2))
            compressed_image_path = "screenshot_after_compressed.png"
            
            png.save(compressed_image_path, "png")

            if not os.path.exists(compressed_image_path):
                raise FileNotFoundError(f"ファイル '{compressed_image_path}' が見つかりません")

        except FileNotFoundError as e:
            self.logger.error(f"指定の画像が見つかりません: {e}")

        except Exception as e:
            self.logger.error(f"画像処理でエラーが発生しました: {e}")


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

        print(response.status_code)
        print(response.text)

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
