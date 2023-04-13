#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import pandas as pa
import DataWrapper as dw
import scipy.stats as ss
import ProgressBar as pb

from multipledispatch import dispatch

#
class NormalDistributionChecker(object):

     wrapper: dw.DataWrapper

     #     
     def __init__(self) -> None:
          self.wrapper = dw.DataWrapper()
          pass

     #
     @dispatch(str, int, int, str)
     def checkByShapiroWilk(self, symbol: str, start_index: int, slice_count: int, which: str) -> bool:
          series: pa.Series = self.wrapper.getDataSet(symbol, start_index, slice_count)[which]
          series = series.dropna()

          result: ss.ShapiroResult = ss.shapiro(series)
          print(f'symbol = {symbol}, result = {result}')
          return True if (result.pvalue > 0.05) else False

     #
     @dispatch(str, int, int)
     def checkByShapiroWilk(self, symbol: str, start_index: int, slice_count: int) -> bool:
          return self.checkByShapiroWilk(symbol, start_index, slice_count, 'Close')

     #
     @dispatch(str, str, str, str)
     def checkByShapiroWilk(self, symbol: str, start_date: str, close_date: str, which: str) -> bool:
          series: pa.Series = self.wrapper.getDataSet(symbol, start_date, close_date)[which]
          series = series.dropna()

          result: ss.ShapiroResult = ss.shapiro(series)
          print(f'symbol = {symbol}, result = {result}')
          return True if (result.pvalue > 0.05) else False

     #
     @dispatch(str, str, str)
     def checkByShapiroWilk(self, symbol: str, start_date: str, close_date: str) -> bool:
          return self.checkByShapiroWilk(symbol, start_date, close_date, 'Close')

     #
     @dispatch(str)
     def checkByShapiroWilk(self, symbol: str, start_date: str = '', close_date: str = '', which: str = 'Close') -> bool:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

          return self.checkByShapiroWilk(symbol, start_date, close_date, which)

     #
     @dispatch(str, int, int, str)
     def checkByAndersonDarling(self, symbol: str, start_index: int, slice_count: int, which: str) -> bool:
          series: pa.Series = self.wrapper.getDataSet(symbol, start_index, slice_count)[which]
          series = series.dropna()
          
          result: ss.AndersonResult = ss.anderson(series)
          va = result.statistic
          la: list = list(result.significance_level)
          lb: list = list(result.critical_values)
          vb = lb[la.index(5.0)]
          print(f'symbol = {symbol}, result = {result}')
          return True if (va < vb) else False

     #
     @dispatch(str, int, int)
     def checkByAndersonDarling(self, symbol: str, start_index: int, slice_count: int) -> bool:
          return self.checkByAndersonDarling(symbol, start_index, slice_count, 'Close')

     #
     @dispatch(str, str, str, str)
     def checkByAndersonDarling(self, symbol: str, start_date: str, close_date: str, which: str) -> bool:
          series: pa.Series = self.wrapper.getDataSet(symbol, start_date, close_date)[which]
          series = series.dropna()

          result: ss.AndersonResult = ss.anderson(series)
          va = result.statistic
          la: list = list(result.significance_level)
          lb: list = list(result.critical_values)
          vb = lb[la.index(5.0)]
          print(f'symbol = {symbol}, result = {result}')
          return True if (va < vb) else False

     #
     @dispatch(str, str, str)
     def checkByAndersonDarling(self, symbol: str, start_date: str, close_date: str) -> bool:
          return self.checkByAndersonDarling(symbol, start_date, close_date, 'Close')

     #
     @dispatch(str)
     def checkByAndersonDarling(self, symbol: str, start_date: str = '', close_date: str = '', which: str = 'Close') -> bool:

          start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
          close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

          return self.checkByAndersonDarling(symbol, start_date, close_date, which)

     #
     def findMaxSubsetByShapiroWilk(self, which: str = 'Close') -> tuple:
          try:
               found = False
               data_frame_size = len(self.wrapper.data_btc)
               progressBar = pb.ProgressBar(max= data_frame_size, min= 30)
               for range_count in range(data_frame_size, 30, -1):
                    progressBar.setValue(data_frame_size - range_count)
                    for start_index in range(0, data_frame_size - range_count):
                         is_normal_btc = self.checkByShapiroWilk('BTC', start_index, range_count, which)
                         is_normal_eth = self.checkByShapiroWilk('ETH', start_index, range_count, which)
                         if (is_normal_btc and is_normal_eth):
                              found = True
                              break
                    if (found):
                         break
               progressBar.clear()
               start_date = self.wrapper.data_btc.index[start_index]
               close_date = self.wrapper.data_btc.index[start_index + range_count]
               return start_index, range_count, start_date, close_date
          except Exception as e:
               progressBar.clear()
               print(f'exception -> type = {type(e)}, args = {e.args}')
               return 0, 0, None, None

     #
     def findMaxSubsetByAndersonDarling(self, which: str = 'Close') -> tuple:
          try:
               found = False
               data_frame_size = len(self.wrapper.data_btc)
               progressBar = pb.ProgressBar(max= data_frame_size, min= 30)
               for range_count in range(data_frame_size, 30, -1):
                    progressBar.setValue(data_frame_size - range_count)
                    for start_index in range(0, data_frame_size - range_count):
                         is_normal_btc = self.checkByAndersonDarling('BTC', start_index, range_count, which)
                         is_normal_eth = self.checkByAndersonDarling('ETH', start_index, range_count, which)
                         if (is_normal_btc and is_normal_eth):
                              found = True
                              break
                    if (found):
                         break
               progressBar.clear()
               start_date = self.wrapper.data_btc.index[start_index]
               close_date = self.wrapper.data_btc.index[start_index + range_count]
               return start_index, range_count, start_date, close_date
          except Exception as e:
               progressBar.clear()
               print(f'exception -> type = {type(e)}, args = {e.args}')
               return 0, 0, None, None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#
def present(start_index: int, range_count: int, start_date: str, close_date: str):
     args: list = []
     args.append(start_index)
     args.append(range_count)
     args.append(str(start_date)[0:10])
     args.append(str(close_date)[0:10])
     argz = {
          'Normal Distributed Range':args
     }
     return pa.DataFrame(argz, index= ['start index', 'range count', 'start date', 'close date'])

that = NormalDistributionChecker()
that.checkByShapiroWilk('BTC')
that.checkByShapiroWilk('ETH')
that.checkByShapiroWilk('BTC', which= 'SRClose')
that.checkByShapiroWilk('ETH', which= 'SRClose')
that.checkByAndersonDarling('BTC')
that.checkByAndersonDarling('ETH')
that.checkByAndersonDarling('BTC', which= 'SRClose')
that.checkByAndersonDarling('ETH', which= 'SRClose')

print(that.checkByShapiroWilk('BTC', 100, 50))
print(that.checkByShapiroWilk('ETH', 100, 50))
print(that.checkByShapiroWilk('BTC', '2020-01-01', '2020-11-10'))
print(that.checkByShapiroWilk('ETH', '2020-01-01', '2020-11-10'))
print(that.checkByShapiroWilk('ETH', '2021-12-27', '2022-05-12'))
print('=====')
print(that.checkByAndersonDarling('BTC', 100, 50))
print(that.checkByAndersonDarling('ETH', 100, 50))
print(that.checkByAndersonDarling('BTC', '2020-01-01', '2020-11-10'))
print(that.checkByAndersonDarling('ETH', '2020-01-01', '2020-11-10'))
print(that.checkByAndersonDarling('BTC', '2021-12-27', '2022-05-12'))
print('=====')

# si, rc, sd, cd = that.findMaxSubsetByShapiroWilk()
# df = present(start_index= si, range_count= rc, start_date= sd, close_date= cd)
# df
# si, rc, sd, cd = that.findMaxSubsetByAndersonDarling()
# df = present(start_index= si, range_count= rc, start_date= sd, close_date= cd)
# df
