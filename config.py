# coding: utf-8
# ----------------------------------------------------------------------------------
# Configクラス
# 2023/1/29制作
# 仮想環境 / source autologin-v1/bin/activate


#---バージョン---
# Python==3.8.10

#---流れ--
#----------------------------------------------------------------------------------
import time
import sys
import os

# モジュール
from debugLogger import Logger


class Config:
    def __init__(self):
        # Loggerクラスを初期化
        debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
        self.logger_instance = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.logger_instance.get_logger()
        self.debug_mode = debug_mode


    def progress_bar(self, duration):
        total_steps = 20
        interval = duration / total_steps

        for i in range(total_steps):
            time.sleep(interval)  # 次のステップまで待機
            sys.stdout.write('■')  # プログレスバーの一部を表示
            sys.stdout.flush()  # 出力をフラッシュして即時表示
        sys.stdout.write('\n')  # プログレスバーの終了後に改行を出力


