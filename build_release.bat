@echo off
setlocal

:: ========================
:: 配置变量
:: ========================
set SCRIPT=FormatToLearning.py
set ICON=be.ico
set OUTNAME=FormatToLearning
set VERSION=v1.0
set ZIPNAME=%OUTNAME%_%VERSION%.zip

:: 检查 pyinstaller 是否存在
where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pyinstaller 未安装，请运行：pip install pyinstaller
    pause
    exit /b
)

:: 清理旧的构建
echo [INFO] 清理旧的构建目录和文件...
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
del %OUTNAME%.spec >nul 2>&1
del %ZIPNAME% >nul 2>&1

:: 开始打包
echo [INFO] 正在打包 %SCRIPT%...
pyinstaller --onefile --windowed --icon=%ICON% %SCRIPT%

:: 检查打包是否成功
if not exist dist\%OUTNAME%.exe (
    echo [ERROR] 打包失败，请检查错误输出。
    pause
    exit /b
)

:: 拷贝附加文件到 dist 目录
echo [INFO] 拷贝 README 和图标到 dist...
copy README.txt dist\ >nul
copy %ICON% dist\ >nul

:: 生成 version.txt
echo [INFO] 生成 version.txt ...
powershell ^
  "$v='版本号：%VERSION%';" ^
  "$t='构建时间：'+(Get-Date -Format 'yyyy-MM-dd HH:mm');" ^
  "$f='构建文件：%OUTNAME%.exe';" ^
  "$lines=($v,$t,$f);" ^
  "Set-Content -Path dist\\version.txt -Value $lines"


:: 创建 zip 压缩包
echo [INFO] 正在压缩为 %ZIPNAME%...
powershell Compress-Archive -Path dist\* -DestinationPath %ZIPNAME%

:: 打开文件夹
echo [SUCCESS] 打包和压缩完成！
start .

endlocal
pause
