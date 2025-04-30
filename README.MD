0.安装相关打包成exe 相关环境安装 setup enviroment:
pip install pyinstaller
pyinstaller --onefile --windowed --icon=be.ico FormatToLearning.py

git tag v1.0.0
在GITHUB上新建release

打包成release 
sudo apt install rar
rar a FormatToLearning.rar



macOS 用 .sh 脚本（适用于打包 .app 或 CLI）
使用方法：
chmod +x build_mac.sh
./build_mac.sh

UPX 压缩它进一步减小体积（可选）
pip install upx
pyinstaller --onefile --windowed --icon=be.ico --upx-dir /path/to/upx FormatToLearning.py


1.功能一：
自动生成 version.txt
版本号：v1.0
构建时间：2025-04-30 20:17
构建文件：FormatToLearning.exe

2.功能二：
生成 version.txt （已经作废 修改成下面的格式）
echo [INFO] 生成 version.txt ...
powershell ^
"$v='版本号：%VERSION%';" ^
"$t='构建时间：'+(Get-Date -Format 'yyyy-MM-dd HH:mm');" ^
"$f='构建文件：%OUTNAME%.exe';" ^
"$lines=($v,$t,$f);" ^
"Set-Content -Path dist\\version.txt -Value $lines"

3.功能三：
打包完成后自动将 ZIP 文件备份到 releases/ 文件夹中保存历史版本
:: 自动备份 zip 到 releases 文件夹
echo [INFO] 正在备份 zip 到 releases\ 文件夹...
if not exist releases (
mkdir releases
)
copy "%ZIPNAME%" releases\ >nul


4.功能四：
自动给 ZIP 文件加上版本号 + 时间戳
for /f %%i in ('powershell -Command "Get-Date -Format yyyyMMdd_HHmm"') do set TIMESTAMP=%%i
set ZIPNAME=%OUTNAME%_%VERSION%_%TIMESTAMP%.zip

5.功能五：
version.txt 中的时间 和 zip 的时间戳保持一致
自动输入版本号（如 v1.1、v2.0）

:: 生成 version.txt，使用一致时间戳
echo [INFO] 生成 version.txt ...
powershell ^
"$v='版本号：%VERSION%';" ^
"$t='构建时间：%TIMESTAMP:~0,4%-%TIMESTAMP:~4,2%-%TIMESTAMP:~6,2% %TIMESTAMP:~9,2%:%TIMESTAMP:~11,2%';" ^
"$f='构建文件：%OUTNAME%.exe';" ^
"$lines=($v,$t,$f);" ^
"Set-Content -Path dist\\version.txt -Value $lines"

:: ========================
:: 配置变量
:: ========================

:: 用户输入版本号
set /p VERSION=请输入版本号（如 v1.1）：

set SCRIPT=mulFormatTolearning.py
set ICON=be.ico
set OUTNAME=mulFormatTolearning

:: 获取时间戳
for /f %%i in ('powershell -Command "Get-Date -Format yyyyMMdd_HHmm"') do set TIMESTAMP=%%i

:: 拼接 zip 文件名
set ZIPNAME=%OUTNAME%_%VERSION%_%TIMESTAMP%.zip




