# -*- coding: utf-8 -*-
# ${NAME}.py created at ${DATE} by ${USER}
from tkinter import *
import platform

FormatToLearningGui = Tk()
FormatToLearningGui.title("人卫题库导入学习通小程序")
FormatToLearningGui.geometry("2400x1600+500+500")


# 设置统一字体样式
##   default_font = ("微软雅黑", 44)


# # 根据系统选择字体
# if platform.system() == 'Windows':
#     default_font = ("微软雅黑", 44)
# elif platform.system() == 'Darwin':  # macOS
#     default_font = ("PingFang SC", 44)
# else:  # Linux
#     default_font = ("SimHei", 44)

# default_font = ("song ti", 32) #不显示乱码了
default_font = ("fangsong ti", 32)




def format_to_learning():
    renweifile = open("renwei.txt", "a", encoding="UTF-8")  # encoding="utf-8"
    renweifile.write("{{ \n")
    renweifile.write("%s" % exerciseText.get(1.0, END))
    renweifile.write("}} \n")


Label(FormatToLearningGui, text="输入A3/A4题目", font=default_font, height=3).pack()  # , font=default_font
exerciseText = Text(FormatToLearningGui, font=default_font)
exerciseText.pack()

saveButtom = Button(FormatToLearningGui, text="转换", command=format_to_learning, font=default_font, height=2, width=10) #  font=default_font
saveButtom.pack()










FormatToLearningGui.mainloop()


