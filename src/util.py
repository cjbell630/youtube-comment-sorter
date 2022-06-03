def replace_html_escapes(html: str):
    # TODO
    return html.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"").replace("&#39;", "'")