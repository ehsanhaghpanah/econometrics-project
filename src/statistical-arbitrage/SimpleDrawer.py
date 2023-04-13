#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import matplotlib.pyplot as pl
import DataWrapper as dw
from matplotlib.pyplot import figure

#
class SimpleDrawer(object):

     wrapper: dw.DataWrapper

     #     
     def __init__(self) -> None:
          self.wrapper = dw.DataWrapper()
          pass

     # draws historical charts
     def drawCharts(self, start_date: str = '', close_date: str = '', which: str = 'Close') -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

          series_btc = self.wrapper.data_btc[start_date:close_date][which]
          series_eth = self.wrapper.data_eth[start_date:close_date][which]

          # normalizing prices
          series_btc = series_btc / series_btc.mean()
          series_eth = series_eth / series_eth.mean()

          # drawing
          figure(figsize= (8, 6), dpi= 75)
          pl.plot(series_btc, 'r', label= "BTC/USD")
          pl.plot(series_eth, 'g', label= "ETH/USD")
          pl.ylabel("Normalized Price")
          pl.xlabel("Time (Year)")
          pl.legend(loc= "upper left")
          pl.show()
          pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

that = SimpleDrawer()
that.drawCharts(which= 'High')
that.drawCharts('2020-01-01', '2021-02-01', 'High')
