#!/usr/bin/env python3
"""燒錄口袋百寶箱・繁體中文版到 FoloToy AI Passport（ESP32-C3 / 8 MB）。

由 flash-macos.command / flash-windows.bat 呼叫，也可以自己跑：

    python3 flash.py                 # 自動找序列埠並燒錄
    python3 flash.py --port COM5     # 指定序列埠
    python3 flash.py --verify-only   # 只驗證檔案，不燒錄
"""

import argparse
import hashlib
import pathlib
import sys

IMAGE = "passport-os-zh-Hant-2026-11-18.bin"
EXPECTED_SHA256 = "d6c753f4023696214c77633d301dd1f1c1c801ec4444717b652926e8a0e00257"

ESPTOOL_ARGS = [
    "--chip", "esp32c3",
    "-b", "460800",
    "--before", "default_reset",
    "--after", "hard_reset",
    "write_flash",
    "--flash_mode", "dio",
    "--flash_size", "8MB",
    "--flash_freq", "80m",
    "0x0", IMAGE,
]

PORT_HINTS = ("usbmodem", "usbserial", "wchusbserial", "SLAB_USBtoUART", "COM")


def sha256_of(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def available_ports() -> list[tuple[str, str]]:
    try:
        from serial.tools import list_ports
    except ImportError:
        return []
    return [(port.device, port.description or "") for port in list_ports.comports()]


def looks_like_board(device: str) -> bool:
    name = pathlib.PurePath(device).name
    return any(hint.lower() in name.lower() for hint in PORT_HINTS)


def choose_port(requested: str | None) -> str:
    if requested:
        return requested
    ports = available_ports()
    candidates = [device for device, _ in ports if looks_like_board(device)]
    if len(candidates) == 1:
        print("找到序列埠：%s" % candidates[0])
        return candidates[0]

    if ports:
        print("\n可用的序列埠：")
        for device, description in ports:
            print("  %-24s %s" % (device, description))
    else:
        print("\n找不到任何序列埠。")

    print(
        "\n請確認：\n"
        "  1. 裝置已用「可傳資料」的 USB 線接到電腦（不是只能充電的線）\n"
        "  2. 裝置已開機；沒反應的話拔插一次 USB\n"
        "  3. macOS 是 /dev/cu.usbmodemXXXX，Windows 是 COM3、COM5 這類名稱"
    )
    while True:
        answer = input("\n請輸入序列埠名稱（直接按 Enter 結束）：").strip()
        if not answer:
            raise SystemExit("已取消。")
        return answer


def main() -> int:
    parser = argparse.ArgumentParser(description="燒錄繁體中文版映像")
    parser.add_argument("--port", help="序列埠，例如 /dev/cu.usbmodem1101 或 COM5")
    parser.add_argument("--verify-only", action="store_true", help="只驗證檔案，不燒錄")
    args = parser.parse_args()

    here = pathlib.Path(__file__).resolve().parent
    image = here / IMAGE
    if not image.is_file():
        print("找不到 %s，請把整個資料夾解壓縮後再執行。" % IMAGE)
        return 1

    print("檢查檔案...")
    actual = sha256_of(image)
    if actual != EXPECTED_SHA256:
        print("檔案雜湊不符，可能在傳輸過程中損壞。")
        print("  預期：%s" % EXPECTED_SHA256)
        print("  實際：%s" % actual)
        print("請重新取得這個映像檔。")
        return 1
    print("檔案完整（%d bytes）" % image.stat().st_size)

    if args.verify_only:
        print("--verify-only：不燒錄。")
        return 0

    port = choose_port(args.port)
    print("\n開始燒錄到 %s，請不要拔線（約 15 秒）...\n" % port)

    command = [sys.executable, "-m", "esptool", "-p", port] + ESPTOOL_ARGS
    try:
        result = subprocess_run(command, cwd=here)
    except KeyboardInterrupt:
        print("\n已中斷。")
        return 1
    if result != 0:
        print(
            "\n燒錄失敗（esptool 結束碼 %d）。常見原因：\n"
            "  * 序列埠被其他程式佔用（關掉序列埠監看軟體再試）\n"
            "  * 選錯埠（回到上一步換一個）\n"
            "  * 線材只能充電\n"
            "  * macOS 權限：系統設定 → 隱私權與安全性，允許 Terminal 存取\n"
            % result
        )
        return 1

    print(
        "\n燒錄完成，裝置會自動重開。\n"
        "裝置原有的 Wi-Fi 與設定已被清除，請依畫面指示重新配網。\n"
        "開機後若標題是「設定 / 電台 / 番茄鐘」等繁體字，就代表成功。"
    )
    return 0


def subprocess_run(command: list[str], cwd: pathlib.Path) -> int:
    import subprocess

    return subprocess.call(command, cwd=str(cwd))


if __name__ == "__main__":
    raise SystemExit(main())
