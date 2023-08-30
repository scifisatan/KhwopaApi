from scrapper import *



def convert_to_dict(HTML):
    values = HTML.find_all("td")
    parsed_data = {}

    for i in range(0, len(values), 2):
        key = values[i].text[8:]
        value = values[i + 1].text
        parsed_data[key] = "TBD" if value == " " else int(value)

    return parsed_data


def convert_to_dict_internal(HTML):
    values = HTML.find_all("td")
    parsed_data = {}

    for i in range(0, len(values), 3):
        key = values[i].text
        internal_value = values[i + 1].text
        practical_value = values[i + 2].text

        parsed_data[key] = {
            "internal": "TBD" if internal_value == '' else int(internal_value),
            "practical": "TBD" if practical_value == " " else int(practical_value),
        }

    return parsed_data
