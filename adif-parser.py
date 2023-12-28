#!/bin/python3.10

import adif_io
import sys

from termcolor import colored

print(sys.argv[1:])

qsos, header = adif_io.read_from_file(sys.argv[1])

PRINT_DUPLICATES = False
#PRINT_LOTW_ONLY = False 
PRINT_LOTW_ONLY = True
PRINT_QSL_STATUS = False

MAX_PROVINCE_COUNT = 20

total_count = 0
province_count = {}

PROVINCE_DICTIONARY = {"NOVA_SCOTIA":["VA1","VE1","VC1"],
                       "QUEBEC": ["VA2","VE2","VC2"],
                       "ONTARIO": ["VA3","VE3", "VC3"],
                       "MANITOBA": ["VA4","VE4","VC4"],
                       "SASKATCHEWAN": ["VA5","VE5","VC5"],
                       "ALBERTA": ["VA6","VE6","VC6"],
                       "BRITISH_COLUMBIA": ["VA7","VE7","VC7"],
                       "NORTHWEST_TERRITORIES": ["VE8", "VC8"],
                       "NEW_BRUNSWICK": ["VA9","VE9", "VC9"],
                       "YUKON": ["VY1"],
                       "NUNAVUT": ["VY0"],
                       "PEI": ["VY2"],
                       "LABRADOR": ["VO1"],
                       "NEWFOUNDLAND": ["VO2"],
                       "SPECIAL": ["VC", "VY", "CY"]}

for province in PROVINCE_DICTIONARY.keys():
  province_count[province] = 0

#print(province_count)

callsigns = []

for qso in qsos:
  if(qso["APP_QRZLOG_STATUS"] == "C"):
    duplicate = False
    lotw = False

    qsod = qso["QSO_DATE"]
    qsot = qso["TIME_OFF"]
    qsop = ""

    call = qso["CALL"]
    if call in callsigns:
      duplicate = True
      if PRINT_DUPLICATES:
        print(colored("DUPLICATE: ","red", attrs=['bold']), end="")
    else:
      callsigns.append(call)

    for province in PROVINCE_DICTIONARY.keys():
      for prefix in PROVINCE_DICTIONARY[province]:
        if prefix in call:
          qsop = province
          if not duplicate and province_count[province] < MAX_PROVINCE_COUNT:
            province_count[province] += 1
          elif not duplicate:
            print(colored("Province count exceeded for province: " + province + "!", "red", attrs=['bold']) + " Excluding: " + call)
            duplicate = True
          break
      if qsop != "":
        break

    if qsop == "":
      raise Exception("NO VALID PROVINCE FOUND")

    qsl = []
    if qso["APP_QRZLOG_STATUS"] == "C":
      qsl.append("QRZ")
    try:
      if qso["LOTW_QSL_RCVD"] == "Y":
        qsl.append("LOTW")
        lotw = True
    except:
      continue

    if PRINT_DUPLICATES or not duplicate:
      if lotw or not PRINT_LOTW_ONLY:
        if PRINT_QSL_STATUS:
          if lotw:
            print(colored("LOTW/QRZ CONFIRMED: ","green", attrs=['bold']), end="")
          else:
            print(colored("QRZ CONFIRMED ONLY: ","yellow", attrs=['bold']), end="")
        print(", ".join([qso["CALL"],
              '-'.join([qsod[:4], qsod[4:6], qsod[6:]]),
              ':'.join([qsot[:2], qsot[2:]]),
              qso["BAND"],
              qso["MODE"],
              qsop,
              '/'.join(qsl)]))
        total_count += 1

print("Total QSL's: " + str(total_count))
print("Province counts: " + str(province_count).replace("{","").replace("}","").replace("'",""))
