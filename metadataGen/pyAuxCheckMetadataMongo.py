# -*- coding: utf-8 -*-

# CENSO APP
# Class metadataMongoDB
# Keep content of a Mongo Metadata DB.
#

import sys;

from pymongo import MongoClient

reload(sys)  
sys.setdefaultencoding('utf8')

class metadataMongoDB:

  def __init__ (self, strMongoCnx, strMongoMetadataColl):
    #print "str|File=",strFile;
    self.strMongoCnx = strMongoCnx; # string connection for MongoDB
    self.strMongoMetadataColl = strMongoMetadataColl; # The metadata collection
    self.censoId = 0; # ID of censo
    self.intCensoYear = 0; # Year of censo
    self.strDataType = "";
    self.currentCollection = {};
  # End - def __init__ (self, strFile):

  # Function to load a censo from MongoDB
  # Return: 0 - OK; 1 - Censo do not exist; 2 - Inconsistency. More than one censo
  def loadCenso (self, censoId, intCensoYear, strDataType):
    self.censoId = censoId;
    self.intCensoYear = intCensoYear;
    self.strDataType = strDataType;

    # Connect to Mongo
    if (self.strMongoCnx == ""):
      self.censoMongoClient = MongoClient();
    else:
      self.censoMongoClient = MongoClient(self.strMongoCnx);
    
    # Connect to appCenso
    db = self.censoMongoClient.appCenso
    # Get metadata collection
    self.coltGeral = db [self.strMongoMetadataColl]; # store the hole censo collection
    # Get themes collection
    #self.coltThemes = db.tThemes; # store themes

    intIdVar = 0;
    intNewVarId = 0;
    # Check if census exists in MongoDB
    intCountCenso = 0;
    intCountCenso = self.coltGeral.find({"year":intCensoYear}).count();
    if (intCountCenso > 1):
      #print "==========> Erro: Censo", intCensoYear, "inconsistente (mais que um)";
      return (2);
    elif (intCountCenso == 0):
      #print "=> Censo", intCensoYear, "não existe!";
      return (1);
    else:
      print "=> Censo", intCensoYear, "existe. Vai carregar";

    self.collCenso = self.coltGeral.find({"year":intCensoYear}) [0];
    #print self.collCenso.count();

    # Check census data (dbName, source etc)
    strKeys = self.collCenso.keys();
    #for i in range (0, len(strKeys)):
    #  print strKeys [i];

    if (len(strKeys) != 7):
      print "Censo", intCensoYear, ": wrong keys!", strKeys;

    # Get collections
    self.arrayCollection = self.collCenso ["collection"];

    idxColDataType = -1;
    if (strDataType != ""):
      for i in range (0, len (self.arrayCollection)):
        #arrayCollections [i].find ({"sex":"Male", "City":{"$exists": False}},{});
        strNameColl = self.arrayCollection [i]["value"];
        if (strNameColl == strDataType):
          idxColDataType = i;

      if (idxColDataType == -1):
        # Didn't find collection of required type. Can include it.
        #print "Mongo: Collections", strDataType, "não existe. Vai incluir";
        return (3);
      else:
        # Found collection of required type. Can update it.
        self.currentCollection = self.arrayCollection [idxColDataType];
        #print "Encontrou coleção:", idxColDataType, "-", strDataType, \
        #      self.currentCollection.keys(), len (self.currentCollection ["variable"]);

    self.censoMongoClient.close();

    return (0);
  # End - def loadCenso (self, censoId, intCensoYear, strDataType):

  def getNumberOfVariables (self):
    return len (self.currentCollection ["variable"]);
  # End - def numberOfCollections (self)

  def numberOfCollections (self):
    try:
      intNumOfColl = len (self.collCenso ["collection"]);
    except Exception as e:
      # Collection do not exist
      return (0);
    else:
      return intNumOfColl;
  # End - def numberOfCollections (self)

  def setDataType (self, strDataType):
    idxColDataType = -1;
    for i in range (0, len (self.arrayCollection)):
      strNameColl = self.arrayCollection [i]["value"];
      if (strNameColl == strDataType):
        idxColDataType = i;

    if (idxColDataType == -1):
      # Didn't find collection of required type. Can include it.
      print "Mongo: Collections", strDataType, "não existe. Vai incluir";
      return (1);
    else:
      # Found collection of required type.
      self.currentCollection = {};
      self.currentCollection = arrayCollections [idxColDataType];
      # print "Encontrou coleção:", idxColDataType, "-", strDataType, colCollection.keys();
      return (0);
  # End - def numberOfCollections (self)

  def compareCategories (self, objCategoryXls, objCategoryMongo):
    strAux = "";
    for i in range (0, len (objCategoryXls)):
      #for j in range (0, len (objCategoryMongo);
      if (self.getIndexCategoryMongo (objCategoryXls [i], objCategoryMongo) == -1):
        if (strAux == ""):
          strAux = objCategoryXls [i][0] + " / " + objCategoryXls [i][1];
        else:
          strAux = strAux + "; " + objCategoryXls [i][0] + " / " + objCategoryXls [i][1];
    # End - for i in range (0, len (objCategoryXls)):
    if (strAux != ""):
      strAux = "Categorias não existentes no mongo: " + strAux;
      #print "XLS:", objCategoryXls, "\nMongo:", objCategoryMongo

    
    isFirst = True;
    for i in range (0, len (objCategoryMongo)):
      #for j in range (0, len (objCategoryMongo);
      if (self.getIndexCategoryXls (objCategoryMongo [i], objCategoryXls) == -1):
        try:
          strLabel = objCategoryMongo [i]["label"];
        except Exception as e:
          strLabel = "SEM LABEL"

        if (isFirst):
          isFirst = False;
          strAux = strAux + "\n--> Categorias não existentes no XLS: " + str (objCategoryMongo [i]["value"]) + " / " + strLabel;
        else:
          strAux2 = str (objCategoryMongo [i]["value"]) + " / " + str(strLabel);
          strAux = strAux + "; " + strAux2;
    # End - for i in range (0, len (objCategoryXls)):
      

    return strAux;
  # End - def compareCategories (self, objCategoryXls, objCategoryMongo):

  def getIndexCategoryMongo (self, objCategoryXls, objCategoryMongo):
    bolAchou = False;
    idxCat = 0;
    while (idxCat < len (objCategoryMongo) and not bolAchou):
      # Get category content
      try:
        strCatXlsValue = str (objCategoryXls [0]).strip();
      except Exception as e:
        strCatXlsValue = "";
      
      try:
        strCatMongoValue = str (objCategoryMongo [idxCat]["value"]).strip();
      except Exception as e:
        strCatMongoValue = "";
      
      try:
        strCatXlsLabel = str (objCategoryXls [1]).strip ();
      except Exception as e:
        strCatXlsLabel = "";
      
      try:
        strCatMongoLabel = str (objCategoryMongo [idxCat]["label"]).strip ();
      except Exception as e:
        strCatMongoLabel = "";
     
#      if (strCatXlsValue == strCatMongoValue and strCatXlsLabel == strCatMongoLabel):
      if ((strCatXlsValue == strCatMongoValue and strCatXlsLabel == strCatMongoLabel) or
          (strCatXlsLabel == strCatMongoLabel and strCatXlsValue == "col" and strCatMongoValue == "0")):
        bolAchou = True;
      else:
        idxCat = idxCat + 1;

    if (bolAchou):
      return idxCat;
    else:
      #print "Não Encontrou", strVarCode;
      return -1;
  # End - def getIndexCategoryMongo (objCategoryXls, objCategoryMongo):

  def getIndexCategoryXls (self, objCategoryMongo, objCategoryXls):
    bolAchou = False;
    idxCat = 0;
    while (idxCat < len (objCategoryXls) and not bolAchou):
      # Get category content
      try:
        strCatXlsValue = str (objCategoryXls [idxCat][0]).strip();
      except Exception as e:
        strCatXlsValue = "";
      
      try:
        strCatMongoValue = str (objCategoryMongo ["value"]).strip();
      except Exception as e:
        strCatMongoValue = "";
      
      try:
        strCatXlsLabel = str (objCategoryXls [idxCat][1]).strip ();
      except Exception as e:
        strCatXlsLabel = "";
      
      try:
        strCatMongoLabel = str (objCategoryMongo ["label"]).strip ();
      except Exception as e:
        strCatMongoLabel = "";

#      if (strCatXlsValue == strCatMongoValue and strCatXlsLabel == strCatMongoLabel):
      if ((strCatXlsValue == strCatMongoValue and strCatXlsLabel == strCatMongoLabel) or
          (strCatXlsLabel == strCatMongoLabel and strCatXlsValue == "col" and strCatMongoValue == "0")):
        bolAchou = True;
      else:
        idxCat = idxCat + 1;

    if (bolAchou):
      return idxCat;
    else:
      return -1;
  # End - def getIndexCategoryMongo (objCategoryXls, objCategoryMongo):

  # Function to perform comparison between XLS and Mongo, pointing diferences.
  def compareVariablesBetweenXlsAndMongo (self, idxDataTypeXLS, objDataType):
    # Search dataType in mongo
    # Check if XLS variables are in mongoDB
    for idxVariable in range (0, objDataType.getNumberOfVariables ()):
      strVariableXLS = objDataType.getVariable (idxVariable) ["varCode"];
      print "\nVariável:", strVariableXLS, ":"
      if (self.getVariableIndex (strVariableXLS) < 0):
        print "===> Não encontrou variável do XLS", strVariableXLS, "no Mongo";
      else:
        # Check variable content, if properties are the same
        objVarMongo = self.getVariable (strVariableXLS);
        arrayNonExistentsVar = [];
        strXlsKeys = objDataType.getVariable (idxVariable).keys();
        for i in range (0, len (strXlsKeys)):
          if (strXlsKeys [i] != "strTheme" and strXlsKeys [i] != "regType"): # Ignore strTheme and regTytpe (not in mongo)
            varMongoExists = True;
            try:
              varMongoContent = objVarMongo [strXlsKeys [i]];
            except Exception as e:
              # variable do not exist in Mongo
              varMongoExists = False;

            if (varMongoExists):
              varXlsContent = objDataType.getVariable (idxVariable) [strXlsKeys [i]];
              if (strXlsKeys [i] == "category"):
                # Compare categories
                ret = self.compareCategories (varXlsContent, varMongoContent);
                if (ret != ""):
                  print "-->", ret;
              else:
                if (varXlsContent != varMongoContent):
                  print "--> Diferença em", strXlsKeys [i], "(XLS / Mongo) -", varXlsContent, "/", varMongoContent;
            else:
              arrayNonExistentsVar.append (strXlsKeys [i]);
          # End - if (strXlsKeys [i] != "strTheme" and strXlsKeys [i] != "regType"):
        # End - for i in range (0, len (strXlsKeys)):
        if (len (arrayNonExistentsVar) > 0):
          strAux = ""
          for j in range (0, len (arrayNonExistentsVar)):
            if (j == 0):
              strAux = arrayNonExistentsVar [j];
            else:
              strAux = strAux + ", " + arrayNonExistentsVar [j];
          print "--> Campos do XLS não existentes no Mongo:", strAux;
        # End - if (len (arrayNonExistentsVar) > 0):

        # Check fields variables in mongo that doesn't exist in XLS
        arrayNonExistentsVar = [];
        strMongoKeys = objVarMongo.keys();
        for idxKeyMongo in range (0, len(strMongoKeys)):
          try:
            intAux = strXlsKeys.index (strMongoKeys [idxKeyMongo]);
          except Exception as e:
            # Field do not exist in Xls
            arrayNonExistentsVar.append (strMongoKeys [idxKeyMongo])
        # End - for idxKeyMongo in range (0, len(strMongoKeys)):
        if (len (arrayNonExistentsVar) > 0):
          strAux = ""
          for j in range (0, len (arrayNonExistentsVar)):
            if (j == 0):
              strAux = arrayNonExistentsVar [j];
            else:
              strAux = strAux + ", " + arrayNonExistentsVar [j];
          print "--> Campos do Mongo não existentes no XLS:", strAux;
        # End - if (len (arrayNonExistentsVar) > 0):

      # End - Else - if (self.getVariableIndex (strVariableXLS) < 0):
    # End - for idxVariable in range (0, objDataType.getNumberOfVariables ()):

    # Check if mongoDB variables is in XLS File
    try:
      intNumOfVar = len (self.currentCollection ["variable"]);
    except Exception as e:
      # Collection do not exist
      intNumOfVar = 0;
    for idxVariable in range (0, intNumOfVar):
      strVariableMongo = self.currentCollection ["variable"][idxVariable]["varCode"];
      #print "Vai checar var do mongo", strVariableMongo;
      if (objDataType.getVariableIndex (strVariableMongo) < 0):
        print "\n===> Não encontrou variável do Mongo", strVariableMongo, "no XLS";
      #else:
      #  print "OK. Encontrou variável do Mongo", strVariableMongo, "no XLS";
    # End - for idxVariable in range (0, intNumOfVar):

  # End - def compareVariablesBetweenXlsAndMongo (self, idxDataTypeXLS, objDataType):

  def getVariable (self, strVarCode):

    idxVariable = self.getVariableIndex (strVarCode);
    if (idxVariable == -1):
      return {};
    else:
      return (self.currentCollection ["variable"][idxVariable]);
  # End - def getVariableIndex (self, strVarCode)

  def getVariableIndex (self, strVarCode):
    try:
      intNumOfVar = len (self.currentCollection ["variable"]);
    except Exception as e:
      # Collection do not exist
      intNumOfVar = 0;

    bolAchou = False;
    idxVariable = 0;
    while (idxVariable < intNumOfVar and not bolAchou):
      strVarName = self.currentCollection ["variable"][idxVariable]["varCode"];
      if (strVarName == strVarCode):
        bolAchou = True;
      else:
        idxVariable = idxVariable + 1;

    if (bolAchou):
      #print "Encontrou", strVarCode, "na posição", idxVariable;
      return idxVariable;
    else:
      #print "Não Encontrou", strVarCode;
      return -1;
  # End - def getVariableIndex (self, strVarCode)

  def checkVariable (self, idxVariableXLS, objVariable):
    # Search variable in mongo
    bolAchou = False;
    idxVariable = 0;
    while (idxVariable < len (self.currentCollection ["variable"]) and not bolAchou):
      strVarName = self.currentCollection ["variable"][idxVariable]["varCode"];
      if (strVarName == objVariable ["varCode"]):
        bolAchou = True;
      else:
        idxVariable = idxVariable + 1;

    if (bolAchou):
      print "Encontrou ", idxVariableXLS, "-", objVariable ["varCode"], "na posição", idxVariable;
      return (0);
    else:
      print "Não Encontrou ", objVariable ["varCode"];
      return (-1);
  # End - def checkVariable (self, idxVariableXLS, objVariable):

  def createCenso (self, censoId, intCensoYear, strDataType, objDataType):
    print "Vai inserir:",self.censoId,self.intCensoYear,self.strDataType,self.strMongoMetadataColl;
    #post_id = posts.insert_one(post).inserted_id
    # Create collection array
    localArrayVariable = objDataType.getArrayVariable();
    for idxVar in range (0, len(localArrayVariable)):
      if (len(localArrayVariable [idxVar]["category"]) > 0):
        newIdCat = 1;
        arrayCat = [];
        arrayOldCat = localArrayVariable [idxVar]["category"];
        for idxCat in range (0, len(arrayOldCat)):
          objCat = {
            "_id": newIdCat,
            "value": arrayOldCat [idxCat][0],
            "label": arrayOldCat [idxCat][1],
            "varCode": localArrayVariable [idxVar]["varCode"]
          };
          arrayCat.append (objCat);
          newIdCat = newIdCat + 1
        localArrayVariable [idxVar]["category"] = arrayCat;
      # if (len(localArrayVariable [idxVar]["category"] > 0):
    # for idxVar in range (0, len(localArrayVariable)):

    objColl = {
      "_id":1, # _if is 1 because there is no censo. It's the first.
      #"sourceId":self.censoId,
      "value":self.strDataType,
      "label":"Domicilio",
      "variable":localArrayVariable
    };
    collArray = [];
    collArray.append (objColl);
    post = {
      "_id":self.censoId,
      "source":"censo",
      "year":self.intCensoYear,
      "month":0,
      "available":1,
      "dbName":"c" + str (self.intCensoYear),
      "collection": collArray
    };
    ins_id = self.coltGeral.insert_one(post).inserted_id;
    print "Inseriu:,", ins_id;

    '''
    self.censoId = censoId;
    self.intCensoYear = intCensoYear;
    self.strDataType = strDataType;
    self.censoId = censoId;
    self.intCensoYear = intCensoYear;
    self.strDataType = strDataType;

    # Connect to Mongo
    if (self.strMongoCnx == ""):
      self.censoMongoClient = MongoClient();
    else:
      self.censoMongoClient = MongoClient(self.strMongoCnx);
    
    # Connect to appCenso
    db = self.censoMongoClient.appCenso
    # Get metadata collection
    self.coltGeral = db [self.strMongoMetadataColl]; # store the hole censo collection
    # Get themes collection
    #self.coltThemes = db.tThemes; # store themes

    intIdVar = 0;
    intNewVarId = 0;
    # Check if census exists in MongoDB
    intCountCenso = 0;
    intCountCenso = self.coltGeral.find({"year":intCensoYear}).count();
   ''' 
  # End - def createCenso (self, censoId, intCensoYear, strDataType):

  def insertColl (self, censoId, intCensoYear, strDataType, objDataType):
    print "Vai inserir coleção:",self.censoId,self.intCensoYear,self.strDataType,self.strMongoMetadataColl;
    # post_id = posts.insert_one(post).inserted_id
    idxNewColl = len (self.collCenso ["collection"]);
    #print "Tamanho:", idxNewColl, "Posição:", idxNewColl+1;

    localArrayVariable = objDataType.getArrayVariable();
    for idxVar in range (0, len(localArrayVariable)):
      if (len(localArrayVariable [idxVar]["category"]) > 0):
        newIdCat = 1;
        arrayCat = [];
        arrayOldCat = localArrayVariable [idxVar]["category"];
        for idxCat in range (0, len(arrayOldCat)):
          objCat = {
            "_id": newIdCat,
            "value": arrayOldCat [idxCat][0],
            "label": arrayOldCat [idxCat][1],
            "varCode": localArrayVariable [idxVar]["varCode"]
          };
          arrayCat.append (objCat);
          newIdCat = newIdCat + 1
        localArrayVariable [idxVar]["category"] = arrayCat;
      # if (len(localArrayVariable [idxVar]["category"] > 0):
    # for idxVar in range (0, len(localArrayVariable)):

    objUpdateValue = {
      "_id": idxNewColl + 1, # Position: next
      #"sourceId":self.censoId,
      "value":self.strDataType,
      "label":"Pessoa",
      "variable":localArrayVariable
    };

    # Create collection array
    #collArray = [];
    #objUpdateValue = {
    #  "_id":1, # _if is 1 because there is no censo. It's the first.
      #"sourceId":self.censoId,
    #  "value":self.strDataType,
    #  "label":"Domicilio",
    #  "variable":objDataType.getArrayVariable()
    #};
    #collArray.append (strUpdateValue);
    #post = {
    #  "_id":self.censoId,
    #  "source":"censo",
    #  "year":self.intCensoYear,
    #  "month":0,
    #  "available":1,
    #  "dbName":"c" + str (self.intCensoYear),
    #  "collection": collArray
    #};
    
    strPath = "collection." + str (idxNewColl);
    ins_id = self.coltGeral.update({"year":intCensoYear},{"$set":{strPath:objUpdateValue}});
    print "Atualizou:,", ins_id;
    
    '''
    ins_id = self.coltGeral.insert_one(post).inserted_id;

          strUpdateValue = {"_id":intNewIdMongo};
          strPath = "collection." + str (idxColDataType) + ".variable." + str (intIdMongo);
          coltGeral.update({"year":intCenso,"collection.value":strDataType},{"$set":{strPath:strUpdateValue}});

          strUpdateValue = strVariable;
          strPath = "collection." + str (idxColDataType) + ".variable." + str (intIdMongo) + ".varCode";
          coltGeral.update({"year":intCenso,"collection.value":strDataType},{"$set":{strPath:strUpdateValue}});

          strUpdateValue = strLabel;
          strPath = "collection." + str (idxColDataType) + ".variable." + str (intIdMongo) + ".label";
          coltGeral.update({"year":intCenso,"collection.value":strDataType},{"$set":{strPath:strUpdateValue}});


    self.censoId = censoId;
    self.intCensoYear = intCensoYear;
    self.strDataType = strDataType;
    self.censoId = censoId;
    self.intCensoYear = intCensoYear;
    self.strDataType = strDataType;

    # Connect to Mongo
    if (self.strMongoCnx == ""):
      self.censoMongoClient = MongoClient();
    else:
      self.censoMongoClient = MongoClient(self.strMongoCnx);
    
    # Connect to appCenso
    db = self.censoMongoClient.appCenso
    # Get metadata collection
    self.coltGeral = db [self.strMongoMetadataColl]; # store the hole censo collection
    # Get themes collection
    #self.coltThemes = db.tThemes; # store themes

    intIdVar = 0;
    intNewVarId = 0;
    # Check if census exists in MongoDB
    intCountCenso = 0;
    intCountCenso = self.coltGeral.find({"year":intCensoYear}).count();
    ''' 
  # End - def insertColl (self, censoId, intCensoYear, strDataType):

# End - class metadataMongoDB:
