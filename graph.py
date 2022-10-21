import numpy as np
import seaborn as sns
import pandas as pd
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import AutoMinorLocator
from matplotlib.pyplot import figure
plt.style.use('./oldIBM.style')
figure(figsize=(7.878, 4.125), dpi=320)
ibmmono = fm.FontProperties(fname='C:\Windows\Fonts\IBMPlexMono-Light.ttf')
primus = fm.FontProperties(fname='C:\Windows\Fonts\Primus Light.otf')
from datetime import datetime, date

class Test:
    def __init__(self, file):
        #data reading functions
        fname = file
        data = np.loadtxt(fname, max_rows=500000)
        tdata = np.loadtxt(fname, skiprows=500000, usecols=1, dtype=str)

        # x-axis processor
        stime = tdata[0]
        etime = tdata[1]
        time_elapsed = datetime.strptime(etime, '%H:%M:%S.%f') - datetime.strptime(stime, '%H:%M:%S.%f')
        size = data.size
        size_array = np.array(list(range(1, (data.size + 1))))
        sample_rate = size/time_elapsed.total_seconds()
        time_array = size_array/sample_rate

        #pre-trimmng and time normalisation
        mavgsum = 0
        mavgcount = 0
        mavg = 0
        ptpoint = 0
        for x in np.nditer(data):
            mavgcount += 1
            mavgsum += x
            mavg = mavgsum / mavgcount
            if mavg > 10000:
                mavg = mavg/4.5

            if x/5 > mavg and mavgcount > 1000:
                ptpoint = mavgcount
                break

        ptpoint = ptpoint - 50
        ptdata = data[ptpoint:]
        ptTimeStart = time_array[ptpoint]
        pttime_array = time_array[ptpoint:] - ptTimeStart

        #post trimming
        udpcount = 0
        atpoint = 0
        for x in np.nditer(ptdata):
            udpcount += 1
            if x <= mavg and udpcount > 150:
                atpoint = udpcount
                break

        atpoint = atpoint + 50
        atdata = ptdata[:atpoint]
        if atdata.size < 750:
            atpoint += 750-atdata.size
            atdata = ptdata[:atpoint]
            attime_array = pttime_array[:atpoint]

        else:
            atpoint = 750
            atdata = ptdata[:atpoint]
            attime_array = pttime_array[:atpoint]

        # zeroing
        if mavg > 1000:
            mavg = mavg * 4.5
        zdata = atdata - mavg
        zdata = np.clip(zdata, 0, 2**(16))

        # adc read to newton reading conversion, exporting data
        newtonData = (((6600/2**(16))*zdata)*200/8352.9642)*9.8

        self.data = newtonData
        self.time = attime_array
        self.max = np.amax(newtonData)

class CalData:
    def __init__(self, cal):
        self.testOne = Test(cal + "-1.txt")
        self.testTwo = Test(cal + "-2.txt")
        self.testThree = Test(cal + "-3.txt")
        self.testFour = Test(cal + "-4.txt")
        self.testFive = Test(cal + "-5.txt")
        #self.averageDataArray = (self.testOne.data + self.testTwo.data + self.testThree.data + self.testFour.data + self.testFive.data)/5 #np.mean([testOne.data, testTwo.data, testThree.data, testFour.data, testFive.data])
        #self.averageTimeArray = (self.testOne.time + self.testTwo.time + self.testThree.time + self.testFour.time + self.testFive.time)/5 #np.mean([testOne.time, testTwo.time, testThree.time, testFour.time, testFive.time])
        #self.AverageMax = (self.testOne.max + self.testTwo.max + self.testThree.max + self.testFour.max + self.testFive.max)/5
        if cal == '10':
            self.AverageMax = (self.testOne.max + self.testTwo.max + self.testThree.max + self.testFour.max)/4
            self.averageTimeArray = (self.testOne.time + self.testTwo.time + self.testThree.time + self.testFour.time)/4
            self.averageDataArray = (self.testOne.data + self.testTwo.data + self.testThree.data + self.testFour.data)/4
        else:
            self.averageTimeArray = (self.testOne.time + self.testTwo.time + self.testThree.time + self.testFour.time + self.testFive.time)/5
            self.averageDataArray = (self.testOne.data + self.testTwo.data + self.testThree.data + self.testFour.data + self.testFive.data)/5
            self.AverageMax = (self.testOne.max + self.testTwo.max + self.testThree.max + self.testFour.max + self.testFive.max)/5

    def linegraph(self):
        plt.plot(self.testOne.time, self.testOne.data, color='#C01406', alpha=0.65, linestyle='dashed')
        plt.plot(self.testTwo.time, self.testTwo.data, color='#C01406', alpha=0.65, linestyle='dashed')
        plt.plot(self.testThree.time, self.testThree.data, color="#C01406", alpha=0.65, linestyle='dashed')
        plt.plot(self.testFour.time, self.testFour.data, color='#C01406', alpha=0.65, linestyle='dashed')
        plt.plot(self.testFive.time, self.testFive.data, color='#C01406', alpha=0.65, linestyle='dashed')
        plt.plot(self.averageTimeArray, self.averageDataArray, color='#4476AE')

    def linegraphsolid(self):
        plt.plot(self.testOne.time, self.testOne.data, color='#C01406')
        plt.plot(self.testTwo.time, self.testTwo.data, color='green')
        plt.plot(self.testThree.time, self.testThree.data, color='#4476AE')
        plt.plot(self.testFour.time, self.testFour.data, color='black')
        plt.plot(self.testFive.time, self.testFive.data, color='pink')

    def avglinegraph(self, color):
        plt.plot(self.averageTimeArray, self.averageDataArray, color=color)


def boxplot():
    tt = [60.4, 60.4, 61.5, 68.5, 64.1]
    te = [166.2, 101.7, 139.5, 138.4, 91.5]
    nm = [116, 133.6, 153.7, 164.6, 170.7]
    ff = [259.5, 248.1, 213.4, 265.6, 209.9]
    tm = [237.8, 219.8, 337.7, 266.6, 248.7]
    data = [tt, te, nm, ff, tm]
    ft = ['.22', '.38', '9mm', '.45', '10mm']
    blue = '#4476AE'
    red = '#C01406'
    plt.boxplot(data, medianprops=dict(color=red), whiskerprops=dict(color=blue), capprops=dict(color=blue), flierprops=dict(color=blue, markeredgecolor=blue))
    ax = plt.gca()
    ax.set_title('Peak Force Box graph', fontproperties=ibmmono, size=18)
    ax.set(ylim=(0,350))
    ax.set_xticklabels(ft, fontproperties=ibmmono, size=10)
    ax.set_yticklabels(ax.get_yticks(), fontproperties=ibmmono, size=10)
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    plt.xlabel("Caliber", fontproperties=ibmmono, size=14)
    plt.ylabel("Peak force (Newtons)", fontproperties=ibmmono, size=14)
    plt.show()

def stemplot():
    tt = [60.4, 60.4, 61.5, 68.5, 64.1]
    te = [166.2, 101.7, 139.5, 138.4, 91.5]
    nm = [116, 133.6, 153.7, 164.6, 170.7]
    ff = [259.5, 248.1, 213.4, 265.6, 209.9]
    tm = [237.8, 219.8, 337.7, 266.6, 248.7]
    data = tt + te + nm + ff + tm
    ft = ['.22-1', '.22-2', '.22-3', '.22-4', '.22-5', '.38-1','.38-2', '.38-3', '.38-4', '.38-5', '9mm-1', '9mm-2', '9mm-3', '9mm-4', '9mm-5', '.45-1', '.45-2', '.45-3', '.45-4', '.45-5', '10mm-1', '10mm-2', '10mm-3', '10mm-4', '10mm-5']
    blue = '#4476AE'
    red = '#C01406'
    (markers, stemlines, baseline) = plt.stem(data)
    plt.setp(stemlines, color=blue, linewidth=0.5)
    plt.setp(markers, markersize=10, color=red , markeredgewidth=0.5, fillstyle='none')
    ax = plt.gca()
    ax.set_title('Peak Force Stem graph', fontproperties=ibmmono, size=18)
    ax.set(ylim=(0,350), xlim=(-1,25))
    my_range=range(0,25)
    ax.set_xticklabels(ax.get_xticks(), fontproperties=ibmmono, size=4)
    plt.xticks(my_range, ft)
    ax.set_yticklabels(ax.get_yticks(), fontproperties=ibmmono, size=10)

    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(axis="y", color="black", alpha=1, linewidth=.2, linestyle=":", which="major")
    ax.grid(axis="y", color="black", alpha=1, linewidth=.05, linestyle=":", which="minor")

    plt.xlabel("Test and Caliber", fontproperties=ibmmono, size=14)
    plt.ylabel("Peak force (Newtons)", fontproperties=ibmmono, size=14)
    plt.show()

def scatterplot():
    tt = [60.4, 60.4, 61.5, 68.5, 64.1]
    te = [166.2, 101.7, 139.5, 138.4, 91.5]
    nm = [116, 133.6, 153.7, 164.6, 170.7]
    ff = [259.5, 248.1, 213.4, 265.6, 209.9]
    tm = [237.8, 219.8, 337.7, 266.6, 248.7]
    data = tt + te + nm + ff + tm
    mass = [2.59196, 2.59196, 2.59196, 2.59196, 2.59196, 8.42386, 8.42386, 8.42386, 8.42386, 8.42386, 7.45187, 7.45187, 7.45187, 7.45187, 7.45187, 14.9037, 14.9037, 14.9037, 14.9037, 14.9037, 11.6638, 11.6638, 11.6638, 11.6638, 11.6638]
    blue = '#4476AE'
    red = '#C01406'
    plt.scatter( mass, data, marker='o', s=130, facecolor='none', edgecolor=blue, linewidth=.5)
    plt.scatter( mass, data, marker='o', s=2, color=red)

    ax = plt.gca()
    ax.set_title('Mass/Force Scatter graph', fontproperties=ibmmono, size=18)
    ax.set(ylim=(0,350))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xticklabels(ax.get_xticks(), fontproperties=ibmmono, size=10)
    ax.set_yticklabels(ax.get_yticks(), fontproperties=ibmmono, size=10)
    ax.grid(axis="x", color="black", alpha=1, linewidth=.2, linestyle=":", which="major")
    ax.grid(axis="y", color="black", alpha=1, linewidth=.2, linestyle=":", which="major")
    ax.grid(axis="x", color="black", alpha=1, linewidth=.05, linestyle=":", which="minor")
    ax.grid(axis="y", color="black", alpha=1, linewidth=.05, linestyle=":", which="minor")

    plt.xlabel("Bullet mass (grams)", fontproperties=ibmmono, size=14)
    plt.ylabel("Peak force (Newtons)", fontproperties=ibmmono, size=14)

    plt.show()


def scatterplot2():
    tt = [60.4, 60.4, 61.5, 68.5, 64.1]
    te = [166.2, 101.7, 139.5, 138.4, 91.5]
    nm = [116, 133.6, 153.7, 164.6, 170.7]
    ff = [259.5, 248.1, 213.4, 265.6, 209.9]
    tm = [237.8, 219.8, 337.7, 266.6, 248.7]
    data = tt + te + nm + ff + tm
    velocity = [379.9, 385.5, 381.5, 383.9, 384.5, 257.8, 254.6, 249.1, 256.2, 249.9, 384.7, 347.34, 359.7, 348.9, 354.3, 267.5, 264.3, 268.6, 261.8, 268.6, 403.9, 391.4, 388.8, 397.7, 410.0]
    blue = '#4476AE'
    red = '#C01406'
    plt.scatter( velocity, data, marker='o', s=130, facecolor='none', edgecolor=blue, linewidth=.5)
    plt.scatter( velocity, data, marker='o', s=2, color=red)

    ax = plt.gca()
    ax.set_title('Velocity/Force Scatter graph', fontproperties=ibmmono, size=18)
    ax.set(ylim=(0,350))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xticklabels(ax.get_xticks(), fontproperties=ibmmono, size=10)
    ax.set_yticklabels(ax.get_yticks(), fontproperties=ibmmono, size=10)
    ax.grid(axis="x", color="black", alpha=1, linewidth=.2, linestyle=":", which="major")
    ax.grid(axis="y", color="black", alpha=1, linewidth=.2, linestyle=":", which="major")
    ax.grid(axis="x", color="black", alpha=1, linewidth=.05, linestyle=":", which="minor")
    ax.grid(axis="y", color="black", alpha=1, linewidth=.05, linestyle=":", which="minor")

    plt.xlabel("Velocity (m/s)", fontproperties=ibmmono, size=14)
    plt.ylabel("Peak force (Newtons)", fontproperties=ibmmono, size=14)

    plt.show()

def scatterplot3():
    tt = [60.4, 60.4, 61.5, 68.5, 64.1]
    te = [166.2, 101.7, 139.5, 138.4, 91.5]
    nm = [116, 133.6, 153.7, 164.6, 170.7]
    ff = [259.5, 248.1, 213.4, 265.6, 209.9]
    tm = [237.8, 219.8, 337.7, 266.6, 248.7]
    data = tt + te + nm + ff + tm
    velocity = [379.9, 385.5, 381.5, 383.9, 384.5, 257.8, 254.6, 249.1, 256.2, 249.9, 384.7, 347.34, 359.7, 348.9, 354.3, 267.5, 264.3, 268.6, 261.8, 268.6, 403.9, 391.4, 388.8, 397.7, 410.0]
    mass = [2.59196, 2.59196, 2.59196, 2.59196, 2.59196, 8.42386, 8.42386, 8.42386, 8.42386, 8.42386, 7.45187, 7.45187, 7.45187, 7.45187, 7.45187, 14.9037, 14.9037, 14.9037, 14.9037, 14.9037, 11.6638, 11.6638, 11.6638, 11.6638, 11.6638]
    momentum = np.array(mass) * np.array(velocity)
    blue = '#4476AE'
    red = '#C01406'
    x = np.linspace(0, 5000)
    y = 0.0558*x+7.1
    plt.plot(x, y, linestyle=":", alpha=0.7)
    plt.scatter( momentum, data, marker='o', s=130, facecolor='none', edgecolor=blue, linewidth=.5)
    plt.scatter( momentum, data, marker='o', s=2, color=red)

    ax = plt.gca()
    ax.set_title('Momentum/Force Scatter graph', fontproperties=ibmmono, size=18)
    ax.set(ylim=(0,350))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xticklabels(ax.get_xticks(), fontproperties=ibmmono, size=10)
    ax.set_yticklabels(ax.get_yticks(), fontproperties=ibmmono, size=10)
    ax.grid(axis="x", color="black", alpha=1, linewidth=.2, linestyle=":", which="major")
    ax.grid(axis="y", color="black", alpha=1, linewidth=.2, linestyle=":", which="major")
    ax.grid(axis="x", color="black", alpha=1, linewidth=.05, linestyle=":", which="minor")
    ax.grid(axis="y", color="black", alpha=1, linewidth=.05, linestyle=":", which="minor")

    plt.xlabel("Momentum", fontproperties=ibmmono, size=14)
    plt.ylabel("Peak force (Newtons)", fontproperties=ibmmono, size=14)

    plt.show()

def linegraph():
    #CalData('22').avglinegraph('green')
    #CalData('38').avglinegraph('blue')
    #CalData('9').avglinegraph('red')
    #CalData('45').avglinegraph('orange')
    #CalData('10').avglinegraph('black')
    #CalData('10').linegraph()
    ax = plt.gca()
    ax.set_title('10mm Force/Time graph', fontproperties=ibmmono, size=18)
    ax.set(xlim=(0, 0.040), ylim=(0,350))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.set_xticklabels(ax.get_xticks(), fontproperties=ibmmono, size=10)
    ax.set_yticklabels(ax.get_yticks(), fontproperties=ibmmono, size=10)
    ax.grid(axis="x", color="black", alpha=1, linewidth=.2, linestyle=":", which="major")
    ax.grid(axis="y", color="black", alpha=1, linewidth=.2, linestyle=":", which="major")
    ax.grid(axis="x", color="black", alpha=1, linewidth=.05, linestyle=":", which="minor")
    ax.grid(axis="y", color="black", alpha=1, linewidth=.05, linestyle=":", which="minor")
    plt.xlabel("Time (s)", fontproperties=ibmmono, size=14)
    plt.ylabel("Newtons", fontproperties=ibmmono, size=14)
    plt.show()

scatterplot3()
