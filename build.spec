# -*- mode: python ; coding: utf-8 -*-
import os
import platform
from dotenv import load_dotenv

# 加載環境變量獲取版本號
load_dotenv()
version = os.getenv('VERSION', '1.0.0')

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
        ('cursor_auth.py', '.'),
        ('reset_machine_manual.py', '.'),
        ('cursor_register.py', '.'),
        ('new_signup.py', '.'),
        ('new_tempemail.py', '.'),
        ('quit_cursor.py', '.'),
        ('cursor_register_manual.py', '.'),
        ('oauth_auth.py', '.'),
        ('utils.py', '.'),
        ('.env', '.'),
        ('block_domain.txt', '.')
    ],
    hiddenimports=[
        'cursor_auth',
        'reset_machine_manual',
        'new_signup',
        'new_tempemail',
        'quit_cursor',
        'cursor_register_manual',
        'oauth_auth',
        'utils'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

target_arch = os.environ.get('TARGET_ARCH', None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=output_name,  # 使用动态生成的名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=True,  # 对非Mac平台无影响
    target_arch=target_arch,  # 仅在需要时通过环境变量指定
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)