#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

#
class DataUtility(object):

     #
     def round(number: float) -> str:
          if (abs(number) >= 10):
               return str(number)[:str(number).index('.')]
          if ((abs(number) >= 1) and (abs(number) < 10)):
               return str(number)[:str(number).index('.') + 2]
          if ((abs(number) >= 0) and (abs(number) < 1)):
               return str(number)[:str(number).index('.') + 8]
          return str(number)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
