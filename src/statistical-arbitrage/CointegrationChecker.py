#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import pandas as pa
import DataWrapper as dw
import matplotlib.pyplot as pl

from statsmodels.tsa.stattools import adfuller
from scipy.stats import linregress
from dataclasses import dataclass

@dataclass
class DrawArgs(object):
     legend_location: list
     start_date: str = ''
     close_date: str = ''
     xlabel: str = ''
     ylabel: str = ''
     title: str = ''
     label: str = ''

@dataclass
class DickyFullerResult(object):
     criticalValues: dict
     statistics: float = 0.0
     pvalue: float = 0.0

#
class CointegrationChecker(object):

     wrapper: dw.DataWrapper

     #     
     def __init__(self) -> None:
          self.wrapper = dw.DataWrapper()
          pass

     #
     def draw(self, args: DrawArgs, drawKind: str = 'var', rollingSize:int = 21, which: str = 'Close') -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(args.start_date) == 0) else args.start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(args.close_date) == 0) else args.close_date

          sera: pa.Series = self.wrapper.getDataSet('BTC', start_date, close_date)[which]
          serb: pa.Series = self.wrapper.getDataSet('ETH', start_date, close_date)[which]

          sera = sera.dropna()     # clearing NA out
          serb = serb.dropna()     # clearing NA out
          
          sram = sera.rolling(rollingSize).mean()
          srbm = serb.rolling(rollingSize).mean()

          sram = sram.dropna()
          srbm = srbm.dropna()

          srav = sera.rolling(rollingSize).std() if (drawKind == 'std') else sera.rolling(rollingSize).var()
          srbv = serb.rolling(rollingSize).std() if (drawKind == 'std') else serb.rolling(rollingSize).var()

          srav = srav.dropna()
          srbv = srbv.dropna()

          labl = f'Standard Deviation({rollingSize})' if (drawKind == 'std') else f'Variance ({rollingSize})'

          fig, (ax1, ax2) = pl.subplots(1, 2)
          fig.suptitle(args.title)
          fig.set_dpi(75)
          fig.set_size_inches(14, 7)
          ax1.plot(sera, 'coral', label= 'BTCUSDT')
          ax1.plot(sram, 'purple', label= f'Mean({rollingSize})')
          ax1.plot(srav, 'blue', label= labl)
          ax1.set_xlabel(args.xlabel)
          ax1.set_ylabel(args.ylabel)
          ax1.legend(loc= str(args.legend_location[0]))
          ax2.plot(serb, 'coral', label= 'ETHUSDT')
          ax2.plot(srbm, 'purple', label= f'Mean({rollingSize})')
          ax2.plot(srbv, 'blue', label= labl)
          ax2.set_xlabel(args.xlabel)
          ax2.set_ylabel(args.ylabel)
          ax2.legend(loc= str(args.legend_location[1]))
          pl.show()

          pass

     #
     def drawResiduals(self, args: DrawArgs, drawKind: str = 'var', rollingSize:int = 21, which: str = 'Close') -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(args.start_date) == 0) else args.start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(args.close_date) == 0) else args.close_date

          sera: pa.Series = self.wrapper.getDataSet('BTC', start_date, close_date)[which]
          serb: pa.Series = self.wrapper.getDataSet('ETH', start_date, close_date)[which]

          sera = sera.dropna()     # clearing NA out
          serb = serb.dropna()     # clearing NA out

          # calculating linear regression
          regrea = linregress(sera.values, serb.values)
          regreb = linregress(serb.values, sera.values)
          # creating residuals series
          resdua: pa.Series = sera - regrea.slope * serb
          resdub: pa.Series = serb - regreb.slope * sera

          sram = resdua.rolling(rollingSize).mean()
          srbm = resdub.rolling(rollingSize).mean()

          sram = sram.dropna()
          srbm = srbm.dropna()

          srav = resdua.rolling(rollingSize).std() if (drawKind == 'std') else resdua.rolling(rollingSize).var()
          srbv = resdub.rolling(rollingSize).std() if (drawKind == 'std') else resdub.rolling(rollingSize).var()

          srav = srav.dropna()
          srbv = srbv.dropna()

          labl = f'Standard Deviation({rollingSize})' if (drawKind == 'std') else f'Variance ({rollingSize})'

          fig, (ax1, ax2) = pl.subplots(1, 2)
          fig.suptitle(args.title)
          fig.set_dpi(75)
          fig.set_size_inches(14, 7)
          ax1.plot(resdua, 'skyblue', label= 'Residuals (BTC(t) - lambda * ETH(t))')
          ax1.plot(sram, 'purple', label= f'Mean({rollingSize})')
          ax1.plot(srav, 'blue', label= labl)
          ax1.set_xlabel(args.xlabel)
          ax1.set_ylabel(args.ylabel)
          ax1.legend(loc= str(args.legend_location[0]))
          ax2.plot(resdub, 'skyblue', label= 'Residuals (ETH(t) - lambda * BTC(t))')
          ax2.plot(srbm, 'purple', label= f'Mean({rollingSize})')
          ax2.plot(srbv, 'blue', label= labl)
          ax2.set_xlabel(args.xlabel)
          ax2.set_ylabel(args.ylabel)
          ax2.legend(loc= str(args.legend_location[1]))
          pl.show()

          pass

     #
     def check(self, start_date: str = '', close_date: str = '', which: str = 'Close', reverse: bool = False) -> bool:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

          sera: pa.Series = self.wrapper.getDataSet('BTC', start_date, close_date)[which]
          serb: pa.Series = self.wrapper.getDataSet('ETH', start_date, close_date)[which]

          sera = sera.dropna()     # clearing NA out
          serb = serb.dropna()     # clearing NA out

          ts_a = sera.values if (not reverse) else serb.values   # time series A(t)
          ts_b = serb.values if (not reverse) else sera.values   # time series B(t)

          # calculating linear regression
          regres = linregress(ts_a, ts_b)
          print(f'linear regression result = {regres}')
          # creating residuals series
          resdua = ts_a - regres.slope * ts_b
          
          # applying augmented dicky-fuller test
          output = adfuller(resdua)
          result: DickyFullerResult = DickyFullerResult(statistics= output[0], pvalue= output[1], criticalValues= output[4])
          print(f'augmented dicky-fuller test result = {result}')
          return True if (result.pvalue <= 0.05) else False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def check1():
     that = CointegrationChecker()
     args = DrawArgs(
          legend_location = ['upper left', 'upper left'],
          start_date= '', 
          close_date= '', 
          xlabel= 'Time (Year)', 
          ylabel= 'Price (USD)'
     )
     that.draw(args, drawKind= 'std', rollingSize= 55, which= 'Close')

def check2():
     that = CointegrationChecker()
     args = DrawArgs(
          legend_location = ['upper left', 'lower left'],
          start_date= '', 
          close_date= '', 
          xlabel= 'Time (Year)', 
          ylabel= 'Price (USD)'
     )
     that.drawResiduals(args, drawKind= 'std', rollingSize= 55, which= 'Close')

def check3():
     that = CointegrationChecker()
     args = DrawArgs(
          legend_location = ['lower right', 'lower right'],
          start_date= '', 
          close_date= '', 
          xlabel= 'Time (Year)', 
          ylabel= 'Return'
     )
     that.draw(args, drawKind= 'var', rollingSize= 21, which= 'SRClose')

def check4():
     that = CointegrationChecker()
     args = DrawArgs(
          legend_location = ['upper right', 'lower left'],
          start_date= '', 
          close_date= '', 
          xlabel= 'Time (Year)', 
          ylabel= 'Return'
     )
     that.drawResiduals(args, drawKind= 'var', rollingSize= 21, which= 'SRClose')

def check5():
     that = CointegrationChecker()
     r1 = that.check(reverse= False, which= 'Close')
     r2 = that.check(reverse= True,  which= 'Close')
     print(r1)
     print(r2)

def check6():
     that = CointegrationChecker()
     r1 = that.check(reverse= False, which= 'SRClose')
     r2 = that.check(reverse= True,  which= 'SRClose')
     print(r1)
     print(r2)

check1()
check2()
check3()
check4()
check5()
check6()

