import csv
from configparser import ConfigParser
from datetime import datetime

datetime.now().strftime("%Y-%m-%d")

config = ConfigParser()
config.read("./configurations.cfg")

def encrypt():
    pass

def csvToXML(csvFileName):

    csvFilePath = f"./{config.get('FOLDER_PATH', 'INPUT_FOLDER_PATH')}/{csvFileName}"
    csvFileName = csvFileName.split(".")[0]
    xmlFilePath = f"/{config.get('FOLDER_PATH', 'OUTPUT_FOLDER_PATH')}/{csvFileName}.xml"   

    with open(csvFilePath, mode='r', newline='') as file:
        csv_reader = csv.reader(file)

        header = next(csv_reader)
        headerLength = len(header)

        with open(xmlFilePath, 'w') as xmlFile:
            xmlFile.write(f"<{csvFileName}>")
            xmlFile.write(f"<UpdatedDate>")
            xmlFile.write(f'{(datetime.now().strftime("%Y-%m-%d")).strip()}')
            xmlFile.write(f"</UpdatedDate>")
            for line in csv_reader:
                xmlFile.write("\t<item>\n")
                for i in range(headerLength):
                    try: 
                        xmlFile.write(f"\t\t<{header[i]}>{line[i]}</{header[i]}>\n")
                    except IndexError:
                        xmlFile.write(f"\t\t<{header[i]}>None</{header[i]}>\n")
                    except:
                        pass
                xmlFile.write("\t</item>\n")
            xmlFile.write(f"</{csvFileName}>")

for csvFileName in config.get('CSV_NAMES', 'CSV_NAMES_LIST').split(","):
    csvToXML(csvFileName)
