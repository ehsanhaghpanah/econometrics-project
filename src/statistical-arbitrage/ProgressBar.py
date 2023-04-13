#
# Copyright (C) Remittan (remittan.com), 2023.
# All rights reserved.
# Ehsan Haghpanah; haghpanah@remittan.com
#

import sys

#
class ProgressBar(object):

     maxValue: int
     minValue: int = 0
     value: int

     #     
     def __init__(self, min: int, max: int) -> None:
          self.minValue = min
          self.maxValue = max
          self.value = min
          pass

     #
     def setValue(self, value: int) -> None:
          if ((self.minValue > value) or (value > self.maxValue)):
               pass
          self.value = value
          v = (self.value - self.minValue) / (self.maxValue - self.minValue)
          i = int(v * 20)
          sys.stdout.write('\r')
          sys.stdout.write("[%-20s] %d%%" % ('=' * i, 5 * i))
          sys.stdout.flush()
     
     #
     def clear(self):
          sys.stdout.write('\n')
          sys.stdout.flush()
          pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
