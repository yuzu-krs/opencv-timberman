import keyboard 
import mss
import cv2
import numpy as np
from time import time, sleep
import pyautogui

pyautogui.PAUSE = 0

print("s(スタート)")
print("q(やめる)")

# sを押すまで待機
keyboard.wait("s")

sct = mss.mss()

dimensions_left = {
    'left': 656,   # 左上の x 座標
    'top': 1419,   # 左上の y 座標
    'width': 848 - 656,   # 幅 (右上の x 座標 - 左上の x 座標)
    'height': 1555 - 1419   # 高さ (右上の y 座標 - 左上の y 座標)
}

dimensions_right = {
    'left': 1040,   # 左上の x 座標
    'top': 1417,   # 左上の y 座標
    'width': 1235 - 1040,   # 幅 (右上の x 座標 - 左上の x 座標)
    'height': 1550 - 1417   # 高さ (右上の y 座標 - 左上の y 座標)
}

# 画像読み込み
left_branch = cv2.imread('left_branch.png')
right_branch = cv2.imread('right_branch.png')

w = right_branch.shape[1]
h = right_branch.shape[0]

# フレームレート計算
fpsTime = time()

while True:
    if keyboard.is_pressed('q'):
        break
    
    scr_left = np.array(sct.grab(dimensions_left))
    scr_right = np.array(sct.grab(dimensions_right))
    
    # スクリーンショットからアルファチャンネルを取り除く処理
    scr_remove_left = scr_left[:,:,:3]
    scr_remove_right = scr_right[:,:,:3]

    # 左の枝のテンプレートマッチングを行う
    result_left = cv2.matchTemplate(scr_remove_left, left_branch, cv2.TM_SQDIFF_NORMED)
    _, maxVal_left, _, maxLoc_left = cv2.minMaxLoc(result_left)

    # 右の枝のテンプレートマッチングを行う
    result_right = cv2.matchTemplate(scr_remove_right, right_branch, cv2.TM_SQDIFF_NORMED)
    _, maxVal_right, _, maxLoc_right = cv2.minMaxLoc(result_right)

    print("これは左に枝がある場合" if maxVal_left < maxVal_right else "これは右に枝がある場合")
    print(f"Max Val: {maxVal_left if maxVal_left < maxVal_right else maxVal_right} Max Loc: {maxLoc_left if maxVal_left < maxVal_right else maxLoc_right}")

    # 単純な位置情報で判断
    if maxLoc_left == (106, 91):
        print("左側に枝が見つかりました。右矢印を押します。")
        pyautogui.press('right')
    elif maxLoc_right == (10, 92) or maxLoc_right==(22,68):
        print("右側に枝が見つかりました。左矢印を押します。")
        pyautogui.press('left')

    # スクリーンショットを表示し、フレームレートを計算して表示
    cv2.imshow('Screen Shot', scr_left if maxVal_left < maxVal_right else scr_right)
    cv2.waitKey(1)
    # sleep(0.13)  # この行を削除することで、連打が可能になります
    print('FPS: {}'.format(1 / (time() - fpsTime)))
    fpsTime = time()