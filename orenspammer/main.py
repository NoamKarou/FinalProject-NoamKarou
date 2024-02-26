import pyautogui
import time

time.sleep(2)
print(pyautogui.position())

def invite():
    pyautogui.click()
    pyautogui.moveTo(748, 932)
    pyautogui.click()
    time.sleep(0.15)
    pyautogui.moveTo(1307, 404)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.press("esc")

for i in range(50):
    invite()