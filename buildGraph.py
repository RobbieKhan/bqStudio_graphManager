from math import ceil
import matplotlib.pyplot as plot
import matplotlib.ticker as tck
import matplotlib.backend_bases as bkndbs
import datetime as time
from zoomPan import*

# Constants and other values
THRESHOLD_OVER_VOLTAGE = 3700
THRESHOLD_UNDER_VOLTAGE = 2000
THRESHOLD_CHARGE_VOLTAGE = 21600
THRESHOLD_DISCHARGE_VOLTAGE = 12000
SIGNALS_NUMBER = 66                             # number of data columns
SIGNAL_LINE_IN_LOGFILE = 15                     # signal names in log file can be found in this line
DATA_START_IN_LOGFILE = 16                      # data in log file starts from string with this number
XAXIS_RAW_IN_LOGFILE = "DateTime"               # have to be in "smth HH:MM:SS" format. Otherwise 'CalculateXaxis()' func have to be modified


class LogGraph:
    def __init__(self):
        self.graphWindowsNum = 0
        self.figureNum = 0
        self.buildCellVolt = None
        self.buildCurrent = None
        self.buildVoltage = None
        self.inputCellsNum = None
        self.buildCovThreshold = None
        self.buildCuvThreshold = None
        self.buildChargeVoltageThreshold = None
        self.buildDischargeVoltageThreshold = None
        self.DATA_LIST = []
        self.SIGNAL_LIST = []

    def ParseFile(self, fileContent):
        self.samplesNum = len(fileContent) - DATA_START_IN_LOGFILE
        self.DATA_LIST.clear()
        self.SIGNAL_LIST.clear()
        for signalName in (fileContent[SIGNAL_LINE_IN_LOGFILE].split(',')):
            self.SIGNAL_LIST.append(signalName)
        for signalNum in range(SIGNALS_NUMBER):
            self.DATA_LIST.append([])
            for dataNum in range(self.samplesNum):
                self.DATA_LIST[signalNum].append(fileContent[dataNum + DATA_START_IN_LOGFILE].split(',')[signalNum])

    def CalculateXaxis(self):
        timeList = list([data.split(' ')[1] for data in self.DATA_LIST[self.SIGNAL_LIST.index(XAXIS_RAW_IN_LOGFILE)]])
        xAxisList = [str(time.datetime.strptime(timeStep, "%H:%M:%S") - time.datetime.strptime(timeList[0], "%H:%M:%S")) for timeStep in timeList[0:self.samplesNum]]
        return xAxisList

    def DrawThreshold(self, *thresholds):
        xAxis = self.CalculateXaxis()
        plot.figure(self.figureNum)
        for threshold in thresholds:
            plot.plot(xAxis, [threshold]*self.samplesNum, "--")

    def DrawSignal(self, *signals):
        self.figureNum = self.figureNum + 1
        # Calculating X axis time stamps
        xAxis = self.CalculateXaxis()
        # Creating figure with "figureNum" id and adding a title and icon
        plot.figure(self.figureNum).canvas.set_window_title(f"Лог №{self.graphWindowsNum}")
        thisManager = plot.get_current_fig_manager()
        thisManager.window.wm_iconbitmap("icon.ico")
        # Drawing graphs
        __allData = []
        for signalName in signals:
            signal = self.SIGNAL_LIST.index(signalName)
            self.DATA_LIST[signal] = [int(data) for data in self.DATA_LIST[signal]]
            for eachData in self.DATA_LIST[signal]:
                __allData.append(eachData)
            plot.plot(xAxis, self.DATA_LIST[signal], label=signalName)
            plot.legend()
        plot.gca().xaxis.set_major_locator(tck.MultipleLocator(base=ceil(self.samplesNum / 5)))
        plot.xticks(rotation=45)
        plot.gca().yaxis.set_major_locator(tck.MultipleLocator(base=ceil((max(__allData) - 0) / 20)))
        # Adding zoom and pan control
        zp = ZoomPan()
        zp.zoom_factory(plot.gca(), base_scale=1.1)
        zp.pan_factory(plot.gca())

    def DrawFinalGraph(self, fileContent):
        self.ParseFile(fileContent)
        # Configuring figure's toolbar
        bkndbs.NavigationToolbar2.toolitems = {
            ('Save', 'Сохранить график', 'filesave', 'save_figure'),
        }
        # Building voltages graph if related checkbox is checked
        if self.buildCellVolt.get() == True:
            voltageData = self.SIGNAL_LIST[self.SIGNAL_LIST.index("CellVolt1"):self.SIGNAL_LIST.index("CellVolt1")+int(self.inputCellsNum.get())]
            self.DrawSignal(*voltageData)
            # Building COV threshold if related checkbox is checked
            if self.buildCovThreshold.get():
                self.DrawThreshold(THRESHOLD_OVER_VOLTAGE)
            # Building CUV threshold if related checkbox is checked
            if self.buildCuvThreshold.get():
                self.DrawThreshold(THRESHOLD_UNDER_VOLTAGE)
        # Building current graph if related checkbox is checked
        if self.buildCurrent.get() == True:
            self.DrawSignal("Current")
        # Building battery voltage graph if related checkbox is checked
        if self.buildVoltage.get() == True:
            self.DrawSignal("Voltage")
            # Building charge voltage threshold if related checkbox is checked
            if self.buildChargeVoltageThreshold.get():
                self.DrawThreshold(THRESHOLD_CHARGE_VOLTAGE)
            # Building discharge voltage threshold if related checkbox is checked
            if self.buildDischargeVoltageThreshold.get():
                self.DrawThreshold(THRESHOLD_DISCHARGE_VOLTAGE)
        # plot.gca().invert_yaxis()
        plot.show()
        pass
