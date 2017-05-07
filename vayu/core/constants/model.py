class machine_info :
    host = ""
    password = ""
    user = ""

    def __init__(self,user,host,password):
        self.host = host
        self.user = user
        self.password = password

class project_info :
    id = ""
    path = ""
    entry_point = ""
    type = ""

    def __init__(self,id,type,path,entry_point,port_number):
        self.id = id
        self.path = path
        self.entry_point = entry_point
        self.type = type
        self.port = port_number