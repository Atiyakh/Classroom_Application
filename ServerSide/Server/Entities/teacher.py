import time

class Teacher:
    async def signup(self, conn):
        payload = await self.RecvProto(conn)
        if self.DB.Check(self.teacher_account, self.where[self.teacher_account.username == payload['username']]):
            await self.SendSignal(conn, 0)
        else:
            self.DB.Insert(self.teacher_account, {
                'username': payload['username'],
                'password': self.Crypto.Hash.Sha512(payload['password']),
                '_connection_': conn
            })
            await self.SendSignal(conn, 1)
    async def login(self, conn):
        payload = await self.RecvProto(conn)
        password_hashed = self.Crypto.Hash.Sha512(payload['password'])
        if self.DB.Check(self.teacher_account, self.where[(self.teacher_account.username == payload['username']) & (self.teacher_account.password == password_hashed)]):
            self.DB.Update(self.teacher_account, where=self.where[(self.teacher_account.username == payload['username']) & (self.teacher_account.password == password_hashed)],data={
                '_connection_': conn
            })
            await self.SendSignal(conn, 1)
        else:
            await self.SendSignal(conn, 0)
    async def get_classrooms(self, conn):
        query = self.DB.Check(self.teacher_account, self.where[self.teacher_account._connection_ == conn], fetch=1, columns=['id'])
        if query:
            classes = self.DB.Check(self.classroom, self.where[self.classroom.teacherId == query[0][0]], fetch='*', columns=['id', 'classroom_name', 'classroom_description'])
            await self.SendSignal(conn, 1)
            await self.SendProto(conn, classes)
        else:
            await self.SendSignal(conn, 0)
    async def create_classroom(self, conn):
        payload = await self.RecvProto(conn)
        query = self.DB.Check(self.teacher_account, self.where[self.teacher_account._connection_ == conn], fetch=1, columns=['id'])
        if query:
            if not self.DB.Check(self.classroom, self.where[(self.classroom.teacherId == query[0][0]) & (self.classroom.classroom_name == payload['classroom_name'])]):
                self.DB.Insert(self.classroom, {
                    'teacherId': query[0][0],
                    'classroom_name': payload['classroom_name'],
                    'classroom_description': payload['classroom_description'],
                })
                query_2 = self.DB.Check(self.classroom, self.where[
                    (self.classroom.teacherId == query[0][0]) & (self.classroom.classroom_name == payload['classroom_name'])
                ], columns=['id'], fetch=1)
                if query_2:
                    await self.SendSignal(conn, 3)
                    await self.SendSignal(conn, query_2[0][0])
                else:
                    await self.SendSignal(conn, 2)
            await self.SendSignal(conn, 1)
        else:
            await self.SendSignal(conn, 0)
    async def announce(self, conn):
        payload = await self.RecvProto(conn)
        date = time.ctime()
        self.DB.Insert(self.announcement, {
            'announcement_body': payload['announcement_body'],
            'announcer_name': payload['announcer_name'],
            'classroomId': payload['classroomId'],
            'date': date
        })
        await self.SendSignal(conn, 1)
        query = self.DB.Check(self.classroom, self.where[self.classroom.id == payload['classroomId']], fetch='1', columns=['teacherId'])
        if query:
            teacheId = query[0][0]
            query_2 = self.DB.Check(self.teacher_account, self.where[self.teacher_account.id == teacheId], fetch='1', columns=['_connection_'])
            if query_2:
                teacher_ip = query_2[0][0]
                conn_1 = self.Connections[teacher_ip]
                if conn_1:
                    teacher_connection = await self.Communicate(conn, conn_1, 'recv_announcement')
                    if teacher_connection:
                        await self.SendProto(teacher_connection, {
                            'announcement_body': payload['announcement_body'],
                            'announcer': payload['announcer_name'],
                            'date': date
                        })
                        await self.RecvSignal(teacher_connection)
        query_3 = self.DB.Check(self.studet_classroom, self.where[self.studet_classroom.classroomId == payload['classroomId']], fetch='*', columns=['studetId'])
        for id_ in query_3:
            query_4 = self.DB.Check(self.student_account, self.where[self.student_account.id == id_[0]], fetch='*', columns=['_connection_'])
            if query_4:
                student_ip = query_4[0][0]
                conn_2 = self.Connections[student_ip]
                if conn_2:
                    student_connection = await self.Communicate(conn, conn_2, 'recv_announcement')
                    if student_connection:
                        await self.SendProto(student_connection, {
                            'announcement_body': payload['announcement_body'],
                            'announcer': payload['announcer_name'],
                            'date': date
                        })
                        await self.RecvSignal(student_connection)
    async def get_announcements(self, conn):
        classroomId = (await self.RecvProto(conn))['classroomId']
        query = self.DB.Check(self.announcement, self.where[self.announcement.classroomId == classroomId], fetch='*', columns=['announcement_body', 'announcer_name', 'date'])
        await self.SendProto(conn, query)
    async def submit_exam(self, conn):
        payload = await self.RecvProto(conn)
        examId = self.DB.Insert(self.exam, {
            'exam_name': payload['exam_name'],
            'num': payload['num'],
            'classroomId': payload['classroomId']
        })
        for MCQ in payload['MCQs']:
            self.DB.Insert(self.mcq, {
                'question':MCQ['question'],
                'ch1': MCQ['ch1'][0],
                'ch2': MCQ['ch2'][0],
                'ch3': MCQ['ch3'][0],
                'ch4': MCQ['ch4'][0],
                'ch1_': MCQ['ch1'][1],
                'ch2_': MCQ['ch2'][1],
                'ch3_': MCQ['ch3'][1],
                'ch4_': MCQ['ch4'][1],
                'examId': examId
            })
        for TF in payload['TFs']:
            self.DB.Insert(self.tf, {
                'question': TF['statement'],
                'answer': TF['answer'],
                'examId': examId
            })
        await self.SendProto(conn, [examId])
    async def get_exams(self, conn):
        classroomId = (await self.RecvProto(conn))['classroomId']
        query = self.DB.Check(self.exam, self.where[self.exam.classroomId == classroomId], fetch='*', columns=['id', 'exam_name'])
        await self.SendProto(conn, query)
    async def get_people(self, conn):
        classroomId = (await self.RecvProto(conn))['classroomId']
        query = self.DB.Check(self.studet_classroom, self.where[self.studet_classroom.classroomId == classroomId], fetch='*', columns=['studetId'])
        response = []
        if query:
            for student_id in query:
                query_1 = self.DB.Check(self.student_account, self.where[self.student_account.id == student_id[0]], fetch=1, columns=['username'])
                if query_1:
                    response.append({
                        'username': query_1[0][0],
                        'id': student_id[0]
                    })
        await self.SendProto(conn, response)
    async def get_grades(self, conn):
        classroomId = (await self.RecvProto(conn))['classroomId']
        query = self.DB.Check(self.studet_classroom, self.where[self.studet_classroom.classroomId == classroomId], fetch='*', columns=['studetId'])
        response = []
        if query:
            for student_id in query:
                query_1 = self.DB.Check(self.student_account, self.where[self.student_account.id == student_id[0]], fetch=1, columns=['username'])
                if query_1:
                    query_2 = self.DB.Check(self.student_exam, self.where[self.student_exam.studetId == student_id[0]], fetch='*', columns=['examId', 'mark'])
                    if query_2:
                        Exam = dict()
                        for exam_ in query_2:
                            examId = exam_[0]
                            query_3 = self.DB.Check(self.exam, self.where[self.exam.id == examId], fetch=1, columns=['exam_name'])
                            if query_3:
                                Exam[query_3[0][0]] = exam_[1]
                response.append({
                    'name': query_1[0][0],
                    'id': student_id[0],
                    'exam': Exam
                })
        await self.SendProto(conn, response)
