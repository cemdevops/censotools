# -*- coding: utf-8 -*-

# CENSO APP
# Class themeXLS
# Keep content of a XLS Theme file.
#
# The order of the variables in the class will be the order that they are in XLS file

import sys;
import xlrd;

reload(sys)  
sys.setdefaultencoding('utf8')

# Indexes
IDX_THEME_ID = 0;
IDX_THEME_COLLECTION = 1;
IDX_THEME_THEMEID = 2;
IDX_THEME_LABEL = 3;
IDX_THEME_DESC = 4;
IDX_THEME_AVAILABLE = 5;

# Class representing theme XLS file
class themeXLSFile:

  def __init__ (self, strFile):
    #print "str|File=",strFile;
    self.file = strFile;

    self.bolHeaderExists = True; # indicate if there is a header
    self.arrayTheme = []; # array to store variables
    self.intNumThemes = 0;
    self.intCurrentIdxTheme = 0; # indicate index of current variable
    # Object to keep current variable
    self.objCurrentTheme = {
      "_id": 0,           # int
      "collection": "",   # str
      "themeId": 0,       # int
      "label": "",        # str
      "description": "",  # str
      "avaiable": 1,      # int
      "obs": ""           # str
    };
  # End - def __init__ (self, strFile):
    
  # Function to load XLS file.
  def loadFile (self, strFile, censoId, dataTypeId, intCenso, strDataType):
    self.file = strFile;
    print "Theme file:", self.file;
    # Open XLS file
    try:
      workbook = xlrd.open_workbook(strFile);
    except Exception as e:
      print "Erro ao abrir arquivo", strFile;
      return (2);
    
    # Open worksheet (0)
    try:
      sheet = workbook.sheet_by_index(0);
    except Exception as e:
      print "Erro ao abrir aba em", strFile;
      return (3);

    # Get lines in XLS file
    intXlsLine = 0;
    for linhaXLS in range (sheet.nrows): # for each line of XLS file do...
      # Update XLS line count
      intXlsLine = intXlsLine + 1;
      # Get cols of the line
      cols = sheet.row_values(linhaXLS);
      # check if it is the first line (header)
      if (self.bolHeaderExists and intXlsLine == 1):
        # Header is being checked. Ignore.
        print "Cabeçalho do XLS de tema será ignorado."
      else:
        # Get values from XLS file.
        # Create new theme object
        objCurrentTheme = {
          "_id": 0,           # int
          "collection": "",   # str
          "themeId": 0,       # int
          "label": "",        # str
          "description": "",  # str
          "avaiable": 1,      # int
        };

        # Update theme values in object
        objCurrentTheme ["_id"] = int (cols [IDX_THEME_ID]);
        objCurrentTheme ["collection"] = cols [IDX_THEME_COLLECTION].strip();
        objCurrentTheme ["themeId"] = int (cols [IDX_THEME_THEMEID]);
        objCurrentTheme ["label"] = cols [IDX_THEME_LABEL].strip(); # Get variable label
        objCurrentTheme ["description"] = cols [IDX_THEME_DESC].strip(); # Get variable description
        objCurrentTheme ["avaiable"] = int (cols [IDX_THEME_AVAILABLE]);

        # Add variable to variable array
        self.arrayTheme.append (objCurrentTheme);
        self.intNumThemes = self.intNumThemes + 1;
        # Update current variable object
        self.objCurrentTheme = objCurrentTheme;
      # End - (else) if self.bolHeaderExists and intLine == 1:
    # End - for linhaXLS in range (sheet.nrows):

    # OK. Return 0.
    return(0);
  # End - def loadFile (self, strFile, censoId, dataTypeId, intCenso, strDataType):

  def getNumberOfThemes (self):
    #print self.intNumVariables, len (self.arrayVariable);
    return self.intNumThemes;
  # End - def getNumberOfVariables (self):

  def getCurrentTheme (self):
    return self.objCurrentTheme;
  # End - def getCurrentVariable (self):

  def getTheme (self, idxTheme):
    return self.arrayTheme [idxTheme];
  # End - def getVariable (self, idxVariable):

  def getFile (self):
    return self.file;
  # End - def getFile (self):

  def getThemeLabel (self, idxTheme):
    return self.arrayTheme [idxTheme]["label"];
  # End - def getThemeLabel (self, idxTheme)

  def getThemeColl (self, idxTheme):
    return self.arrayTheme [idxTheme]["collection"];
  # End - def getThemeLabel (self, idxTheme)

# End -class metadataXLSFile:
