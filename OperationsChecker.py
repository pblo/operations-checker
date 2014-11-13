#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math,sys,timeit
from OperationsCheckerException import OperationsCheckerException

class OperationsChecker():

  FIELDS_LEN = 5
  OPERANDS = { 
                     '*' : lambda(arg): arg[0]*arg[1],
                     '/' : lambda(arg): arg[0]/arg[1],
                     '+' : lambda(arg): arg[0]+arg[1],
                     '-' : lambda(arg): arg[0]-arg[1],
                     '^' : lambda(arg): math.pow(arg[0],arg[1]),
                   }
  data = []
  
  def readData(self, fileName):
    self.data = open(fileName).readlines()

  def validateData(self):
    try:
      self._currentRow = 1
      for row in self.data:
        row = row.strip().replace(',','.')
        fields = self._fields(row)
        self._validate(fields)
        if self._check(fields) == False: 
          print "Validation failed!"
          break
        self._currentRow += 1

      if len(self.data) == self._currentRow-1:
        print "OK\n"

    except OperationsCheckerException:
      print "Something wrong with data format, it should be csv with format: val1;val2;operant;result;priority"

  def _fields(self,row):
    return row.split(';')

  def _validate(self, fields):
    if len(fields) != self.FIELDS_LEN or \
                  fields[2].strip() not in self.OPERANDS or \
                  fields[4].lower() not in ('true','false'):
       raise OperationsCheckerException('Uncorrect data format.')

  def _readNumerics(self, fields):
    try:
      a = float(fields[0])
      b = float(fields[1])
      expected = float(fields[3])
    except ValueError:
      return False;

    return (a,b,expected)
    

  def _check(self,fields):
    priority = fields[4].lower()
    operand = fields[2].strip()
 
    data = self._readNumerics(fields)

    if (data == False and priority == 'true' ):
      self._debugFields(fields,3,None)
      return False
    
    if (data == False and priority == 'false' ):
      self._debugFields(fields,1,None)
      return True

    a,b,expected = data

    result = self.OPERANDS[operand]((a,b))

    if (expected != result and priority == 'true' ):
      self._debugFields(fields,2,result)
      return False

    if (expected != result and priority == 'false' ):
      self._debugFields(fields,1,result)

    return True

  def _debugFields(self, fields, mode, result):
    print fields
    if mode == 2:
      sys.stderr.write("Row: %s , Unexpected value, should be: %s\n"%(self._currentRow, result))
    elif mode == 3:
      sys.stderr.write("Row: %s , Not numeric value.\n"%(self._currentRow))

class OperationsCheckerException(Exception):
  pass

def timeprobe():
    operiationsChecker = OperationsChecker()
    operiationsChecker.readData(sys.argv[1])
    operiationsChecker.validateData()

if __name__ == '__main__':
  if len(sys.argv) < 2:
    sys.stderr.write('\nUsage: python %s filename.csv\n\n'%(sys.argv[0]))
    sys.exit(1)

  print "Time consumed: %s"%timeit.timeit('import OperationsChecker; OperationsChecker.timeprobe()', number = 1)
