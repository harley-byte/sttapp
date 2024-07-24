# cicd.spec
# -*- mode: python ; coding: utf-8 -*-

import os
import sys,platform
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None
# 收集 demucs 相关文件和子模块
demucs_datas = collect_data_files('demucs')
demucs_hiddenimports = collect_submodules('demucs')
# 检查操作系统类型
bb = []
is_windows = platform.system() == 'Windows'
if is_windows:
    ffmpeg_path = os.getenv('FFMPEG_PATH', '')
    if ffmpeg_path:
        ffmpeg_executable = os.path.join(ffmpeg_path, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_executable):
            bb = [(ffmpeg_executable, 'ffmpeg')]
        else:
            print(f"FFmpeg executable not found at {ffmpeg_executable}")
    else:
        print("FFMPEG_PATH environment variable not set")


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=bb,
    datas=[('icon.ico', '.'), ('Icon.icns', '.')] + demucs_datas,
    hiddenimports=demucs_hiddenimports + ['torch', 'torchaudio','ffmpeg'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
     # 在这里添加环境变量
    environ={
        'OSS_ACCESS_KEY': os.environ.get('OSS_ACCESS_KEY', ''),
        'OSS_SECRET_KEY': os.environ.get('OSS_SECRET_KEY', ''),
        'DASHSCOPE_AK': os.environ.get('DASHSCOPE_AK', ''),
    }
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)

#app = BUNDLE(
#    coll,
#    name='dawanbox.app',
#    icon='Icon.icns',  # Set the icon for the macOS app
#    bundle_identifier='com.dawannettech.com',
#    info_plist={
#        'CFBundleName': 'Da Wan Box',
#        'CFBundleDisplayName': 'Da Wan Box',
#        'CFBundleVersion': '0.1.0',
#        'CFBundleShortVersionString': '0.1.0',
#        'CFBundleIconFile': 'Icon.icns',
#    },
#)