
GLOBAL_VAR = dict()

class Communication:
    def recv_announcement(self, conn):
        payload = self.RecvProto(conn)
        self.SendSignal(conn, 1)
        print(payload)
        GLOBAL_VAR['self'].__setattr__('announcement_', payload['announcement_body'])
        GLOBAL_VAR['self'].__setattr__('announcer_', payload['announcer'])
        GLOBAL_VAR['self'].__setattr__('date_', payload['date'])
        GLOBAL_VAR['create_announcement']()

class RequestsPanel:
    Communication = Communication()
    def signup(self, conn, data): # (username, password)
        self.SendProto(conn, data)
        return self.RecvSignal(conn)
    def login(self, conn, data):  # (username, password)
        self.SendProto(conn, data)
        return self.RecvSignal(conn)
    def get_classrooms(self, conn, data):
        if self.RecvSignal(conn):
            return self.RecvProto(conn)
        else:return []
    def create_classroom(self, conn, data):
        self.SendProto(conn, data)
        if self.RecvSignal(conn):
            return {'id': self.RecvSignal(conn)}
        else:return 0
    def announce(self, conn, data):
        self.SendProto(conn, data)
        return self.RecvSignal(conn)
    def get_announcements(self, conn, data):
        self.SendProto(conn, data)
        return self.RecvProto(conn)
    def submit_exam(self, conn, data):
        self.SendProto(conn, data)
        return self.RecvProto(conn)[0]
    def get_exams(self, conn, data):
        self.SendProto(conn, data)
        return self.RecvProto(conn)
    def get_people(self, conn, data):
        self.SendProto(conn, data)
        return self.RecvProto(conn)
    def get_grades(self, conn, data):
        self.SendProto(conn, data)
        return self.RecvProto(conn)
