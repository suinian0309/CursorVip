# ➤ Cursorvip

<div align="center">
<p align="center">
  <img src="./images/logo.png" alt="Cursor Pro Logo" width="200" style="border-radius: 6px;"/>
</p>

<p align="center">

[![Release](https://img.shields.io/github/v/release/suinian0309/cursorvip?style=flat-square&logo=github&color=blue)](https://github.com/suinian0309/cursorvip/releases/latest)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC_BY--NC--ND_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
[![Stars](https://img.shields.io/github/stars/suinian0309/cursorvip?style=flat-square&logo=github)](https://github.com/suinian0309/cursorvip/stargazers)
[![Download](https://img.shields.io/github/downloads/suinian0309/cursorvip/total?style=flat-square&logo=github&color=52c41a1)](https://github.com/suinian0309/cursorvip/releases/latest)

</p>
<h4>Support Latest 0.48.x Version | 支持最新 0.48.x 版本</h4>

This tool registers accounts with custom emails, support Google and GitHub account registrations, temporary GitHub account registration, kills all Cursor's running processes, resets and wipes Cursor data and hardware info.

Supports Windows, macOS and Linux.

For optimal performance, run with privileges and always stay up to date.

Always clean your browser's cache and cookies. If possible, use a VPN to create new accounts.


这是一个自动化工具，自动注册，支持 Windows 和 macOS 系统，完成 Auth 验证，重置 Cursor 的配置。

<p align="center">
  <img src="./images/pro_2025-04-05_18-47-56.png" alt="new" width="800" style="border-radius: 6px;"/><br>
</p>

##### If you don't have Google Chrome, you can download it from [here](https://www.google.com/intl/en_pk/chrome/)

##### 如果没有 Google Chrome，可以从[这里](https://www.google.com/intl/en_pk/chrome/)下载

</div>

## 🔄 Change Log | 更新日志

[Watch Change Log | 查看更新日志](CHANGELOG.md)

## ✨ Features | 功能特點

* 🌟 Google OAuth Authentication with Lifetime Access<br>使用 Google OAuth 认证（终身访问）<br>

* ⭐ GitHub OAuth Authentication with Lifetime Access<br>使用 GitHub OAuth 认证（终身访问）<br>

* Automatically register Cursor membership<br>自动注册 Cursor 会员<br>

* Support Windows and macOS systems<br>支持 Windows 和 macOS 系统<br>

* Complete Auth verification<br>完成 Auth 验证<br>

* Reset Cursor's configuration<br>重置 Cursor 的配置<br>

* Delete Cursor Google Account<br>删除 Cursor Google 账号<br>

* Multi-language support (English, 简体中文, 繁體中文, Vietnamese)<br>多语言支持（英文、简体中文、繁体中文、越南语）<br>

## 💻 System Support | 系統支持

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
curl -fsSL https://raw.githubusercontent.com/suinian0309/cursorvip/main/scripts/install.sh -o install.sh && chmod +x install.sh && ./install.sh
```

**Windows**

```powershell
irm https://raw.githubusercontent.com/suinian0309/cursorvip/main/scripts/install.ps1 | iex
```

</details>

<details>
<summary><b>⭐ Manual Reset Machine | 手动运行重置机器</b></summary>

**Linux/macOS**

```bash
curl -fsSL https://raw.githubusercontent.com/suinian0309/cursorvip/main/scripts/reset.sh | sudo bash
```

**Windows**

```powershell
irm https://raw.githubusercontent.com/suinian0309/cursorvip/main/scripts/reset.ps1 | iex
```

</details>

If you want to stop the script, please press Ctrl+C<br>要停止脚本，请按 Ctrl+C

## ❗ Note | 注意事項

📝 Config | 文件配置
`Win / Macos / Linux Path | 路径 [Documents/.Cursorvip/config.ini]`
<details>
<summary><b>⭐ Config | 文件配置</b></summary>

```
[Chrome]
# Default Google Chrome Path | 默认Google Chrome 浏览器路径
chromepath = C:\Program Files\Google/Chrome/Application/chrome.exe

[Turnstile]
# Handle Turnstile Wait Time | 等待人机验证时间
handle_turnstile_time = 2
# Handle Turnstile Wait Random Time (must merge 1-3 or 1,3) | 等待人机验证随机时间（必须是 1-3 或者 1,3 这样的组合）
handle_turnstile_random_time = 1-3

[OSPaths]
# Storage Path | 存储路径
storage_path = /Users/username/Library/Application Support/Cursor/User/globalStorage/storage.json
# SQLite Path | SQLite路径
sqlite_path = /Users/username/Library/Application Support/Cursor/User/globalStorage/state.vscdb
# Machine ID Path | 机器ID路径
machine_id_path = /Users/username/Library/Application Support/Cursor/machineId
# For Linux users: ~/.config/cursor/machineid

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

[Utils]
# Check Update | 检查更新
check_update = True
# Show Account Info | 显示账号信息
show_account_info = True
```

</details>

* Use administrator privileges to run the script <br>请使用管理员身份运行脚本

* Confirm that Cursor is closed before running the script <br>请确保在运行脚本前已经关闭 Cursor<br>

* This tool is only for learning and research purposes <br>此工具仅供学习和研究使用<br>

* Please comply with the relevant software usage terms when using this tool <br>使用本工具时请遵守相关软件使用条款

## 🚨 Common Issues | 常見問題

|                   如果遇到权限问题，请确保：                    |                   此脚本以管理员身份运行                    |
|:--------------------------------------------------:|:------------------------------------------------:|
| If you encounter permission issues, please ensure: | This script is run with administrator privileges |
| Error 'User is not authorized' | This means your account was banned for using temporary (disposal) mail. Ensure using a non-temporary mail service |


## 📩 Disclaimer | 免責聲明

本工具仅供学习和研究使用，使用本工具所产生的任何后果由使用者自行承担。 <br>

This tool is only for learning and research purposes, and any consequences arising from the use of this tool are borne
by the user.

## 💰 Buy Me a Coffee | 请我喝杯咖啡

<div align="center">
  <table>
    <tr>
      <td>
        <img src="./images/provi-code.jpg" alt="buy_me_a_coffee" width="280"/><br>
      </td>
  </table>
</div>

## ⭐ Star History | 星星数

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=suinian0309/cursorvip&type=Date)](https://star-history.com/#suinian0309/cursorvip&Date)

</div>
## 📝  | 致谢
本项目部分代码参考[此项目](https://github.com/suinian0309/suinian0309)，表示感谢

## 📝 License | 授權

本项目采用 [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) 授权。
Please refer to the [LICENSE](LICENSE.md) file for details.
