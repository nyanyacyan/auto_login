import requests

class LineNotify:
    def __init__(self):
        # 作成したトークンを挿入
        # LINE通知したい人を選定してトークン作成=> ここに貼り付ける
        self.line_notify_token = '2YDEXfVx0mgOrCAY4HOa5wRPRyKArCvY2oBAkfMyKjk'

    def line_notify(self, notification_message):
        """
        "Line Notify"からラインメッセージのみ通知する
        """
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        data = {'message': {notification_message}}
        requests.post(line_notify_api, headers = headers, data=data)


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
        requests.post(line_notify_api, headers = headers, data=data, files=image_dic)



