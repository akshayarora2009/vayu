class machine_info :
    host = ""
    password = ""
    user = ""

    def __init__(self,user,host,password):
        self.host = host
        self.user = user
        self.password = password
