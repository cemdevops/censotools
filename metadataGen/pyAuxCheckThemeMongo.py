# -*- coding: utf-8 -*-

# CENSO APP
# Class metadataXLSFile
# Keep content of a XLS Metadata file.
#

import sys;

from pymongo import MongoClient

reload(sys)  
sys.setdefaultencoding('utf8')

class ThemeMongoDB:

  def __init__ (self, strMongoCnx, strMongoThemeColl):
    print "Coleção de tema:", strMongoThemeColl;
    self.strMongoCnx = strMongoCnx; # string connection for MongoDB
    self.strMongoThemeColl = strMongoThemeColl; # The metadata collection
    self.currentTheme = {};
    self.arrayTheme = [];
  # End - def __init__ (self, strFile):

  # Function to load a censo from MongoDB
  # Return: 0 - OK; 1 - Censo do not exist; 2 - Inconsistency. More than one censo
  def loadTheme (self, censoId, intCensoYear, strDataType):

    # Connect to Mongo
    if (self.strMongoCnx == ""):
      self.themeMongoClient = MongoClient();
    else:
      self.themeMongoClient = MongoClient(self.strMongoCnx);

    # Connect to appCenso
    db = self.themeMongoClient.appCenso
    # Get themes collection
    self.collTheme = db [self.strMongoThemeColl]; # store themes

    # Get themes
    self.themeCollection = self.collTheme.find({});

    # Get Number of themes
    self.intNumThemes = self.themeCollection.count();
    if (self.intNumThemes <= 0):
      #print "=> Themes inexistentes!";
      return (1);
    else:
      print "=> Themes:", self.intNumThemes;

    for i in range (0, self.intNumThemes):
      self.arrayTheme.append (self.themeCollection [i]);

    self.themeMongoClient.close();

    return (0);
  # End - def loadTheme (self, censoId, intCensoYear, strDataType):


  def getThemeIndexByThemeLabelAndColl (self, strTheme, strColl):
    bolAchou = False;
    idxTheme = 0;
    while (idxTheme < self.intNumThemes and not bolAchou):
      strThemeName = self.arrayTheme [idxTheme]["label"];
      strThemeColl = self.arrayTheme [idxTheme]["collection"];
      if (strThemeName == strTheme and strThemeColl == strColl):
        bolAchou = True;
      else:
        idxTheme = idxTheme + 1;

    if (bolAchou):
      #print "Encontrou", strVarCode, "na posição", idxVariable;
      return idxTheme;
    else:
      #print "Não Encontrou", strVarCode;
      return -1;
  # End - def getThemeIndexByThemeLabelAndColl (self, strTheme):

  def getThemeByThemeLabelAndColl (self, strTheme, strColl):
    bolAchou = False;
    idxTheme = 0;
    while (idxTheme < self.intNumThemes and not bolAchou):
      strThemeName = self.arrayTheme [idxTheme]["label"];
      strThemeColl = self.arrayTheme [idxTheme]["collection"];
      if (strThemeName == strTheme and strThemeColl == strColl):
        bolAchou = True;
      else:
        idxTheme = idxTheme + 1;

    if (bolAchou):
      #print "Encontrou", strVarCode, "na posição", idxVariable;
      return self.arrayTheme [idxTheme];
    else:
      #print "Não Encontrou", strVarCode;
      return -1;
  # End - def getThemeByThemeLabelAndColl (self, strTheme, strColl):

  def getThemeIdByThemeLabelAndColl (self, strTheme, strColl):
    bolAchou = False;
    idxTheme = 0;
    while (idxTheme < self.intNumThemes and not bolAchou):
      strThemeName = self.arrayTheme [idxTheme]["label"];
      strThemeColl = self.arrayTheme [idxTheme]["collection"];
      if (strThemeName == strTheme and strThemeColl == strColl):
        bolAchou = True;
      else:
        idxTheme = idxTheme + 1;

    if (bolAchou):
      #print "Encontrou", strVarCode, "na posição", idxVariable;
      return self.themeCollection [idxTheme]["themeId"];
    else:
      #print "Não Encontrou", strVarCode;
      return -1;
  # End - def getThemeIdByThemeLabelAndColl (self, strTheme):


  # Function to perform comparison between XLS and Mongo, pointing diferences.
  def compareThemesBetweenXlsAndMongo (self, objThemesXLS):
    for idxTheme in range (0, objThemesXLS.getNumberOfThemes ()):
      strThemeLabelXLS = objThemesXLS.getThemeLabel (idxTheme);
      strThemeCollXLS = objThemesXLS.getThemeColl (idxTheme);
      print "\nTema:", strThemeLabelXLS, "/", strThemeCollXLS, ":"
      if (self.getThemeIndexByThemeLabelAndColl (strThemeLabelXLS, strThemeCollXLS) < 0):
        print "--> Não encontrou tema do XLS", strThemeLabelXLS, "no Mongo";
      else:
        arrayNonExistentThemes = [];
        objThemeMongo = self.getThemeByThemeLabelAndColl (strThemeLabelXLS, strThemeCollXLS);
        strXlsKeys = objThemesXLS.getTheme (idxTheme).keys();
        for i in range (0, len (strXlsKeys)):
          themeMongoExists = True;
          try:
            themeMongoContent = objThemeMongo [strXlsKeys [i]];
          except Exception as e:
            # variable do not exist in Mongo
            themeMongoExists = False;

          if (themeMongoExists):
            themeXlsContent = objThemesXLS.getTheme (idxTheme) [strXlsKeys [i]];
            if (themeXlsContent != themeMongoContent):
              print "--> Diferença em", strXlsKeys [i], "(XLS / Mongo) -", themeXlsContent, "/", themeMongoContent;
          else:
            arrayNonExistentThemes.append (strXlsKeys [i]);

        if (len (arrayNonExistentThemes) > 0):
          strAux = ""
          for j in range (0, len (arrayNonExistentThemes)):
            if (j == 0):
              strAux = arrayNonExistentThemes [j];
            else:
              strAux = strAux + ", " + arrayNonExistentThemes [j];
          print "--> Campos não existentes no Mongo:", strAux;
  # End - def compareThemesBetweenXlsAndMongo (self, objThemesXLS):

  def checkMissingThemes (self, objThemesXLS):
    arrayXLSThemes = [];
    for i in range (0, objThemesXLS.getNumberOfThemes ()):
      arrayXLSThemes.append (objThemesXLS.getThemeLabel (i));

    for i in range (0, len (self.arrayTheme)):
      strAux = "";
      try:
        strAux = self.arrayTheme [i]["label"];
        idxAux = arrayXLSThemes.index (strAux);
      except Exception as e:
        print "\n===>Tema", strAux, "existe no Mongo mas não XLS\n";
  # End - def checkMissingThemes (self, objThemesXLS):

# End - class metadataMongoDB:
