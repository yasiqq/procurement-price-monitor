import xml.etree.ElementTree as ET
from locale import currency

import requests

def read_quotes_from_cbr():

    url = 'https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/10/2024&date_req2=27/10/2026&VAL_NM_RQ=R01235'

    response = requests.get(url, timeout=5)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    records_data = root.findall("Record")

    quotes = []

    for record in records_data:
        date = record.get("Date")
        currency_id = record.get("Id")
        nominal = record.find("Nominal").text
        value = record.find("Value").text
        valuerate = record.find("VunitRate").text

        dict_row = {
            "Date": date,
            "Id": currency_id,
            "Nominal": nominal,
            "Value": value,
            "VunitRate": valuerate,
        }
        quotes.append(dict_row)

    return quotes


