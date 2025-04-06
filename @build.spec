# -*- mode: python ; coding: utf-8 -*-
import os
import platform
from dotenv import load_dotenv

# 加载环境变量获取版本号
load_dotenv()
version = os.getenv('VERSION', '1.8.07')  # 默认使用最新版本号

# 设置Windows特定输出名称
output_name = f"CursorVIP_{version}_windows"

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('turnstilePatch', 'turnstilePatch'),
        ('PBlock', 'PBlock'),
        ('locales', 'locales'),
        ('cursor_auth.py', '.'),
        ('reset_machine_manual.py', '.'),
        ('cursor_register_manual.py', '.'),
        ('quit_cursor.py', '.'),
        ('oauth_auth.py', '.'),
        ('utils.py', '.'),
        ('disable_auto_update.py', '.'),
        ('totally_reset_cursor.py', '.'),
        ('delete_cursor_google.py', '.'),
        ('bypass_version.py', '.'),
        ('.env', '.'),
        ('block_domain.txt', '.')
    ],
    hiddenimports=[
        'cursor_auth',
        'reset_machine_manual',
        'quit_cursor',
        'cursor_register_manual',
        'oauth_auth',
        'utils',
        'disable_auto_update',
        'totally_reset_cursor',
        'delete_cursor_google',
        'bypass_version',
        'webdriver_manager.chrome',
        'webdriver_manager.microsoft',
        'webdriver_manager.core',
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.common.keys',
        'selenium.webdriver.common.by',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',
        'DrissionPage'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

# Windows特定配置
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
    icon=None,  # 不使用图标
    version=None,  # 不使用版本信息文件
    uac_admin=True  # 请求管理员权限
)
