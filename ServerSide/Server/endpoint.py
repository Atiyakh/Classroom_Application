from .Entities.student import Student
from .Entities.teacher import Teacher
from .Entities.user import User
from .protocol import loadConnectionProtocols, loadProtocols

class viewsRouting:
    def __init__(self, server):
        self.server = server
        loadConnectionProtocols(server)
        self.student = Student(); loadProtocols(self, self.student)
        self.teacher = Teacher(); loadProtocols(self, self.teacher)
        self.user = User(); loadProtocols(self, self.user)
        self.structure = {
            'student': self.student,
            'teacher': self.teacher,
            'user': self.user,
        }
