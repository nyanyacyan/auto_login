import requests

class LineNotify:
    def __init__(self):
        # 作成したトークンを挿入
        # LINE通知したい人を選定してトークン作成=> ここに貼り付ける
        self.line_notify_token = '2YDEXfVx0mgOrCAY4HOa5wRPRyKArCvY2oBAkfMyKjk'

    def line_notify(self, notification_message):
        """
        ログインに成功した際にライン通知する
        """
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {self.line_notify_token}'}
        data = {'message': {notification_message}}
        requests.post(line_notify_api, headers = headers, data=data)


