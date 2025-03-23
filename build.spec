# -*- mode: python ; coding: utf-8 -*-
import os
import platform
from dotenv import load_dotenv

# 加载环境变量获取版本号
load_dotenv()
version = os.getenv('VERSION', '1.8.05')  # 更新默认版本号

# 根据系统类型设置输出名称
system = platform.system().lower()
if system == "windows":
    os_type = "windows"
elif system == "linux":
    os_type = "linux"
else:  # Darwin
    os_type = "mac"

output_name = f"CursorVIP_{version}_{os_type}"

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('turnstilePatch', 'turnstilePatch'),
        ('PBlock', 'PBlock'),
        ('locales', 'locales'),
        ('images', 'images'),
        ('cursor_auth.py', '.'),
        ('reset_machine_manual.py', '.'),
        ('cursor_register.py', '.'),
        ('new_signup.py', '.'),
        ('new_tempemail.py', '.'),
        ('quit_cursor.py', '.'),
        ('cursor_register_manual.py', '.'),
        ('cursor_register_google.py', '.'),
        ('cursor_register_github.py', '.'),
        ('or_register_manual.py', '.'),
        ('delete_account.py', '.'),
        ('cursor_delete_account.py', '.'),
        ('totally_reset_cursor.py', '.'),
        ('disable_auto_update.py', '.'),
        ('show_wechat_group.py', '.'),
        ('utils.py', '.'),
        ('config.py', '.'),
        ('.env', '.')
    ],
    hiddenimports=[
        'cursor_auth',
        'reset_machine_manual',
        'new_signup',
        'new_tempemail',
        'quit_cursor',
        'cursor_register_manual',
        'cursor_register_google',
        'cursor_register_github',
        'or_register_manual',
        'delete_account',
        'cursor_delete_account',
        'totally_reset_cursor',
        'disable_auto_update',
        'show_wechat_group',
        'utils',
        'config',
        'DrissionPage',
        'colorama',
        'dotenv',
        'requests',
        'selenium',
        'webdriver_manager',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=output_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,  # Windows不需要argv模拟
    target_arch=None,  # 使用默认架构
    codesign_identity=None,
    entitlements_file=None,
    version='file_version_info.txt',  # 添加版本信息
    uac_admin=True,  # 请求管理员权限
)