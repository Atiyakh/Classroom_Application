from Client.connection_vent import *
from request import RequestsPanel as requests
from PyQt5.QtWidgets import *
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from time import ctime
from request import GLOBAL_VAR
import sys, random

class QCheckEdit(QCheckBox):
    def focusOutEvent_(self, e):
        self.updateLabelText()
    def __init__(self, label='', parent=None):
        super().__init__(label, parent)
        # Create a line edit widget
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedHeight(23)
        self.line_edit.hide()  # Initially hidden
        self.line_edit.focusOutEvent = self.focusOutEvent_
        self.line_edit.returnPressed.connect(self.updateLabelText)

    def mouseDoubleClickEvent(self, event):
        self.line_edit.setText(self.text())
        self.line_edit.selectAll()
        self.line_edit.setFocus()
        self.line_edit.show()
        
    def updateLabelText(self):
        new_text = self.line_edit.text()
        self.setText(new_text)
        self.line_edit.hide()

class Student(QMainWindow):
    class QExamWindow(QScrollArea):
        def __init__(self, mainclass, id_, check):
            super().__init__()
            self.id_ = id_
            mainclass.scroll_content_layout_2.addWidget(self)
            self.mainclass = mainclass
            self.setStyleSheet('background-color: #444; color: #FFF')
            self.setWidgetResizable(True)
            self.widget_ = QWidget()
            self.widget_.setStyleSheet('background-color: #444; color: #FFF; border-radius: 5px')
            self.setWidget(self.widget_)

            # Set window properties
            self.setWindowTitle("Dark Theme Quiz Platform")
            self.setGeometry(100, 100, 700, 450)

            # Create layout
            self.layout = QVBoxLayout(self.widget_)
            self.layout.setAlignment(Qt.AlignTop)

            # Add submit button
            if not check:
                submit_button = QPushButton("Submit")
                submit_button.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                submit_button.setObjectName("SubmitButton")
                submit_button.clicked.connect(self.submit_answers)
            else:
                submit_button = QPushButton("Close")
                submit_button.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                submit_button.setObjectName("SubmitButton")
                submit_button.clicked.connect(self.hide)
            self.layout.addWidget(submit_button)

            self.setStyleSheet("""
        QGroupBox#QuestionGroupBox {
            color: white;
            background-color: #444;
            border: 1px solid white;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        QGroupBox#QuestionGroupBox > * {
            margin: 10px;
        }
        QRadioButton#AnswerButton {
            background-color: #444;
            color: white;
        }
        QPushButton#SubmitButton {
            color: white;
            background-color: #444;
            border: 1px solid white;
            border-radius: 5px;
            padding: 5px 10px;
        }
        QPushButton#SubmitButton:hover {
            background-color: #444;
        }
    """)
        def load_correct_answers(self, list_):
            self.correct_answers = list_

        def add_question(self, question_text, choices, id_of_question, check=None):
            question_group_box = QGroupBox("Question: " + question_text)
            question_group_box.setFont(QFont('arial', 16))
            question_group_box.setObjectName("QuestionGroupBox")
            question_layout = QVBoxLayout()
            question_group_box.setLayout(question_layout)
            num = 0
            for choice in choices:
                answer_button = QRadioButton(choice)
                if choice == check:
                    answer_button.setStyleSheet('color: red;')
                answer_button.id_of_question = id_of_question
                if len(choices) == 2:answer_button.type_of_question = 'TF'
                else:answer_button.type_of_question = 'MCQ'
                answer_button.setFont(QFont('arial', 16))
                answer_button.setObjectName("AnswerButton")
                question_layout.addWidget(answer_button)
                num+=1

            self.layout.insertWidget(0, question_group_box)

        def submit_answers(self):
            IDs = []
            answers = []
            for i in range(self.layout.count()):
                question_group_box = self.layout.itemAt(i).widget()
                question_layout = question_group_box.layout()
                if question_layout:
                    x = True
                    for j in range(question_layout.count()):
                        answer_button = question_layout.itemAt(j).widget()
                        if answer_button.isChecked():
                            x = False
                            IDs.append([answer_button.id_of_question, answer_button.type_of_question])
                            answers.append(answer_button.text())
            score = 0
            answers = list(reversed(answers))
            data = []
            for i in range(len(answers)):
                if answers[i] == self.correct_answers[i]:
                    score+=1
                    data.append(IDs[i]+[answers[i]])
            if self.mainclass.Server.PostRequest(requests.submit_exam,{
                'examId': self.id_,
                'mark': f"{score}/{len(answers)}",
                'data': data
            }):
                QMessageBox.information(self, "Answers", f"{score}/{len(answers)}")
            else:
                QMessageBox.information(self, "Answers", "Error")
            self.hide()
    def __init__(self):
        self.Server = ConnectionHandler(self)
        self.initiate()
    def initiate(self):
        super().__init__()
        self.setStyleSheet("background-color: #222222;")
        self.setWindowIcon(QtGui.QIcon('static\\icon.png'))
        self.mian_widget_1 = QWidget()
        self.setCentralWidget(self.mian_widget_1)
        self.mian_widget_1.setWindowTitle("Classroom - Student's Version")
        self.mian_widget_1.setStyleSheet("background-color: #222222;")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.mian_widget_1.setLayout(main_layout)

        title_label = QLabel("Classroom - Student's Version")
        title_label.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)

        title_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.addLayout(title_layout)

        form_layout = QVBoxLayout()
        form_layout.setAlignment(QtCore.Qt.AlignCenter)

        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #ffffff; font-size: 16px;")

        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 8px;")

        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #ffffff; font-size: 16px;")

        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 8px;")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.USERNAME = ''
        
        def login_button_f(e):
            response = self.Server.PostRequest(requests.login, data={
                'username': self.username_input.text(),
                'password': self.password_input.text()
            })
            if response:
                self.USERNAME = self.username_input.text()
                self.classrooms = self.Server.PostRequest(requests.get_classrooms, None)
                for classroom in self.classrooms:
                    insert_classroom(*classroom)
                self.setCentralWidget(self.main_widget_2)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Username or password is incorrect")
                msg.setWindowTitle("Classroom:")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        login_button.setCursor(QtCore.Qt.PointingHandCursor)
        login_button.clicked.connect(login_button_f)

        def sign_up_button_f(e):
            response = self.Server.PostRequest(requests.signup, data={
                'username': self.username_input.text(),
                'password': self.password_input.text()
            })
            if response:
                self.USERNAME = self.username_input.text()
                self.classrooms = self.Server.PostRequest(requests.get_classrooms, None)
                for classroom in self.classrooms:
                    insert_classroom(*classroom)
                self.setCentralWidget(self.main_widget_2)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("The username you entered already exists")
                msg.setWindowTitle("Classroom:")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.setStyleSheet("background-color: #555555; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 8px;")
        sign_up_button.setCursor(QtCore.Qt.PointingHandCursor)
        sign_up_button.clicked.connect(sign_up_button_f)

        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_button)
        form_layout.addWidget(sign_up_button)
        
        self.main_widget_2 = QWidget()
        self.main_widget_2.setStyleSheet("background-color: #222222;")
        
        main_layout.addLayout(form_layout)
        
        self.setWindowTitle("Classroom")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.main_widget_2.setLayout(main_layout)

        # Upper Section - Create New Class
        create_class_layout = QVBoxLayout()

        create_title_label = QLabel("Enter new class")
        create_title_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        create_class_layout.addWidget(create_title_label)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText('Classroom id')
        self.id_input.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 8px;")
        create_class_layout.addWidget(self.id_input)

        def create_button_f(e):
            id_ = self.id_input.text()
            response = self.Server.PostRequest(requests.enter_classroom, {
                'classroomId': id_
            })
            if response and response != 0:
                insert_classroom(id_, response['name'], response['desc'])
                self.id_input.setText('')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("enrollment refused!")
                msg.setWindowTitle("Classroom:")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
        
        create_button = QPushButton("Enter")
        create_button.clicked.connect(create_button_f)
        create_button.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        create_class_layout.addWidget(create_button)

        main_layout.addLayout(create_class_layout)

        # Lower Section - Existing Classrooms
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 10px;")
        scroll_area.setWidgetResizable(True)

        scroll_content_widget = QWidget()
        scroll_content_layout = QVBoxLayout()
        scroll_content_layout.setContentsMargins(1,1,1,1)
        scroll_content_widget.setLayout(scroll_content_layout)
        scroll_content_layout.setAlignment(Qt.AlignTop)

        classes_title_label = QLabel("Classrooms available")
        classes_title_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        scroll_content_layout.addWidget(classes_title_label)

        class QLabel_clickable(QLabel):
            x = 0
            mainclass = self
            def mode(self, x, id_):
                self.id_ = id_
                self.x = 1
            def insert_data(self, id_, name_, desc_):
                self.id_ = id_
                self.name_ = name_
                self.desc_ = desc_
            def mousePressEvent(self, e):
                if self.x:
                    response = self.mainclass.Server.PostRequest(requests.get_exam, {
                        'examId': self.exam_id
                    })
                    if response:
                        exam = self.mainclass.QExamWindow(self.mainclass, self.id_,
                            check=True if response[0]==2 else False)
                        num = response[1][0]; MCQs = response[1][1]; TFs = response[1][2]
                        switch = True
                        NUM = 0
                        correct_answers = []
                        while True:
                            if NUM == num:break
                            else:
                                if switch:
                                    if MCQs:
                                        Q = MCQs.pop(random.randint(0,len(MCQs)-1))
                                        exam.add_question(Q[0], [Q[1], Q[2], Q[3], Q[4]], Q[9],
                                            check=Q[10] if response[0]==2 else None)
                                        if Q[5]:answer = Q[1]
                                        elif Q[6]:answer = Q[2]
                                        elif Q[7]:answer = Q[3]
                                        elif Q[8]:answer = Q[4]
                                        correct_answers.append(answer)
                                        NUM += 1
                                else:
                                    if TFs:
                                        Q = TFs.pop(random.randint(0,len(TFs)-1))
                                        exam.add_question(Q[0], ['True', 'False'], Q[2],
                                            check=Q[3] if response[0]==2 else None)
                                        correct_answers.append('True') if Q[1] else correct_answers.append('False')
                                        NUM += 1
                                switch = bool(random.randint(0,1))
                        exam.load_correct_answers(correct_answers)
                        exam.show()
                else:
                    self.mainclass.CLASS_ID = self.id_
                    self.mainclass.CLASS_NAME = self.name_
                    self.mainclass.CLASS_DESC = self.desc_
                    self.mainclass.setCentralWidget(self.mainclass.main_widget_3)
                    load_announcements()
                    load_exams()
                    self.mainclass.setWindowTitle(self.mainclass.CLASS_NAME)
                    self.mainclass.tab1_background_image_label.setText(self.mainclass.CLASS_NAME)
                    self.mainclass.tab1_background_image_label.adjustSize()
                    self.mainclass.setMinimumSize(1000, 550)

        def insert_classroom(id_, name, desc):
            classroom_widget = QWidget()
            classroom_widget.__class__.id_ = id_
            classroom_widget.__class__.name_ = name
            classroom_widget.__class__.desc_ = desc
            classroom_widget.setStyleSheet("border: 1px solid #555555; border-radius: 8px; padding: 10px;")
            classroom_layout = QVBoxLayout(classroom_widget)

            classroom_name_label = QLabel_clickable(f'[{id_}] ' + name)
            classroom_name_label.insert_data(id_, name, desc)
            classroom_name_label.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold;  border-color:  #333333;")
            classroom_layout.addWidget(classroom_name_label)

            classroom_description_label = QLabel(desc)
            classroom_description_label.setStyleSheet("color: #ffffff; font-size: 14px;border-color:  #333333;")
            classroom_layout.addWidget(classroom_description_label)

            scroll_content_layout.addWidget(classroom_widget)
        
        scroll_area.setWidget(scroll_content_widget)
        main_layout.addWidget(scroll_area)
        
        self.setWindowIcon(QIcon('static\\icon.png'))
        self.main_widget_3 = QWidget()
        self.main_widget_3.setStyleSheet('background-color: #222222;')
        self.main_layout_3 = QVBoxLayout()
        self.main_layout_3.setAlignment(Qt.AlignHCenter)
        self.main_widget_3.setLayout(self.main_layout_3)
        self.tabs_layout = QHBoxLayout()
        self.tabs_widget = QWidget()
        self.tabs_widget.setLayout(self.tabs_layout)

        self.tab2 = QScrollArea()
        self.tab2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab2.setFixedWidth(970)
        self.tab2.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 10px;")
        self.tab2.setWidgetResizable(True)
        self.tab2.setParent(None)

        scroll_content_widget_2 = QWidget()
        scroll_content_layout_2 = QVBoxLayout()
        self.scroll_content_layout_2 = scroll_content_layout_2
        scroll_content_layout_2.setContentsMargins(1,1,1,1)
        scroll_content_widget_2.setLayout(scroll_content_layout_2)
        scroll_content_layout_2.setAlignment(Qt.AlignTop)
        self.tab2.setWidget(scroll_content_widget_2)
        
        self.tab1 = QScrollArea()
        self.tab1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab1.setFixedWidth(970)
        self.tab1.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 10px;")
        self.tab1.setWidgetResizable(True)
        self.tab1.setParent(None)

        scroll_content_widget_1 = QWidget()
        scroll_content_layout_1 = QVBoxLayout()
        scroll_content_layout_1.setContentsMargins(1,1,1,1)
        scroll_content_widget_1.setLayout(scroll_content_layout_1)
        scroll_content_layout_1.setAlignment(Qt.AlignTop)
        self.tab1.setWidget(scroll_content_widget_1)
        
        # tab_1:
        self.TAB = 0
        def tab_1_f():
            if self.TAB != 1: 
                tab_1.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_2.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                for child in self.main_widget_3.children():
                    if child in [self.tab1, self.tab2]:
                        child.setParent(None)
                self.main_layout_3.addWidget(self.tab1)
                self.TAB = 1
        tab_1 = QPushButton("Stream")
        tab_1.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_1.setCursor(Qt.PointingHandCursor)
        tab_1.clicked.connect(tab_1_f)
        # tab_2
        def tab_2_f():
            if self.TAB != 2: 
                tab_2.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_1.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                for child in self.main_widget_3.children():
                    if child in [self.tab1, self.tab2]:
                        child.setParent(None)
                self.main_layout_3.addWidget(self.tab2)
                self.TAB = 2
        tab_2 = QPushButton("Exams")
        tab_2.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_2.setCursor(Qt.PointingHandCursor)
        tab_2.clicked.connect(tab_2_f)

        self.tabs_layout.addWidget(tab_1)
        self.tabs_layout.addWidget(tab_2)

        self.main_layout_3.addWidget(self.tabs_widget)
        tab_1_f()
        
        self.tab1_background_image = QWidget()
        scroll_content_layout_1.addWidget(self.tab1_background_image)
        self.tab1_background_image.setStyleSheet("background-color: #444444; border-radius: 8px; background-image : url(static/image.jpg); background-position: center center;")
        self.tab1_background_image.setMaximumHeight(250)
        self.tab1_background_image.setMinimumHeight(200)
        self.tab1_background_image_label = QLabel(self.tab1_background_image)
        font = QFont('Arial', 25)
        font.setBold(True)
        self.tab1_background_image_label.setFont(font)
        self.tab1_background_image_label.setStyleSheet("background-color: transparent; border-top-right-radius: 10px; background-image : url(); color: #FFF")
        self.tab1_background_image_label.adjustSize()
        self.tab1_background_image_label.show()
        
        class MyPlainTextEdit(QPlainTextEdit):
            def focusInEvent(self, event):
                self.setStyleSheet(
                    "QPlainTextEdit {"
                    "    background-color: #444444;"
                    "    color: #FFF;"
                    "    border: 1px solid #4d90fe;"
                    "    border-radius: 4px;"
                    "    padding: 4px;"
                    "    selection-background-color: #a3c4ff;"
                    "}"
                )
                super().focusInEvent(event)

            def focusOutEvent(self, event):
                self.setStyleSheet(
                    "QPlainTextEdit {"
                    "    color: #FFF;"
                    "    background-color: #444444;"
                    "    border: 1px solid #555555;"
                    "    border-radius: 4px;"
                    "    padding: 4px;"
                    "    selection-background-color: #a3c4ff;"
                    "}"
                )
                super().focusOutEvent(event)
        
        widget_post = QWidget()
        widget_post_layout = QVBoxLayout()
        widget_post_layout.setContentsMargins(0, 0, 0, 0)
        widget_post_layout.setAlignment(Qt.AlignTop)
        widget_post.setLayout(widget_post_layout)
        
        plain_text_post = MyPlainTextEdit()
        plain_text_post.setPlaceholderText('announce something to your class')
        plain_text_post.setStyleSheet(
                    "QPlainTextEdit {"
                    "    color: #FFF;"
                    "    background-color: #444444;"
                    "    border: 1px solid #555555;"
                    "    border-radius: 4px;"
                    "    padding: 4px;"
                    "    selection-background-color: #a3c4ff;"
                    "}"
                )
        plain_text_post.setFont(QFont('arial', 13))
        plain_text_post.setFixedHeight(140)
        widget_post_layout.addWidget(plain_text_post)
        
        widget_post_tools = QWidget()
        widget_post_tools.setStyleSheet('border-color:#555; border-width: 0px; border-style: solid;')
        widget_post_tools_layoust = QVBoxLayout()
        widget_post_tools_layoust.setAlignment(Qt.AlignTop)
        widget_post_tools_layoust.setContentsMargins(0,0,0,0)
        widget_post_tools.setLayout(widget_post_tools_layoust)
        widget_post_layout.addWidget(widget_post_tools)
        
        widget_post_tools_buts = QWidget()
        widget_post_tools_buts.setFixedHeight(45)
        widget_post_tools_buts_layout = QHBoxLayout()
        widget_post_tools_buts.setLayout(widget_post_tools_buts_layout)
        
        class QAnnouncementWidget(QWidget):
            def load_data(self, announcement, announcer, date):
                self.announcement = announcement
                self.announcer = announcer
                self.date = date
            def create(self):
                scroll_content_layout_1.insertWidget(2, self)
                self.layout = QVBoxLayout()
                self.setLayout(self.layout)
                # announcer's name label
                self.Announcer = QLabel(self.announcer)
                self.Announcer.setFixedWidth(917)
                self.Announcer.setStyleSheet('color: white; background-color: #333; border-color: #444; border-width: 0px; border-style:solid; border-radius: 5px;')
                f = QFont('Arial', 20); f.setBold(True)
                self.Announcer.setFont(f)
                self.layout.addWidget(self.Announcer)
                # date label
                self.date_label = QLabel(self.date)
                self.date_label.setFixedWidth(917)
                self.date_label.setStyleSheet('color: white; background-color: #333; border-color: #444; border-width: 0px; border-style:solid; border-radius: 5px;')
                self.date_label.setFont(QFont('Arial', 9))
                self.layout.addWidget(self.date_label)
                # announcement label
                self.Announcement = QLabel(self.announcement)
                self.Announcement.setWordWrap(True)
                self.Announcement.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.Announcement.setFixedWidth(917)
                self.Announcement.adjustSize()
                self.Announcement.setStyleSheet('color: white; background-color: #333; border-color: #444; border-width: 1px; border-style:solid; border-radius: 5px;')
                self.Announcement.setFont(QFont('Arial', 13))
                self.layout.addWidget(self.Announcement)
        
        def link_1_f():
            announcement_widget = QAnnouncementWidget()
            announcement_widget.load_data(
                announcement=self.announcement_,
                announcer=self.announcer_,
                date=self.date_
            )
            announcement_widget.create()
        link_1 = QPushButton()
        link_1.clicked.connect(link_1_f)
        GLOBAL_VAR['create_announcement'] = link_1.click
        GLOBAL_VAR['self'] = self
        
        def load_announcements():
            announcements = self.Server.PostRequest(requests.get_announcements, {
                'classroomId': self.CLASS_ID
            })
            
            for announcement_body, announcer, date in announcements:
                announcement = QAnnouncementWidget()
                announcement.load_data(
                    announcement_body,
                    announcer, date
                )
                announcement.create()

        def load_exams():
            exams = self.Server.PostRequest(requests.get_exams, {
                'classroomId': self.CLASS_ID
            })
            for id_, exam_name in exams:
                exam = QExamWidget()
                exam.create(id_, exam_name)

        def widget_post_b1_f():
            if self.Server.PostRequest(requests.announce, {
                'announcement_body': plain_text_post.toPlainText(),
                'announcer_name': self.USERNAME,
                'classroomId': self.CLASS_ID
            }):
                plain_text_post.setPlainText('')
        
        widget_post_b1 = QPushButton()
        widget_post_b1.clicked.connect(widget_post_b1_f)
        widget_post_b1.setCursor(Qt.PointingHandCursor)
        widget_post_b1.setFixedSize(35, 35)
        widget_post_b1.setIconSize(QSize(47, 47))
        widget_post_b1.setIcon(QIcon('static\\send.png'))
        widget_post_tools_buts_layout.addWidget(widget_post_b1)
        widget_post_tools_buts_layout.addStretch(1)

        widget_post_tools_layoust.addWidget(widget_post_tools_buts)

        scroll_content_layout_1.addWidget(widget_post)
        scroll_content_layout_1.addStretch(1)
        
        class QExamWidget(QWidget):
            def create(self, id_, name):
                self.setStyleSheet('color: white; border-width:1px; border-color: #444; border-style: solid; border-radius: 5px')
                scroll_content_layout_2.addWidget(self)
                self.layout = QVBoxLayout()
                self.setLayout(self.layout)
                f = QFont('arial', 17); f.setBold(True)
                name_label = QLabel_clickable(name)
                name_label.mode(1, id_)
                name_label.exam_id = id_
                name_label.setFont(f)
                self.layout.addWidget(name_label)
                id_label = QLabel('Id: ' + str(id_))
                id_label.setFont(QFont('arial', 9))
                self.layout.addWidget(id_label)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    student = Student()
    sys.exit(app.exec_())
