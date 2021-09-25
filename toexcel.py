from win32com.client import Dispatch


def write_to_excel(data,unit):
    xlApp = Dispatch("Excel.Application")
    xlApp.Visible = 1
    xlApp.Workbooks.Add()
    
    xlApp.ActiveSheet.Cells(1,1).Value = 'Unit'
    xlApp.ActiveSheet.Cells(1,2).Value = unit
    
    xlApp.ActiveSheet.Cells(2,1).Value = 'No'
    xlApp.ActiveSheet.Cells(2,2).Value = "Value"
    i = 1
    
    for x in data:
        xlApp.ActiveSheet.Cells(i+2,1).Value = i
        xlApp.ActiveSheet.Cells(i+2,2).Value = x
        i += 1
    
    