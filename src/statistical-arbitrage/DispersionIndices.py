#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import pandas as pa
import DataWrapper as dw

from DataUtility import DataUtility

#
class DispersionIndices(object):

     wrapper: dw.DataWrapper

     #     
     def __init__(self) -> None:
          self.wrapper = dw.DataWrapper()
          pass

     # 
     def calc(self, symbol: str, start_date: str = '', close_date: str = '', label: str = '', which: str = 'Close') -> pa.DataFrame:
          try:

               start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
               close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

               sers: pa.Series = self.wrapper.getDataSet(symbol, start_date, close_date)[which]
               args = [DataUtility.round(sers.var()), DataUtility.round(sers.std()), DataUtility.round(sers.max() - sers.min())]
               args.append(sers.skew())
               args.append(sers.kurtosis())

               label = start_date + '~' + close_date

               argz = {
                    f"{symbol} ({label})": args
               }
               return pa.DataFrame(argz, index= ['variance', 'standard deviation', 'range', 'skewness', 'kurtosis'])
          except Exception as e:
               print(f'exception -> type = {type(e)}, args = {e.args}')
               return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

that = DispersionIndices()
df = that.calc('BTC')
df = that.calc('ETH')
df = that.calc('BTC', which= 'SRClose')
df = that.calc('ETH', which= 'SRClose')
df
