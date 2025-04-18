# 检测本系统有哪些字体
import tkinter as tk
from tkinter import font

root = tk.Tk()
fonts = list(font.families())
fonts.sort()

for f in fonts:
    print(f)
