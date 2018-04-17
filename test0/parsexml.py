import xml.etree.ElementTree

f = open('dirlist.txt', 'w')

e = xml.etree.ElementTree.parse('default.xml').getroot()

for atype in e.findall('project'):
    f.write(atype.get('name') + "\n")

f.close()
