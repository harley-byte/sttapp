import sys
import os
import platform
from cx_Freeze import setup, Executable

# 定义应用程序名称
APP_NAME = "DaWanBox"

# 定义版本号
VERSION = "0.1.0"

# 收集 demucs 相关文件和子模块
# 注意: cx_Freeze 没有直接等效于 collect_data_files 和 collect_submodules 的函数
# 您可能需要手动指定这些文件和模块

# 检查操作系统类型
is_windows = platform.system() == 'Windows'
base = "Win32GUI" if is_windows else None

# 设置图标
icon = "icon.ico" if is_windows else "Icon.icns"

# 设置 include_files
include_files = [icon, '.env.local']
if is_windows:
    ffmpeg_path = os.getenv('FFMPEG_PATH', '')
    if ffmpeg_path:
        ffmpeg_executable = os.path.join(ffmpeg_path, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_executable):
            include_files.append((ffmpeg_executable, 'ffmpeg.exe'))
        else:
            print(f"FFmpeg executable not found at {ffmpeg_executable}")
    else:
        print("FFMPEG_PATH environment variable not set")

# 设置构建选项
build_exe_options = {
    "packages": ["demucs", "torch", "torchaudio", "ffmpeg"],
    "excludes": [],
    "include_files": include_files,
    "include_msvcr": True,  # 包含 MSVCR DLL
}

# 设置 bdist_mac 选项 (仅适用于 macOS)
bdist_mac_options = {
    "bundle_name": APP_NAME,
    "iconfile": "Icon.icns",
    "custom_info_plist": "Info.plist",
}

# 创建 Executable
executables = [
    Executable(
        "main.py",
        base=base,
        target_name=APP_NAME,
        icon=icon,
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