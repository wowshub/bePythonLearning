# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font, messagebox  # 导入 messagebox



# 提前创建 Tk 根窗口，供 font.families 使用
root = Tk()
root.withdraw()  # 不显示这个临时窗口

# 常见支持中文的字体候选列表（小写！）
chinese_font_candidates = [
    "fangsong ti",
    "song ti",
    "wqy micro hei",
    "wqy zen hei",
    "droid sans fallback",
    "noto sans cjk sc",
    "ar pl ukai cn",
    "wenquanyi zen hei",
]

# 获取支持的字体列表
available_fonts = [f.lower() for f in font.families()]
selected_font_name = next((f for f in chinese_font_candidates if f in available_fonts), "TkDefaultFont")
print(f"[INFO] 使用字体：{selected_font_name}")
default_font = (selected_font_name, 18)

# 创建真正的 GUI 窗口
FormatToLearningGui = Tk()
FormatToLearningGui.title("人卫题库导入学习通小程序")
FormatToLearningGui.geometry("2400x1600+500+500")


def custom_showinfo(title, message, width=500, height=200):
    win = Toplevel(FormatToLearningGui)
    win.title(title)
    win.grab_set()  # 模态窗口（阻止主界面点击）

    # 获取屏幕尺寸
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # 计算弹窗居中坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口大小和位置
    win.geometry(f"{width}x{height}+{x}+{y}")

    # 内容区域
    Label(win, text=message, font=default_font, pady=30).pack()
    Button(win, text="确定", font=default_font, width=10, command=win.destroy).pack(pady=20)



def format_to_learning():
    content = exerciseText.get("1.0", END).strip()
    if not content:
        custom_showinfo("⚠ 提示", "输入框为空，请输入内容后再转换！")
        return

    with open("renwei.txt", "a", encoding="utf-8") as renweifile:
        renweifile.write("{{")
        renweifile.write(content)
        renweifile.write("}}")

    custom_showinfo("转换成功", "🎉 题目已成功写入 renwei.txt")


Label(FormatToLearningGui, text="输入A3/A4题目", font=default_font, height=3).pack()
exerciseText = Text(FormatToLearningGui, font=default_font)
exerciseText.pack(fill=BOTH, expand=True, padx=20, pady=10)
saveButtom = Button(FormatToLearningGui, text="转换", command=format_to_learning, font=default_font, height=2, width=10)
saveButtom.pack(pady=10)

FormatToLearningGui.mainloop()
