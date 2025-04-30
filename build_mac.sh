#!/bin/bash

SCRIPT="mulFormatTolearning.py"
ICON="be.icns"
OUTNAME="mulFormatTolearning"

# 检查 pyinstaller 是否安装
if ! command -v pyinstaller &> /dev/null; then
    echo "[ERROR] pyinstaller 未安装，请先运行：pip install pyinstaller"
    exit 1
fi

# 清理旧内容
echo "[INFO] 清理旧的打包文件..."
rm -rf build dist "$OUTNAME.spec"

# 执行打包
echo "[INFO] 正在打包 $SCRIPT 为 .app..."
pyinstaller --onefile --windowed --icon="$ICON" "$SCRIPT"

# 打包结果检查
if [ -f "dist/$OUTNAME" ]; then
    echo "[SUCCESS] 打包完成：dist/$OUTNAME"
    open dist
else
    echo "[FAIL] 打包失败，请检查错误日志。"
fi
