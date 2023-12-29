#!/bin/python3.10

from termcolor import colored 

from awards.base_award import BaseAward
from constants.constants import PROVINCE_PREFIXES, MODES, BANDS

class CanadaOnlyAward(BaseAward):
  canadian_qsl_list = {}
  provinces = {}

  def __init__(self, qso_list):
    super().__init__(qso_list)

    self.canadian_qsl_list = {}
    self.provinces = {}
    self.eligible = False

  def getQslCount(self):
    return len(self.canadian_qsl_list)

  def setupEndorsements(self):
    self.prefixes = PROVINCE_PREFIXES

    self.provinces = dict.fromkeys(self.prefixes.keys(), False)
    self.bands = {k: dict.fromkeys(self.provinces, False) for k in BANDS}
    self.modes = {k: dict.fromkeys(self.provinces, False) for k in MODES} 

  def printStatus(self, awardName):

    print(colored(awardName + " Eligibility:", attrs=['bold']), end="")
    print(" Total Eligibile Confirmed QSL's: ", end="")
    print(str(self.getQslCount()))
    
    self.printEligibility({"Basic Eligibility":self.checkBasicEligibility(self.provinces)})
    print("")
    
    print(colored("Mode Endorsements:", attrs=['bold']))
    self.printEligibility(self.checkDictEligibility(self.modes))
    print("")

    print(colored("Band Endorsements:", attrs=['bold']))
    self.printEligibility(self.checkDictEligibility(self.bands)) 
    print("")

    if self.eligible:
      self.printQslList()
      print("")

  def printEligibility(self, status):
    for endorsement in status.keys():
      print(endorsement + ": ", end="")
      if status[endorsement]:
        print(colored("Eligibile for award!", "green", attrs=['bold']))
      else:
        print(colored("Not eligible ", "red", attrs=['bold']))

  def checkBasicEligibility(self, provinces):
    for province in provinces.keys():
      if provinces[province] == False:
        return False
    self.eligible = True
    return True

  def checkDictEligibility(self, check):
    rtnDict = {}
    for key in check.keys():
      rtnDict[key] = self.checkBasicEligibility(check[key])
    return rtnDict 

  def printQslList(self):
    for qsl in self.canadian_qsl_list.values():
      qsl.printQSL() 
