import tkinter as tk
from tkinter import scrolledtext

import re


def process_text():
    raw_text = text_input.get("1.0", tk.END)

    # 使用正则表达式切分题目（匹配以数字. 开头的题目）
    # parts = re.split(r'(?<=\n|^)(\d+\.\s)', raw_text)
    parts = re.split(r'(\d+\.\s)', raw_text)

    # 重组题目（跳过空段）
    questions = []
    for i in range(1, len(parts), 2):  # i 是题号，i+1 是题目内容
        number = parts[i].strip()
        content = parts[i+1].strip()
        if content:
            questions.append(f"{number} {{ {content} }}")

    # 显示结果
    processed_text.delete("1.0", tk.END)
    processed_text.insert(tk.END, "\n\n".join(questions))


# 创建窗口
root = tk.Tk()
root.geometry("2480x1424")
root.title("题目分割与格式化器")

# 文本输入框
text_input = scrolledtext.ScrolledText(root, height=55, width=180)
text_input.pack(padx=10, pady=10)

# 按钮
process_button = tk.Button(root, text="处理题目", command=process_text)
process_button.pack(pady=5)

# 输出框
processed_text = scrolledtext.ScrolledText(root, height=55, width=180)
processed_text.pack(padx=10, pady=10)

root.mainloop()



