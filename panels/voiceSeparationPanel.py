import wx
import wx.lib.scrolledpanel as scrolled
import clyp, os, time, spiltvoice, voice2txt
from datetime import datetime
import threading
class VoiceSeparationPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 文件选择框
        self.file_picker = wx.FilePickerCtrl(self, message="选择一个文件")
        sizer.Add(self.file_picker, 0, wx.ALL | wx.EXPAND, 5)

        # Flex布局
        flex_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 模型选择列
        model_sizer = wx.BoxSizer(wx.VERTICAL)
        model_sizer.Add(wx.StaticText(self, label="选择模型"), 0, wx.ALL | wx.CENTER, 5)
        self.model_radio_box = wx.RadioBox(self, choices=['htdemucs', 'htdemucs_ft', 'hdemucs_mmi','mdx'], style=wx.RA_SPECIFY_ROWS)
        model_sizer.Add(self.model_radio_box, 0, wx.ALL | wx.EXPAND, 5)
        flex_sizer.Add(model_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 分离方式列
        source_sizer = wx.BoxSizer(wx.VERTICAL)
        source_sizer.Add(wx.StaticText(self, label="选择分离方式"), 0, wx.ALL | wx.CENTER, 5)
        self.sources_radio_box = wx.RadioBox(self, choices=['vocals', 'drums', 'bass', 'other'], style=wx.RA_SPECIFY_ROWS)
        source_sizer.Add(self.sources_radio_box, 0, wx.ALL | wx.EXPAND, 5)
        flex_sizer.Add(source_sizer, 1, wx.ALL | wx.EXPAND, 5)

        # 将Flex布局添加到主布局
        sizer.Add(flex_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # 上传按钮
        self.upload_button = wx.Button(self, label="上传")
        sizer.Add(self.upload_button, 0, wx.ALL | wx.CENTER, 5)
        self.upload_button.Bind(wx.EVT_BUTTON, self.on_upload)

        # 文件列表
        self.file_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.file_list.InsertColumn(0, '输出文件', width=wx.LIST_AUTOSIZE_USEHEADER)
        sizer.Add(self.file_list, 1, wx.ALL | wx.EXPAND, 5)

        # 绑定双击事件
        self.file_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated)

        self.SetSizer(sizer)

    def on_upload(self, event):
        file_path = self.file_picker.GetPath()
        if file_path:
            # 显示处理中提示框
            self.busy = wx.BusyInfo("音频越长处理时间越长,初次处理需要下载模型，完成较慢。\n请稍候...")
            self.upload_button.Enable(False)
            self.file_picker.Disable()
            wx.Yield()  # 刷新UI

            # 开启新线程处理文件
            threading.Thread(target=self.process_file, args=(file_path,)).start()
        else:
            wx.MessageBox("请选择一个文件", "提示", wx.OK | wx.ICON_INFORMATION)

    def on_item_activated(self, event):
        item_index = event.GetIndex()
        file_path = self.file_list.GetItemText(item_index)
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            wx.MessageBox(f"文件不存在: {file_path}", "错误", wx.OK | wx.ICON_ERROR)

    def process_file(self, file_path):
        # 假设这是上传文件并获得响应内容的函数
        # 这里我们模拟一个较长的响应内容
        try:
            current_working_directory = os.getcwd()
            now = datetime.now()
            out_path = os.path.join(current_working_directory, now.strftime("%Y%m%d%H%M%S")+".wav")
            #clyp.splitaudio(file_path, out_path)
            selected_value = self.model_radio_box.GetStringSelection()
            source_value=self.sources_radio_box.GetStringSelection();
            spiltvoice.separate_audio(out_path, os.path.join(current_working_directory),selected_value, source_value)
            response_content = [os.path.join(current_working_directory, selected_value,"output",source_value+".wav")]

        except Exception as e:
            print(e)
            response_content = []

        # 更新UI必须在主线程中进行
        wx.CallAfter(self.update_ui, response_content)

    def update_ui(self, response_content):
        self.busy = None  # 关闭处理中提示框
        self.upload_button.Enable(True)
        self.file_picker.Enable(True)
        self.text_ctrl.SetValue(response_content)