from tkinter import *

FormatToLearningGui = Tk()
FormatToLearningGui.title("人卫题库导入学习通小程序")
FormatToLearningGui.geometry("1900x600+500+500")


# 设置统一字体样式
default_font = ("微软雅黑", 44)

def format_to_learning():
    renweifile= open("renwei.txt", "a",encoding="utf-8")
    renweifile.write("{{")
    renweifile.write("%s" % exerciseText.get(1.0, END))
    renweifile.write("}}")


Label(FormatToLearningGui, text="输入A3/A4题目",height=2, font=default_font).pack()
exerciseText = Text(FormatToLearningGui)
exerciseText.pack()

saveButtom = Button(FormatToLearningGui, text="转换", command=format_to_learning, font=default_font)
saveButtom.pack()










FormatToLearningGui.mainloop()


