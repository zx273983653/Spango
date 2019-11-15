def url(regex, view=None):
    if view is None:
        view = regex

    return_json = {
        'regex': regex,
        'view': view,
    }

    return return_json
