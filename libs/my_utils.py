import os.path

class MyUtils:
    def __init__(self):
        pass

    def touch_file(self, fileName, mode):
        try:
            with open(fileName, mode) as jf:
                jf.write('{}')
                pass

        except Exception as e:
            raise(e)

    def file_exists(self, fileName):
        return os.path.exists(fileName)


