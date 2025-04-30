setup enviroment:
pip install pyinstaller
pyinstaller --onefile --windowed --icon=be.ico FormatToLearning1.0.py

macOS 用 .sh 脚本（适用于打包 .app 或 CLI）
使用方法：
chmod +x build_mac.sh
./build_mac.sh

UPX 压缩它进一步减小体积（可选）
pip install upx
pyinstaller --onefile --windowed --icon=be.ico --upx-dir /path/to/upx FormatToLearning1.0.py


