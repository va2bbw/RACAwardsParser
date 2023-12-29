#!/bin/python3.10

#Worked All RAC Award
#
#The WARAC award is available to any Amateur who has submitted satisfactory evidence to RAC showing two-way communication with at least 10 official RAC stations.
#
#The Official RAC stations are VA1RAC, VA2RAC, VA3RAC, VA4RAC, VA5RAC, VA6RAC, VA7RAC, VE1RAC, VE3RAC, VE4RAC, VE5RAC, VE6RAC, VE7RAC, VE8RAC, VE9RAC, VO1RAC, VO2RAC, VY0RAC, VY1RAC, VY2RAC, VA3RHQ and VE3RHQ.
#
# - All contacts must be made after July 1, 1998.
# - All contacts must be made from within the same DXCC entity.
# - Contacts made by the same applicant using different call signs are permitted, although proof is required showing the applicant was holder of that call sign at the time the contact was made.
# - Contacts using repeaters do not count towards this award.
# - For call areas having two official stations, only one of the two counts towards the total of 10 stations required for the award.

from constants.constants import RAC_STATIONS
from awards.canadian_award import CanadaOnlyAward

class WARAC(CanadaOnlyAward):

  def __init__(self, qso_list):
    super().__init__(qso_list)

    self.setupEndorsements()
    self.getCanadianOnlyCalls()
    self.printStatus("WARAC")

  def getCanadianOnlyCalls(self):
    for qsl in self.qsl_list:
      for province in self.prefixes.keys():
        for prefix in self.prefixes[province]:
          if prefix in qsl.station:
            #Remove duplicate call sign confirmations:
            #If callsign exists in qsl list already do not add second instance
            if qsl.station not in self.canadian_qsl_list:
              if qsl.station in RAC_STATIONS:
                self.canadian_qsl_list[qsl.station] = qsl

                # Calculate basic qualification
                self.provinces[province] = True

                # Calculate band endorsement
                self.bands[qsl.band][province] = True

                #Calculate mode endorsement
                self.modes["MIXED"][province] = True
                if qsl.digital: self.modes["DIGITAL"][province] = True
                if qsl.phone: self.modes["PHONE"][province] = True
                if qsl.cw: self.modes["CW"][province] = True
