from math import ceil
import matplotlib.pyplot as plot
import matplotlib.ticker as tck
import matplotlib.backend_bases as bkndbs
import datetime as time
from zoomPan import*


# Constants and other values
global THRESHOLD_OVER_VOLTAGE, THRESHOLD_UNDER_VOLTAGE, THRESHOLD_CHARGE_VOLTAGE
THRESHOLD_OVER_VOLTAGE = 3700
THRESHOLD_UNDER_VOLTAGE = 2000
THRESHOLD_CHARGE_VOLTAGE = 21600
THRESHOLD_DISCHARGE_VOLTAGE = 12000

SIGNALS_NUMBER = 66             # number of data columns
DATA_START_IN_LOGFILE = 16      # data in log file starts from string with this number
global DATA_LIST, SIGNAL_LIST
DATA_LIST = []
SIGNAL_LIST = ["Sample", "DateTime", "ElapsedTime", "ManufAccess", "RemCapAlarm", "RemTimeAlarm", "BattMode", "@Rate(@)", "@TimeFull",
               "@TimeEmpty", "@RateOK", "Temperature", "Voltage", "Current", "AvgCurr", "MaxErr", "RSOC", "ASOC", "RemCap", "FullChgCap",
               "RunTimeEmty", "RunTimeEmty", "AvgTimeFull", "ChgCurr", "ChgVolt", "BattStat", "CycleCnt", "PendingEdv", "SoH", "OpStatA",
               "OpStatB", "TempRange", "ChgStat", "GaugeStat", "MfgStat", "SafetyAlertAB", "SafetyStatAB", "SafetyAlertCD", "SafetyStatCD",
               "PFAlertAB", "PFStatAB", "PFStatAB", "CellVolt1", "CellVolt2", "CellVolt3", "CellVolt4", "CellVolt5", "CellVolt6", "CellVolt7",
               "CellVolt8", "CellVolt9", "CellVolt10", "CellVolt11", "CellVolt12", "CellVolt13", "CellVolt14", "CellVolt15", "ExtAvgCellVolt",
               "TS1 Temp", "TS2 Temp", "TS3 Temp", "CellTemp", "FetTemp", "GaugeInternalTemp", "LogRowTime(ms)", "LogStatus"]

class LogGraph:
    def __init__(self):
        self.graphWindowsNum = 0
        self.buildCellVolt = None
        self.buildCurrent = None
        self.buildVoltage = None
        self.inputCellsNum = None
        self.buildCovThreshold = None
        self.buildCuvThreshold = None
        self.buildChargeVoltageThreshold = None
        self.buildDischargeVoltageThreshold = None
        self.figureNum = 0

    def ParseFile(self, fileContent):
        self.samplesNum = len(fileContent) - DATA_START_IN_LOGFILE
        DATA_LIST.clear()
        for signalNum in range(SIGNALS_NUMBER):
            DATA_LIST.append([])
            for dataNum in range(self.samplesNum):
                DATA_LIST[signalNum].append(fileContent[dataNum + DATA_START_IN_LOGFILE].split(',')[signalNum])

    def DrawThreshold(self, *thresholds):
        timeList = list([data.split(' ')[1] for data in DATA_LIST[SIGNAL_LIST.index("DateTime")]])
        xAxis = [str(time.datetime.strptime(timeStep, "%H:%M:%S") - time.datetime.strptime(timeList[0], "%H:%M:%S")) for timeStep in timeList[0:self.samplesNum]]
        plot.figure(self.figureNum)
        for threshold in thresholds:
            plot.plot(xAxis, [threshold]*self.samplesNum, "--")

    def DrawSignal(self, *signals):
        self.figureNum = self.figureNum + 1
        # Calculating X axis time stamps
        timeList = list([data.split(' ')[1] for data in DATA_LIST[SIGNAL_LIST.index("DateTime")]])
        xAxis = [str(time.datetime.strptime(timeStep, "%H:%M:%S")-time.datetime.strptime(timeList[0], "%H:%M:%S")) for timeStep in timeList[0:self.samplesNum]]
        # Creating figure with "figureNum" id and adding a title and icon
        plot.figure(self.figureNum).canvas.set_window_title(f"Лог №{self.graphWindowsNum}")
        thisManager = plot.get_current_fig_manager()
        thisManager.window.wm_iconbitmap("icon.ico")
        # Drawing graphs
        __allData = []
        for signalName in signals:
            signal = SIGNAL_LIST.index(signalName)
            DATA_LIST[signal] = [int(data) for data in DATA_LIST[signal]]
            for eachData in DATA_LIST[signal]:
                __allData.append(eachData)
            plot.plot(xAxis, DATA_LIST[signal], label=signalName)
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
            voltageData = SIGNAL_LIST[SIGNAL_LIST.index("CellVolt1"):SIGNAL_LIST.index("CellVolt1")+int(self.inputCellsNum.get())]
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
