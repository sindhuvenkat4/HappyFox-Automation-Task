from jproperties import Properties

class Data:
    config = Properties()
    with open('C:\\Users\\admin\\PycharmProjects\\HappyFoxAssignment\\config.properties', 'rb') as data:
        config.load(data)
    browser = config["browser"].data



