import openpyxl
import pandas as pd
from Libraries.Framework.Paths import BasePaths


class PandasExcel:
    def __init__(self, pathDataFile, sheet_name):
        self.pathDataFile = pathDataFile
        self.sheet_name = sheet_name

    def getDataExcel(self):
        return pd.read_excel(self.pathDataFile, sheet_name=self.sheet_name)

    def getRowDataFile(self, df):
        return len(df.axes[0])

    def getRowByIndex(self, indexRowPath):
        result = dict()
        df = self.getDataExcel()
        rows = self.getRowDataFile(df)

        if indexRowPath > rows - 1:
            print('\nTong so dong dang co:  ', rows, ' | So dong can lay ra:  ', indexRowPath + 1)
        else:
            result["TypeOf"] = df['TypeOf'][indexRowPath]
            result["Label"] = df['Label'][indexRowPath]
            result["Value"] = df['Value'][indexRowPath]
        return result

    def getValByIndex1(self, indexRow, colName):
        return self.getRowByIndex(indexRow)[colName]

    def getValByIndex(self, indexRow, colName):
        """
        Lấy giá trị trong file Excel dựa trên chỉ số dòng và tên cột
        :param indexRow: chỉ số dòng (bắt đầu từ 1)
        :param colName: tên cột
        :return: giá trị ô tương ứng
        """
        workbook = openpyxl.load_workbook(self.pathDataFile)
        sheet = workbook[self.sheet_name]
        colIndex = None
        rowIndex = None
        for cell in sheet[1]:
            if cell.value == colName:
                colIndex = cell.column
                break
        if colIndex is None:
            raise ValueError(f"Không tìm thấy cột {colName}")
        for row in sheet.iter_rows(min_row=indexRow, max_row=indexRow):
            for cell in row:
                if cell.column == colIndex:
                    return cell.value
        raise ValueError(f"Không tìm thấy dòng {indexRow}")




if __name__ == "__main__":
    paths = BasePaths()
    print(paths.getPathToDatas())
    pathFile = paths.getPathToDatasByFileName('NDMS2_v2.0.xlsx')
    print('pathFileExcel: /Users/vuthanh/SourceGit/ndms2/Datas/NDMS2_v2.0.xlsx')
    print(pathFile)
    # pe = PandasExcel(pathFile, "TC01CreateWokerSucces")
    # print(pe.getDataExcel())
    # pathFile = 'D:\SourceGit\skedu-auto-ui\Web\Datas\AppConfig\LayerManager.xlsx'
    sheetName = 'F11US1CreateLayerSuccess'
    pe = PandasExcel(pathFile, sheetName)
    # print(pe.getDataExcel())
    # dataRow = pe.getRowByIndex(0)
    # print(dataRow["Value"])
    print(pe.getValByIndex(0, 'Value'))
    #
    # dataRowByIndex = pe.getRowByIndex(0)
    # print(dataRowByIndex)

    # dataExcel = pe.getDataExcel()
    # print(dataExcel)
