import utils.connect


def fetch_settings():
    settings = utils.connect.get_settings()
    for setting in settings:
        print(setting)
    return settings
