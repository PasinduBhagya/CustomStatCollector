import requests
import xml.etree.ElementTree as ET
from datetime import datetime

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
  with open('fetchingURLs.txt', 'r') as FURLS:
    for URL in FURLS:
      URL = URL.strip()
      if (len(URL) != 0):
        print("INFO: Checking " + URL)
        if (getResponse(URL) != None):
          items, tagList = getResponse(URL)
          for item in items:
            for tag in tagList:
                try:
                  print(tag + "\t" + item.find(tag).text)
                except AttributeError:
                  print(tag + "\t" + str(item.find(tag)))
                except:
                  pass

main()