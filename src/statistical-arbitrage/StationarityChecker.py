#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import pandas as pa
import DataWrapper as dw
import matplotlib.pyplot as pl

from matplotlib.pyplot import figure
from dataclasses import dataclass
from statsmodels.tsa.stattools import adfuller

@dataclass
class DrawArgs(object):
     start_date: str = ''
     close_date: str = ''
     xlabel: str = ''
     ylabel: str = ''
     legend_location: str = 'upper right'
     title: str = ''
     label: str = ''

@dataclass
class DickyFullerResult(object):
     criticalValues: dict
     statistics: float = 0.0
     pvalue: float = 0.0

#
class StationarityChecker(object):

     wrapper: dw.DataWrapper

     #     
     def __init__(self) -> None:
          self.wrapper = dw.DataWrapper()
          pass

     #
     def draw(self, symbol: str, args: DrawArgs, which: str = 'Close') -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(args.start_date) == 0) else args.start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(args.close_date) == 0) else args.close_date

          series = self.wrapper.getDataSet(symbol, start_date, close_date)[which]

          figure(figsize= (8, 6), dpi= 75)
          pl.plot(series, 'coral', label= args.label)
          pl.ylabel(args.ylabel)
          pl.xlabel(args.xlabel)
          pl.hlines(y= 0, xmin= min(series.index), xmax= max(series.index), ls= ['dotted'], colors= ['black'], lw= 1)
          pl.hlines(y= +0.15, xmin= min(series.index), xmax= max(series.index), ls= ['dotted'], colors= ['blue'], lw= 1)
          pl.hlines(y= -0.15, xmin= min(series.index), xmax= max(series.index), ls= ['dotted'], colors= ['blue'], lw= 1)
          pl.legend(loc= args.legend_location)
          pl.show()

          pass

     #
     def drawAvecMeanAndVariance(self, symbol: str, args: DrawArgs, which: str = 'Close') -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(args.start_date) == 0) else args.start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(args.close_date) == 0) else args.close_date

          series: pa.Series = self.wrapper.getDataSet(symbol, start_date, close_date)[which]
          series = series.dropna()
          serm = series.rolling(30).mean()
          serm = serm.dropna()
          serv = series.rolling(30).var()
          serv = serv.dropna()

          figure(figsize= (8, 6), dpi= 75)
          pl.plot(series, 'coral', label= args.label)
          pl.plot(serm, 'g', label= 'Mean')
          pl.plot(serv, 'b', label= 'Variance')
          pl.ylabel(args.ylabel)
          pl.xlabel(args.xlabel)
          pl.hlines(y= 0, xmin= min(series.index), xmax= max(series.index), colors= ['black'], lw= 1)
          pl.hlines(y= +0.15, xmin= min(series.index), xmax= max(series.index), ls= ['dotted'], colors= ['blue'], lw= 1)
          pl.hlines(y= -0.15, xmin= min(series.index), xmax= max(series.index), ls= ['dotted'], colors= ['blue'], lw= 1)
          pl.legend(loc= args.legend_location)
          pl.show()

          pass

     #
     def checkByDickyFuller(self, symbol: str, start_date: str = '', close_date: str = '', which: str = 'Close') -> bool:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

          series: pa.Series = self.wrapper.getDataSet(symbol, start_date, close_date)[which]
          series = series.dropna()

          output = adfuller(series)
          result: DickyFullerResult = DickyFullerResult(statistics= output[0], pvalue= output[1], criticalValues= output[4])
          print(f'result = {result}')
          return True if (result.pvalue <= 0.05) else False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def check1():
     checker = StationarityChecker()
     args = DrawArgs(
          start_date= '', 
          close_date= '', 
          xlabel= 'Time (in Year)', 
          ylabel= 'Return', 
          label= 'BTCUSD'
     )
     checker.draw('BTC', args, which= 'SRClose')

def check2():
     checker = StationarityChecker()
     args = DrawArgs(
          start_date= '', 
          close_date= '', 
          xlabel= 'Time (in Year)', 
          ylabel= 'Return', 
          label= 'ETHUSD'
     )
     checker.draw('ETH', args, which= 'SRClose')

def check3():
     checker = StationarityChecker()
     args = DrawArgs(
          start_date= '', 
          close_date= '', 
          xlabel= 'Time (Year)', 
          ylabel= 'Return (BTCUSDT)', 
          label= 'BTCUSDT'
     )
     checker.drawAvecMeanAndVariance('BTC', args, which= 'SRClose')

def check4():
     checker = StationarityChecker()
     checker.checkByDickyFuller('ETH', which= 'SRClose')

check1()
check2()
check3()
check4()
