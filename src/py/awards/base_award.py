#!/bin/python3.10

# Base award class

import traceback
import json
from termcolor import colored

from abc import ABC, abstractmethod
from constants.constants import LOTW_QSL_CONFIRMED_KEYS, QRZ_QSL_CONFIRMED_KEYS, PHONE, DIGITAL, CW
from config.config import QRZ_CONFIRMATION, LOTW_CONFIRMATION

class BaseAward(ABC):

  qsl_list = []

  def __init__(self, qso_list):
    self.qso_list = qso_list
    self.getQsl(self.qso_list)

  @abstractmethod
  def printStatus(self):
    pass

  #========================== Methods ==========================#

  def getQslCount(self):
    if len(self.qsl_list) == 0:
      raise Exception("QSL List is either empty or not parsed (run: getQsl(qso_list))")
    else:
      return len(self.qsl_list)

  def getQsl(self, qso_list):
    keyList = {}
    if LOTW_CONFIRMATION:
      keyList.update(LOTW_QSL_CONFIRMED_KEYS)
    if QRZ_CONFIRMATION:
      keyList.update(QRZ_QSL_CONFIRMED_KEYS)

    for qso in qso_list:
      for key in keyList.keys():
        try:
          #Check if QSL is confirmed based on keys from constants.QSL_CONFIRMED_KEYS
          if qso[key] == keyList[key][0]:
            self.qsl_list.append(QSL(qso, keyList[key][1]))
            break
        except:
          continue
    return self.qsl_list

  #======================== End Methods ========================#

class QSL:

  station = ""
  band = ""
  mode = ""
  time = ""
  date = ""
  qsl_method = ""

  digital = False
  phone = False
  cw = False

  def __init__(self, qsl, qsl_method="LOTW"):
    try:
      self.station     = qsl["CALL"].upper()
      self.band        = qsl["BAND"].upper()
      self.time        = ':'.join([qsl["TIME_ON"][:2], qsl["TIME_ON"][2:]])
      self.qsl_method  = qsl_method

      try:
        self.mode = qsl["SUBMODE"]
      except:
        self.mode = qsl["MODE"]

      try:
        self.date      = '-'.join([qsl["QSO_DATE"][:4], qsl["QSO_DATE"][4:6], qsl["QSO_DATE"][6:]])
      except:
        self.date      = '-'.join([qsl["QSO_DATE_OFF"][:4], qsl["QSO_DATE_OFF"][4:6], qsl["QSO_DATE_OFF"][6:]])

      if self.mode in PHONE: self.phone = True
      if self.mode in DIGITAL: self.digital = True
      if self.mode in CW: self.cw = True

    except Exception as e:
      print("QSL did not match expected key format")
      print(json.dumps(qsl, indent=2))
      traceback.print_exc()

  def printQSL(self):
    print(', '.join([self.station, self.date, self.time, self.band, self.mode, self.qsl_method]))


