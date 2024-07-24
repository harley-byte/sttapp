import os.path,subprocess
import wx,sys
from pathlib import Path
from panels import voiceSeparationPanel,videoToTextPanel
class BusyInfo(wx.Frame):
    def __init__(self, parent, message):
        wx.Frame.__init__(self, parent, style=wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.SIMPLE_BORDER)
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(panel, label=message)
        sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER, 15)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        self.Fit()
        self.CenterOnParent()




class AAFunctionPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 这里添加AA功能的UI组件
        self.label = wx.StaticText(self, label="尽情期待")
        sizer.Add(self.label, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(sizer)

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        if hasattr(sys, '_MEIPASS'):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).resolve().parent
        # 设置应用程序图标
        icon = wx.Icon(os.path.join(base_path,"icon.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # 创建Notebook
        self.notebook = wx.Notebook(self.panel)

        # 添加人声抽离面板
        self.voice_separation_panel = voiceSeparationPanel.VoiceSeparationPanel(self.notebook)
        self.notebook.AddPage(self.voice_separation_panel, "人声抽离")

        # 添加视频转文字面板
        self.video_to_text_panel = videoToTextPanel.VideoToTextPanel(self.notebook)
        self.notebook.AddPage(self.video_to_text_panel, "视频转文字")

        # 添加AA功能面板
        self.aa_function_panel = AAFunctionPanel(self.notebook)
        self.notebook.AddPage(self.aa_function_panel, "更多功能")

        main_sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        # 版权信息
        copyright_text = wx.StaticText(self.panel, label="© 2024 大碗网络科技. 版权所有.")
        main_sizer.Add(copyright_text, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizer(main_sizer)
        self.SetTitle("大碗百宝箱")
        self.SetSize((700, 600))

class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None)
        frame.Show(True)
        return True

if __name__ == '__main__':
    os.environ['NO_PROXY'] = '*'
    os.environ['no_proxy'] = '*'
    if "--test-ffmpeg" in sys.argv:
        ffmpeg_path = os.getenv('FFMPEG_PATH')
        try:
            result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True)
            print(f"ffmpeg version: {result.stdout}")
        except Exception as e:
            print(f"Error testing ffmpeg: {e}")
        sys.exit(0)
    app = MyApp(False)
    app.MainLoop()