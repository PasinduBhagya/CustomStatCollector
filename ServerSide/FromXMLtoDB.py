import requests
import xml.etree.ElementTree as ET
import mysql.connector
from datetime import datetime
from configparser import ConfigParser

config = ConfigParser()
config.read('./configurations.cfg')

def createSQLQuery(tagList):
  TABLE_NAME = config.get('DATABASE', 'TABLE_NAME')

  TableColumns = ("(" + ", ".join(tagList) + ")")
  TableColumnStrings = []
  for i in range(len(tagList)):
    TableColumnStrings.append(f"%s")
        
  TableColumnString = ("(" + ", ".join(tuple(TableColumnStrings)) + ")")
      
  SQL_QUERY = f"INSERT INTO {TABLE_NAME} {TableColumns} VALUES {TableColumnString}"

  return SQL_QUERY

def connectToDatabase():
    return mysql.connector.connect(
        host=config.get('DATABASE', 'HOST'),
        user=config.get('DATABASE', 'USER'),
        password=config.get('DATABASE', 'PASSWORD'),
        database=config.get('DATABASE', 'DATABASE'),
    )


def addtoDB(valuesDictionary, tagList, SQL_QUERY):
  database = connectToDatabase()
  dbcursor = database.cursor()
  
  valuesList = []
  
  for tag in tagList:
    valuesList.append(valuesDictionary[tag])
  
  valuesForSQLQuery = tuple(valuesList)

  dbcursor.execute(SQL_QUERY, valuesForSQLQuery)
  database.commit()
  

def getResponse(url):
  tagList = []
  response = requests.get(url)
  xml_content = response.content

  root = ET.fromstring(xml_content)

  items = root.findall('.//item')
  updatedDate = root.find('.//UpdatedDate')

  if updatedDate.text.strip() == datetime.now().strftime("%Y-%m-%d"):
    for item in items:
      for child in item:
          tag = child.tag
          tagList.append(tag)
      break
    
    return items, tagList
  else:
    print(f"Warning: {url} has not been updated.")
 
    return None

def main():
  with open('fetchingURLs.conf', 'r') as FURLS:
    for URL in FURLS:
      URL = URL.strip()
      if (len(URL) != 0):
        print("INFO: Checking " + URL)
        if (getResponse(URL) != None):
          
          items, tagList = getResponse(URL)
          SQL_QUERY = createSQLQuery(tagList)

          for item in items:
            valuesDictionary = {}
            for tag in tagList:
                try:
                  valuesDictionary[tag] = item.find(tag).text
                except AttributeError:
                  valuesDictionary[tag] = item.find(tag)
                except:
                  pass
            addtoDB(valuesDictionary, tagList, SQL_QUERY)
     
      else:
        tagList = []
      
main()