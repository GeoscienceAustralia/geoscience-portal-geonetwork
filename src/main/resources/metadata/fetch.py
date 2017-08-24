#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=invalid-name
# pylint: disable=blacklisted-name
# pylint: disable=bad-builtin
# pylint: disable=broad-except
# pylint: disable=line-too-long
# pylint: disable=fixme

import os
import shutil
import traceback
import xml.etree.cElementTree as ET
import xml.dom.minidom as Minidom
import urllib3
import uuid

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

def fetch_metadata_from_csw(catalogue):
    def get_request():
        request_filename = catalogue[0] + "/request.xml"
        request_body = read_file(request_filename)
        return http.urlopen("POST", catalogue[1],
                            headers={"Content-type": "text/xml"},
                            body=request_body)

    fetch_metadata(catalogue, get_request)

def fetch_metadata_from_url(catalogue):
    def get_request():
        return http.urlopen("GET", catalogue[1])

    fetch_metadata(catalogue, get_request)

def fetch_metadata(catalogue, get_request):
    try:
        save_metadata(catalogue, get_request())

    except Exception as _:
        traceback.print_exc()

def save_metadata(catalogue, response):
    csw_response = parse_response(response)

    metadata_dir = catalogue[0] + "/records/"
    setup_metadata_directory(metadata_dir)

    num_records = 0
    metadata_records = csw_response.findall(".//gmd:MD_Metadata", namespaces)
    for r in metadata_records:
        check_file_identifier(r)
        write_metadata(metadata_dir, r)
        num_records += 1

    print("Fetched %d records from %s" % (num_records, catalogue[1]))

def parse_response(response):
    text = response.data.decode(encoding="UTF-8")
    text = text[text.index('\n'):] #skip preamble
    return ET.fromstring("<root>" + text + "</root>")

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

def check_file_identifier(metadata_record):
    record_id = metadata_record.find("gmd:fileIdentifier/gco:CharacterString", namespaces)
    if record_id is None:
        record_id = metadata_record.attrib.get("uuid")

        if not record_id:
            record_id = metadata_record.attrib.get("id")
        else:
            record_id = str(uuid.uuid4().hex)

        id_element_text = '''
            <gmd:fileIdentifier
                xmlns:gco="http://www.isotc211.org/2005/gco"
                xmlns:gmd="http://www.isotc211.org/2005/gmd">

                <gco:CharacterString>%s</gco:CharacterString>
            </gmd:fileIdentifier>
        ''' % (record_id)
        id_element = ET.fromstring(id_element_text)
        metadata_record.insert(0, id_element)

def extract_id(metadata_record):
    return metadata_record.find("gmd:fileIdentifier/gco:CharacterString", namespaces).text

def xml_string(metadata_record):
    return Minidom.parseString(ET.tostring(metadata_record, "utf-8")).toprettyxml()

def main():
    # fetch_metadata_from_csw(("mrt", "https://data.thelist.tas.gov.au/datagn/srv/eng/csw"))
    # fetch_metadata_from_csw("aster-maps",
    #                "http://aster.nci.org.au/geonetwork/srv/en/csw")
    # fetch_metadata_from_url(("geological-survey-of-victoria",
    #                          "http://geology.data.vic.gov.au/searchAssistant/csw/gsv-solr-csw.xml"))


if __name__ == "__main__":
    main()
