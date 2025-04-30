setup enviroment:
pip install pyinstaller
pyinstaller --onefile --windowed --icon=be.ico FormatToLearning1.0.py

macOS 用 .sh 脚本（适用于打包 .app 或 CLI）
使用方法：
chmod +x build_mac.sh
./build_mac.sh

UPX 压缩它进一步减小体积（可选）
pip install upx
pyinstaller --onefile --windowed --icon=be.ico --upx-dir /path/to/upx FormatToLearning.py


自动生成 version.txt
版本号：v1.0
构建时间：2025-04-30 20:17
构建文件：FormatToLearning.exe

打包完成后自动将 ZIP 文件备份到 releases/ 文件夹中保存历史版本

自动给 ZIP 文件加上版本号 + 时间戳
for /f %%i in ('powershell -Command "Get-Date -Format yyyyMMdd_HHmm"') do set TIMESTAMP=%%i
set ZIPNAME=%OUTNAME%_%VERSION%_%TIMESTAMP%.zip
