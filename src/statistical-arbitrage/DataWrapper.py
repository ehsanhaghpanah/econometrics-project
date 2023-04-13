#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import pandas as pa
import numpy as np

from multipledispatch import dispatch

#
class DataWrapper(object):

     data_btc: pa.DataFrame
     data_eth: pa.DataFrame

     # class initializer
     def __init__(self) -> None:
          
          self.data_btc = self.__load__('data-csv\\btc_usdt.csv')
          self.data_eth = self.__load__('data-csv\\eth_usdt.csv')
          self.calcSR()
          self.calcLR()
          pass
     
     # loads raw data into pandas data frame(s)
     def __load__(self, path: str) -> pa.DataFrame:
          try:
               df: pa.DataFrame = pa.read_csv(path, index_col= 'OpenDate', parse_dates= True)
               df.index.rename('At', inplace= True)
               df.drop('CloseDate', inplace= True, axis= 1)
               df.drop('Unnamed: 0', inplace= True, axis= 1)
               return df
          except Exception as e:
               print(f'exception -> type = {type(e)}, args = {e.args}')
               return None

     # SR = Simple Return
     def calcSR(self) -> None:
          self.data_btc['SRClose'] = (self.data_btc['Close'] / self.data_btc['Close'].shift(1)) - 1
          self.data_eth['SRClose'] = (self.data_eth['Close'] / self.data_eth['Close'].shift(1)) - 1
          pass

     # LR = Logarithmic Return
     def calcLR(self) -> None:
          self.data_btc['LRClose'] = np.log(self.data_btc['Close'] / self.data_btc['Close'].shift(1))
          self.data_eth['LRClose'] = np.log(self.data_eth['Close'] / self.data_eth['Close'].shift(1))
          pass

     #
     @dispatch(str, int, int)
     def getDataSet(self, symbol: str, start_index: int, slice_count: int) -> pa.DataFrame:
          try:
               if (symbol.upper() in ['BTC', 'BTCUSD', 'BTCUSDT']):
                    return self.data_btc[start_index:start_index + slice_count]
               if (symbol.upper() in ['ETH', 'ETHUSD', 'ETHUSDT']):
                    return self.data_eth[start_index:start_index + slice_count]
               raise Exception(f"'{symbol}' Data Set Not Found!")
          except Exception as e:
               print(f'exception -> type = {type(e)}, args = {e.args}')
               return None

     #
     @dispatch(str, str, str)
     def getDataSet(self, symbol: str, start_date: str, close_date: str) -> pa.DataFrame:
          try:
               start_date = str(self.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
               close_date = str(self.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

               if (symbol.upper() in ['BTC', 'BTCUSD', 'BTCUSDT']):
                    return self.data_btc[start_date:close_date]
               if (symbol.upper() in ['ETH', 'ETHUSD', 'ETHUSDT']):
                    return self.data_eth[start_date:close_date]
               raise Exception(f"'{symbol}' Data Set Not Found!")
          except Exception as e:
               print(f'exception -> type = {type(e)}, args = {e.args}')
               return None

     #
     @dispatch(str)
     def getDataSet(self, symbol: str) -> pa.DataFrame:
          return self.getDataSet(symbol, '', '')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
