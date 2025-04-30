# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
from tkinter.ttk import Combobox
import re

# 提前创建 Tk 根窗口，供 font.families 使用
root = Tk()
root.withdraw()

# 中文字体候选
chinese_font_candidates = [
    "fangsong ti", "song ti", "wqy micro hei", "wqy zen hei",
    "droid sans fallback", "noto sans cjk sc", "ar pl ukai cn", "wenquanyi zen hei"
]

available_fonts = [f.lower() for f in font.families()]
selected_font_name = next((f for f in chinese_font_candidates if f in available_fonts), "TkDefaultFont")
print(f"[INFO] 使用字体：{selected_font_name}")
default_font = (selected_font_name, 18)

# 创建主窗口
FormatToLearningGui = Tk()
FormatToLearningGui.title("人卫题库导入学习通小程序")
FormatToLearningGui.geometry("2400x1600+500+500")

# 居中弹窗
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

# A3/A4 题型处理
def wrap_a3a4_questions(text: str) -> str:
    lines = text.strip().splitlines()
    output_blocks = []
    current_block = []
    block_counter = 1
    sub_counter = 1

    for line in lines:
        stripped_line = line.strip()
        if re.match(r"\(\d+~\d+题共用题干\)", stripped_line):
            if current_block:
                block_text = "\n".join(current_block).strip()
                output_blocks.append(f"{block_counter}.{{{{\n{block_text}\n}}}}")
                block_counter += 1
                sub_counter = 1
                current_block = []
            current_block.append(stripped_line)
        else:
            if re.match(r"^\(\d+\)", stripped_line):
                converted_line = re.sub(r"^\(\d+\)", f"{sub_counter}.", stripped_line)
                current_block.append(converted_line)
                sub_counter += 1
            else:
                current_block.append(stripped_line)

    if current_block:
        block_text = "\n".join(current_block).strip()
        output_blocks.append(f"{block_counter}.{{{{\n{block_text}\n}}}}")

    return "\n\n".join(output_blocks)

# B1 题型处理
def wrap_b1_questions(text: str) -> str:
    lines = text.strip().splitlines()
    output_blocks = []
    current_block = []
    block_counter = 1

    for line in lines:
        stripped = line.strip()
        if re.match(r"^\（?\d+～\d+共用备选答案\）?", stripped):
            if current_block:
                block_text = "\n".join(current_block).strip()
                output_blocks.append(f"{block_counter}.{{{{\n{block_text}\n}}}}")
                block_counter += 1
                current_block = []
        current_block.append(stripped)

    if current_block:
        block_text = "\n".join(current_block).strip()
        output_blocks.append(f"{block_counter}.{{{{\n{block_text}\n}}}}")

    return "\n\n".join(output_blocks)

# 格式转换主函数（根据下拉选择切换）
def format_to_learning():
    content = exerciseText.get("1.0", END).strip()
    if not content:
        custom_showinfo("⚠ 提示", "输入框为空，请输入内容后再转换！")
        return

    selected_type = type_selector.get()
    if selected_type == "A3/A4题型":
        formatted = wrap_a3a4_questions(content)
    elif selected_type == "B1题型":
        formatted = wrap_b1_questions(content)
    else:
        custom_showinfo("❌ 错误", "请先选择题型")
        return

    with open("mulrenweim.txt", "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

    custom_showinfo("转换成功", "🎉 所有内容已成功写入 mulrenweim.txt")

# 全选功能 Ctrl+A
def select_all(event):
    event.widget.tag_add("sel", "1.0", "end")
    return "break"

# 安全撤销 Ctrl+Z
def safe_undo(event):
    try:
        event.widget.edit_undo()
    except TclError:
        pass
    return "break"

# 界面控件区域
Label(FormatToLearningGui, text="选择题型", font=default_font).pack(pady=5)
type_selector = Combobox(FormatToLearningGui, values=["A3/A4题型", "B1题型"], font=default_font, state="readonly", width=20)
type_selector.set("A3/A4题型")
type_selector.pack(pady=5)

Label(FormatToLearningGui, text="输入题目文本", font=default_font, height=2).pack()
exerciseText = Text(FormatToLearningGui, font=default_font, undo=True, autoseparators=True, maxundo=-1)
exerciseText.pack(fill=BOTH, expand=True, padx=20, pady=10)

# 绑定快捷键 Ctrl+A Ctrl+Z（含 macOS）
exerciseText.bind("<Control-a>", select_all)
exerciseText.bind("<Command-a>", select_all)
exerciseText.bind("<Control-z>", safe_undo)
exerciseText.bind("<Command-z>", safe_undo)

# 转换按钮
Button(FormatToLearningGui, text="转换", command=format_to_learning, font=default_font, height=2, width=10).pack(pady=10)

# 启动窗口
FormatToLearningGui.mainloop()
