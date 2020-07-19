import os
from bs4 import BeautifulSoup as BS
from xml.etree import ElementTree as ET
import lxml

from fetcher import parse_ncbi

def find_thing(raw, search_query):
    soup = BS(raw, 'lxml')


def main():
    # test_gene = "Opuntia AND Rpl16"
    test_gene = "QEHR01000001"
    parsed = parse_ncbi(test_gene, "gb")
    find_thing(parsed, "..")


    # write_to_file(parsed)


    # print(parsed[0]["GBSeq_feature-table"][3]['GBFeature_quals'][0]['GBQualifier_value'])


if __name__ == "__main__":
    main()
