#!/usr/bin/env python3

# pylint: disable=missing-docstring, invalid-name, blacklisted-name, bad-builtin, broad-except

import os
import shutil
import sys
import xml.etree.cElementTree as ET
import xml.dom.minidom as Minidom
import urllib3

namespaces = {
    "csw": "http://www.opengis.net/cat/csw/2.0.2",
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gco": "http://www.isotc211.org/2005/gco"
    }

ET.register_namespace("csw", "http://www.opengis.net/cat/csw/2.0.2")
ET.register_namespace("gmd", "http://www.isotc211.org/2005/gmd")
ET.register_namespace("gco", "http://www.isotc211.org/2005/gco")

urllib3.disable_warnings()
http_proxy = os.environ.get('http_proxy')
http = urllib3.proxy_from_url(http_proxy) if http_proxy else urllib3.PoolManager()

def fetch_metadata(catalogue_name, csw_endpoint):
    try:
        csw_request_filename = catalogue_name + "/request.xml"
        csw_request = read_file(csw_request_filename)
        csw_response = send_csw_request(csw_endpoint, csw_request)

        metadata_dir = catalogue_name + "/records/"
        setup_metadata_directory(metadata_dir)

        num_records = 0
        metadata_records = csw_response.iterfind("csw:SearchResults/gmd:MD_Metadata", namespaces)
        for r in metadata_records:
            write_metadata(metadata_dir, r)
            num_records += 1

        print("Fetched %d records from %s" % (num_records, csw_endpoint))

    except Exception as e:
        sys.stderr.write(str(e))

def send_csw_request(csw_endpoint, request_body):
    response = http.urlopen("POST", csw_endpoint,
                            headers={"Content-type": "text/xml"},
                            body=request_body)
    return ET.fromstring(response.data.decode(encoding="UTF-8"))

def read_file(filename):
    with open(filename, "r") as f:
        return f.read()

def write_metadata(metadata_dir, metadata_record):
    with open(metadata_dir + metadata_filename(metadata_record), "w") as f:
        f.write(xml_string(metadata_record))

def setup_metadata_directory(directory_name):
    if os.path.exists(directory_name):
        shutil.rmtree(directory_name)
    os.makedirs(directory_name, exist_ok=True)

def metadata_filename(metadata_record):
    return extract_id(metadata_record) + ".xml"

def extract_id(metadata_record):
    return metadata_record.find("gmd:fileIdentifier/gco:CharacterString", namespaces).text

def xml_string(metadata_record):
    return Minidom.parseString(ET.tostring(metadata_record, "utf-8")).toprettyxml()

def main():
    fetch_metadata("mrt", "https://data.thelist.tas.gov.au/datagn/srv/eng/csw")

if __name__ == "__main__":
    main()
