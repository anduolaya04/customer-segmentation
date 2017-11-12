import wx
import wx.grid as grid
import matplotlib.pyplot as plt
from segmentation import classify
from data_io import DataIO


########################################################################
class MainForm(wx.Frame):
    # ----------------------------------------------------------------------
    def __init__(self):
        self.data_io = DataIO()
        self.input = None
        self.content_data = None
        self.execute_data, self.prior_1, self.prior_2, self.leave = None, None, None, None
        wx.Frame.__init__(self, None, wx.ID_ANY, "Customer Segmentation", size=(800, 640))

        self.panel = wx.Panel(self, wx.ID_ANY)
        status = self.CreateStatusBar()

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        file_label = wx.StaticText(self.panel, -1, "Input:", (30, 20))
        self.InputPathTextBox = wx.TextCtrl(self.panel, -1, "", size=(200, -1), pos=(100, 21))
        self.browse_btn = wx.Button(self.panel, -1, "Browse", pos=(310, 20))
        self.Bind(wx.EVT_BUTTON, self.onOpenFile, self.browse_btn)

        # output_label = wx.StaticText(self.panel, -1, "Ket qua:", (30, 50))
        # self.OutputPathTextBox = wx.TextCtrl(self.panel, -1, "", size=(200, -1), pos=(100, 47))

        self.execute_btn = wx.Button(self.panel, -1, "Phân tích", pos=(400, 20))
        self.Bind(wx.EVT_BUTTON, self.onExecute, self.execute_btn)
        self.execute_btn.Disable()

        inform_label = wx.StaticText(self.panel, -1, "Tổng quát:", (30, 60))
        self.inform_txt = wx.TextCtrl(self.panel, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY,
                                      size=(463, 70), pos=(100, 60))

        self.prior1_btn = wx.Button(self.panel, -1, "Nhóm Ưu tiên 1", pos=(98, 140))
        self.Bind(wx.EVT_BUTTON, self.onOpenPrior1, self.prior1_btn)
        self.prior1_btn.Disable()

        self.prior2_btn = wx.Button(self.panel, -1, "Nhóm Ưu tiên 2", pos=(210, 140))
        self.Bind(wx.EVT_BUTTON, self.onOpenPrior2, self.prior2_btn)
        self.prior2_btn.Disable()

        self.leave_btn = wx.Button(self.panel, -1, "Dự đoán rời mạng", pos=(320, 140))
        self.Bind(wx.EVT_BUTTON, self.onOpenLeave, self.leave_btn)
        self.leave_btn.Disable()

        self.total_btn = wx.Button(self.panel, -1, "Toàn bộ các nhóm", pos=(443, 140))
        self.Bind(wx.EVT_BUTTON, self.onOpenTotal, self.total_btn)
        self.total_btn.Disable()

        self.chart_btn = wx.Button(self.panel, -1, "Biểu đồ", pos=(580, 140))
        self.Bind(wx.EVT_BUTTON, self.onOpenChart, self.chart_btn)
        self.chart_btn.Disable()

        self.save_btn = wx.Button(self.panel, -1, "Export", pos=(680, 140))
        self.Bind(wx.EVT_BUTTON, self.onSaveFile, self.save_btn)
        self.save_btn.Disable()

        self.data_grid = grid.Grid(self.panel, size=(780, 400), pos=(5, 180))
        self.data_grid.CreateGrid(20, 10)

        self.panel.SetSizer(self.sizer)

    def onOpenFile(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir='../data/',
            defaultFile="",
            wildcard="Excel files (*.xlsx, *.xls)|*.xlsx; *.xls",
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()
            # print("You chose the following file:", path)
            self.InputPathTextBox.ChangeValue(path[0])
            self.input = path[0]
            data = self.data_io.import_data(path[0])
            self.content_data = self.fill_grid_data(data)
            self.execute_btn.Enable()
            self.prior1_btn.Disable()
            self.prior2_btn.Disable()
            self.leave_btn.Disable()
            self.total_btn.Disable()
            self.chart_btn.Disable()
            self.save_btn.Disable()
            self.inform_txt.ChangeValue('')
        dlg.Destroy()

    def onOpenPrior1(self, event):
        self.fill_grid_data(self.prior_1)

    def onOpenPrior2(self, event):
        self.fill_grid_data(self.prior_2)

    def onOpenLeave(self, event):
        self.fill_grid_data(self.leave)

    def onOpenTotal(self, event):
        self.fill_grid_data(self.execute_data)

    def onSaveFile(self, event):
        dlg = wx.FileDialog(
            self, message="Save as",
            defaultDir='../data/',
            defaultFile="",
            wildcard="Excel files (*.xlsx, *.xls)|*.xlsx; *.xls",
            style=wx.FD_SAVE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()[0]
            self.data_io.export_data(self.execute_data, path)
            # print("You chose the following file:", self.path)
        dlg.Destroy()

    def onExecute(self, event):
        if not self.content_data:
            msg = "You have an error.\nPlease reopen data file"
            self.show_error_dialog(msg, "ERROR", wx.OK | wx.ICON_EXCLAMATION)
        else:

            executed_data, prior_1, prior_2, leave = classify(self.content_data)
            self.execute_data = executed_data
            self.fill_grid_data(self.execute_data)
            self.prior_1 = prior_1
            self.prior_2 = prior_2
            self.leave = leave

            nums = len(self.content_data) - 1
            summary = 'Tổng số thuê bao: {}\n'.format(len(self.content_data) - 1)
            rate = 100 * (len(self.prior_1) - 1) / nums
            summary += 'Số thuê bao ưu tiên 1: {0} ({1:.2f}%)\n'.format(len(self.prior_1) - 1, round(rate, 2))
            rate = 100 * (len(self.prior_2) - 1) / nums
            summary += 'Số thuê bao ưu tiên 2: {0} ({1:.2f}%)\n'.format(len(self.prior_2) - 1, round(rate, 2))
            rate = 100 * (len(self.prior_1) - 1) / nums
            summary += 'Số thuê bao dự đoán rời mạng: {0} ({1:.2f}%)'.format(len(self.leave) - 1, round(rate, 2))
            self.inform_txt.ChangeValue(summary)
            self.prior1_btn.Enable()
            self.prior2_btn.Enable()
            self.leave_btn.Enable()
            self.total_btn.Enable()
            self.save_btn.Enable()
            self.chart_btn.Enable()
            # else:
            #     msg = "Something error. Please try again."
            #     self.show_error_dialog(msg, "ERROR", wx.OK | wx.ICON_EXCLAMATION)

    def onOpenChart(self, event):
        self.draw()

    def show_error_dialog(self, msg, title, style):
        dlg = wx.MessageDialog(parent=None, message=msg,
                               caption=title, style=style)
        dlg.ShowModal()
        dlg.Destroy()

    def fill_grid_data(self, data):
        # print(data[11])
        current_nrows, new_nrows = (self.data_grid.GetNumberRows(), len(data))
        if current_nrows < new_nrows:
            self.data_grid.AppendRows(new_nrows - current_nrows)
        elif current_nrows > new_nrows:
            self.data_grid.DeleteRows(new_nrows, current_nrows - new_nrows)
        current_ncols, new_ncols = (self.data_grid.GetNumberCols(), len(data[0]))
        if current_ncols < new_ncols:
            self.data_grid.AppendCols(new_ncols - current_ncols)
        elif current_ncols > new_ncols:
            self.data_grid.DeleteCols(new_ncols, current_ncols - new_ncols)

        for i in range(new_ncols):
            self.data_grid.SetCellValue(0, i, str(data[0][i]))

        for row in range(1, new_nrows):
            for col in range(new_ncols):
                self.data_grid.SetCellValue(row, col, str(data[row][col]))
        return data

    def draw(self):
        labels = ['Nhóm Ưu tiên 1', 'Nhóm Ưu tiên 2', 'Dự đoán rời mạng']
        sizes = [len(self.prior_1) - 1, len(self.prior_2) - 1, len(self.leave) - 1]
        explode = (0, 0, 0.1)

        fig, ax = plt.subplots()
        fig.canvas.set_window_title('Biểu đồ')
        plt.title('Tỉ lệ các nhóm thuê bao')
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')

        plt.tight_layout()
        plt.show()


# ----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainForm().Show()
    app.MainLoop()
