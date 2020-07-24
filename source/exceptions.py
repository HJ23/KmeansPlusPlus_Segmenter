
class EXCEPTION(Exception):
    def __init__(self,msg):
        self.msg=msg
    def getError(self):
        return self.msg

class KVALUE_ERROR(EXCEPTION):
    def __init__(self,msg="K value error occured!"):
        exception.__init__(self,msg)

class IMAGE_PATH_ERROR(EXCEPTION):
    def __init__(self,msg="Image path entered is not valid"):
        exception.__init__(self,msg)

    