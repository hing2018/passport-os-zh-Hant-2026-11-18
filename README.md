# 口袋百寶箱・繁體中文版（passport-os zh-Hant）

FoloToy AI Passport（ESP32-C3 / 8 MB Flash）用的 **繁體中文** 韌體。
以 [manchunx7-bit/passport-os](https://github.com/manchunx7-bit/passport-os) `0.2.0-rc.59` 為基底，
介面文字轉為繁體中文（台灣用語），UI 結構、功能、資料完全沿用上游。

只改「顯示」：語音命令、電台名、城市名的比對仍用簡體，操作不受影響。

---

## 下載

| 檔案 | 說明 |
| --- | --- |
| [`passport-os-zh-Hant-2026-11-18.zip`](https://github.com/hing2018/passport-os-zh-Hant-2026-11-18/raw/main/passport-os-zh-Hant-2026-11-18.zip) | **建議用這個**：映像 + 燒錄腳本 + 說明，解壓即用 |
| `passport-os-zh-Hant-2026-11-18.bin` | 完整映像（4,175,808 bytes，從 0x0 寫入） |

映像 SHA-256：

```
d6c753f4023696214c77633d301dd1f1c1c801ec4444717b652926e8a0e00257
```

zip SHA-256：

```
04637fc9901bc3685fe8784bfc33d5caac4ac41800bc3dbedffdb0cce098f777
```

## 燒錄（最簡單）

1. 解壓縮 zip，得到一個資料夾（**不要只拉出 .bin**）。
2. 用「可傳資料」的 USB 線把裝置接到電腦，並開機。
3. **macOS**：雙擊 `flash-macos.command`
   （第一次被 Gatekeeper 擋下 → 在檔案上按右鍵 →「打開」）
   **Windows**：雙擊 `flash-windows.bat`
   （SmartScreen →「更多資訊」→「仍要執行」）
4. 腳本會驗證雜湊、自動找序列埠、必要時安裝 esptool，然後燒錄（約 15 秒）。

手動燒錄與常見問題請看 [`README-flash.txt`](README-flash.txt)。

## 燒錄後會發生什麼

- **原有 Wi-Fi 帳密與設定會被清除**（映像覆蓋 NVS 分區），首次開機需依畫面重新配網。
- 裝置序號／出廠資料分區（0x410000 之後）不會被更動。
- 開機後標題應為「設定 / 電台 / 番茄鐘 / 天氣 / 小智」等繁體字。

## 硬體需求

只適用 FoloToy AI Passport（ESP32-C3、8 MB Flash）。這是完整映像，
已包含 bootloader + 分區表 + 應用程式，不需其他檔案。

## 已知限制

- 伺服器即時回傳的長句只套用單字對照表，少數詞彙型台灣用語（如「軟件→軟體」）可能不轉。
- 字集外的罕用字會退回 16 px 字型或顯示方塊。
- 語音、藍牙配網、各 App 的深度流程未逐一實測。

## 授權

上游 passport-os 為 MIT License（Copyright (c) 2026 FoloToy），本衍生版本沿用同一授權，
詳見 [`LICENSE`](LICENSE)。本專案與 FoloToy 官方無隸屬關係。
