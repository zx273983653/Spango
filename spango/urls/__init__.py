def url(regex, view=None):
    if view is None:
        view = regex

    return_json = {
        'regex': regex,
        'view': view,
        'args': None,
    }

    return return_json
