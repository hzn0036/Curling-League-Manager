class DuplicateOid(Exception):
    def __init__(self, oid):
        self.oid = oid

class DuplicateEmail(Exception):
    def __init__(self, email):
        self.email = email