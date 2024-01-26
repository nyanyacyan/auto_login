# ----------------------------------------------------------------------------------
# recaptchaProcessクラス
# 2023/1/20制作
# source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10
# ----------------------------------------------------------------------------------
import logging

class LoggerBasicColor(logging.Formatter):
    COLORS = {
        "INFO": "\033[94m",  # 青色
        "ERROR" : "\033[91m",
    }

    RESET = "\033[0m"

    def format(self, record):
        message = super().format(record)
        color = self.COLORS.get(record.levelname, "")
        return f"{color}{message}{self.RESET}"

class Logger:
    def __init__(self):
        self.logger = logging.getLogger()

        # 同じログは表示しないように設定
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)

            # コンソールにログを出力するハンドラを追加
            console_handler = logging.StreamHandler()
            self.logger.addHandler(console_handler)

            # ログのフォーマットを設定
            log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(log_format)

            log_format = LoggerBasicColor('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(log_format)

    def get_logger(self):
        return self.logger