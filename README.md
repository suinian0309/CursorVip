# ➤ CursorVIP

<div align="center">
<p align="center">
  <img src="./images/logo.png" alt="Cursor Pro Logo" width="200" style="border-radius: 6px;"/>
</p>

<p align="center">
  <a href="https://github.com/suinian0309/CursorVip/releases/latest">
<h4>Support Latest 0.47.x Version | 支持最新 0.47.x 版本</h4>

This is a tool to automatically register, support Windows and macOS systems, complete Auth verification, and reset
Cursor's configuration.

这是一个自动化工具，自动注册，支持 Windows 和 macOS 系统，完成 Auth 验证，重置 Cursor 的配置。

<p align="center">
  <img src="./images/new_2025-02-27_10-42-44.png" alt="new" width="400" style="border-radius: 6px;"/><br>
</p>

##### If you don't have Google Chrome, you can download it from [here](https://www.google.com/intl/en_pk/chrome/)

##### 如果没有 Google Chrome，可以从[这里](https://www.google.com/intl/en_pk/chrome/)下载

</div>

## 🔄 Change Log | 更新日志

[Watch Change Log | 查看更新日志](CHANGELOG.md)

## ✨ Features | 功能特点

* 🌟 Google OAuth Authentication with Lifetime Access<br>使用 Google OAuth 认证（终身访问）<br>

* ⭐ GitHub OAuth Authentication with Lifetime Access<br>使用 GitHub OAuth 认证（终身访问）<br>

* Automatically register Cursor membership<br>自动注册 Cursor 会员<br>

* Support Windows and macOS systems<br>支持 Windows 和 macOS 系统<br>

* Complete Auth verification<br>完成 Auth 验证<br>

* Reset Cursor's configuration<br>重置 Cursor 的配置<br>

* Multi-language support (English, 简体中文, 繁體中文, Vietnamese)<br>多语言支持（英文、简体中文、繁體中文、越南语）<br>

## 💻 System Support | 系统支持

| Windows |  x64  | ✅ | macOS |     Intel     | ✅ |
|:-------:|:-----:|:-:|:-----:|:-------------:|:-:|
| Windows |  x86  | ✅ | macOS | Apple Silicon | ✅ |
|  Linux  |  x64  | ✅ | Linux |      x86      | ✅ |
|  Linux  | ARM64 | ✅ | Linux |     ARM64     | ✅ |

## 👀 How to use | 如何使用

<details open>
<summary><b>⭐ Auto Run Script | 脚本自动化运行</b></summary>

**Linux/macOS**

```bash
curl -fsSL https://raw.githubusercontent.com/suinian0309/CursorVip/main/scripts/install.sh -o install.sh && chmod +x install.sh && ./install.sh
```

**Windows**

```powershell
irm https://raw.githubusercontent.com/suinian0309/CursorVip/main/scripts/install.ps1 | iex
```

</details>

<details>
<summary><b>⭐ Manual Reset Machine | 手动运行重置机器</b></summary>

**Linux/macOS**

```bash
curl -fsSL https://raw.githubusercontent.com/suinian0309/CursorVip/main/scripts/reset.sh | sudo bash
```

**Windows**

```powershell
irm https://raw.githubusercontent.com/suinian0309/CursorVip/main/scripts/reset.ps1 | iex
```

</details>

2. If you want to stop the script, please press Ctrl+C<br>要停止脚本，请按 Ctrl+C

## ❗ Note | 注意事项

📝 Config | 文件配置
`Win / Macos / Linux Path | 路径 [Documents/.cursor-free-vip/config.ini]`
<details>
<summary><b>⭐ Config | 文件配置</b></summary>

```
[Chrome]
# Default Google Chrome Path | 默认Google Chrome 浏览器路径
chromepath = C:\Program Files\Google/Chrome/Application/chrome.exe

[Turnstile]
# Handle Tuenstile Wait Time | 等待人机验证时间
handle_turnstile_time = 2
# Handle Tuenstile Wait Random Time (must merge 1-3 or 1,3) | 等待人机验证随机时间（必须是 1-3 或者 1,3 这样的组合）
handle_turnstile_random_time = 1-3

[OSPaths]
# Storage Path | 存储路径
storage_path = /Users/username/Library/Application Support/Cursor/User/globalStorage/storage.json
# SQLite Path | SQLite路径
sqlite_path = /Users/username/Library/Application Support/Cursor/User/globalStorage/state.vscdb
# Machine ID Path | 机器ID路径
machine_id_path = /Users/username/Library/Application Support/Cursor/machineId

[Timing]
# Min Random Time | 最小随机时间
min_random_time = 0.1
# Max Random Time | 最大随机时间
max_random_time = 0.8
# Page Load Wait | 页面加载等待时间
page_load_wait = 0.1-0.8
# Input Wait | 输入等待时间
input_wait = 0.3-0.8
# Submit Wait | 提交等待时间
submit_wait = 0.5-1.5
# Verification Code Input | 验证码输入等待时间
verification_code_input = 0.1-0.3
# Verification Success Wait | 验证成功等待时间
verification_success_wait = 2-3
# Verification Retry Wait | 验证重试等待时间
verification_retry_wait = 2-3
# Email Check Initial Wait | 邮件检查初始等待时间
email_check_initial_wait = 4-6
# Email Refresh Wait | 邮件刷新等待时间
email_refresh_wait = 2-4
# Settings Page Load Wait | 设置页面加载等待时间
settings_page_load_wait = 1-2
# Failed Retry Time | 失败重试时间
failed_retry_time = 0.5-1
# Retry Interval | 重试间隔
retry_interval = 8-12
# Max Timeout | 最大超时时间
max_timeout = 160
```

</details>

* Use administrator to run the script <br>请使用管理员身份运行脚本

* Confirm that Cursor is closed before running the script <br>请确保在运行脚本前已经关闭 Cursor<br>

* This tool is only for learning and research purposes <br>此工具仅供学习和研究使用<br>

* Please comply with the relevant software usage terms when using this tool <br>使用本工具请遵守相关软件使用条款

## 🚨 Common Issues | 常见问题

|                   如果遇到权限问题，请确保：                    |                   此脚本以管理员身份运行                    |
|:--------------------------------------------------:|:------------------------------------------------:|
| If you encounter permission issues, please ensure: | This script is run with administrator privileges |



## 📩 Disclaimer | 免责声明

本工具仅供学习和研究使用，使用本工具所产生的任何后果由使用者自行承担。 <br>

This tool is only for learning and research purposes, and any consequences arising from the use of this tool are borne
by the user.


## ⭐ Star History | 星星数

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=suinian0309/CursorVip&type=Date)](https://star-history.com/#suinian0309/CursorVip&Date)

</div>

## 📝 License | 授权

本项目采用 [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) 授权。
Please refer to the [LICENSE](LICENSE.md) file for details.
