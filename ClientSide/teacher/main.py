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
import sys

def clearLayout(layout):
  while layout.count():
    child = layout.takeAt(0)
    if child.widget():
      child.widget().setParent(None)

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

class Teacher(QMainWindow):
    def __init__(self):
        self.Server = ConnectionHandler(self)
        self.initiate()
    def initiate(self):
        super().__init__()
        self.setStyleSheet("background-color: #222222;")
        self.setWindowIcon(QtGui.QIcon('static\\icon.png'))
        self.mian_widget_1 = QWidget()
        self.setCentralWidget(self.mian_widget_1)
        self.mian_widget_1.setWindowTitle("Classroom - Teacher's Version")
        self.mian_widget_1.setStyleSheet("background-color: #222222;")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.mian_widget_1.setLayout(main_layout)

        title_label = QLabel("Classroom - Teacher's Version")
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

        create_title_label = QLabel("Create a New Class")
        create_title_label.setStyleSheet("color: #ffffff; font-size: 20px; font-weight: bold;")
        create_class_layout.addWidget(create_title_label)

        name_label = QLabel("Name")
        name_label.setStyleSheet("color: #ffffff; font-size: 16px;")
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 8px;")
        create_class_layout.addWidget(name_label)
        create_class_layout.addWidget(self.name_input)

        description_label = QLabel("Description")
        description_label.setStyleSheet("color: #ffffff; font-size: 16px;")
        self.description_input = QLineEdit()
        self.description_input.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 14px; border-radius: 5px; padding: 8px;")
        create_class_layout.addWidget(description_label)
        create_class_layout.addWidget(self.description_input)

        def create_button_f(e):
            name = self.name_input.text()
            desc = self.description_input.text()
            response = self.Server.PostRequest(requests.create_classroom, {
                'classroom_name':name,
                'classroom_description': desc
            })
            if response:
                insert_classroom(response['id'], name, desc)
                self.name_input.setText('')
                self.description_input.setText('')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Unable to create the classroom")
                msg.setWindowTitle("Classroom:")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
        
        create_button = QPushButton("Create")
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
            mainclass = self
            def insert_data(self, id_, name_, desc_):
                self.id_ = id_
                self.name_ = name_
                self.desc_ = desc_
            def mousePressEvent(self, e):
                self.mainclass.CLASS_ID = self.id_
                self.mainclass.CLASS_NAME = self.name_
                self.mainclass.CLASS_DESC = self.desc_
                self.mainclass.setCentralWidget(self.mainclass.main_widget_3)
                load_announcements()
                get_exams()
                student = self.mainclass.Server.PostRequest(requests.get_people, {'classroomId': self.mainclass.CLASS_ID})
                if student:
                    addToPeople(student)
                students_grades = self.mainclass.Server.PostRequest(requests.get_grades, {'classroomId': self.mainclass.CLASS_ID})
                if students_grades:
                    for i in students_grades:
                        self.mainclass.QGradeBook().insertInLayout(scroll_content_layout_4, i)
                self.mainclass.setMinimumSize(1000, 550)
                self.mainclass.setWindowTitle(self.mainclass.CLASS_NAME)
                self.mainclass.tab1_background_image_label.setText(self.mainclass.CLASS_NAME)
                self.mainclass.tab1_background_image_label.adjustSize()

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
        
        self.setWindowIcon(QIcon('icon.png'))
        self.main_widget_3 = QWidget()
        self.main_widget_3.setStyleSheet('background-color: #222222;')
        self.main_layout_3 = QVBoxLayout()
        self.main_layout_3.setAlignment(Qt.AlignHCenter)
        self.main_widget_3.setLayout(self.main_layout_3)
        self.tabs_layout = QHBoxLayout()
        self.tabs_widget = QWidget()
        self.tabs_widget.setLayout(self.tabs_layout)
        
        self.tab4 = QScrollArea()
        self.tab4.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab4.setFixedWidth(970)
        self.tab4.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 10px;")
        self.tab4.setWidgetResizable(True)
        self.tab4.setParent(None)

        scroll_content_widget_4 = QWidget()
        scroll_content_layout_4 = QVBoxLayout()
        scroll_content_layout_4.setContentsMargins(1,1,1,1)
        scroll_content_widget_4.setLayout(scroll_content_layout_4)
        scroll_content_layout_4.setAlignment(Qt.AlignTop)
        self.tab4.setWidget(scroll_content_widget_4)
        
        self.tab3 = QScrollArea()
        self.tab3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab3.setFixedWidth(970)
        self.tab3.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 10px;")
        self.tab3.setWidgetResizable(True)
        self.tab3.setParent(None)

        scroll_content_widget_3 = QWidget()
        scroll_content_layout_3 = QVBoxLayout()
        scroll_content_layout_3.setContentsMargins(1,1,1,1)
        scroll_content_widget_3.setLayout(scroll_content_layout_3)
        scroll_content_layout_3.setAlignment(Qt.AlignTop)
        self.tab3.setWidget(scroll_content_widget_3)

        self.tab2 = QScrollArea()
        self.tab2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tab2.setFixedWidth(970)
        self.tab2.setStyleSheet("background-color: #333333; border-radius: 5px; padding: 10px;")
        self.tab2.setWidgetResizable(True)
        self.tab2.setParent(None)

        scroll_content_widget_2 = QWidget()
        scroll_content_layout_2 = QVBoxLayout()
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
                tab_4.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_3.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                for child in self.main_widget_3.children():
                    if child in [self.tab1, self.tab2, self.tab3, self.tab4]:
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
                tab_3.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_4.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_2.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_1.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                for child in self.main_widget_3.children():
                    if child in [self.tab1, self.tab2, self.tab3, self.tab4]:
                        child.setParent(None)
                self.main_layout_3.addWidget(self.tab2)
                self.TAB = 2
        tab_2 = QPushButton("Exams")
        tab_2.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_2.setCursor(Qt.PointingHandCursor)
        tab_2.clicked.connect(tab_2_f)
        # tab_3
        def tab_3_f():
            if self.TAB != 3: 
                tab_3.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_2.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_4.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_1.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                for child in self.main_widget_3.children():
                    if child in [self.tab1, self.tab2, self.tab3, self.tab4]:
                        child.setParent(None)
                self.main_layout_3.addWidget(self.tab3)
                self.TAB = 3
        tab_3 = QPushButton("People")
        tab_3.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_3.setCursor(Qt.PointingHandCursor)
        tab_3.clicked.connect(tab_3_f)
        # tab_4
        def tab_4_f():
            if self.TAB != 4: 
                tab_4.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_3.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_2.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                tab_1.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
                for child in self.main_widget_3.children():
                    if child in [self.tab1, self.tab2, self.tab3, self.tab4]:
                        child.setParent(None)
                self.main_layout_3.addWidget(self.tab4)
                self.TAB = 4
        tab_4 = QPushButton("Grades")
        tab_4.setStyleSheet("background-color: #333333; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        tab_4.setCursor(Qt.PointingHandCursor)
        tab_4.clicked.connect(tab_4_f)
        self.tabs_layout.addWidget(tab_1)
        self.tabs_layout.addWidget(tab_2)
        self.tabs_layout.addWidget(tab_3)
        self.tabs_layout.addWidget(tab_4)
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

        self.PEOPLE = []

        class QPersonWidget(QWidget):
            def create(self, id_, name, mainclass):
                mainclass.PEOPLE.append(id_)
                self.setStyleSheet('color: white; border-width:1px; border-color: #444; border-style: solid; border-radius: 5px')
                scroll_content_layout_3.addWidget(self)
                self.layout = QVBoxLayout()
                self.setLayout(self.layout)
                f = QFont('arial', 17); f.setBold(True)
                name_label = QLabel(name)
                name_label.setFont(f)
                self.layout.addWidget(name_label)
                id_label = QLabel('Id: ' + str(id_))
                id_label.setFont(QFont('arial', 9))
                self.layout.addWidget(id_label)

        def addToPeople(list_):
            for student in list_:
                id_ = student['id']
                name = student['username']
                if id_ not in self.PEOPLE:
                    QPersonWidget().create(id_, name, self)
        
        class QGradeBook(QWidget):
            def insertInLayout(self, parent, student):
                self.layout = QVBoxLayout()
                self.setLayout(self.layout)
                self.setStyleSheet('border-color: #444; border-width: 1px; border-style: solid; border-radius: 5px; color: white;')
                
                f = QFont('arial', 17); f.setBold(True)
                name_label = QLabel(student['name'])
                name_label.setFont(f)
                self.layout.addWidget(name_label)
                grades_text = ''
                for i in student['exam']:
                    grades_text += f"{i}: {student['exam'][i]}\n"
                exams_label = QLabel(grades_text[:-1])
                exams_label.setWordWrap(True)
                exams_label.setFont(QFont('arial', 13))
                self.layout.addWidget(exams_label)

                parent.addWidget(self)
        self.QGradeBook = QGradeBook
        
        create_exam_widget = QWidget()
        create_exam_widget.setWindowIcon(QIcon('icon.png'))
        create_exam_widget.setWindowTitle('classroom - create exam')
        create_exam_widget.setStyleSheet('color: white; background-color: #333;')
        create_exam_widget_layout = QVBoxLayout()
        create_exam_widget.setLayout(create_exam_widget_layout)
        create_exam_widget_label = QLabel('Create Exam')
        f = QFont('Arial', 20); f.setBold(True)
        create_exam_widget_label.setFont(f)
        create_exam_widget_layout.addWidget(create_exam_widget_label)
        create_exam_widget_name_e = QLineEdit()
        create_exam_widget_name_e.setFont(QFont('Arial', 15))
        create_exam_widget_name_e.setStyleSheet('border-color: #555; border-width: 1px; border-style: solid; border-radius:5px; background-color: #444')
        create_exam_widget_name_e.setPlaceholderText('Exam name')
        create_exam_widget_layout.addWidget(create_exam_widget_name_e)
        create_exam_widget_student_questions_e = QLineEdit()
        create_exam_widget_student_questions_e.setStyleSheet('border-color: #555; border-width: 1px; border-style: solid; border-radius:5px; background-color: #444')
        create_exam_widget_student_questions_e.setFont(QFont('Arial', 15))
        create_exam_widget_student_questions_e.setPlaceholderText('Number of questions')
        create_exam_widget_layout.addWidget(create_exam_widget_student_questions_e)
        
        questions_widget_ = QScrollArea()
        questions_widget_.setWidgetResizable(True)
        questions_widget_.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        questions_widget_.setMinimumSize(700, 450)
        questions_widget_.setStyleSheet('border-color: #555; border-width: 1px; border-style: solid; border-radius:5px; background-color: #444')
        create_exam_widget_layout.addWidget(questions_widget_)

        questions_widget = QWidget()
        questions_widget_layout = QVBoxLayout()
        questions_widget_layout.setContentsMargins(1,1,1,1)
        questions_widget.setLayout(questions_widget_layout)
        questions_widget_layout.setAlignment(Qt.AlignTop)
        questions_widget_.setWidget(questions_widget)
        
        def questions_widget_create_question_button_MCQ_f():
            if not MCQ_widget.isVisible():
                MCQ_widget.show()
        
        def questions_widget_create_question_button_TF_f():
            if not TF_widget.isVisible():
                TF_widget.show()
        
        questions_widget_create_question_button_MCQ = QPushButton('Generate MCQ question')
        questions_widget_create_question_button_MCQ.clicked.connect(questions_widget_create_question_button_MCQ_f)
        questions_widget_create_question_button_MCQ.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        questions_widget_create_question_button_MCQ.setCursor(Qt.PointingHandCursor)
        questions_widget_create_question_button_TF = QPushButton('Generate True or False question')
        questions_widget_create_question_button_TF.clicked.connect(questions_widget_create_question_button_TF_f)
        questions_widget_create_question_button_TF.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        questions_widget_create_question_button_TF.setCursor(Qt.PointingHandCursor)
        
        MCQ_widget = QWidget()
        MCQ_widget.setWindowTitle('classroom exams - MCQ question')
        MCQ_widget.setFixedHeight(230)
        MCQ_widget.setFixedWidth(550)
        MCQ_widget.setStyleSheet('color: white; background-color: #333;')
        MCQ_widget_layout = QVBoxLayout()
        MCQ_widget.setLayout(MCQ_widget_layout)
        
        MCQ_widget_question_e = QLineEdit()
        MCQ_widget_question_e.setFont(QFont('Arial', 15))
        MCQ_widget_question_e.setStyleSheet('border-color: #555; border-width: 1px; border-style: solid; border-radius:5px; background-color: #444')
        MCQ_widget_layout.addWidget(MCQ_widget_question_e)
        
        choice_1 = QCheckEdit('choice 1')
        choice_2 = QCheckEdit('choice 2')
        choice_3 = QCheckEdit('choice 3')
        choice_4 = QCheckEdit('choice 4')
        
        self.MCQs = []
        self.TFs = []

        for i in [choice_1, choice_2, choice_3, choice_4]:
            i.setFont(QFont('Arial', 15))
            i.line_edit.setFont(QFont('Arial', 15))
            MCQ_widget_layout.addWidget(i)
        
        def insertMCQInLayout(dict_):
            MCQ_sample_label = QLabel('MCQ - ' + dict_['question'])
            MCQ_sample_label.setFont(QFont('Arial', 15))
            MCQ_sample_label.setFixedHeight(30)
            questions_widget_layout.insertWidget(1, MCQ_sample_label)
            self.MCQs.append(dict_)
        
        def insertTFInLayout(dict_):
            TF_sample_label = QLabel('T\F - ' + dict_['statement'])
            TF_sample_label.setFont(QFont('Arial', 15))
            TF_sample_label.setFixedHeight(30)
            questions_widget_layout.insertWidget(1, TF_sample_label)
            self.TFs.append(dict_)

        def MCQ_button_f():
            question = MCQ_widget_question_e.text()
            ch1 = (choice_1.text(), int(choice_1.isChecked()))
            ch2 = (choice_2.text(), int(choice_2.isChecked()))
            ch3 = (choice_3.text(), int(choice_3.isChecked()))
            ch4 = (choice_4.text(), int(choice_4.isChecked()))
            MCQ_widget_question_e.setText('')
            n = 0
            for i in [choice_1, choice_2, choice_3, choice_4]:
                n += 1
                i.setText(f'choice {n}')
                i.setChecked(False)
            insertMCQInLayout({
                'question': question,
                'ch1': ch1, 'ch2': ch2,
                'ch3': ch3, 'ch4': ch4,
            })
            
        MCQ_button = QPushButton('Done')
        MCQ_button.setCursor(Qt.PointingHandCursor)
        MCQ_button.clicked.connect(MCQ_button_f)
        MCQ_button.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        MCQ_widget_layout.addWidget(MCQ_button)

        questions_widget_create_question_buttons_widget = QWidget()
        questions_widget_create_question_buttons_widget_layout = QHBoxLayout()
        questions_widget_create_question_buttons_widget.setLayout(questions_widget_create_question_buttons_widget_layout)
        questions_widget_create_question_buttons_widget_layout.addWidget(questions_widget_create_question_button_MCQ)
        questions_widget_create_question_buttons_widget_layout.addWidget(questions_widget_create_question_button_TF)
        questions_widget_layout.addWidget(questions_widget_create_question_buttons_widget)
        
        def get_exams():
            for id_, name in self.Server.PostRequest(requests.get_exams, {
                'classroomId': self.CLASS_ID
            }):
                QExamWidget().create(id_, name)

        def create_exam_widget_submit_button_f():
            try:
                num = int(create_exam_widget_student_questions_e.text())
                name = create_exam_widget_name_e.text()
                if name and len(self.TFs) + len(self.MCQs) >= num:
                    id_ = self.Server.PostRequest(requests.submit_exam, {
                        'classroomId': self.CLASS_ID,
                        'exam_name': name,
                        'num': num,
                        'MCQs': self.MCQs,
                        'TFs': self.TFs
                    })
                    if id_ != 'error':
                        self.TFs.clear(); self.MCQs.clear()
                        clearLayout(questions_widget_layout)
                        create_exam_widget_student_questions_e.setText('')
                        create_exam_widget_name_e.setText('')
                        QExamWidget().create(id_, name)
                else:pass
            except:pass
        
        create_exam_widget_submit_button = QPushButton('submit')
        create_exam_widget_submit_button.clicked.connect(create_exam_widget_submit_button_f)
        create_exam_widget_submit_button.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        create_exam_widget_layout.addWidget(create_exam_widget_submit_button)
        
        def create_exam_button_f():
            create_exam_widget.show()
        
        create_exam_button = QPushButton("create exam")
        create_exam_button.clicked.connect(create_exam_button_f)
        create_exam_button.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        create_exam_button.setCursor(Qt.PointingHandCursor)
        scroll_content_layout_2.addWidget(create_exam_button)
        
        TF_widget = QWidget()
        TF_widget.setWindowTitle('classroom exams - true or False question')
        TF_widget.setFixedHeight(100)
        TF_widget.setFixedWidth(550)
        TF_widget.setStyleSheet('color: white; background-color: #333;')
        TF_widget_layout = QVBoxLayout()
        TF_widget.setLayout(TF_widget_layout)
        
        TF_input = QCheckEdit('statement')
        TF_input.line_edit.setFont(QFont('Arial', 15))
        TF_input.setFont(QFont('Arial', 15))
        TF_input.setChecked(True)
        TF_widget_layout.addWidget(TF_input)
        
        def TF_button_f():
            insertTFInLayout({
                'statement': TF_input.text(),
                'answer': int(TF_input.isChecked())
            })
            TF_input.setText('statement')
            TF_input.setChecked(True)
            

        TF_button = QPushButton('Done')
        TF_button.setCursor(Qt.PointingHandCursor)
        TF_button.clicked.connect(TF_button_f)
        TF_button.setStyleSheet("background-color: #007ACC; color: #ffffff; font-size: 16px; border-radius: 8px; padding: 10px 16px;")
        TF_widget_layout.addWidget(TF_button)
        
        class QExamWidget(QWidget):
            def create(self, id_, name):
                self.setStyleSheet('color: white; border-width:1px; border-color: #444; border-style: solid; border-radius: 5px')
                scroll_content_layout_2.addWidget(self)
                self.layout = QVBoxLayout()
                self.setLayout(self.layout)
                f = QFont('arial', 17); f.setBold(True)
                name_label = QLabel(name)
                name_label.setFont(f)
                self.layout.addWidget(name_label)
                id_label = QLabel('Id: ' + str(id_))
                id_label.setFont(QFont('arial', 9))
                self.layout.addWidget(id_label)
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    teacher = Teacher()
    sys.exit(app.exec_())
