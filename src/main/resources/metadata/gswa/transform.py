from lxml import etree
import os
def setup_records_directory(directory_name):
  if os.path.exists(directory_name):
    shutil.rmtree(directory_name)
  os.makedirs(directory_name, exist_ok=True)

etree.register_namespace("xsi","http://www.w3.org/2001/XMLSchema-instance" )
etree.register_namespace("gco","http://www.isotc211.org/2005/gco" )
etree.register_namespace("gmd","http://www.isotc211.org/2005/gmd")
etree.register_namespace("gts","http://www.isotc211.org/2005/gts")
etree.register_namespace("gsr","http://www.isotc211.org/2005/gsr")
etree.register_namespace("gss","http://www.isotc211.org/2005/gss")
etree.register_namespace("gmx","http://www.isotc211.org/2005/gmx")
etree.register_namespace("gml","http://www.opengis.net/gml")
etree.register_namespace("xlink","http://www.w3.org/1999/xlink")

RECEIVED_DIR = "received"
RECORDS_DIR = "records"
XSL = "transform.xsl"

files = os.listdir(RECEIVED_DIR)

setup_records_directory(RECORDS_DIR)
for file in files:
  dom=etree.parse(os.path.join(RECEIVED_DIR,file))
  xslt = etree.parse("transform.xsl")
  transform = etree.XSLT(xslt)
  newdom = transform(dom)
  newdom.write(os.path.join(RECORDS_DIR,file))

