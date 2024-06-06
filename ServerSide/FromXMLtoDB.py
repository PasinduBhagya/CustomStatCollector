import requests
import xml.etree.ElementTree as ET

def getResponse(url):
  tagList = []
  response = requests.get(url)
  xml_content = response.content

  root = ET.fromstring(xml_content)

  items = root.findall('.//item')

  for item in items:
    for child in item:
        tag = child.tag
        tagList.append(tag)
    break
  
  return items, tagList

def main():
  with open('fetchingURLs.txt', 'r') as FURLS:
    for URL in FURLS:
      if (len(URL.strip()) != 0):
        print("Checking " + URL)
        items, tagList = getResponse(URL.strip())
        for item in items:
          for tag in tagList:
              try:
                print(tag + "\t" + item.find(tag).text)
              except AttributeError:
                print(tag + "\t" + str(item.find(tag)))
              except:
                pass

main()