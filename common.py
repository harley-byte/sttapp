import sys,os,platform
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            if is_windows():
                return os.path.join(os.path.dirname(sys.executable), relative_path)
            base_path = os.path.dirname(sys.executable)
            base_path = os.path.dirname(base_path)
            base_path = os.path.join(base_path,'Resources')

    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def is_windows():
    return sys.platform.startswith('win') or platform.system() == 'Windows'