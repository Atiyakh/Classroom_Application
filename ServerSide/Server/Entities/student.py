import time

class Student:
    async def signup(self, conn):
        payload = await self.RecvProto(conn)
        if self.DB.Check(self.student_account, self.where[self.student_account.username == payload['username']]):
            await self.SendSignal(conn, 0)
        else:
            self.DB.Insert(self.student_account, {
                'username': payload['username'],
                'password': self.Crypto.Hash.Sha512(payload['password']),
                '_connection_': conn
            })
            await self.SendSignal(conn, 1)
    async def login(self, conn):
        payload = await self.RecvProto(conn)
        password_hashed = self.Crypto.Hash.Sha512(payload['password'])
        if self.DB.Check(self.student_account, self.where[(self.student_account.username == payload['username']) & (self.teacher_account.password == password_hashed)]):
            self.DB.Update(self.student_account, where=self.where[(self.student_account.username == payload['username']) & (self.student_account.password == password_hashed)],data={
                '_connection_': conn
            })
            await self.SendSignal(conn, 1)
        else:
            await self.SendSignal(conn, 0)
    async def get_classrooms(self, conn):
        query = self.DB.Check(self.student_account, self.where[self.student_account._connection_ == conn], fetch=1, columns=['id'])
        if query:
            query_2 = self.DB.Check(self.studet_classroom, self.where[self.studet_classroom.studetId == query[0][0]], fetch='*', columns=['classroomId'])
            print(query_2)
            classes = []
            for q in query_2:
                classroomId = q[0]
                classes.append(self.DB.Check(self.classroom, self.where[self.classroom.id == classroomId], fetch='1', columns=['id', 'classroom_name', 'classroom_description'])[0])
            await self.SendSignal(conn, 1)
            await self.SendProto(conn, classes)
        else:
            await self.SendSignal(conn, 0)
    async def enter_classroom(self, conn):
        payload = await self.RecvProto(conn)
        if self.DB.Check(self.classroom, self.where[self.classroom.id == payload['classroomId']]):
            query = self.DB.Check(self.student_account, self.where[self.student_account._connection_ == conn], fetch=1, columns=['id'])
            if query:
                self.DB.Insert(self.studet_classroom, {
                    'studetId': query[0][0],
                    'classroomId': payload['classroomId']
                })
                query_2 = self.DB.Check(self.classroom, self.where[self.classroom.id == payload['classroomId']], fetch=1, columns=['classroom_name', 'classroom_description'])
                await self.SendSignal(conn, 1)
                await self.SendProto(conn, {
                    'name': query_2[0][0],
                    'desc': query_2[0][1]
                })
            else:
                await self.SendSignal(conn, 0)
        else:
            await self.SendSignal(conn, 0)
    async def get_announcements(self, conn):
        classroomId = (await self.RecvProto(conn))['classroomId']
        query = self.DB.Check(self.announcement, self.where[self.announcement.classroomId == classroomId], fetch='*', columns=['announcement_body', 'announcer_name', 'date'])
        await self.SendProto(conn, query)
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
    async def get_exams(self, conn):
        classroomId = (await self.RecvProto(conn))['classroomId']
        query = self.DB.Check(self.exam, self.where[self.exam.classroomId == classroomId], fetch='*', columns=['id', 'exam_name'])
        await self.SendProto(conn, query)
    async def get_exam(self, conn):
        examId = (await self.RecvProto(conn))['examId']
        validation = self.DB.Check(self.student_account, self.where[self.student_account._connection_ == conn], fetch=1, columns=['id'])
        if validation:
            if not self.DB.Check(self.student_exam, self.where[(self.student_exam.studetId == validation[0][0]) & (self.student_exam.examId == examId)]):
                query = self.DB.Check(self.exam, self.where[self.exam.id == examId], fetch=1, columns=['num'])
                if query:
                    num = query[0][0]
                    query_2 = self.DB.Check(self.mcq, self.where[self.mcq.examId == examId], fetch='*', columns=['question', 'ch1', 'ch2', 'ch3', 'ch4', 'ch1_', 'ch2_', 'ch3_', 'ch4_', 'id'])
                    query_3 = self.DB.Check(self.tf, self.where[self.tf.examId == examId], fetch='*', columns=['question', 'answer', 'id'])
                    await self.SendSignal(conn, 1)
                    await self.SendProto(conn, [num, query_2, query_3])
            else:
                query = self.DB.Check(self.student_exam, self.where[(self.student_exam.studetId == validation[0][0]) & (self.student_exam.examId == examId)], fetch=1, columns=['id'])
                if query:
                    query_2 = self.DB.Check(self.question_answer, self.where[self.question_answer.studentExamId == query[0][0]], fetch='*', columns=['MCQId', 'TFId', 'answer'])
                    if query_2:
                        query_3 = self.DB.Check(self.exam, self.where[self.exam.id == examId], fetch=1, columns=['num'])
                        if query_3:
                            num = query[0][0]
                            MCQs = self.DB.Check(self.mcq, self.where[self.mcq.examId == examId], fetch='*', columns=['question', 'ch1', 'ch2', 'ch3', 'ch4', 'ch1_', 'ch2_', 'ch3_', 'ch4_', 'id'])
                            TFs = self.DB.Check(self.tf, self.where[self.tf.examId == examId], fetch='*', columns=['question', 'answer', 'id'])
                    MCQ_data = []; TF_data = []
                    for question in query_2:
                        if question[0]:
                            for MCQ_ in MCQs:
                                if MCQ_[9] == question[0]:
                                    MCQ_data.append(MCQ_+(question[2], ))
                        elif question[1]:
                            for TF_ in TFs:
                                if TF_[2] == question[0]:
                                    TF_data.append(TF_+(question[2], ))
                    await self.SendSignal(conn, 2)
                    await self.SendProto(conn, [num, MCQ_data, TF_data])
        else: await self.SendSignal(conn, 0)
    async def submit_exam(self, conn):
        payload = await self.RecvProto(conn)
        print(payload['data'])
        query = self.DB.Check(self.student_account, self.where[self.student_account._connection_ == conn], fetch=1, columns=['id'])
        if query:
            studentExamId = self.DB.Insert(self.student_exam, {
                'studetId': query[0][0],
                'examId': payload['examId'],
                'mark': payload['mark']
            })
            for question in payload['data']:
                print(question)
                type_= 'MCQId' if question[1] == 'MCQ' else 'TFId'
                self.DB.Insert(self.question_answer, {
                    'studentExamId': studentExamId,
                    type_: question[0],
                    'answer': question[2]
                })
            await self.SendSignal(conn, 1)
        else:
            await self.SendSignal(conn, 0)
