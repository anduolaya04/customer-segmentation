import xlrd
import xlsxwriter


class DataIO:
    def __init__(self):
        pass

    def import_data(self, filename):
        data = []
        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)
        labels = sheet.row_values(0)
        data.append(labels)

        for row in range(1, sheet.nrows):
            cols = sheet.row_values(row)
            if cols[1]:
                data.append(cols)
        return data

    def export_data(self, data, path):
        writer_workbook = xlsxwriter.Workbook(path)
        writer_sheet = writer_workbook.add_worksheet()
        label_format = writer_workbook.add_format()
        labels = data[0]
        writer_sheet.write_row(0, 0, labels, label_format)
        for row in range(1, len(data)):
            cols = data[row]
            writer_sheet.write_row(row, 0, cols)
