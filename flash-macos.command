#!/bin/bash
# 雙擊即可執行：驗證映像並燒錄到 FoloToy AI Passport。
cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
    echo
    echo "找不到 python3。"
    echo "macOS 需要「命令列工具」才內建 python3，現在幫你開啟安裝視窗..."
    echo "（安裝完成後，重新雙擊這個檔案即可）"
    xcode-select --install 2>/dev/null
    echo
    read -r -p "按 Enter 關閉視窗 "
    exit 1
fi

if ! python3 -c "import esptool" >/dev/null 2>&1; then
    echo
    echo "需要安裝燒錄工具 esptool（Python 套件，只裝一次）。"
    read -r -p "現在安裝嗎？[Y/n] " answer
    case "$answer" in
        n|N) echo "已取消。"; read -r -p "按 Enter 關閉視窗 "; exit 0 ;;
    esac
    python3 -m pip install --user --upgrade esptool || {
        echo
        echo "安裝失敗。請手動執行：python3 -m pip install --user esptool"
        read -r -p "按 Enter 關閉視窗 "
        exit 1
    }
fi

python3 flash.py "$@"
status=$?

echo
read -r -p "按 Enter 關閉視窗 "
exit $status
