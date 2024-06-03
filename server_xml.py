from xml.dom import minidom

# parse an xml file by name
file = minidom.parse('models.xml')

#use getElementsByTagName() to get tag
models = file.getElementsByTagName('model')

# one specific item attribute
print('model #2 attribute:')
print(models[1].attributes['name'].value)

# all item attributes
print('\nAll attributes:')
for elem in models:
  print(elem.attributes['name'].value)

# one specific item's data
print('\nmodel #2 data:')
print(models[1].firstChild.data)
print(models[1].childNodes[0].data)

# all items data
print('\nAll model data:')
for elem in models:
  print(elem.firstChild.data)
