# -*- coding: utf-8 -*-

# The order of the variables in Mongo collection will be the order that they are in XLS file

import sys;
import csv;
import os;
from pyAuxCheckMetadataXls import metadataXLSFile
from pyAuxCheckThemesXls import themeXLSFile
from pyAuxCheckMetadataMongo import metadataMongoDB
from pyAuxCheckThemeMongo import ThemeMongoDB

from pymongo import MongoClient

reload(sys)  
sys.setdefaultencoding('utf8')

# mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
# client = MongoClient("mongodb://mongodb0.example.net:27017")
# BD
strMongoConn = "mongodb://mongoAdm:cem#123@200.144.244.241:27017";
#strMongoConn = "mongodb://172.16.1.94:27017";
#strMongoConn = "";

strDir = "C:/Local/Clovis/01-CEM/01-Censos/04-ArqsEntrada/03-Metadados/"

# strMongoMetadataColl = "tGeral";
# strMongoMetadataColl = "tGeralPad";
strMongoMetadataColl = "metadata1";
strMongoThemeColl = "tThemes";

strThemeFile = "C:/Local/Clovis/01-CEM/01-Censos/04-ArqsEntrada/03-Metadados/05-Temas/Temas-20180423.xls"
#C:\Local\Clovis\01-CEM\01-Censos\04-ArqsEntrada\03-Metadados

arrayYears = [2010,2000,1991,1980,1970,1960];
arrayCols = ["tDom", "tPes"];

# Check Themes
# Load XLS Theme file
print "Vai checar temas:"
print "================="
themeFile = themeXLSFile ("");
themeFile.loadFile (strThemeFile, 0, 0, 0, "strDataType");

# Load Mongo Theme objects
themeMongo = ThemeMongoDB (strMongoConn, strMongoThemeColl);
#strThemeFile = "c:/Clovis/01-Censos/04-ArqsEntrada/03-Metadados/05-Temas/Temas-20180423.xls"
if (themeMongo.loadTheme (0, 0, strMongoThemeColl) == 0):
  themeMongo.compareThemesBetweenXlsAndMongo (themeFile);
  themeMongo.checkMissingThemes (themeFile);
else:
  print "Não existe temas no mongo!"

# Load XLS Files and mongo objects in arrays.
strCol = "";
arrayXLSFiles = [];
arrayMongoDB = [];
for intAno in range (0, len (arrayYears)):
  for intCol in range (0, len (arrayCols)):
    if (arrayCols [intCol] == "tDom"):
      strCol = "Domicilio";
    elif (arrayCols [intCol] == "tPes"):
      strCol = "Pessoa";
    else:
      strCol = "";

    print "\nVai verificar censo -", arrayYears[intAno], "-", strCol;
    print "-------------------------------------------------";
    strXlsFile = str (arrayYears [intAno]) + "_Metadados_" + strCol + ".xls";
    print arrayYears[intAno], "-", arrayCols [intCol], "=", "Vai carregar arquivo", strXlsFile, "-", intAno+1,intCol+1,arrayYears[intAno],arrayCols [intCol];
    file = metadataXLSFile ("");
    # Load XLS File
    if (file.loadFile (strDir + strXlsFile, intAno + 1, intCol + 1, arrayYears [intAno], arrayCols [intCol], themeMongo) == 0):
      arrayXLSFiles.append (file);
      print "Load XLS OK -", file.getNumberOfVariables(), "variáveis";

    print "Vai verificar metadados no mongo, na coleção", strMongoMetadataColl;
    mongo = metadataMongoDB (strMongoConn, strMongoMetadataColl);
    # Load censo from Mongo
    retMongoLoadCenso = mongo.loadCenso (intAno + 1, arrayYears [intAno], arrayCols [intCol]);
    if (retMongoLoadCenso == 0): # Load OK.
      arrayMongoDB.append (mongo);
      print "Load Mongo OK", mongo.getNumberOfVariables(), "variáveis";
      print "==>", arrayYears [intAno], ":", arrayCols [intCol], "- Vai verificar se todas as variáveis do XLS estão no Mongo e vice-versa"
      mongo.compareVariablesBetweenXlsAndMongo (intCol + 1, file);
      print "<==", arrayYears [intAno], ":", arrayCols [intCol], "- Verificou se todas as variáveis do XLS estão no Mongo e vice-versa"
    elif (retMongoLoadCenso == 1): # Do not exist.
      print arrayYears [intAno], ":", arrayCols [intCol], "- Não existe no Mongo. Inclui"
      mongo.createCenso (intAno + 1, arrayYears [intAno], arrayCols [intCol], file);
    elif (retMongoLoadCenso == 2): # Do not exist.
      print arrayYears [intAno], ":", arrayCols [intCol], "- Inconsistência! Há mais de um registro de ano!"
    elif (retMongoLoadCenso == 3): # Do not exist.
      print arrayYears [intAno], ":", arrayCols [intCol], "- Não existe coleção! Inclui"
      mongo.insertColl (intAno + 1, arrayYears [intAno], arrayCols [intCol], file);


print "\nFIM DE EXECUÇÃO"
sys.exit("\nFIM")
print "ATENÇÃO!! Não retornou"
