#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import numpy as np
import DataWrapper as dw
import matplotlib.pyplot as pl

from matplotlib.pyplot import figure
from multipledispatch import dispatch

#
class CorrelationChecker(object):

     wrapper: dw.DataWrapper

     #     
     def __init__(self) -> None:
          self.wrapper = dw.DataWrapper()
          pass

     #
     @dispatch(int, int, str)
     def calc(self, start_index: int, slice_count: int, which: str) -> float:
          
          x = self.wrapper.getDataSet('BTCUSD', start_index, slice_count)[which]
          y = self.wrapper.getDataSet('ETHUSD', start_index, slice_count)[which]

          return round(np.corrcoef(x, y)[0][1], 8)

     #
     @dispatch(int, int)
     def calc(self, start_index: int, slice_count: int) -> float:
          return self.calc(start_index, slice_count, 'Close')

     #
     @dispatch(str, str, str)
     def calc(self, start_date: str, close_date: str, which: str) -> float:
          
          x = self.wrapper.getDataSet('BTCUSD', start_date, close_date)[which]
          y = self.wrapper.getDataSet('ETHUSD', start_date, close_date)[which]

          return round(np.corrcoef(x, y)[0][1], 8)

     #
     @dispatch(str, str)
     def calc(self, start_date: str, close_date: str) -> float:
          return self.calc(start_date, close_date, 'Close')

     #
     def draw(self, start_index: int, slice_count: int, xlabel: str = '', ylabel: str = '', which: str = 'Close') -> None:
          
          lx: list = []
          ly: list = []
          for ix in range(len(self.wrapper.data_btc) - (start_index + slice_count)):
               lx.append(self.wrapper.data_btc.index[ix])
               ly.append(self.calc(ix, slice_count, which))

          figure(figsize= (8, 6), dpi= 75)
          pl.plot(lx, ly, 'r', label= "CC:BTC-ETH")
          pl.ylabel(ylabel)
          pl.xlabel(xlabel)
          pl.hlines(y= 0, xmin= min(lx), xmax= max(lx), linestyles= ['dashdot'], colors= ['blue'])
          pl.hlines(y= 1, xmin= min(lx), xmax= max(lx), linestyles= ['dashdot'], colors= ['blue'])
          pl.hlines(y= 0.6, xmin= min(lx), xmax= max(lx), linestyles= ['dashdot'], colors= ['green'])
          pl.legend(loc= "lower right")
          pl.show()
          pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

that = CorrelationChecker()
that.draw(0, 30, xlabel= 'Time (in Year)', ylabel= 'Correlation-Coefficient (Price)')
that.draw(0, 30, xlabel= 'Time (in Year)', ylabel= 'Correlation-Coefficient (Return)', which= 'SRClose')
print(that.calc(100, 50))
print(that.calc('2020-01-01', '2020-01-10'))

