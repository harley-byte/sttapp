import wx
import wx.lib.scrolledpanel as scrolled
import  voice2txt,os,clyp
from datetime import datetime
import threading
class VideoToTextPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 文件选择框
        self.file_picker = wx.FilePickerCtrl(self, message="选择一个文件")
        sizer.Add(self.file_picker, 0, wx.ALL | wx.EXPAND, 5)

        # 上传按钮
        self.upload_button = wx.Button(self, label="上传")
        sizer.Add(self.upload_button, 0, wx.ALL | wx.CENTER, 5)
        self.upload_button.Bind(wx.EVT_BUTTON, self.on_upload)

        # 可滚动的文本框
        self.scroll_panel = scrolled.ScrolledPanel(self, size=(500, 400), style=wx.SIMPLE_BORDER)
        self.scroll_panel.SetupScrolling()
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(self.scroll_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        scroll_sizer.Add(self.text_ctrl, 1, wx.EXPAND)
        self.scroll_panel.SetSizer(scroll_sizer)

        sizer.Add(self.scroll_panel, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer)

    def on_upload(self, event):
        file_path = self.file_picker.GetPath()
        if file_path:
            # 显示处理中提示框
            self.busy = wx.BusyInfo("处理中，请稍候...")
            self.upload_button.Enable(False)
            self.file_picker.Disable()
            wx.Yield()  # 刷新UI

            # 开启新线程处理文件
            threading.Thread(target=self.process_file, args=(file_path,)).start()
        else:
            wx.MessageBox("请选择一个文件", "提示", wx.OK | wx.ICON_INFORMATION)

    def process_file(self, file_path):
        # 假设这是上传文件并获得响应内容的函数
        # 这里我们模拟一个较长的响应内容
        try:
            current_working_directory = os.getcwd()
            now = datetime.now()
            out_path = os.path.join(current_working_directory, now.strftime("%Y%m%d%H%M%S") + ".wav")
            clyp.splitaudio(file_path, out_path)
            outContent = voice2txt.voice_to_text(voice2txt.upload_file(out_path))
            response_content = "{}\n\n".format(outContent)

        except Exception as e:
            print(e)
            response_content = str(e)

        # 更新UI必须在主线程中进行
        wx.CallAfter(self.update_ui, response_content)

    def update_ui(self, response_content):
        self.busy = None  # 关闭处理中提示框
        self.upload_button.Enable(True)
        self.file_picker.Enable(True)
        self.text_ctrl.SetValue(response_content)
