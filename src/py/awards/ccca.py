#!/bin/python3.10

#Canadian Century Club Award
#
#The Canadian Century Club Award is available to any Amateur who has submitted satisfactory evidence to RAC showing two-way communication with at least 100 different Amateur stations in Canada.
#
# - Of the 100 contacts, a minimum of one contact must be made with a station in each province, and one contact must be made with a station in any of the three territories.
# - Of the 100 contacts, no more than 20 can be made with stations from a single province, and no more than 20 contacts can be made with stations located in any of the three territories.
# - All contacts must be made after 1945.
# - All contacts must be made from within the same DXCC entity.
# - Contacts made by the same applicant using different call signs are permitted, although proof is required showing the applicant was holder of that call sign at the time the contact was made.
# - Contacts made with stations using the VE0 prefix do not count towards this award.
# - Contacts using repeaters do not count towards this award.
# - There are no endorsements available for the Canadian Century Club.

from termcolor import colored

from constants.constants import CCCA_PREFIXES, CCCA_TOTAL
from awards.canadian_award import CanadaOnlyAward

class CCCA(CanadaOnlyAward):

  def __init__(self, qso_list):
    super().__init__(qso_list)

    self.setupEndorsements()
    self.getCanadianOnlyCalls()
    self.printStatus("Canadian Century Club Award")

  def setupEndorsements(self):
    self.prefixes = CCCA_PREFIXES

    self.provinces = dict.fromkeys(self.prefixes.keys(), False)

  def getCanadianOnlyCalls(self):
    self.province_count = dict.fromkeys(CCCA_PREFIXES, 0)

    for qsl in self.qsl_list:
      for province in self.prefixes.keys():
        for prefix in self.prefixes[province]:
          if prefix in qsl.station:
            #Remove duplicate call sign confirmations:
            #If callsign exists in qsl list already do not add second instance
            if qsl.station not in self.canadian_qsl_list:
              if self.province_count[province] < 20:
                self.province_count[province] += 1

                self.canadian_qsl_list[qsl.station] = qsl
                if len(self.canadian_qsl_list) >= CCCA_TOTAL:
                  self.eligible = True
                  return

  def printStatus(self, awardName):
    print(colored(awardName + " Eligibility:", attrs=['bold']), end="")
    print(" Total Eligibile Confirmed QSL's: ", end="")
    print(str(self.getQslCount()))

    self.printEligibility({"Basic Eligibility":self.eligible})
    print("")

    if self.eligible:
      self.printQslList()
      print("")
