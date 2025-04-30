# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
from tkinter.ttk import Combobox
import re

# 初始化 Tk 根窗口（供字体检测用）
root = Tk()
root.withdraw()

# 字体选择（中文兼容）
chinese_font_candidates = [
    "fangsong ti", "song ti", "wqy micro hei", "wqy zen hei",
    "droid sans fallback", "noto sans cjk sc", "ar pl ukai cn", "wenquanyi zen hei"
]
available_fonts = [f.lower() for f in font.families()]
selected_font_name = next((f for f in chinese_font_candidates if f in available_fonts), "TkDefaultFont")
default_font = (selected_font_name, 18)

# 创建 GUI 主窗口
FormatToLearningGui = Tk()
FormatToLearningGui.title("人卫题库导出工具")
FormatToLearningGui.geometry("2400x1600+500+500")

# 居中弹窗
def custom_showinfo(title, message, width=500, height=200):
    win = Toplevel(FormatToLearningGui)
    win.title(title)
    win.grab_set()
    x = (win.winfo_screenwidth() - width) // 2
    y = (win.winfo_screenheight() - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")
    Label(win, text=message, font=default_font, pady=30).pack()
    Button(win, text="确定", font=default_font, width=10, command=win.destroy).pack(pady=20)

# A3/A4题型处理函数
def wrap_a3a4_questions(text: str) -> str:
    lines = text.strip().splitlines()
    output_blocks = []
    current_block = []
    block_counter = 1
    sub_counter = 1

    for line in lines:
        stripped = line.strip()
        if re.match(r"\(\d+~\d+题共用题干\)", stripped):
            if current_block:
                output_blocks.append(f"{block_counter}.{{{{\n" + "\n".join(current_block).strip() + "\n}}}}")
                block_counter += 1
                sub_counter = 1
                current_block = []
            current_block.append(stripped)
        else:
            if re.match(r"^\(\d+\)", stripped):
                line = re.sub(r"^\(\d+\)", f"{sub_counter}.", stripped)
                sub_counter += 1
            current_block.append(line)

    if current_block:
        output_blocks.append(f"{block_counter}.{{{{\n" + "\n".join(current_block).strip() + "\n}}}}")

    return "\n\n".join(output_blocks)

# B1题型处理函数
def wrap_b1_questions(text: str) -> str:
    lines = text.strip().splitlines()
    output_blocks = []
    current_block = []
    block_counter = 1

    for line in lines:
        stripped = line.strip()
        if re.match(r"^\（?\d+～\d+共用备选答案\）?", stripped):
            if current_block:
                output_blocks.append(f"{block_counter}.{{{{\n" + "\n".join(current_block).strip() + "\n}}}}")
                block_counter += 1
                current_block = []
        current_block.append(stripped)

    if current_block:
        output_blocks.append(f"{block_counter}.{{{{\n" + "\n".join(current_block).strip() + "\n}}}}")

    return "\n\n".join(output_blocks)

# 格式转换主函数
def format_to_learning():
    content = exerciseText.get("1.0", END).strip()
    if not content:
        custom_showinfo("⚠ 提示", "输入框为空，请输入内容后再转换！")
        return

    selected_type = type_selector.get()
    if selected_type == "A3/A4题型":
        formatted = wrap_a3a4_questions(content)
        output_file = "renweiA3A4Output.txt"
    elif selected_type == "B1题型":
        formatted = wrap_b1_questions(content)
        output_file = "renweiB1Output.txt"
    else:
        custom_showinfo("❌ 错误", "请先选择题型")
        return

    try:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
        custom_showinfo("转换成功", f"🎉 内容已写入 {output_file}")
    except Exception as e:
        custom_showinfo("写入错误", str(e))

# 快捷键 Ctrl+A：全选
def select_all(event):
    event.widget.tag_add("sel", "1.0", "end")
    return "break"

# 快捷键 Ctrl+Z：撤销
def safe_undo(event):
    try:
        event.widget.edit_undo()
    except TclError:
        pass
    return "break"


# ===== 界面布局 =====
Label(FormatToLearningGui, text="选择题型", font=default_font).pack(pady=5)
type_selector = Combobox(FormatToLearningGui, values=["A3/A4题型", "B1题型"], font=default_font, state="readonly", width=20)
type_selector.set("A3/A4题型")
type_selector.pack(pady=5)

Label(FormatToLearningGui, text="输入题目内容", font=default_font).pack(pady=5)
exerciseText = Text(FormatToLearningGui, font=default_font, undo=True, autoseparators=True, maxundo=-1)
exerciseText.pack(fill=BOTH, expand=True, padx=20, pady=10)

exerciseText.bind("<Control-a>", select_all)
exerciseText.bind("<Command-a>", select_all)
exerciseText.bind("<Control-z>", safe_undo)
exerciseText.bind("<Command-z>", safe_undo)

Button(FormatToLearningGui, text="转换", command=format_to_learning, font=default_font, height=2, width=10).pack(pady=10)

# 启动主循环
FormatToLearningGui.mainloop()
