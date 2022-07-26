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

    def write_section(self, fileName, data):

        try:
            with open(fileName, 'w') as jf:
                jf.write(json.dumps(data))

        except Exception as e:
            raise(e)
