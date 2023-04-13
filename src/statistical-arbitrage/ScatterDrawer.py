#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import numpy as np
import DataWrapper as dw
import matplotlib.pyplot as pl

from matplotlib.pyplot import figure

#
class ScatterDrawer(object):

     wrapper: dw.DataWrapper

     #     
     def __init__(self) -> None:
          self.wrapper = dw.DataWrapper()
          pass

     #
     def drawAvecColors(self, start_date: str = '', close_date: str = '', which: str = 'Close') -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

          x = self.wrapper.getDataSet('BTCUSD', start_date, close_date)[which]
          y = self.wrapper.getDataSet('ETHUSD', start_date, close_date)[which]
          
          colors = np.random.rand(len(x))
          alphas = np.random.uniform(low= 0.01, high= 0.99, size= len(x))

          figure(figsize= (8, 6), dpi= 75)
          pl.scatter(x, y, c= colors, alpha= alphas)
          pl.ylabel(f'ETHUSDT ({which})')
          pl.xlabel(f'BTCUSDT ({which})')
          pl.show()          
          pass

     #
     def drawBubbles(self, start_date: str = '', close_date: str = '', which: str = 'Close') -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

          x = self.wrapper.getDataSet('BTCUSD', start_date, close_date)[which]
          y = self.wrapper.getDataSet('ETHUSD', start_date, close_date)[which]
          
          # 
          figure(figsize= (8, 6), dpi= 75)
          pl.scatter(x, y, s= 80, facecolors= 'none', edgecolors= 'r', alpha= 0.5)
          pl.ylabel(f'ETHUSDT ({which})')
          pl.xlabel(f'BTCUSDT ({which})')
          pl.show()
          pass
     #
     def drawAvecCurveFit(self, start_date: str = '', close_date: str = '', title:str = '', which: str = 'Close') -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

          x = self.wrapper.getDataSet('BTCUSD', start_date, close_date)[which]
          y = self.wrapper.getDataSet('ETHUSD', start_date, close_date)[which]
          
          l = np.polyfit(x, y, 1)
          p = np.poly1d(l)
          
          xa, xb = x.min(), x.max()
          ya, yb = p(xa), p(xb)

          alphas = np.random.uniform(low= 0.01, high= 0.99, size= len(x))

          # 
          figure(figsize= (8, 6), dpi= 75)
          pl.scatter(x, y, s= 80, facecolors= 'skyblue', edgecolors= 'skyblue', alpha= alphas)
          pl.suptitle(title)
          pl.plot([xa, xb], [ya, yb], 'gray')
          pl.ylabel(f'ETHUSDT ({which})')
          pl.xlabel(f'BTCUSDT ({which})')
          pl.show()
          pass

     #
     def drawAvecCurveFitColors(self, start_date: str = '', close_date: str = '', title:str = '', which: str = 'Close') -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

          x = self.wrapper.getDataSet('BTCUSD', start_date, close_date)[which]
          y = self.wrapper.getDataSet('ETHUSD', start_date, close_date)[which]
          
          l = np.polyfit(x, y, 1)
          p = np.poly1d(l)
          
          xa, xb = x.min(), x.max()
          ya, yb = p(xa), p(xb)

          colors = np.random.rand(len(x))

          figure(figsize= (8, 6), dpi= 75)
          pl.scatter(x, y, c= colors)
          pl.suptitle(title)
          pl.plot([xa, xb], [ya, yb], 'coral', lw= '2')
          pl.ylabel(f'ETHUSDT ({which})')
          pl.xlabel(f'BTCUSDT ({which})')
          pl.show()          
          pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

that = ScatterDrawer()
that.drawAvecColors()
that.drawAvecCurveFit()
that.drawAvecCurveFitColors(title= 'Cointegration')
that.drawAvecCurveFitColors(start_date= '2021-12-27', close_date= '2022-05-12', title= 'Cointegration')
that.drawAvecColors(which= 'SRClose')
that.drawBubbles(which= 'SRClose')
that.drawAvecColors('2021-12-27', '2022-05-12')
that.drawBubbles('2021-12-27', '2022-05-12')
