import json

class JsonParser:
    def __init__(self):
        pass

    def load_json(self, fileName, section = None):
        try:
            with open(fileName) as jf:
                if section is not None: 
                    return json.load(jf)[section]
                else:
                    return json.load(jf)

        except Exception as e:
            raise(e)

    def write_section(self, fileName, section = None):
        jd = self.load_json(fileName)

        if section in jd:
            print('Section found')
