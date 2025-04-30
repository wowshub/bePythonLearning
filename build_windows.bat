@echo off
setlocal

:: 设置变量
set SCRIPT=FormatToLearning.py
set ICON=be.ico
set OUTNAME=FormatToLearning

:: 检查 Python 环境
where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pyinstaller 未安装，请先运行：pip install pyinstaller
    pause
    exit /b
)

:: 清理旧打包内容
echo [INFO] 清理旧的构建文件...
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
del %OUTNAME%.spec >nul 2>&1

:: 执行打包
echo [INFO] 开始打包 %SCRIPT% 为单文件 .exe
pyinstaller --onefile --windowed --icon=%ICON% %SCRIPT%

:: 打包完成，打开 dist 文件夹
if exist dist\%OUTNAME%.exe (
    echo [SUCCESS] 打包成功：dist\%OUTNAME%.exe
    start dist
) else (
    echo [FAIL] 打包失败，请检查错误日志。
)

endlocal
pause
