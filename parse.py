def convert_to_dict(HTML):
    values = HTML.find_all("td")
    parsed_data = {}

    # Use list comprehension instead of for loop
    keys = [values[i].text[8:] for i in range(0, len(values), 2)]
    values = [values[i + 1].text for i in range(0, len(values), 2)]

    # Use zip to combine keys and values
    for key, value in zip(keys, values):
        parsed_data[key] = "TBD" if value == " " else int(value)

    return parsed_data

def convert_to_dict_internal(HTML):
    values = HTML.find_all("td")
    parsed_data = {}

    # Use list comprehension and generator expressions
    keys = [values[i].text for i in range(0, len(values), 3)]
    internal_values = (values[i + 1].text for i in range(0, len(values), 3))
    practical_values = (values[i + 2].text for i in range(0, len(values), 3))

    # Use zip to combine keys, internal_values, and practical_values
    for key, internal_value, practical_value in zip(keys, internal_values, practical_values):
        parsed_data[key] = {
            "internal": "TBD" if internal_value == '' else int(internal_value),
            "practical": "TBD" if practical_value == " " else int(practical_value),
        }

    return parsed_data