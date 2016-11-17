import os

path ='records'

OLD_STRING = "dapds00.nci.org.au"
NEW_STRING = "dap-wms.nci.org.au"

filenames = os.listdir(path)

for filename in filenames:
    filename = os.path.join(path,filename)
    if filename.endswith('.xml'):
        with open(filename,'r') as aster_file:
            aster = aster_file.read()
            aster = aster.replace(OLD_STRING, NEW_STRING)
        with open(filename,'w') as aster_file:
            aster_file.write(aster)
        