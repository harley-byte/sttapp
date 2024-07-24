import ffmpeg
import os
import sys
from pathlib import Path

def get_ffmpeg_path():
    ffmpeg_path="/opt/homebrew/bin/ffmpeg"
    if hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
        # 对于 Windows 和 macOS 分别处理 ffmpeg 路径
        if sys.platform == "win32":
            ffmpeg_path = os.path.join(base_path, 'ffmpeg','ffmpeg.exe')
        else:
            ffmpeg_path = base_path / 'ffmpeg' / 'ffmpeg'

    return str(ffmpeg_path)

def splitaudio(fpath, outpath):
    try:
        if Path(get_ffmpeg_path()).exists():
            ffmpeg.input(fpath).output(outpath, format='wav', acodec='pcm_s16le', ar=16000).run(cmd=get_ffmpeg_path())
        else:
            ffmpeg.input(fpath).output(outpath, format='wav', acodec='pcm_s16le', ar=16000).run()


    except ffmpeg.Error as e:
        print(e)
        raise e