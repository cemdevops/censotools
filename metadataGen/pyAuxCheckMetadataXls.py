# -*- coding: utf-8 -*-

# CENSO APP
# Class metadataXLSFile
# Keep content of a XLS Metadata file.
#
# The order of the variables in the class will be the order that they are in XLS file

import sys;
import xlrd;

reload(sys)  
sys.setdefaultencoding('utf8')

# Indexes
IDX_REG_TYPE = 0; # Type of registry (1-Layout & metadata, 2-layout only, 3-metadata only, 4-Information only, 5-Processed, 6-Processed and metadata)
IDX_VARIABLE = 1;
IDX_LABEL = 2;
IDX_DESC = 3;
IDX_POPTOAPPLY = 4;
IDX_OBS = 5;
IDX_THEME = 6;
IDX_INIC_POS = 7;
IDX_FINAL_POS = 8;
IDX_INT_SIZE = 9;
IDX_DEC_SIZE = 10;
IDX_TYPE = 11; # Type of variable (N - Numeric)
IDX_CAT = 12;
IDX_CAT_TYPE = 13; # Type of categories (0-Collection, 1-Categories one selection, 2-)
IDX_MANDATORY = 14; # Type of categories (0-Collection, 1-Categories one selection, 2-)

# Registry types
REG_LAYOUT_METADATA = 1
REG_LAYOUT_ONLY = 2
REG_METADATA_ONLY = 3
REG_INFO_ONLY = 4
REG_PROCESSED = 5
REG_PROCESSED_METADATA = 6
REG_HARMONIZED = 7
REG_HARMONIZED_METADATA = 8

# Category types
CATEGORY_COLLECTION = 0
CATEGORY_ONE_SELECTION = 1
CATEGORY_MULTI_SELECTION = 2
CATEGORY_NUMERIC_VALUE = 3
CATEGORY_NUMERIC_VALUE_CATEG = 4
CATEGORY_COLLECTION_CATEG = 5
CATEGORY_EXTENDED = 6

strEndLine = "\n";
strSeparator = "*->";

# Class representing metadata XLS file
class metadataXLSFile:

  def __init__ (self, strFile):
    #print "str|File=",strFile;
    self.file = strFile;
    self.fileExt = [];
    self.fileExt.append ("fileExt");

    self.bolHeaderExists = True; # indicate if there is a header
    self.intNumVariables = 0; # keep number of variables in XLS file
    self.arrayVariable = []; # array to store variables
    self.intCurrentIdxVariable = 0; # indicate index of current variable
    # Object to keep current variable
    self.objCurrentVariable = {
      "_id": 0,           # int
      "collectionId": 0,  # int
      "sourceId": 0,      # int
      "regType": 0,       # int
      "varCode": "",      # str
      "label": "",        # str
      "description": "",  # str
      "popToApply": "",   # str
      "obs": "",          # str
      "strTheme": "",     # str
      "themeId": 0,       # int
      "original": "",     # str
      "dataType": "",     # str
      "inicPos": 0,       # int
      "finalPos": 0,      # int
      "intSize": 0,       # int
      "decSize": 0,       # int
      "showInPage": 1,    # int
      "mandatory": 0,     # int
      "catType": 0,       # int
      "category": []      # array
    };
  # End - def __init__ (self, strFile):
    
  def add_file_ext (self, strAux):
    self.fileExt [0] = strAux;
  # End - def add_file_ext (self, strAux):

  # Function to load XLS file.
  def loadFile (self, strFile, censoId, dataTypeId, intCenso, strDataType, objThemeMongo):
    self.file = strFile;
    print "File:", self.file;
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
      intCurrentNumCategory = 0; # num of categories in this variable
      # Get cols of the line
      cols = sheet.row_values(linhaXLS);
      # check if it is the first line (header)
      if (self.bolHeaderExists and intXlsLine == 1):
        # Header is being checked. Ignore.
        print strFile, "- Cabeçalho do XLS será ignorado."
      else:
        # Check if registry is Metadata
#        if (cols [IDX_REG_TYPE] == 8 or cols [IDX_REG_TYPE] == REG_LAYOUT_METADATA or
#            cols [IDX_REG_TYPE] == REG_METADATA_ONLY or cols [IDX_REG_TYPE] == REG_PROCESSED_METADATA):

        # Get values from XLS file.
        # Create new variable object
        objCurrentVariable = {
          "_id": 0,           # int
          "collectionId": 0,  # int
          "sourceId": 0,      # int
          "regType": 0,       # int
          "varCode": "",      # str
          "label": "",        # str
          "description": "",  # str
          "popToApply": "",   # str
          "obs": "",          # str
          "strTheme": "",     # str
          "themeId": 0,       # int
          "original": "",     # str
          "dataType": "",     # str
          "inicPos": 0,       # int
          "finalPos": 0,      # int
          "intSize": 0,       # int
          "decSize": 0,       # int
          "showInPage": 1,    # int
          "mandatory": 0,     # int
          "catType": 0,       # int
          "category": []      # array
        };

        # Update variable values in object
        objCurrentVariable ["_id"] = intXlsLine;
        objCurrentVariable ["collectionId"] = dataTypeId;
        objCurrentVariable ["sourceId"] = censoId;
        objCurrentVariable ["regType"] = int (cols [IDX_REG_TYPE]);
        objCurrentVariable ["varCode"] = cols [IDX_VARIABLE].strip(); # Get variable name
        objCurrentVariable ["label"] = cols [IDX_LABEL].strip(); # Get variable label
        objCurrentVariable ["description"] = cols [IDX_DESC].strip(); # Get variable description
        objCurrentVariable ["popToApply"] = cols [IDX_POPTOAPPLY].strip(); # Get variable population to apply
        objCurrentVariable ["obs"] = cols [IDX_OBS].strip(); # Get variable observation
        objCurrentVariable ["strTheme"] = cols [IDX_THEME].strip(); # Get variable theme
        if (cols [IDX_INIC_POS] != ""):
          objCurrentVariable ["inicPos"] = int (cols [IDX_INIC_POS]);
        else:
          objCurrentVariable ["inicPos"] = 0;
        if (cols [IDX_FINAL_POS] != ""):
          objCurrentVariable ["finalPos"] = int (cols [IDX_FINAL_POS]);
        else:
          objCurrentVariable ["finalPos"] = 0;
        if (cols [IDX_INT_SIZE] != ""):
          objCurrentVariable ["intSize"] = int (cols [IDX_INT_SIZE]);
        else:
          objCurrentVariable ["intSize"] = 0;
        if (cols [IDX_DEC_SIZE] != ""):
          objCurrentVariable ["decSize"] = int (cols [IDX_DEC_SIZE]);
        else:
          objCurrentVariable ["decSize"] = 0;
        objCurrentVariable ["dataType"] = cols [IDX_TYPE].strip(); # Get variable type
        if (cols [IDX_CAT_TYPE] == ""):
          print "Erro:", intXlsLine, "CatTypoe";
          return (6);
        objCurrentVariable ["catType"] = int (cols [IDX_CAT_TYPE]); # Get category type
        objCurrentVariable ["mandatory"] = int (cols [IDX_MANDATORY]); # Get category type

        objCurrentVariable ["themeId"] = objThemeMongo.getThemeIdByThemeLabelAndColl (objCurrentVariable ["strTheme"], strDataType);

        strCat = cols [IDX_CAT].strip(); # Get variable categories

        # Performs some consistency over XLS data
        # Check if number of categories match to type of variable
        if ((objCurrentVariable ["catType"] == CATEGORY_NUMERIC_VALUE and len(strCat) != 0) or
            (objCurrentVariable ["catType"] != CATEGORY_NUMERIC_VALUE and len(strCat) == 0)):
          # Only numeric value don't have categories
          print "=> Erro em Categoria. Categoria=" + str (intCatType) + " e Tam Categ=" + str (len(arrayCategory));
          return (0);

        # Load and check categories
        idxAux = -1;
        arrayCategory = [];
        if (objCurrentVariable ["catType"] != CATEGORY_NUMERIC_VALUE):
          arrayCategory = strCat.split (strEndLine);
          # Check if there is '\r' na string. 
          idxAux = -1;
          for i in range (0,len(arrayCategory)):
            try:
              idxAux = arrayCategory.index ("\r");
            except Exception as e:
              idxAux = -1;
              #bolEnd = True;
            else:
              print "Encontrou \\r em", arrayCategory [i];
              # remove

          # Remove white spaces at beginning and end of string
          for i in range (0,len(arrayCategory)):
            arrayCategory[i] = arrayCategory[i].strip();

          # Remove empty lines
          bolEnd = False;
          idxAux = -1;
          while (not bolEnd):
            try:
              idxAux = arrayCategory.index ("");
            except Exception as e:
              bolEnd = True;
            else:
              arrayCategory.remove ("");
          
          # Create category matrix
          matrixCategories = [[0 for x in range(2)] for y in range(len(arrayCategory))];
          # Check categories. Use separator to split values and labels
          for i in range (0,len(arrayCategory)):
            arrayOneCateg = arrayCategory[i].split (strSeparator);
            intNumCateg = len (arrayOneCateg);
            if (intNumCateg != 2):
              # Categories have format (value, label). Error if there are more than thet. Return error 4.
              print "=> Erro em categoria: ", arrayOneCateg;
              return (4);
            else:
              # Put category in matrix
              matrixCategories [i][0] = arrayOneCateg [0].strip();
              matrixCategories [i][1] = arrayOneCateg [1].strip();
        # End - if (intCatType != CATEGORY_NUMERIC_VALUE):
        else:
          # Numeric value. Do not have categories
          matrixCategories = [];
        # End - Else - if (intCatType != CATEGORY_NUMERIC_VALUE):

        # Insert category in variable object
        objCurrentVariable ["category"] = matrixCategories;

        if (objCurrentVariable ["regType"] == 7 or objCurrentVariable ["regType"] == 8):
          objCurrentVariable ["original"] = "padronizada";
        else:
          objCurrentVariable ["original"] = "original";

        if (cols [IDX_REG_TYPE] in [REG_LAYOUT_METADATA, REG_METADATA_ONLY, REG_PROCESSED_METADATA, REG_HARMONIZED_METADATA]):
          # increment (update) number of variables counter
          self.intNumVariables = self.intNumVariables + 1;
          # Add variable to variable array
          self.arrayVariable.append (objCurrentVariable);
          # Update current variable object
          self.objCurrentVariable = objCurrentVariable;

        # End - if (cols [IDX_REG_TYPE] == REG_LAYOUT_METADATA or cols [IDX_REG_TYPE] == REG_METADATA_ONLY or cols [IDX_REG_TYPE] == REG_PROCESSED_METADATA):
#        else:
#          print self.intNumVariables, "-", strDataType, intCenso, "-",cols [IDX_VARIABLE].strip() + ": ", "Não é de metadados - ", cols [IDX_REG_TYPE],"\n";
        # End - if (cols [IDX_REG_TYPE] == REG_LAYOUT_METADATA or cols [IDX_REG_TYPE] == REG_METADATA_ONLY):

      # End - (else) if intLine == 1:
    # End - for linhaXLS in range (sheet.nrows):

    # OK. Return 0.
    return(0);
  # End - def loadFile (self, strFile, censoId, dataTypeId, intCenso, strDataType):

  def getNumberOfVariables (self):
    #print self.intNumVariables, len (self.arrayVariable);
    return self.intNumVariables;
  # End - def getNumberOfVariables (self):

  def getCurrentVariable (self):
    return self.objCurrentVariable;
  # End - def getCurrentVariable (self):

  def getVariable (self, idxVariable):
    return self.arrayVariable [idxVariable];
  # End - def getVariable (self, idxVariable):

  def getVarCode (self, idxVariable):
    return self.arrayVariable [idxVariable] ["varCode"];
  # End - def getVariable (self, idxVariable):

  def getNumVariable (self):
    return self.intNumVariables;
  # End - def getNumVariable (self):

  def getArrayVariable (self):
    return self.arrayVariable;
  # End - def getArrayVariable (self):

  def getFile (self):
    return self.file;
  # End - def getFile (self):

  def getVariableIndex (self, strVar):
    bolAchou = False;
    idxVar = -1;
    i = 0
    while (i < len (self.arrayVariable) and not bolAchou):
      if (self.arrayVariable [i] ["varCode"] == strVar):
        idxVar = i;
        bolAchou = True;
      else:
        i = i + 1;
    # End - while (i < len (self.arrayVariable) and not bolAchou):
    return (idxVar);
  # End - def getFile (self):

# End -class metadataXLSFile:
