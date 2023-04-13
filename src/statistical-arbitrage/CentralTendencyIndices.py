#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import pandas as pa
import DataWrapper as dw

from DataUtility import DataUtility

#
class CentralTendencyIndices(object):

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

               sers = self.wrapper.getDataSet(symbol, start_date, close_date)[which]
               args = [DataUtility.round(sers.mean()), DataUtility.round(sers.median()), DataUtility.round(sers.mode()[0])]

               label = start_date + '~' + close_date

               argz = {
                    f"{symbol} ({label})": args
               }
               return pa.DataFrame(argz, index= ['mean', 'median', 'mode'])
          except Exception as e:
               print(f'exception -> type = {type(e)}, args = {e.args}')
               return None

     # 
     def calcAvecCompare(self, start_date: str = '', close_date: str = '', which: str = 'Close') -> pa.DataFrame:
          try:

               start_date = str(self.wrapper.data_btc.index.min())[0:10] if (len(start_date) == 0) else start_date
               close_date = str(self.wrapper.data_btc.index.max())[0:10] if (len(close_date) == 0) else close_date

               sers_btc = self.wrapper.data_btc[start_date:close_date][which]
               sers_eth = self.wrapper.data_eth[start_date:close_date][which]
               args_btc = [DataUtility.round(sers_btc.mean()), DataUtility.round(sers_btc.median()), DataUtility.round(sers_btc.mode()[0])]
               args_eth = [DataUtility.round(sers_eth.mean()), DataUtility.round(sers_eth.median()), DataUtility.round(sers_eth.mode()[0])]

               label_btc = f'BTC({start_date}~{close_date})'
               label_eth = f'ETH({start_date}~{close_date})'

               args = {
                    label_btc: args_btc, 
                    label_eth: args_eth
               }
               return pa.DataFrame(args, index= ['mean', 'median', 'mode'])
          except Exception as e:
               print(f'exception -> type = {type(e)}, args = {e.args}')
               return None

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

that = CentralTendencyIndices()
df = that.calc('BTC')
df = that.calc('ETH')
df = that.calc('BTC', which= 'SRClose')
df = that.calc('ETH', which= 'SRClose')
df = that.calc('BTC', start_date= '2021-12-27', close_date= '2022-05-12')
df = that.calc('ETH', start_date= '2021-12-27', close_date= '2022-05-12')
df = that.calcAvecCompare(start_date= '2018-01-29', close_date= '2018-06-19')
df
