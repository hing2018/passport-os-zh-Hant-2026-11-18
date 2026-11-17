口袋百寶箱・繁體中文版（Pocket Companion OS / passport-os）
=============================================================

這個資料夾裡有：

  passport-os-zh-Hant-2026-11-18.bin   完整韌體映像（4,175,808 bytes）
  flash-macos.command                  macOS：雙擊執行
  flash-windows.bat                    Windows：雙擊執行
  flash.py                             上面兩個腳本共用的燒錄程式
  README-flash.txt                     本說明

基底：passport-os 0.2.0-rc.59（上游 manchunx7-bit/passport-os）
介面：繁體中文（台灣用語）。語音指令、電台名、城市名比對仍用簡體，
      不影響操作。
雜湊：SHA-256 d6c753f4023696214c77633d301dd1f1c1c801ec4444717b652926e8a0e00257


一、最簡單的燒錄方式（雙擊）
----------------------------
1. 把整個資料夾解壓縮（不要只拉出 .bin）。
2. 用「可傳資料」的 USB 線把裝置接到電腦，並開機。
3. macOS：雙擊 flash-macos.command
   Windows：雙擊 flash-windows.bat
4. 腳本會自己驗證檔案、找序列埠、必要時安裝 esptool，然後開始燒錄。
   第一次執行若問「要安裝 esptool 嗎」，選 Y。
5. 看到「燒錄完成」後裝置會自動重開；腳本會列出可用的序列埠供你選擇。

macOS 第一次雙擊 .command 若被系統擋下，是 Gatekeeper 的正常行為：
  在檔案上按右鍵 →「打開」→ 再按「打開」。
也可以開 Terminal 執行：
  cd <這個資料夾>
  ./flash-macos.command

Windows 若被 SmartScreen 攔下，選「更多資訊」→「仍要執行」。


二、手動燒錄（不想用腳本時）
----------------------------
電腦需要有 Python 與 esptool：pip install esptool

  python -m esptool --chip esp32c3 -p <PORT> -b 460800 \
      --before default_reset --after hard_reset \
      write_flash --flash_mode dio --flash_size 8MB --flash_freq 80m \
      0x0 passport-os-zh-Hant-2026-11-18.bin

  macOS/Linux 序列埠長得像 /dev/cu.usbmodem1101
  Windows 序列埠長得像 COM5（看裝置管理員的「連接埠」）
  Windows 的命令換行請用 ^ 取代 \


三、硬體需求
------------
只適用 FoloToy AI Passport（ESP32-C3、8 MB Flash）。這是「完整映像」，
已包含 bootloader + 分區表 + 應用程式，從位址 0x0 一次寫入，不需要
其他檔案。


四、燒錄後會發生什麼
--------------------
* 裝置原有的 Wi-Fi 帳密與設定會被清除（映像覆蓋 NVS 分區），
  首次開機請依畫面指示重新配網。
* 裝置序號／出廠資料分區（0x410000 之後）不會被更動。
* 開機後標題與各 App 文字應為繁體（設定、電台、番茄鐘、天氣、小智…）。
  若仍是簡體，代表燒到舊映像，或寫入位址不是 0x0。


五、常見問題
------------
找不到序列埠
  * 換一條「可傳資料」的 USB 線（很多線只能充電）。
  * 拔插 USB、確認裝置已開機。
  * Windows 10/11 與 macOS 都不需要另外裝驅動（ESP32-C3 內建 USB）。

燒錄失敗／埠被佔用
  * 關掉任何序列埠監看軟體（Arduino IDE、idf.py monitor、PuTTY）再試。
  * macOS：系統設定 → 隱私權與安全性，允許 Terminal 存取。

檔案雜湊不符
  * 下載或解壓縮過程損壞，請重新取得整個資料夾。
  * 自行驗證：
      macOS  shasum -a 256 passport-os-zh-Hant-2026-11-18.bin
      Windows certutil -hashfile passport-os-zh-Hant-2026-11-18.bin SHA256
