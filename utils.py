def parse_int_list(text):
    text = text.replace(",", " ").replace("\n", " ")
    parts = [x.strip() for x in text.split() if x.strip()]
    return [int(x) for x in parts]