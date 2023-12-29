#!/bin/python3.10

# Canadaward
#
# The Canadaward is available to any Amateur who has submitted satisfactory evidence to RAC showing two-way communication with other Amateur stations in each province and territory of Canada.
#
#  - All contacts must be made after July 1, 1977.
#  - All contacts must be made from within the same DXCC entity.
#  - Contacts made by the same applicant using different call signs are permitted, although proof is required showing the applicant was holder of that call sign at the time the contact was made.
#  - Contacts made with stations using the VE0 prefix do not count towards this award.
#  - Contacts using repeaters do not count towards this award.
#
# https://www.rac.ca/operating/rac-operating-awards/

from termcolor import colored

from constants.constants import PROVINCE_PREFIXES, MODES, BANDS
from awards.canadian_award import CanadaOnlyAward

class Canadaward(CanadaOnlyAward) :

  def __init__(self, qso_list):
    super().__init__(qso_list)

    self.setupEndorsements()
    self.getCanadianOnlyCalls()
    self.printStatus("Canadaward")

  def getCanadianOnlyCalls(self):

    for qsl in self.qsl_list:
      for province in self.prefixes.keys():
        for prefix in self.prefixes[province]:
          if prefix in qsl.station:
            #Remove duplicate call sign confirmations:
            #If callsign exists in qsl list already do not add second instance
            if qsl.station not in self.canadian_qsl_list:
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
