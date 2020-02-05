from tkinter.filedialog import*
from buildGraph import*

# GUI parameters
GUI_MAIN_SCREEN_WIDTH = 400
GUI_MAIN_SCREEN_HEIGHT = 600
GUI_WINDOW_TITLE = "Менеджер графиков bqStudio"
# Global vars
global fileContent


def GUI_ButtonHandler():
    global fileContent
    graph.DrawFinalGraph(fileContent)

def GUI_OpenFile():
    global fileContent
    fileName = askopenfilename(parent=mainWindow, filetypes=[("TI bqStudio logs", "*.log")])
    if fileName != "":
        graph.graphWindowsNum = graph.graphWindowsNum + 1
        if fileName.split('/')[-1].split('.')[-1] == "log":
            fileObject = open(fileName, "r")
            fileContent = fileObject.readlines()
            # Configuring hidden components to make them visible
            canvas.itemconfig(textFileName, text="Выбранный файл - " + fileName.split('/')[-1])
            canvas.itemconfig(buttonBuildGraph, window=Button(canvas, text="Построить графики", bg="lightyellow", fg="black", font="TimesNewRoman 12", command=GUI_ButtonHandler))
            canvas.itemconfig(checkboxCellVoltages, window=Checkbutton(text="Напряжения ячеек. Число ячеек", variable=graph.buildCellVolt, font="TimesNewRoman 12", bg="lightblue", selectcolor="lightyellow"))
            canvas.itemconfig(checkboxCurrent, window=Checkbutton(text="Ток", variable=graph.buildCurrent, font="TimesNewRoman 12", bg="lightblue", selectcolor="lightyellow"))
            canvas.itemconfig(checkboxVoltage, window=Checkbutton(text="Напряжение батареи", variable=graph.buildVoltage, font="TimesNewRoman 12", bg="lightblue", selectcolor="lightyellow"))
            canvas.itemconfig(checkboxCovThreshold, window=Checkbutton(text="порог COV", variable=graph.buildCovThreshold, font="TimesNewRoman 12", bg="lightblue", selectcolor="lightyellow"))
            canvas.itemconfig(checkboxCuvThreshold, window=Checkbutton(text="порог CUV", variable=graph.buildCuvThreshold, font="TimesNewRoman 12", bg="lightblue", selectcolor="lightyellow"))
            canvas.itemconfig(checkboxChargeVoltageThreshold, window=Checkbutton(text="верхний порог напряжения батареи", variable=graph.buildChargeVoltageThreshold, font="TimesNewRoman 12", bg="lightblue", selectcolor="lightyellow"))
            canvas.itemconfig(checkboxDischargeVoltageThreshold, window=Checkbutton(text="нижний порог напряжения батареи", variable=graph.buildDischargeVoltageThreshold, font="TimesNewRoman 12", bg="lightblue", selectcolor="lightyellow"))
            canvas.itemconfig(textGraphSelect, text="Выберите графики, которые хотите построить:")
            canvas.itemconfig(inputboxCellNumber, window=Spinbox(textvariable=graph.inputCellsNum, font="TimesNewRoman 12", width=2, bg="lightyellow", from_=1, to=15, increment=1))
        else:
            canvas.itemconfig(textFileName, text="Выбранный файл не является логом!")

if __name__ == '__main__':
    #global buildCellVolt, buildCurrent, inputCellsNum
    graph = LogGraph()
    # Configuring main window and menu bar
    mainWindow = Tk()
    mainWindow.title(GUI_WINDOW_TITLE)
    mainWindow.resizable(False, False)
    #mainWindow.attributes("-toolwindow", True)
    mainWindow.attributes("-topmost", True, "-toolwindow", True)
    guiMenuBar = Menu(mainWindow)
    guiFileMenu = Menu(guiMenuBar, tearoff=0)
    guiFileMenu.add_command(label="Выбрать логи", command=GUI_OpenFile)
    guiFileMenu.add_separator()
    guiFileMenu.add_command(label="Выход", command=mainWindow.quit)
    guiMenuBar.add_cascade(label="Файл", menu=guiFileMenu)
    # Adding buttons, labels, checkboxes and so on to main window
    canvas = Canvas(mainWindow, width=GUI_MAIN_SCREEN_WIDTH, height=GUI_MAIN_SCREEN_HEIGHT, bg="lightblue", cursor="arrow")
    textFileName = canvas.create_text(GUI_MAIN_SCREEN_WIDTH/2, 20, text="Файл с логами не выбран.", font="TimesNewRoman 12")
    buttonBuildGraph = canvas.create_window(GUI_MAIN_SCREEN_WIDTH/2, 60)
    # Creating variables for checkboxes
    graph.buildCellVolt = BooleanVar()
    graph.buildCurrent = BooleanVar()
    graph.buildVoltage = BooleanVar()
    graph.buildCovThreshold = BooleanVar()
    graph.buildCuvThreshold = BooleanVar()
    graph.buildChargeVoltageThreshold = BooleanVar()
    graph.buildDischargeVoltageThreshold = BooleanVar()
    graph.inputCellsNum = IntVar()
    # Filling checkboxes with initial data
    graph.inputCellsNum.set(6)
    graph.buildCellVolt.set(False)
    graph.buildCurrent.set(False)
    graph.buildVoltage.set(False)
    graph.buildCovThreshold.set(False)
    graph.buildCuvThreshold.set(False)
    graph.buildChargeVoltageThreshold.set(False)
    graph.buildDischargeVoltageThreshold.set(False)
    # Creating and allocating each component
    checkboxCellVoltages = canvas.create_window(27, 140, anchor=W)
    checkboxCurrent = canvas.create_window(27, 220, anchor=W)
    checkboxVoltage = canvas.create_window(27, 250, anchor=W)
    checkboxCovThreshold = canvas.create_window(47, 165, anchor=W)
    checkboxCuvThreshold = canvas.create_window(47, 190, anchor=W)
    checkboxChargeVoltageThreshold = canvas.create_window(47, 275, anchor=W)
    checkboxDischargeVoltageThreshold = canvas.create_window(47, 300, anchor=W)
    inputboxCellNumber = canvas.create_window(290, 140, anchor=W)
    textGraphSelect = canvas.create_text(GUI_MAIN_SCREEN_WIDTH / 2, 110, font="TimesNewRoman 12")
    # Creating the result window
    canvas.pack()
    mainWindow.config(menu=guiMenuBar)
    mainWindow.mainloop()