def replace_html_escapes(html: str):
    # TODO
    return html.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&#39;", "'")


def dict_to_json_string(elem):
    if type(elem) is dict:
        return "{" + ", ".join([f"\"{k}\": {dict_to_json_string(v)}" for k, v in elem.items()]) + "}"
    elif type(elem) is list:
        return "[" + ", ".join([dict_to_json_string(e) for e in elem]) + "]"
    elif type(elem) is str:
        return "\"" + elem.replace("\"", "\\\"").replace("\n", "\\n") + "\""
    elif type(elem) is bool:
        return "\"true\"" if elem else "\"false\""
    else:
        return str(elem)
