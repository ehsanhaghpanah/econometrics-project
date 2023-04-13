#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import numpy as np
import pandas as pa
import matplotlib.pyplot as pl
import scipy.stats as ss
import seaborn as sb
import DataWrapper as dw
import warnings

from dataclasses import dataclass

warnings.filterwarnings("ignore")

@dataclass
class DrawArgs(object):
     vshow: list
     start_date: str = ''
     close_date: str = ''
     xlabel: str = ''
     ylabel: str = ''
     legend_location: str = 'upper right'
     title: str = '',
     label: str = ''

#
class Histograms(object):

     wrapper: dw.DataWrapper

     #     
     def __init__(self) -> None:
          self.wrapper = dw.DataWrapper()
          pass

     # 
     def drawAvecPDF(self, symbol: str, args: DrawArgs, which: str = 'Close', bins_count: int = 10) -> None:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(args.start_date) == 0) else args.start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(args.close_date) == 0) else args.close_date

          series: pa.Series = self.wrapper.getDataSet(symbol, start_date, close_date)[which]

          rg = np.linspace(series.min(), series.max(), num= 1000)
          mu = series.mean()
          sg = series.std()
          normal_pdf = ss.norm.pdf(rg, loc= mu, scale= sg)
          
          mu_label = f'{mu:.0f}' if mu >= 1.0 else f'{mu:.6f}'
          sg_label = f'{sg**2:.0f}' if sg >= 1.0 else f'{sg**2:.6f}'

          pdff = lambda x : ss.norm.pdf(x, loc= mu, scale= sg)

          vlnx = [(mu - 2 * sg), (mu - 1 * sg), mu, (mu + 1 * sg), (mu + 2 * sg)]
          ymin = normal_pdf.min()

          fig, ax = pl.subplots(1, 1, figsize= (8, 6))
          fig.set_dpi(75)
          ax.set_title(args.title, fontsize= 12)
          sb.distplot(series, kde= False, color= 'coral', norm_hist= True, ax= ax, bins= bins_count, label= args.label)
          ax.plot(rg, normal_pdf, 'maroon', lw= 3, label= f'N({mu_label}, {sg_label})')
          ax.set_ylabel(args.ylabel)
          ax.set_xlabel(args.xlabel)
          if (args.vshow[0]):
               ax.vlines(vlnx[0], ymin= ymin, ymax= pdff(vlnx[0]), lw= 2, linestyles= 'dotted', colors= 'maroon', label= 'µ-2σ')
          if (args.vshow[1]):
               ax.vlines(vlnx[1], ymin= ymin, ymax= pdff(vlnx[1]), lw= 3, linestyles= 'dotted', colors= 'maroon', label= 'µ-σ')
          if (args.vshow[2]):
               ax.vlines(vlnx[2], ymin= ymin, ymax= pdff(vlnx[2]), lw= 4, linestyles= 'dotted', colors= 'maroon', label= 'µ')
          if (args.vshow[3]):
               ax.vlines(vlnx[3], ymin= ymin, ymax= pdff(vlnx[3]), lw= 3, linestyles= 'dotted', colors= 'maroon', label= 'µ-σ')
          if (args.vshow[4]):
               ax.vlines(vlnx[4], ymin= ymin, ymax= pdff(vlnx[4]), lw= 2, linestyles= 'dotted', colors= 'maroon', label= 'µ+2σ')
          ax.legend(loc= args.legend_location)
          pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def draw1():
     that = Histograms()
     args = DrawArgs(
          xlabel = 'Price (in USDT), bins = 50', 
          ylabel = 'Frequency', 
          title = 'Price Distribution',
          label = 'BTCUSDT',
          vshow =  [False, True, True, True, True]
     )
     that.drawAvecPDF('BTC', args, bins_count= 50)

def draw2():
     that = Histograms()
     args = DrawArgs(
          xlabel = 'Price (in USDT), bins = 50', 
          ylabel = 'Frequency', 
          title = 'Price Distribution',
          label= 'ETHUSDT',
          vshow=  [False, True, True, True, True]
     )
     that.drawAvecPDF('ETH', args, bins_count= 50)

def draw3():
     that = Histograms()
     args = DrawArgs(
          xlabel = 'Simple Return, bins = 25', 
          ylabel = 'Frequency', 
          title = 'Return Distribution',
          label= 'BTCUSDT',
          legend_location= 'upper left',
          vshow=  [True, True, True, True, True]
     )
     that.drawAvecPDF('BTC', args, bins_count= 50, which= 'SRClose')

def draw4():
     that = Histograms()
     args = DrawArgs(
          xlabel = 'Simple Return, bins = 25', 
          ylabel = 'Frequency', 
          title = 'Return Distribution',
          label= 'ETHUSDT',
          legend_location= 'upper left',
          vshow=  [True, True, True, True, True]
     )
     that.drawAvecPDF('ETH', args, bins_count= 50, which= 'SRClose')

def draw5():
     that = Histograms()
     args = DrawArgs(
          start_date= '2021-12-27',
          close_date= '2022-05-12',
          xlabel = 'Price (in USDT), bins = 50', 
          ylabel = 'Frequency', 
          title = 'Price Distribution (2021-12-27~2022-05-12)',
          legend_location= 'upper left',
          label= 'BTCUSDT',
          vshow=  [True, True, True, True, True]
     )
     that.drawAvecPDF('BTC', args, bins_count= 50)

def draw6():
     that = Histograms()
     args = DrawArgs(
          start_date= '2021-12-27',
          close_date= '2022-05-12',
          xlabel = 'Price (in USDT), bins = 50', 
          ylabel = 'Frequency', 
          title = 'Price Distribution (2021-12-27~2022-05-12)',
          legend_location= 'upper left',
          label= 'ETHUSDT',
          vshow=  [True, True, True, True, True]
     )
     that.drawAvecPDF('ETH', args, bins_count= 50)

draw1()
draw2()
draw3()
draw4()
draw5()
draw6()
