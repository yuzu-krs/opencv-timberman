# monitorの寸法を測るときに利用してください。

#pyautoguiのインポート
import pyautogui
#timeモジュールのインポート、時間設定ができるように。
import time

#ctrl+cで終了ができるようにtry　except構文をつくる。
#プリント文で、初期座標を表示

try:
    print(pyautogui.position())
    while True:    #while文で永久動作
        #ポジション1を現在のポジションポジション2を新しいポジション。
        pt1 = pyautogui.position()
        time.sleep(0.1)
        pt2 = pyautogui.position()#ポジション1とポジション2に差分を調べる。
        #0.1秒間隔で差分をみる。

        if pt1 != pt2:#ポジション1とポジション2が違うとき以下の動作をする。
            print(pyautogui.position())
            pt1 = pyautogui.position()
            time.sleep(0.005)
            pt2 = pyautogui.position()
except KeyboardInterrupt:
    #終了時にプリント文で終了させる。
    print("終了しました。")