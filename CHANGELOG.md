# Change Log
## v1.8.00 ( Pre - Release 版本 )
1. Fix: Totally Reset Cursor | 修复完全重置 Cursor

## v1.7.10 ( Pre - Release 版本 )
1. Add: Totally Reset Cursor | 增加完全重置 Cursor
2. Add: Multi-language Support for Totally Reset | 增加完全重置多語言支持

## v1.7.09
1. Add: Development Version Check | 增加開發版本檢查
2. Remove: Github Trial Reset | 移除 Github 試用重置
3. Fixed: Some Issues | 修復一些問題

## v1.7.08
1. Add: Google OAuth Authentication | 增加 Google OAuth 認證
2. Add: GitHub OAuth Authentication | 增加 GitHub OAuth 認證
3. Add: Lifetime Access for OAuth Users | 增加 OAuth 用戶終身訪問權限
4. Add: OAuth Authentication Integration | 增加 OAuth 認證集成
5. Update: Menu System with OAuth Options | 更新菜單系統，添加 OAuth 選項
6. Add: Multi-language Support for OAuth | 增加 OAuth 多語言支持

## v1.7.07
1. Add: Vietnamese Language | 增加越南語言
2. Add: Admin Privilege Management for Windows Executable | 增加 Windows 可執行文件管理員權限
3. Implement admin privilege detection for Windows platform | 實現 Windows 平台管理員權限檢測
4. Add functions to check and request admin rights when running as a frozen executable | 增加檢查和請求管理員權限的功能
5. Enhance startup process with admin privilege verification | 增強啟動過程中的管理員權限驗證
6. Add new admin-related emoji to the EMOJI dictionary | 增加新的管理員相關表情符號到 EMOJI 字典
7. Provide fallback mechanism for non-Windows platforms (macos and linux ) | 提供非 Windows 平台（macos 和 linux）的回退機制
These changes make the application more user-friendly by only requesting admin privileges when necessary (when running as an executable). | 這些改進使應用程序更易於使用，只在必要時（當作為可執行文件運行時）請求管理員權限。

## v1.7.06
1. Add: Update Confirm | 增加更新確認
2. Add: Update Skipped | 增加更新跳過
3. Add: Invalid Choice | 增加無效選擇
4. Fix: Cursor Path | 修復 Cursor 路徑
5. Fix: Path Encoding | 修復路徑編碼
6. Fix: Getting Verification Code | 修復獲取驗證碼
7. Fix: Setting Password | 修復設置密碼
8. Fix: Disable Auto Update | 修復禁用自動更新
9. Add Config.py | 增加 Config.py
10. Add utils.py | 增加 utils.py
11. Rebuild some logic | 重新構建一些邏輯


## v1.7.05
1. Fix: Cursor Version Check | 修復 Cursor 版本檢查
2. Fix: Small Problem | 修復一些小問題


## v1.7.04
1. Hotfix: Small Problem | 修復一些小問題

## v1.7.03
1. Hotfix: Small Problem | 修復一些小問題

## v1.7.02
1. Fix: Cursor Path | 修復 Cursor 路徑
2. Add: Config File | 增加配置文件
3. Remove: Workbench Cursor Path | 移除 Workbench Cursor 路徑
4. Remove: Cursor Main JS | 移除 Cursor main.js

## v1.7.01
- Refactoring: Extract configuration-related code from the `setup_driver` function to an independent `setup_config` function
- Optimization: Improve code maintainability and make configuration management and browser settings more clear
- Improvement: The creation and update logic of the configuration file is clearer and more independent

## v1.6.03
1. Hotfix: Small Problem | 修復一些問題

## v1.6.02
1. Hotfix: Small Problem | 修復一些問題
2. Add: Test some Bypass Code | 測試一些繞過代碼

## v1.6.01
1. Fix: Cursor Auth | 修復 Cursor Auth
2. Add: Create Account Maximum Retry | 增加創建賬號最大重試次數
3. Fix: Cursor Auth Error | 修復 Cursor Auth 錯誤
4. Fix: Update Curl Faild | 修復更新 Curl 失敗

## v1.5.03
1. HOTFIX: Stuck on starting browser | 修復啟動瀏覽器卡住問題
2. Small Fix: Error Handling | 小修錯誤處理
3. Small Fix: Translation | 小修翻譯
4. Small Fix: Performance | 小修性能

## v1.5.02
1. Add: Generate Random Name Alias | 增加生成隨機真實姓名
2. Add: Realistic Name Input | 增加真實姓名輸入
3. Optimize: Error Handling | 優化錯誤處理
4. Optimize: Translation | 優化翻譯
5. Optimize: Performance | 優化性能

## v1.5.01
1. Add: Check Latest Version | 增加檢查最新版本
2. Add: Update Command | 增加更新命令

## v1.4.08
1. Add: Print Some Account Info | 增加打印一些賬號信息

## v1.4.07
1. Add Removed break statements after each operation | 修改結束 event 後的 break 暫停應用
2. Added print_menu() calls to show the menu again | 添加 print_menu（）調用以再次顯示菜單
3. Updated error handling to show menu instead of exiting | 更新錯誤處理以顯示菜單而不是退出

## v1.4.06

1. Add: Blocked Domains Loaded | 增加被屏蔽的域名加載
2. Fix: Cleanup Error | 修復清理進程時出錯
3. Fix: Blocked Domains Loaded Error | 修復被屏蔽的域名加載錯誤
4. Fix: Available Domains Loaded Error | 修復可用域名加載錯誤
5. Fix: Domains Filtered Error | 修復過濾後剩餘域名錯誤
6. Fix: Domains Excluded Error | 修復排除域名錯誤


## v1.4.05

1. Fix: macOS Language Detection | 修復 macOS 語言檢測


## v1.4.04

1. Change Some Language Info to English | 更改一些語言信息為英文
2. Add Auto Detect System Language | 增加自動檢測系統語言
3. Fixed Some Issues | 修復一些問題


## v1.4.03

1. Switch to API-based Registration System | 改用 API 註冊系統替代瀏覽器操作
2. Add Support for Latest Cursor Version | 增加支持最新版本 Cursor
3. Enhance Translation System | 優化多語言翻譯系統
4. Add Database Connection Status Messages | 增加數據庫連接狀態提示
5. Improve Error Handling for Database Operations | 改進數據庫操作的錯誤處理
6. Add New API Integration | 新增 API 集成
7. Optimize Performance and Stability | 優化性能和穩定性

## v1.4.01

1. Add Disable Cursor Auto Upgrade | 增加禁用 Cursor 自動升級

## v1.3.02

1. Add Buy Me a Coffee | 增加請我喝杯咖啡
2. Add PayPal | 增加 PayPal
3. Very Small Fix | 非常小的修復
4. Fix main.py option number | 修復 main.py 選項數量

## v1.3.01

1. Add Manual Email Input | 增加手動輸入郵箱地址
2. Add Manual Code Input | 增加手動輸入驗證碼
3. Fix Cursor Options | 修復 Cursor 選項


## v1.2.02

1. Add PBlock | 增加 PBlock
2. Remove uBlock0.chromium | 移除 uBlock0.chromium
3. Optimize the logic of the script | 優化腳本邏輯
4. Optimize Size | 優化大小


## v1.2.01

1. Fix Cursor Cloudflare Human Verification Problem | 修復 Cursor Cloudflare 人機驗證問題
2. Change to automatic registration account | 全面改為自動註冊賬號
3. Change Mail Site | 改變郵箱網站
4. Fix Cursor Cloudflare Problem | 修復 Cursor Cloudflare 問題


## v1.1.01

<p align="center">
  <img src="./images/cloudflare_2025-02-12_13-43-21.png" alt="free" width="400"/><br>
</p>

1. Hot Fix Cursor Cloudflare Problem | 修復 Cursor Cloudflare 問題
2. Fix Cursor Cloudflare Human Verification Problem | 修復 Cursor Cloudflare 人機驗證問題
3. Remake signup logic | 重做註冊邏輯


## v1.0.10

1. Hot Fix Mac Chrome Problem | 修復 Mac Chrome 問題
2. Fix Linux Start Donet Problem | 修復 Linux 啟動開發者問題


## v1.0.9

<p align="center">
  <img src="./images/cloudflare_2025-02-12_13-43-21.png" alt="free" width="400"/><br>
</p>

1. Fixed New 0.45.x Version Reset Machine | 修復新 0.45 版本重置機器
2. Fix Locale Language | 修復多語言
3. Add Support Crypto Machine Regedit | 增加支持加密機器註冊
4. Add Remake main.js | 重做 main.js


## v1.0.8

1. Fix New 0.45 Version Reset Machine | 修復新 0.45 版本重置機器
2. Fix Locale Language | 修復多語言
3. Add Support Crypto Machine Regedit | 增加支持加密機器註冊


## v1.0.7 - HotFix

1. Fix Reset Machine | 修復重置機器
2. Fix Locale Language | 修復多語言


## v1.0.7

1. Add Locale Language Support | 增加多語言支持
<p align="center">
  <img src="./images/locale_2025-01-15_13-40-08.png" alt="locale" width="400"/><br>
</p>


## v1.0.6

1. Add Quit Cursor Option | 增加退出 Cursor 選項
2. Add Recaptcha Path Patch | 增加 Recaptcha 路徑修復
3. Fix Admin Permission | 修復管理員權限問題
4. Remove all need admin permission | 移除所有需要管理員權限


## v1.0.5 - HotFix

1. Fix: Mac Browser Control | 修復 Mac 瀏覽器控制問題
2. Fix: Verification Code Cant Patch | 修復驗證碼無法修復問題
3. Add Linux Support | 增加 Linux 支持
<p align="center">
  <img src="./images/fix_2025-01-14_21-30-43.png" alt="fix" width="400"/><br>
</p>


## v1.0.5

1. Remove MachineID | 移除機器碼 ID
2. Change to automatic registration account | 全面改為自動註冊賬號
3. Use your own exclusive new account | 使用自己獨享的新賬號
4. Fully automatic reset machine configuration | 全面自動化重置機器配置
<p align="center">
  <img src="./images/pro_2025-01-14_14-40-37.png" alt="Why" width="400"/><br>
</p>


## v1.0.4

1. Fix: Cursor's configuration | 修復 Cursor 的配置問題
2. Fix Cloud Lame | 修復雲端慢速模式


## v1.0.3

1. Fix: Cursor's configuration | 修復 Cursor 的配置問題
2. Add Manual Reset Machine | 增加手動重置機器
3. Add CDN Cloud Control WatchDog | 增加 CDN 雲端控制 WatchDog
4. Add Mac OS Support | 增加 Mac OS 支持
5. 759 ++ People use , but star only a few | 759 ++人使用，但只有幾個人點贊
<p align="center">
  <img src="./images/what_2025-01-13_13-32-54.png" alt="Why" width="400"/><br>
</p>


## v1.0.2
  
1. Fix: Some known issues | 修復了一些已知問題
2. Add cloud control device code | 增加雲端控制設備碼
3. Cloud reset device code | 雲端重置設備碼
4. Remove official WatchDog monitoring | 移除官方 WatchDog 監控
5. Remove Proxy official prompt | 移除 Proxy 官方提示
6. Fix: Too Many Computer | 修復 Too Many Computer 問題
7. Fix Billing Issue | 修復計費問題
8. Fix: Cursor's configuration | 修復 Cursor 的配置問題
9. Fix cursor-slow mode | 修復 cursor-slow 模式


## v1.0.1

1. Fix: Reset machine ID | 修復了重置機器 ID 的問題
2. Fix: Bypass membership check | 修復了 繞過會員檢查的問題
3. Fix: Auto upgrade to "pro" membership | 修復了 自動升級為 pro 會員的問題
4. Fix: Real-time send Token request | 修復了 實時發送 Token 請求的問題
5. Fix: Reset Cursor's configuration | 修復了 重置 Cursor 的配置的問題



## v1.0
1. Preview Image | 預覽圖<br>
<p align="center">
  <img src="./images/pro_2025-01-11_00-50-40.png" alt="Cursor Pro Logo" width="400"/><br>
</p>
<p align="center">
  <img src="./images/pro_2025-01-11_00-51-07.png" alt="Cursor Pro Logo" width="400"/><br>
</p>
2. Add usage period,but can be contacted by leaving MachineID | 不得已才添加，但可以通過留下 MachineID 聯繫作者
<br>

<p align="center">
  <img src="./images/pro_2025-01-11_16-24-03.png" alt="Cursor Pro Logo" width="400"/><br>
</p>
