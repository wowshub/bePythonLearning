# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
import re

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

# 居中弹窗函数
def custom_showinfo(title, message, width=500, height=200):
    win = Toplevel(FormatToLearningGui)
    win.title(title)
    win.grab_set()  # 模态窗口（阻止主界面点击）

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    win.geometry(f"{width}x{height}+{x}+{y}")
    Label(win, text=message, font=default_font, pady=30).pack()
    Button(win, text="确定", font=default_font, width=10, command=win.destroy).pack(pady=20)

def wrap_big_questions(text: str) -> str:
    lines = text.strip().splitlines()
    output_blocks = []
    current_block = []
    block_counter = 1
    sub_counter = 1  # 小题号计数

    for line in lines:
        stripped_line = line.strip()

        # 如果是新的大题开始
        if re.match(r"\(\d+~\d+题共用题干\)", stripped_line):
            if current_block:
                block_text = "\n".join(current_block).strip()
                output_blocks.append(f"{block_counter}.{{\n{block_text}\n}}")
                block_counter += 1
                sub_counter = 1  # 每个大题重新开始小题号
                current_block = []

            current_block.append(stripped_line)
        else:
            # 检查是否是小题行（以 (数字) 开头）
            if re.match(r"^\(\d+\)", stripped_line):
                converted_line = re.sub(r"^\(\d+\)", f"{sub_counter}.", stripped_line)
                current_block.append(converted_line)
                sub_counter += 1
            else:
                current_block.append(stripped_line)

    # 添加最后一块
    if current_block:
        block_text = "\n".join(current_block).strip()
        output_blocks.append(f"{block_counter}.{{\n{block_text}\n}}")

    return "\n\n".join(output_blocks)


# 自动识别大题分段并添加 {{ }} 的函数
def wrap_big_questions(text: str) -> str:
    lines = text.strip().splitlines()
    output_blocks = []
    current_block = []

    for line in lines:
        # 匹配题干开头，例如 (1~2题共用题干)
        if re.match(r"\(\d+~\d+题共用题干\)", line.strip()):
            if current_block:
                output_blocks.append("{{\n" + "\n".join(current_block).strip() + "\n}}")
                current_block = []
        current_block.append(line)

    # 添加最后一组题
    if current_block:
        output_blocks.append("{{\n" + "\n".join(current_block).strip() + "\n}}")

    return "\n\n".join(output_blocks)

# 转换按钮功能
def format_to_learning():
    content = exerciseText.get("1.0", END).strip()
    if not content:
        custom_showinfo("⚠ 提示", "输入框为空，请输入内容后再转换！")
        return

    formatted = wrap_big_questions(content)

    with open("mulrenweim.txt", "a", encoding="utf-8") as renweifile:
        renweifile.write(formatted + "\n")

    custom_showinfo("转换成功", "🎉 所有大题已成功写入 mulrenweim.txt")

# UI 布局
Label(FormatToLearningGui, text="输入A3/A4题目", font=default_font, height=3).pack()
exerciseText = Text(FormatToLearningGui, font=default_font)
exerciseText.pack(fill=BOTH, expand=True, padx=20, pady=10)
saveButtom = Button(FormatToLearningGui, text="转换", command=format_to_learning, font=default_font, height=2, width=10)
saveButtom.pack(pady=10)

# 启动主界面
FormatToLearningGui.mainloop()
