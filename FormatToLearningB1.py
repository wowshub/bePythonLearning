# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
import re

# 提前创建 Tk 根窗口，供 font.families 使用
root = Tk()
root.withdraw()

# 常见支持中文的字体候选列表（小写！）
chinese_font_candidates = [
    "fangsong ti", "song ti", "wqy micro hei", "wqy zen hei",
    "droid sans fallback", "noto sans cjk sc", "ar pl ukai cn", "wenquanyi zen hei"
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

# 居中弹窗函数
def custom_showinfo(title, message, width=500, height=200):
    win = Toplevel(FormatToLearningGui)
    win.title(title)
    win.grab_set()

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    win.geometry(f"{width}x{height}+{x}+{y}")
    Label(win, text=message, font=default_font, pady=30).pack()
    Button(win, text="确定", font=default_font, width=10, command=win.destroy).pack(pady=20)
def select_all(event):
    event.widget.tag_add("sel", "1.0", "end")
    return "break"


# ✅ 最新：识别题干、加编号、替换小题号的函数
def wrap_b1_questions(text: str) -> str:
    lines = text.strip().splitlines()
    output_blocks = []
    current_block = []
    block_counter = 1

    for line in lines:
        stripped = line.strip()

        # 检测是否是 "(数字～数字共用备选答案)" 结构
        if re.match(r"^\（?\d+～\d+共用备选答案\）?", stripped):
            if current_block:
                # 加入前一个大题块
                block_text = "\n".join(current_block).strip()
                output_blocks.append(f"{block_counter}.{{{{\n{block_text}\n}}}}")
                block_counter += 1
                current_block = []

        current_block.append(stripped)

    # 最后一块处理
    if current_block:
        block_text = "\n".join(current_block).strip()
        output_blocks.append(f"{block_counter}.{{{{\n{block_text}\n}}}}")

    return "\n\n".join(output_blocks)


# 转换按钮功能
def format_to_learning():
    content = exerciseText.get("1.0", END).strip()
    if not content:
        custom_showinfo("⚠ 提示", "输入框为空，请输入内容后再转换！")
        return

    formatted = wrap_b1_questions(content)

    with open("renweiB1Output.txt", "a", encoding="utf-8") as renweifile:
        renweifile.write(formatted + "\n")

    custom_showinfo("转换成功", "🎉 所有大题已成功写入 renweiB1Output.txt")

# UI 布局
Label(FormatToLearningGui, text="输入B1题目", font=default_font, height=3).pack()
exerciseText = Text(FormatToLearningGui, font=default_font, undo=True, maxundo=-1, autoseparators=True)
exerciseText.pack(fill=BOTH, expand=True, padx=20, pady=10)


# 绑定 Ctrl+A 快捷键（Windows/Linux）
exerciseText.bind("<Control-a>", select_all)

# 绑定 Command+A（macOS）
exerciseText.bind("<Command-a>", select_all)

def safe_undo(event):
    try:
        event.widget.edit_undo()
    except TclError:
        pass  # 忽略“nothing to undo”的异常
    return "break"

exerciseText.bind("<Control-z>", safe_undo)
exerciseText.bind("<Command-z>", safe_undo)  # macOS 支持




saveButtom = Button(FormatToLearningGui, text="转换", command=format_to_learning, font=default_font, height=2, width=10)
saveButtom.pack(pady=10)

# 启动主界面
FormatToLearningGui.mainloop()
