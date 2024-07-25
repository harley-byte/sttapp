import sys
import os
import platform
from cx_Freeze import setup, Executable

# 定义应用程序名称和版本号
APP_NAME = "DaWanBox"
VERSION = "0.1.0"

# 检查操作系统类型
is_windows = platform.system() == 'Windows'
is_mac = platform.system() == 'Darwin'

# 设置基础
base = "Win32GUI" if is_windows else None

# 设置图标路径
icon_windows = os.path.abspath("icon.ico")
icon_mac = os.path.abspath("Icon.icns")

# 设置 include_files（两个平台通用的文件）
include_files = [
    ('.env.local', '.env.local'),
    ('Info.plist', 'Info.plist'),
    ('icon.ico','icon.ico'),
    ('Icon.icns','Icon.icns')
]

# 如果是 Windows，添加 icon.ico 到 include_files
if is_windows:
    include_files.append((icon_windows, 'icon.ico'))

# 添加 FFmpeg（如果环境变量设置了的话）
ffmpeg_path = os.getenv('FFMPEG_PATH', '')
if ffmpeg_path:
    ffmpeg_executable = os.path.join(ffmpeg_path, 'ffmpeg.exe' if is_windows else 'ffmpeg')
    if os.path.exists(ffmpeg_executable):
        include_files.append((ffmpeg_executable, 'ffmpeg.exe' if is_windows else 'ffmpeg'))
    else:
        print(f"FFmpeg executable not found at {ffmpeg_executable}")
else:
    print("FFMPEG_PATH environment variable not set")

# 设置构建选项
build_exe_options = {
    "packages": ["demucs", "torch", "torchaudio", "ffmpeg"],
    "excludes": [],
    "include_files": include_files,
    "include_msvcr": True,
}

# 设置 bdist_mac 选项 (仅适用于 macOS)
bdist_mac_options = {
    "bundle_name": APP_NAME,
    "iconfile": icon_mac,
    'include_resources':include_files,
    "custom_info_plist": "Info.plist",
}

# 创建 Executable
executables = [
    Executable(
        "main.py",
        base=base,
        target_name=APP_NAME,
        icon=icon_windows if is_windows else None,  # 只在 Windows 上设置 icon
    )
]

# 设置环境变量
os.environ['OSS_ACCESS_KEY'] = os.environ.get('OSS_ACCESS_KEY', '')
os.environ['OSS_SECRET_KEY'] = os.environ.get('OSS_SECRET_KEY', '')
os.environ['DASHSCOPE_AK'] = os.environ.get('DASHSCOPE_AK', '')

# 运行安装程序
setup(
    name=APP_NAME,
    version=VERSION,
    description="Da Wan Box Application",
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
    },
    executables=executables,
)