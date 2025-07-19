from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QLineEdit, QRadioButton, QButtonGroup, QHBoxLayout, QMessageBox, QFrame, QSizePolicy, QScrollArea, QTextEdit, QListWidget, QListWidgetItem, QCalendarWidget, QDateEdit
)
from PySide6.QtGui import QFont, QPixmap, QFontDatabase, QIcon, QColor
from PySide6.QtCore import Qt, QDate

import sys
from data_manager import DataManager

# Initialize data manager
data_manager = DataManager()

# Custom colors
LAVENDER = "#E6E6FA"
CHOCOLATE = "#7B3F00"
WHITE = "#FFFFFF"
BARNEY = "#70177A"

class TitleRow(QWidget):
    def __init__(self, font_family):
        super().__init__()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        title = QLabel("Chocoholics Anonymous")
        title_font = QFont(font_family, 32)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {CHOCOLATE}; margin-right: 10px;")
        layout.addWidget(title)
        icon = QLabel()
        pixmap = QPixmap("choco.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(68, 68, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon.setPixmap(pixmap)
        layout.addWidget(icon)
        self.setLayout(layout)

BANNER_HEIGHT = 200
MAX_BANNER_WIDTH = 1000

class SignInPage(QWidget):
    def __init__(self, main_window, title_font_family):
        super().__init__()
        self.main_window = main_window
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        main_layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        # Title row
        main_layout.addWidget(TitleRow(title_font_family))
        # Centered login box
        login_box = QFrame()
        login_box.setObjectName("loginBox")
        login_box.setStyleSheet(f"""
            QFrame#loginBox {{
                background: {CHOCOLATE};
                border-radius: 40px;
                max-width: 450px;
                margin-left: auto;
                margin-right: auto;
                padding: 32px 40px 32px 40px;
            }}
        """)
        login_layout = QVBoxLayout()
        login_layout.setAlignment(Qt.AlignCenter)
        # Sign In title
        sign_in_label = QLabel("In Chocolate We Trust")
        sign_in_label.setFont(QFont("Arial", 20, QFont.Bold, italic=True))
        sign_in_label.setStyleSheet(f"color: {WHITE}; background: transparent; margin-bottom: 18px;")
        sign_in_label.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(sign_in_label)
        # Username
        user_label = QLabel("Username:")
        user_label.setStyleSheet(f"color: {WHITE}; background: transparent; font-size: 16px; font-weight: bold;")
        login_layout.addWidget(user_label)
        self.username = QLineEdit()
        self.username.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 16px;color: black;")
        login_layout.addWidget(self.username)
        # Password
        pass_label = QLabel("Password:")
        pass_label.setStyleSheet(f"color: {WHITE}; background: transparent; font-size: 16px; font-weight: bold;")
        login_layout.addWidget(pass_label)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 16px;color: black;")
        login_layout.addWidget(self.password)
        # Role selection
        role_row = QHBoxLayout()
        role_label = QLabel("Role:")
        role_label.setStyleSheet(f"color: {WHITE}; background: transparent; font-size: 16px; font-weight: bold;")
        role_row.addWidget(role_label)
        self.role_group = QButtonGroup(self)
        self.manager_radio = QRadioButton("Manager")
        self.provider_radio = QRadioButton("Provider")
        self.manager_radio.setChecked(True)
        for rb in [self.manager_radio, self.provider_radio]:
            rb.setStyleSheet(f"color: {WHITE}; background: transparent; font-size: 16px;")
            self.role_group.addButton(rb)
            role_row.addWidget(rb)
        role_row.addStretch()
        login_layout.addLayout(role_row)
        # Sign In button
        self.signin_btn = QPushButton("Sign In")
        self.signin_btn.clicked.connect(self.try_signin)
        self.signin_btn.setStyleSheet(f"background: {WHITE}; color: {CHOCOLATE}; font-weight: bold; font-size: 18px; border-radius: 10px; padding: 8px 0;")
        login_layout.addWidget(self.signin_btn)
        # Forgot Username/Password
        self.forgot_btn = QPushButton("Forgot Username/Password?")
        self.forgot_btn.setStyleSheet("background: transparent; color: white; font-size: 14px; text-decoration: underline; border: none;")
        self.forgot_btn.clicked.connect(self.goto_forgot)
        login_layout.addWidget(self.forgot_btn)
        login_box.setLayout(login_layout)
        # Add stretch to center the login box
        main_layout.addStretch()
        main_layout.addWidget(login_box, alignment=Qt.AlignHCenter)
        main_layout.addSpacing(40)  # Add spacing below the login box
        main_layout.addStretch()
        self.setLayout(main_layout)
        self.setStyleSheet(f"background: {LAVENDER};")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def try_signin(self):
        username = self.username.text()
        password = self.password.text()
        role = "manager" if self.manager_radio.isChecked() else "provider"

        # Authenticate user using data manager
        if not data_manager.authenticate_user(username, password, role):
            self.show_signin_error("Invalid username, password, or role.")
            return

        # Get user data
        user = data_manager.users.get(username)
        self.main_window.current_user = user
        if role == "manager":
            self.main_window.goto_page("manager_menu")
        else:
            self.main_window.goto_page("provider_menu")

    def show_signin_error(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Sign In Failed")
        msg.setText(message)
        msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        msg.exec()

    def goto_forgot(self):
        self.main_window.goto_page("forgot")


class ManagerMenuPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        # Title
        title_label = QLabel("Manager Main Menu")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 24px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title_label)
        # Buttons container
        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        for text, slot in [
            ("Manage Providers", lambda: main_window.goto_page("manage_providers")),
            ("Generate Report", self.placeholder),
            ("Provider Directory", lambda: main_window.goto_provider_directory(return_to_claim=False, is_manager=True)),
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
            btn.clicked.connect(slot)
            buttons_layout.addWidget(btn)
        layout.addLayout(buttons_layout)
        # Sign Out button (separated and at bottom)
        layout.addSpacing(40)  # Smaller spacing instead of full stretch
        signout_btn = QPushButton("Sign Out")
        signout_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 8px 16px; font-size: 14px; min-width: 120px;")
        signout_btn.clicked.connect(lambda: main_window.goto_page("signin"))
        layout.addWidget(signout_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet(f"background: {LAVENDER};")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def placeholder(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Placeholder")
        msg.setText("This feature is not implemented in the prototype.")
        msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        msg.exec()

class ProviderMenuPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        # Title
        title_label = QLabel("Provider Main Menu")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 24px; color: {CHOCOLATE}; font-weight: bold; margin: 20px 0;")
        layout.addWidget(title_label)
        # Buttons container
        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        for text, slot in [
            ("Request Provider Directory", lambda: main_window.goto_provider_directory(return_to_claim=False, is_manager=False)),
            ("Verify Member Status", lambda: main_window.goto_page("verify_member")),
            ("Submit Service Claim", lambda: main_window.goto_page("service_claim")),
            ("Manage Members", lambda: main_window.goto_page("manage_members")),
            ("Get Reports", self.placeholder),
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
            btn.clicked.connect(slot)
            buttons_layout.addWidget(btn)
        layout.addLayout(buttons_layout)
        # Sign Out button (separated and at bottom)
        layout.addSpacing(40)  # Smaller spacing instead of full stretch
        signout_btn = QPushButton("Sign Out")
        signout_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 8px 16px; font-size: 14px; min-width: 120px;")
        signout_btn.clicked.connect(lambda: main_window.goto_page("signin"))
        layout.addWidget(signout_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet(f"background: {LAVENDER};")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def placeholder(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Placeholder")
        msg.setText("This feature is not implemented in the prototype.")
        msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        msg.exec()

class AddProviderPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Title
        title_label = QLabel("Add New Provider")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 24px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title_label)
        
        # Form container
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        
        # Note about auto-generated ID
        note_label = QLabel("Provider ID will be automatically generated by the system")
        note_label.setAlignment(Qt.AlignCenter)
        note_label.setStyleSheet(f"font-size: 14px; color: {BARNEY}; font-style: italic; margin: 10px 0;")
        form_layout.addWidget(note_label)
        
        self.entries = {}
        field_configs = [
            ("Provider Name (25 chars):", "Name", 25),
            ("Street Address (25 chars):", "Address", 25),
            ("City (14 chars):", "City", 14),
            ("State (2 letters):", "State", 2),
            ("ZIP Code (5 digits):", "Zip", 5)
        ]
        
        for label_text, field_name, max_length in field_configs:
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"font-size: 16px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
            form_layout.addWidget(label)
            
            entry = QLineEdit()
            entry.setMaxLength(max_length)
            entry.setAlignment(Qt.AlignCenter)
            entry.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 16px; color: black; min-width: 300px; max-width: 300px; outline: none;")
            self.entries[field_name] = entry
            form_layout.addWidget(entry, alignment=Qt.AlignCenter)
        
        # Add form to main layout
        layout.addStretch()
        layout.addLayout(form_layout)
        layout.addStretch()
        
        # Buttons
        submit_btn = QPushButton("Add Provider")
        submit_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
        submit_btn.clicked.connect(self.submit)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        
        back_btn = QPushButton("Back to Manager Menu")
        back_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
        back_btn.clicked.connect(lambda: main_window.goto_page("manager_menu"))
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        self.setStyleSheet(f"background: {LAVENDER};")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def submit(self):
        data = {k: v.text() for k, v in self.entries.items()}
        if not all(data.values()):
            QMessageBox.warning(self, "Error", "All fields are required.")
            return
        
        # Validate state format
        state = data['State'].text().strip().upper()
        if not state.isalpha() or len(state) != 2:
            QMessageBox.warning(self, "Error", "State must be exactly 2 letters.")
            return
        
        # Validate ZIP code format
        zip_code = data['Zip'].text().strip()
        if not zip_code.isdigit() or len(zip_code) != 5:
            QMessageBox.warning(self, "Error", "ZIP code must be exactly 5 digits.")
            return
        
        confirm = QMessageBox.question(
            self, "Confirm Provider",
            f"Name: {data['Name']}\nAddress: {data['Address']}\nCity: {data['City']}\nState: {state}\nZIP: {zip_code}\n\nAdd this provider?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            # Add provider using data manager
            provider_id = data_manager.add_provider(
                name=data['Name'],
                address=data['Address'],
                city=data['City'],
                state=state,
                zip_code=zip_code
            )
            
            # Create username from provider name
            username = data['Name'].lower().replace(' ', '')
            
            QMessageBox.information(self, "Success", 
                f"Provider Added Successfully!\n\n"
                f"Provider ID: {provider_id}\n"
                f"Username: {username}\n"
                f"Password: {provider_id}\n\n"
                f"Provider can now log in with these credentials.")
            for entry in self.entries.values():
                entry.clear()
            self.main_window.goto_page("manage_providers")

class ForgotPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        # Message
        label = QLabel("Please call the ChocAn IT Department for assistance resetting your password or recovering your username.\n\nContact: +1 800 555 6000")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: #7B3F00;")
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        back_btn = QPushButton("Back to Sign In")
        back_btn.setStyleSheet("background: #70177A; color: white; font-weight: bold; border-radius: 10px; padding: 8px 24px;")
        back_btn.clicked.connect(lambda: main_window.goto_page('signin'))
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet(f"background: {LAVENDER};")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

class VerifyMemberPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        # Title
        title_label = QLabel("Verify Member Status")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 24px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title_label)
        # Member ID input
        member_id_label = QLabel("Enter Member ID:")
        member_id_label.setAlignment(Qt.AlignCenter)
        member_id_label.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        self.member_id_input = QLineEdit()
        self.member_id_input.setAlignment(Qt.AlignCenter)
        self.member_id_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 18px; color: black; min-width: 300px; max-width: 300px;")
        layout.addWidget(member_id_label)
        layout.addWidget(self.member_id_input, alignment=Qt.AlignCenter)
        # Verify button
        verify_btn = QPushButton("Verify Member")
        verify_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
        verify_btn.clicked.connect(self.verify_member)
        layout.addWidget(verify_btn, alignment=Qt.AlignCenter)
        # Back button
        back_btn = QPushButton("Back to Provider Menu")
        back_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
        back_btn.clicked.connect(lambda: main_window.goto_page("provider_menu"))
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet(f"background: {LAVENDER};")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def verify_member(self):
        member_id = self.member_id_input.text()
        if not member_id:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Member ID cannot be empty.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return

        member = data_manager.get_member(member_id)

        if member:
            status_msg = f"Member ID: {member['member_id']}\nName: {member['name']}\nStatus: {member['status']}"
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Member Status")
            msg.setText(status_msg)
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Member Not Found")
            msg.setText(f"Member with ID '{member_id}' not found in the system.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()

class ServiceClaimPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        # Title
        title_label = QLabel("Submit New Service Claim")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 24px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title_label)
        # Form container
        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        
        # Row 1: Member ID and Date of Service
        row1_layout = QHBoxLayout()
        
        # Member ID (left side)
        member_id_container = QVBoxLayout()
        member_id_label = QLabel("Member ID:")
        member_id_label.setAlignment(Qt.AlignCenter)
        member_id_label.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        self.member_id_input = QLineEdit()
        self.member_id_input.setAlignment(Qt.AlignCenter)
        self.member_id_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 18px; color: black; min-width: 250px; max-width: 250px; outline: none;")
        member_id_container.addWidget(member_id_label)
        member_id_container.addWidget(self.member_id_input)
        row1_layout.addLayout(member_id_container)
        
        # Date of Service (right side)
        date_container = QVBoxLayout()
        date_label = QLabel("Date of Service:")
        date_label.setAlignment(Qt.AlignCenter)
        date_label.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        
        # Date input with popup calendar
        self.date_input = QLineEdit()
        self.date_input.setAlignment(Qt.AlignCenter)
        self.date_input.setPlaceholderText("Click to select date")
        self.date_input.setReadOnly(True)  # Make it read-only so user clicks to open calendar
        self.date_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 18px; color: black; min-width: 250px; max-width: 250px; outline: none; cursor: pointer;")
        self.date_input.mousePressEvent = self.show_calendar_popup
        
        # Set today's date as default
        self.selected_date = QDate.currentDate()
        self.date_input.setText(self.selected_date.toString("MM-dd-yyyy"))
        
        date_container.addWidget(date_label)
        date_container.addWidget(self.date_input)
        row1_layout.addLayout(date_container)
        
        form_layout.addLayout(row1_layout)
        
        # Row 2: Provider Number and Service Code
        row2_layout = QHBoxLayout()
        
        # Provider Number (left side)
        provider_container = QVBoxLayout()
        provider_num_label = QLabel("Provider Number (9 digits):")
        provider_num_label.setAlignment(Qt.AlignCenter)
        provider_num_label.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        self.provider_num_input = QLineEdit()
        self.provider_num_input.setAlignment(Qt.AlignCenter)
        self.provider_num_input.setPlaceholderText("Enter 9-digit provider number")
        self.provider_num_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 18px; color: black; min-width: 250px; max-width: 250px; outline: none;")
        provider_container.addWidget(provider_num_label)
        provider_container.addWidget(self.provider_num_input)
        row2_layout.addLayout(provider_container)
        
        # Service Code (right side)
        service_container = QVBoxLayout()
        service_code_label = QLabel("Service Code (6 digits):")
        service_code_label.setAlignment(Qt.AlignCenter)
        service_code_label.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        self.service_code_input = QLineEdit()
        self.service_code_input.setAlignment(Qt.AlignCenter)
        self.service_code_input.setPlaceholderText("Enter 6-digit service code")
        self.service_code_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 18px; color: black; min-width: 250px; max-width: 250px; outline: none;")
        self.service_code_input.textChanged.connect(self.verify_service_code)
        service_container.addWidget(service_code_label)
        service_container.addWidget(self.service_code_input)
        row2_layout.addLayout(service_container)
        
        form_layout.addLayout(row2_layout)
        
        # Service Name Display
        self.service_name_label = QLabel("")
        self.service_name_label.setAlignment(Qt.AlignCenter)
        self.service_name_label.setStyleSheet(f"font-size: 16px; color: {BARNEY}; font-weight: bold; margin: 5px 0;")
        form_layout.addWidget(self.service_name_label)
        # Lookup Service Code button
        lookup_btn = QPushButton("Lookup Service Code")
        lookup_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 8px 16px; font-size: 14px; min-width: 150px;")
        lookup_btn.clicked.connect(self.lookup_service_code)
        form_layout.addWidget(lookup_btn, alignment=Qt.AlignCenter)
        # Comments
        comments_label = QLabel("Comments (optional):")
        comments_label.setAlignment(Qt.AlignCenter)
        comments_label.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        self.comments_input = QLineEdit()
        self.comments_input.setAlignment(Qt.AlignCenter)
        self.comments_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 18px; color: black; min-width: 300px; max-width: 300px; outline: none;")
        form_layout.addWidget(comments_label, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.comments_input, alignment=Qt.AlignCenter)
        # Add form to main layout
        layout.addStretch()
        layout.addLayout(form_layout)
        layout.addStretch()
        # Buttons
        submit_btn = QPushButton("Submit Service Claim")
        submit_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
        submit_btn.clicked.connect(self.submit_claim)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)
        # Back button
        back_btn = QPushButton("Back to Provider Menu")
        back_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
        back_btn.clicked.connect(lambda: main_window.goto_page("provider_menu"))
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.setStyleSheet(f"background: {LAVENDER};")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def show_calendar_popup(self, event):
        """Show popup calendar when date input is clicked"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout
        
        # Create popup dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date")
        dialog.setModal(True)
        dialog.setStyleSheet(f"""
            QDialog {{
                background: {WHITE};
                border: 2px solid {BARNEY};
                border-radius: 10px;
            }}
        """)
        
        # Create calendar widget
        calendar = QCalendarWidget()
        calendar.setSelectedDate(self.selected_date)
        
        # Enable grid and set header format
        calendar.setGridVisible(True)
        calendar.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)  # Remove week numbers
        calendar.setStyleSheet(f"""
            QCalendarWidget {{
                background: {CHOCOLATE};
                border: none;
                font-size: 14px;
                color: {WHITE};
            }}
            QCalendarWidget QToolButton {{
                background: {BARNEY};
                color: {WHITE};
                border: none;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }}
            QCalendarWidget QToolButton:hover {{
                background: {WHITE};
                color: {CHOCOLATE};
            }}
            QCalendarWidget QMenu {{
                background: {WHITE};
                border: 1px solid {BARNEY};
                color: black;
            }}
            QCalendarWidget QSpinBox {{
                background: {WHITE};
                border: 1px solid {BARNEY};
                border-radius: 3px;
                padding: 2px;
                color: black;
            }}
            QCalendarWidget QAbstractItemView {{
                background: {CHOCOLATE};
                color: {WHITE};
                selection-background-color: {BARNEY};
                selection-color: {WHITE};
            }}
        """)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(calendar)
        dialog.setLayout(layout)
        
        # Connect calendar selection to dialog close
        calendar.clicked.connect(lambda date: self.on_date_selected(date, dialog))
        
        # Show dialog
        dialog.exec()
    
    def on_date_selected(self, date, dialog):
        """Handle date selection from popup calendar"""
        self.selected_date = date
        self.date_input.setText(date.toString("MM-dd-yyyy"))
        dialog.accept()

    def submit_claim(self):
        member_id = self.member_id_input.text().strip()
        date_of_service = self.date_input.text().strip()
        provider_number = self.provider_num_input.text().strip()
        service_code = self.service_code_input.text().strip()
        comments = self.comments_input.text().strip()

        # Validate required fields
        if not member_id or not date_of_service or not provider_number or not service_code:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("All fields are required for a service claim.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Validate provider number (9 digits)
        if not provider_number.isdigit() or len(provider_number) != 9:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Provider number must be exactly 9 digits.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Validate service code (6 digits)
        if not service_code.isdigit() or len(service_code) != 6:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Service code must be exactly 6 digits.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return

        member = data_manager.get_member(member_id)
        if not member:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Member with ID '{member_id}' not found.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return

        service = data_manager.get_service(service_code)
        if not service:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Service code '{service_code}' not found in the directory.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return

        # Add service claim using data manager
        try:
            claim_id = data_manager.add_service_claim(
                member_id=member_id,
                date_of_service=date_of_service,
                provider_number=provider_number,
                service_code=service_code,
                comments=comments
            )
        except ValueError as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(str(e))
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(f"Service Claim Submitted!\n\nClaim ID: {claim_id}\nService: {service['name']}\nService Fee: ${service['fee']:.2f}\nProvider: {provider_number}\nMember: {member_id}")
        msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        msg.exec()
        # Clear form fields
        self.member_id_input.clear()
        self.provider_num_input.clear()
        self.service_code_input.clear()
        self.comments_input.clear()
        # Reset date to today
        self.selected_date = QDate.currentDate()
        self.date_input.setText(self.selected_date.toString("MM-dd-yyyy"))
        self.service_name_label.setText("")
        self.main_window.goto_page("provider_menu")

    def verify_service_code(self):
        service_code = self.service_code_input.text().strip()
        
        if len(service_code) == 6:  # Only verify when 6 digits are entered
            service = data_manager.get_service(service_code)
            if service:
                self.service_name_label.setText(f"Service: {service['name']}")
                self.service_name_label.setStyleSheet(f"font-size: 16px; color: {BARNEY}; font-weight: bold; margin: 5px 0;")
            else:
                self.service_name_label.setText("Service code not found in directory")
                self.service_name_label.setStyleSheet(f"font-size: 16px; color: red; font-weight: bold; margin: 5px 0;")
        else:
            self.service_name_label.setText("")

    def lookup_service_code(self):
        # Navigate to provider directory page with return to claim option
        self.main_window.goto_provider_directory(return_to_claim=True, is_manager=False)

class ProviderDirectoryPage(QWidget):
    def __init__(self, main_window, return_to_claim=False, is_manager=False):
        super().__init__()
        self.main_window = main_window
        self.return_to_claim = return_to_claim
        self.is_manager = is_manager
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Title
        title_label = QLabel("Provider Directory")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 24px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title_label)
        
        # Search section
        search_label = QLabel("Search by Service Code or Name:")
        search_label.setAlignment(Qt.AlignCenter)
        search_label.setStyleSheet(f"font-size: 16px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setAlignment(Qt.AlignCenter)
        self.search_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 16px; color: black; min-width: 300px; max-width: 300px;")
        self.search_input.textChanged.connect(self.filter_services)
        layout.addWidget(self.search_input, alignment=Qt.AlignCenter)
        
        # Results section
        self.results_label = QLabel("All Services:")
        self.results_label.setAlignment(Qt.AlignCenter)
        self.results_label.setStyleSheet(f"font-size: 16px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(self.results_label)
        
        # Results display with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"QScrollArea {{ border: 2px solid {BARNEY}; border-radius: 10px; background: {WHITE}; }}")
        scroll_area.setMinimumHeight(200)
        scroll_area.setMaximumHeight(300)
        scroll_area.setMinimumWidth(400)
        scroll_area.setMaximumWidth(600)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet(f"background: {WHITE}; border: none; font-size: 14px; color: black; padding: 10px;")
        self.results_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.results_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_area.setWidget(self.results_text)
        layout.addWidget(scroll_area, alignment=Qt.AlignCenter)
        
        # Email section (only for provider menu access)
        if not self.return_to_claim:
            layout.addSpacing(20)
            email_label = QLabel("Email Provider Directory:")
            email_label.setAlignment(Qt.AlignCenter)
            email_label.setStyleSheet(f"font-size: 16px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
            layout.addWidget(email_label)
            
            self.email_input = QLineEdit()
            self.email_input.setAlignment(Qt.AlignCenter)
            self.email_input.setPlaceholderText("Enter your email address")
            self.email_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; padding: 8px; font-size: 16px; color: black; min-width: 300px; max-width: 300px;")
            layout.addWidget(self.email_input, alignment=Qt.AlignCenter)
            
            email_btn = QPushButton("Send Directory via Email")
            email_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
            email_btn.clicked.connect(self.send_directory_email)
            layout.addWidget(email_btn, alignment=Qt.AlignCenter)
        
        # Buttons
        if self.return_to_claim:
            back_btn = QPushButton("Back to Service Claim")
            back_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
            back_btn.clicked.connect(lambda: main_window.goto_page("service_claim"))
        elif self.is_manager:
            back_btn = QPushButton("Back to Manager Menu")
            back_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
            back_btn.clicked.connect(lambda: main_window.goto_page("manager_menu"))
        else:
            back_btn = QPushButton("Back to Provider Menu")
            back_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
            back_btn.clicked.connect(lambda: main_window.goto_page("provider_menu"))
        
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        self.setStyleSheet(f"background: {LAVENDER};")
        
        # Initialize with all services
        self.filter_services()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def filter_services(self):
        search_term = self.search_input.text().lower()
        
        if not search_term:
            # Show all services
            filtered_services = data_manager.service_directory
            self.results_label.setText("All Services:")
        else:
            # Filter services based on search term
            filtered_services = data_manager.search_services(search_term)
            
            if filtered_services:
                self.results_label.setText(f"Search Results ({len(filtered_services)} found):")
            else:
                self.results_label.setText("No Results Found")
        
        # Display results
        if filtered_services:
            results_text = ""
            for service in filtered_services:
                results_text += f"{service['code']}: {service['name']} - ${service['fee']:.2f}\n"
            self.results_text.setPlainText(results_text)
        else:
            self.results_text.setPlainText("No services found matching your search criteria.")

    def send_directory_email(self):
        email = self.email_input.text().strip()
        
        if not email:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please enter a valid email address.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Simple email validation (basic check for @ symbol)
        if '@' not in email or '.' not in email:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please enter a valid email address format.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Create alphabetical directory content
        sorted_services = sorted(data_manager.service_directory, key=lambda x: x['name'])
        directory_content = "Chocoholics Anonymous Provider Directory\n"
        directory_content += "=" * 50 + "\n\n"
        directory_content += "Services (Alphabetical Order):\n\n"
        
        for service in sorted_services:
            directory_content += f"{service['name']}\n"
            directory_content += f"  Code: {service['code']}\n"
            directory_content += f"  Fee: ${service['fee']:.2f}\n\n"
        
        # Show success message (simulating email send)
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Email Sent")
        msg.setText(f"Provider Directory has been sent to:\n{email}\n\nDirectory contains {len(sorted_services)} services in alphabetical order.")
        msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        msg.exec()
        
        # Clear the email input
        self.email_input.clear()

class ManageMembersPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.selected_member = None
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Title
        title_label = QLabel("Manage Members")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 24px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title_label)
        
        # Current Members Section
        members_label = QLabel("Current Members:")
        members_label.setAlignment(Qt.AlignCenter)
        members_label.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(members_label)
        
        # Members list with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"QScrollArea {{ border: 2px solid {BARNEY}; border-radius: 10px; background: {WHITE}; }}")
        scroll_area.setMinimumHeight(200)
        scroll_area.setMaximumHeight(300)
        scroll_area.setMinimumWidth(400)
        scroll_area.setMaximumWidth(600)
        
        self.member_list = QListWidget()
        self.member_list.setStyleSheet(f"background: {WHITE}; border: none; font-size: 14px; color: black; padding: 10px;")
        self.member_list.itemClicked.connect(self.on_member_selected)
        
        scroll_area.setWidget(self.member_list)
        layout.addWidget(scroll_area, alignment=Qt.AlignCenter)
        
        # Selection info
        self.selection_label = QLabel("No member selected")
        self.selection_label.setAlignment(Qt.AlignCenter)
        self.selection_label.setStyleSheet(f"font-size: 14px; color: {BARNEY}; font-weight: bold; margin: 5px 0;")
        layout.addWidget(self.selection_label)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        add_btn = QPushButton("Add New Member")
        add_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 150px;")
        add_btn.clicked.connect(self.add_new_member)
        buttons_layout.addWidget(add_btn)
        
        clear_btn = QPushButton("Clear Selection")
        clear_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 150px;")
        clear_btn.clicked.connect(self.clear_selection)
        buttons_layout.addWidget(clear_btn)
        
        layout.addLayout(buttons_layout)
        
        # Action buttons for selected member
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setAlignment(Qt.AlignCenter)
        
        renew_btn = QPushButton("Renew Selected Member")
        renew_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 150px;")
        renew_btn.clicked.connect(self.renew_selected_member)
        action_buttons_layout.addWidget(renew_btn)
        
        modify_btn = QPushButton("Modify Selected Member")
        modify_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 150px;")
        modify_btn.clicked.connect(self.modify_selected_member)
        action_buttons_layout.addWidget(modify_btn)
        
        delete_btn = QPushButton("Delete Selected Member")
        delete_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 150px;")
        delete_btn.clicked.connect(self.delete_selected_member)
        action_buttons_layout.addWidget(delete_btn)
        
        layout.addLayout(action_buttons_layout)
        
        # Back button
        back_btn = QPushButton("Back to Provider Menu")
        back_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 300px;")
        back_btn.clicked.connect(lambda: main_window.goto_page("provider_menu"))
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        self.setStyleSheet(f"background: {LAVENDER};")
        
        # Load members
        self.load_members()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def load_members(self):
        """Load all members into the list widget"""
        self.member_list.clear()
        members = data_manager.members  # Show ALL members (both valid and expired)
        
        if not members:
            item = QListWidgetItem("No members found")
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self.member_list.addItem(item)
            return
        
        for member in members:
            # Format member info for display with proper status
            status = member.get('status', 'Valid')
            if status == 'Valid':
                status_display = "Active"
            elif status == 'Expired':
                status_display = "Expired"
            else:
                status_display = status
            
            member_text = f"{member['name']} (ID: {member['member_id']}) - {status_display}"
            item = QListWidgetItem(member_text)
            item.setData(Qt.UserRole, member)
            self.member_list.addItem(item)

    def on_member_selected(self, item):
        """Handle member selection"""
        if item.data(Qt.UserRole):
            self.selected_member = item.data(Qt.UserRole)
            self.selection_label.setText(f"Selected: {self.selected_member['name']} (ID: {self.selected_member['member_id']})")
            self.selection_label.setStyleSheet(f"font-size: 14px; color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")

    def get_selected_member(self):
        """Get the currently selected member"""
        return self.selected_member

    def clear_selection(self):
        """Clear the current selection"""
        self.selected_member = None
        self.member_list.clearSelection()
        self.selection_label.setText("No member selected")
        self.selection_label.setStyleSheet(f"font-size: 14px; color: {BARNEY}; font-weight: bold; margin: 5px 0;")

    def add_new_member(self):
        # Create a dialog for adding new member
        dialog = QWidget()
        dialog.setWindowTitle("Add New Member")
        dialog.setFixedSize(500, 600)
        dialog.setStyleSheet(f"background: {LAVENDER};")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Add New Member")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 20px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Form fields
        fields = {}
        field_configs = [
            ("Member Name (25 chars):", "name", 25),
            ("Street Address (25 chars):", "address", 25),
            ("City (14 chars):", "city", 14),
            ("State (2 letters):", "state", 2),
            ("ZIP Code (5 digits):", "zip", 5)
        ]
        
        for label_text, field_name, max_length in field_configs:
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")
            layout.addWidget(label)
            
            entry = QLineEdit()
            entry.setMaxLength(max_length)
            entry.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 8px; padding: 8px; font-size: 14px; color: black;")
            fields[field_name] = entry
            layout.addWidget(entry)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        submit_btn = QPushButton("Add Member")
        submit_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        submit_btn.clicked.connect(lambda: self.submit_new_member(fields, dialog))
        button_layout.addWidget(submit_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        cancel_btn.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.show()

    def submit_new_member(self, fields, dialog):
        # Validate all fields are filled
        for field_name, entry in fields.items():
            if not entry.text().strip():
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(f"Please fill in the {field_name} field.")
                msg.setStyleSheet("""
                    QLabel { color: black; }
                    QPushButton { color: black; }
                """)
                msg.exec()
                return
        
        # Validate specific formats
        
        state = fields['state'].text().strip().upper()
        if not state.isalpha() or len(state) != 2:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("State must be exactly 2 letters.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        zip_code = fields['zip'].text().strip()
        if not zip_code.isdigit() or len(zip_code) != 5:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("ZIP code must be exactly 5 digits.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Create new member using data manager
        member_id = data_manager.add_member(
            name=fields['name'].text().strip(),
            address=fields['address'].text().strip(),
            city=fields['city'].text().strip(),
            state=state,
            zip_code=zip_code
        )
        
        # Show success message
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(f"New member added successfully!\n\nMember ID: {member_id}\nName: {fields['name'].text().strip()}\nStatus: Valid\n\nMember information has been recorded.")
        msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        msg.exec()
        
        dialog.close()
        self.refresh_members()  # Refresh the member list after adding

    def renew_member(self):
        # Find expired members
        expired_members = data_manager.get_expired_members()
        
        if not expired_members:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("No Expired Members")
            msg.setText("There are no expired members to renew.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Create dialog for member selection
        dialog = QWidget()
        dialog.setWindowTitle("Renew Member")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet(f"background: {LAVENDER};")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Select Member to Renew")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Member selection
        member_label = QLabel("Enter Member ID:")
        member_label.setStyleSheet(f"color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")
        layout.addWidget(member_label)
        
        member_input = QLineEdit()
        member_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 8px; padding: 8px; font-size: 14px; color: black;")
        layout.addWidget(member_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        renew_btn = QPushButton("Renew Member")
        renew_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        renew_btn.clicked.connect(lambda: self.submit_renew_member(member_input.text().strip(), dialog))
        button_layout.addWidget(renew_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        cancel_btn.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.show()

    def submit_renew_member(self, member_id, dialog):
        if not member_id:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please enter a member ID.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Find member
        member = data_manager.get_member(member_id)
        
        if not member:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Member with ID '{member_id}' not found.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        if member['status'] != 'Expired':
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Member '{member['name']}' is not expired (current status: {member['status']}).")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Renew member using data manager
        if data_manager.renew_member(member_id):
            # Show success message
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Success")
            msg.setText(f"Member renewed successfully!\n\nMember ID: {member_id}\nName: {member['name']}\nPrevious Status: Expired\nNew Status: Valid\n\nMember has been renewed.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            
            dialog.close()

    def modify_member(self):
        # Create dialog for member selection
        dialog = QWidget()
        dialog.setWindowTitle("Modify Member")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet(f"background: {LAVENDER};")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Select Member to Modify")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Member selection
        member_label = QLabel("Enter Member ID:")
        member_label.setStyleSheet(f"color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")
        layout.addWidget(member_label)
        
        member_input = QLineEdit()
        member_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 8px; padding: 8px; font-size: 14px; color: black;")
        layout.addWidget(member_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        find_btn = QPushButton("Find Member")
        find_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        find_btn.clicked.connect(lambda: self.find_member_to_modify(member_input.text().strip(), dialog))
        button_layout.addWidget(find_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        cancel_btn.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.show()

    def find_member_to_modify(self, member_id, dialog):
        if not member_id:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please enter a member ID.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Find member
        member = data_manager.get_member(member_id)
        
        if not member:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Member with ID '{member_id}' not found.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Close selection dialog and open modification dialog
        dialog.close()
        self.show_modify_member_dialog(member)

    def show_modify_member_dialog(self, member):
        # Create modification dialog
        dialog = QWidget()
        dialog.setWindowTitle("Modify Member Information")
        dialog.setFixedSize(500, 600)
        dialog.setStyleSheet(f"background: {LAVENDER};")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Modify Member: {member['name']}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 20px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Current member info
        info_label = QLabel(f"Member ID: {member['member_id']} (cannot be changed)")
        info_label.setStyleSheet(f"color: {BARNEY}; font-weight: bold; margin: 5px 0;")
        layout.addWidget(info_label)
        
        # Form fields with current values
        fields = {}
        field_configs = [
            ("Member Name (25 chars):", "name", 25, member['name']),
            ("Street Address (25 chars):", "address", 25, member.get('address', '')),
            ("City (14 chars):", "city", 14, member.get('city', '')),
            ("State (2 letters):", "state", 2, member.get('state', '')),
            ("ZIP Code (5 digits):", "zip", 5, member.get('zip', ''))
        ]
        
        for label_text, field_name, max_length, current_value in field_configs:
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")
            layout.addWidget(label)
            
            entry = QLineEdit()
            entry.setText(current_value)
            entry.setMaxLength(max_length)
            entry.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 8px; padding: 8px; font-size: 14px; color: black;")
            fields[field_name] = entry
            layout.addWidget(entry)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        save_btn.clicked.connect(lambda: self.save_member_changes(member, fields, dialog))
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        cancel_btn.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.show()

    def save_member_changes(self, member, fields, dialog):
        # Validate state format
        state = fields['state'].text().strip().upper()
        if not state.isalpha() or len(state) != 2:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("State must be exactly 2 letters.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Validate ZIP code format
        zip_code = fields['zip'].text().strip()
        if not zip_code.isdigit() or len(zip_code) != 5:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("ZIP code must be exactly 5 digits.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Update member information using data manager
        data_manager.update_member(
            member['member_id'],
            name=fields['name'].text().strip(),
            address=fields['address'].text().strip(),
            city=fields['city'].text().strip(),
            state=state,
            zip=zip_code
        )
        
        # Show success message
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(f"Member information updated successfully!\n\nMember ID: {member['member_id']}\nName: {member['name']}\nUpdated Information:\n- Address: {member['address']}\n- City: {member['city']}\n- State: {member['state']}\n- ZIP: {member['zip']}\n\nChanges have been saved.")
        msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        msg.exec()
        
        dialog.close()

    def remove_member(self):
        # Create dialog for member selection
        dialog = QWidget()
        dialog.setWindowTitle("Remove Member")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet(f"background: {LAVENDER};")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Select Member to Remove")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Member selection
        member_label = QLabel("Enter Member ID:")
        member_label.setStyleSheet(f"color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")
        layout.addWidget(member_label)
        
        member_input = QLineEdit()
        member_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 8px; padding: 8px; font-size: 14px; color: black;")
        layout.addWidget(member_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        remove_btn = QPushButton("Remove Member")
        remove_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        remove_btn.clicked.connect(lambda: self.submit_remove_member(member_input.text().strip(), dialog))
        button_layout.addWidget(remove_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        cancel_btn.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.show()

    def submit_remove_member(self, member_id, dialog):
        if not member_id:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please enter a member ID.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Find member
        member = data_manager.get_member(member_id)
        
        if not member:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Member with ID '{member_id}' not found.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Confirm removal
        confirm_msg = QMessageBox(self)
        confirm_msg.setIcon(QMessageBox.Question)
        confirm_msg.setWindowTitle("Confirm Removal")
        confirm_msg.setText(f"Are you sure you want to remove this member?\n\nMember ID: {member_id}\nName: {member['name']}\n\nThis action cannot be undone.")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        
        if confirm_msg.exec() == QMessageBox.Yes:
            # Remove member using data manager
            if data_manager.delete_member(member_id):
                # Show success message
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText(f"Member removed successfully!\n\nMember ID: {member_id}\nName: {member['name']}\n\nMember has been removed from the system.")
                msg.setStyleSheet("""
                    QLabel { color: black; }
                    QPushButton { color: black; }
                """)
                msg.exec()
                
                dialog.close()

    def refresh_members(self):
        """Refresh the members list"""
        self.load_members()

    def renew_selected_member(self):
        """Renew the selected member"""
        if not self.selected_member:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please select a member to renew.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Renew the member
        try:
            data_manager.renew_member(self.selected_member['member_id'])
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Success")
            msg.setText(f"Member {self.selected_member['name']} has been renewed successfully.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            self.refresh_members()
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Failed to renew member: {str(e)}")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()

    def modify_selected_member(self):
        """Modify the selected member"""
        if not self.selected_member:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please select a member to modify.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        self.show_modify_member_dialog(self.selected_member)

    def delete_selected_member(self):
        """Delete the selected member"""
        if not self.selected_member:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please select a member to delete.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Confirm deletion
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirm Deletion")
        msg.setText(f"Are you sure you want to delete member {self.selected_member['name']} (ID: {self.selected_member['member_id']})?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        
        if msg.exec() == QMessageBox.Yes:
            try:
                data_manager.delete_member(self.selected_member['member_id'])
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText(f"Member {self.selected_member['name']} has been deleted successfully.")
                msg.setStyleSheet("""
                    QLabel { color: black; }
                    QPushButton { color: black; }
                """)
                msg.exec()
                self.clear_selection()
                self.refresh_members()
            except Exception as e:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(f"Failed to delete member: {str(e)}")
                msg.setStyleSheet("""
                    QLabel { color: black; }
                    QPushButton { color: black; }
                """)
                msg.exec()

class ManageProvidersPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.selected_provider = None
        self.selected_provider_index = -1
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        # Banner image
        self.banner = QLabel()
        self.banner_pixmap = QPixmap("banner.png")
        self.banner.setFixedHeight(BANNER_HEIGHT)
        self.banner.setMinimumHeight(BANNER_HEIGHT)
        self.banner.setMaximumHeight(BANNER_HEIGHT)
        self.banner.setMaximumWidth(MAX_BANNER_WIDTH)
        self.banner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.banner.setAlignment(Qt.AlignCenter)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.banner, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Title
        title_label = QLabel("Manage Providers")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"font-size: 24px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title_label)
        
        # Main content area
        content_layout = QHBoxLayout()
        
        # Left side - Provider list
        left_panel = QVBoxLayout()
        
        # Provider list title
        list_title = QLabel("Current Providers")
        list_title.setAlignment(Qt.AlignCenter)
        list_title.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        left_panel.addWidget(list_title)
        
        # Provider list with scroll area
        self.provider_list = QListWidget()
        self.provider_list.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 10px; font-size: 14px; color: black; padding: 10px;")
        self.provider_list.setMinimumHeight(300)
        self.provider_list.setMaximumHeight(400)
        self.provider_list.setMinimumWidth(400)
        self.provider_list.setMaximumWidth(500)
        self.provider_list.itemClicked.connect(self.on_provider_selected)
        left_panel.addWidget(self.provider_list)
        
        # Selection info
        self.selection_label = QLabel("Select a provider from the list above")
        self.selection_label.setAlignment(Qt.AlignCenter)
        self.selection_label.setStyleSheet(f"font-size: 14px; color: {BARNEY}; font-style: italic; margin: 5px 0;")
        left_panel.addWidget(self.selection_label)
        
        content_layout.addLayout(left_panel)
        
        # Right side - Action buttons
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignTop)
        
        # Action buttons
        add_btn = QPushButton("➕ Add New Provider")
        add_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 250px;")
        add_btn.clicked.connect(self.add_new_provider)
        right_panel.addWidget(add_btn)
        
        right_panel.addSpacing(20)
        
        modify_btn = QPushButton("✏️ Modify Selected Provider")
        modify_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 250px;")
        modify_btn.clicked.connect(self.modify_selected_provider)
        right_panel.addWidget(modify_btn)
        
        right_panel.addSpacing(20)
        
        delete_btn = QPushButton("🗑️ Delete Selected Provider")
        delete_btn.setStyleSheet(f"background: #D32F2F; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 250px;")
        delete_btn.clicked.connect(self.delete_selected_provider)
        right_panel.addWidget(delete_btn)
        
        right_panel.addSpacing(20)
        
        clear_btn = QPushButton("🔄 Clear Selection")
        clear_btn.setStyleSheet(f"background: #666666; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 250px;")
        clear_btn.clicked.connect(self.clear_selection)
        right_panel.addWidget(clear_btn)
        
        right_panel.addStretch()
        
        # Back button
        back_btn = QPushButton("Back to Manager Menu")
        back_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 10px; padding: 12px 24px; font-size: 16px; min-width: 250px;")
        back_btn.clicked.connect(lambda: main_window.goto_page("manager_menu"))
        right_panel.addWidget(back_btn)
        
        content_layout.addLayout(right_panel)
        
        layout.addLayout(content_layout)
        
        self.setLayout(layout)
        self.setStyleSheet(f"background: {LAVENDER};")
        
        # Load providers (start with no selection)
        self.selected_provider = None
        self.selected_provider_index = -1
        self.load_providers()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.banner_pixmap.isNull():
            self.banner.setPixmap(self.banner_pixmap.scaled(min(self.width(), MAX_BANNER_WIDTH), BANNER_HEIGHT, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def load_providers(self):
        """Load and display all providers in the list."""
        providers = data_manager.providers
        
        if not providers:
            self.provider_list.clear()
            self.selection_label.setText("No providers available")
            self.selected_provider = None
            self.selected_provider_index = -1
            return
        
        # Clear the list and populate with providers
        self.provider_list.clear()
        
        for i, provider in enumerate(providers):
            # Create formatted text for each provider
            provider_text = f"{i+1}. {provider['name']}\n"
            provider_text += f"   ID: {provider['provider_id']}\n"
            provider_text += f"   Address: {provider['address']}\n"
            provider_text += f"   City: {provider['city']}, {provider['state']} {provider['zip']}\n"
            provider_text += f"   Username: {provider['name'].lower().replace(' ', '')}\n"
            provider_text += f"   Password: {provider['provider_id']}"
            
            # Create list item
            item = QListWidgetItem(provider_text)
            item.setData(100, i)  # Store provider index in item data
            
            # Set background color for selected item
            if i == self.selected_provider_index:
                item.setBackground(QColor("#E8F4FD"))
                item.setForeground(QColor(CHOCOLATE))
            else:
                item.setBackground(QColor(WHITE))
                item.setForeground(QColor("black"))
            
            self.provider_list.addItem(item)
        
        if self.selected_provider:
            self.selection_label.setText(f"✅ Selected: {self.selected_provider['name']} (ID: {self.selected_provider['provider_id']})")
            self.selection_label.setStyleSheet(f"font-size: 14px; color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")
        else:
            self.selection_label.setText(f"Found {len(providers)} provider(s) - Click on a provider to select it")
            self.selection_label.setStyleSheet(f"font-size: 14px; color: {BARNEY}; font-style: italic; margin: 5px 0;")

    def on_provider_selected(self, item):
        """Handle provider selection from the list widget."""
        provider_index = item.data(100)  # Get provider index from item data
        
        if 0 <= provider_index < len(data_manager.providers):
            # If clicking on the same provider, deselect it
            if self.selected_provider_index == provider_index:
                self.selected_provider_index = -1
                self.selected_provider = None
                self.provider_list.clearSelection()
            else:
                # Clicking on a different provider, select it
                self.selected_provider_index = provider_index
                self.selected_provider = data_manager.providers[provider_index]
            self.load_providers()  # Refresh to show highlight

    def get_selected_provider(self):
        """Get the currently selected provider."""
        return self.selected_provider
    
    def clear_selection(self):
        """Clear the current selection."""
        self.selected_provider_index = -1
        self.selected_provider = None
        self.load_providers()  # Refresh to remove highlight

    def add_new_provider(self):
        """Navigate to add provider page."""
        self.main_window.goto_page("add_provider")
    
    def refresh_providers(self):
        """Refresh the provider list (called when returning from add provider page)."""
        self.load_providers()

    def modify_selected_provider(self):
        """Modify the selected provider."""
        provider = self.get_selected_provider()
        if not provider:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("No Provider Selected")
            msg.setText("Please click on a provider in the list to select it for modification.\n\nThe selected provider will be highlighted with a blue background.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        self.show_modify_provider_dialog(provider)

    def delete_selected_provider(self):
        """Delete the selected provider."""
        provider = self.get_selected_provider()
        if not provider:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("No Provider Selected")
            msg.setText("Please click on a provider in the list to select it for deletion.\n\nThe selected provider will be highlighted with a blue background.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Confirm deletion
        confirm_msg = QMessageBox(self)
        confirm_msg.setIcon(QMessageBox.Question)
        confirm_msg.setWindowTitle("Confirm Deletion")
        confirm_msg.setText(f"Are you sure you want to delete this provider?\n\nProvider ID: {provider['provider_id']}\nName: {provider['name']}\n\nThis action cannot be undone.")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        
        if confirm_msg.exec() == QMessageBox.Yes:
            # Delete provider using data manager
            if data_manager.delete_provider(provider['provider_id']):
                # Also delete the user account
                username = provider['name'].lower().replace(' ', '')
                if username in data_manager.users:
                    del data_manager.users[username]
                    data_manager.save_users()
                
                # Show success message
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText(f"Provider deleted successfully!\n\nProvider ID: {provider['provider_id']}\nName: {provider['name']}\n\nProvider has been removed from the system.")
                msg.setStyleSheet("""
                    QLabel { color: black; }
                    QPushButton { color: black; }
                """)
                msg.exec()
                
                # Reload the provider list
                self.load_providers()



    def modify_provider(self):
        # Create dialog for provider selection
        dialog = QWidget()
        dialog.setWindowTitle("Modify Provider")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet(f"background: {LAVENDER};")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Select Provider to Modify")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Provider selection
        provider_label = QLabel("Enter Provider ID:")
        provider_label.setStyleSheet(f"color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")
        layout.addWidget(provider_label)
        
        provider_input = QLineEdit()
        provider_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 8px; padding: 8px; font-size: 14px; color: black;")
        layout.addWidget(provider_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        find_btn = QPushButton("Find Provider")
        find_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        find_btn.clicked.connect(lambda: self.find_provider_to_modify(provider_input.text().strip(), dialog))
        button_layout.addWidget(find_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        cancel_btn.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.show()

    def find_provider_to_modify(self, provider_id, dialog):
        if not provider_id:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please enter a provider ID.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Find provider
        provider = data_manager.get_provider(provider_id)
        
        if not provider:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Provider with ID '{provider_id}' not found.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Close selection dialog and open modification dialog
        dialog.close()
        self.show_modify_provider_dialog(provider)

    def show_modify_provider_dialog(self, provider):
        # Create modification dialog
        dialog = QWidget()
        dialog.setWindowTitle("Modify Provider Information")
        dialog.setFixedSize(500, 600)
        dialog.setStyleSheet(f"background: {LAVENDER};")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Modify Provider: {provider['name']}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 20px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Current provider info
        info_label = QLabel(f"Provider ID: {provider['provider_id']} (cannot be changed)")
        info_label.setStyleSheet(f"color: {BARNEY}; font-weight: bold; margin: 5px 0;")
        layout.addWidget(info_label)
        
        # Form fields with current values
        fields = {}
        field_configs = [
            ("Provider Name (25 chars):", "name", 25, provider['name']),
            ("Street Address (25 chars):", "address", 25, provider.get('address', '')),
            ("City (14 chars):", "city", 14, provider.get('city', '')),
            ("State (2 letters):", "state", 2, provider.get('state', '')),
            ("ZIP Code (5 digits):", "zip", 5, provider.get('zip', ''))
        ]
        
        for label_text, field_name, max_length, current_value in field_configs:
            label = QLabel(label_text)
            label.setStyleSheet(f"color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")
            layout.addWidget(label)
            
            entry = QLineEdit()
            entry.setText(current_value)
            entry.setMaxLength(max_length)
            entry.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 8px; padding: 8px; font-size: 14px; color: black;")
            fields[field_name] = entry
            layout.addWidget(entry)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        save_btn.clicked.connect(lambda: self.save_provider_changes(provider, fields, dialog))
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        cancel_btn.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.show()

    def save_provider_changes(self, provider, fields, dialog):
        # Validate state format
        state = fields['state'].text().strip().upper()
        if not state.isalpha() or len(state) != 2:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("State must be exactly 2 letters.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Validate ZIP code format
        zip_code = fields['zip'].text().strip()
        if not zip_code.isdigit() or len(zip_code) != 5:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("ZIP code must be exactly 5 digits.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Update provider information using data manager
        data_manager.update_provider(
            provider['provider_id'],
            name=fields['name'].text().strip(),
            address=fields['address'].text().strip(),
            city=fields['city'].text().strip(),
            state=state,
            zip=zip_code
        )
        
        # Show success message
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(f"Provider information updated successfully!\n\nProvider ID: {provider['provider_id']}\nName: {provider['name']}\nUpdated Information:\n- Address: {provider['address']}\n- City: {provider['city']}\n- State: {provider['state']}\n- ZIP: {provider['zip']}\n\nChanges have been saved.")
        msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        msg.exec()
        
        dialog.close()

    def delete_provider(self):
        # Create dialog for provider selection
        dialog = QWidget()
        dialog.setWindowTitle("Delete Provider")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet(f"background: {LAVENDER};")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Select Provider to Delete")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 18px; color: {CHOCOLATE}; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Provider selection
        provider_label = QLabel("Enter Provider ID:")
        provider_label.setStyleSheet(f"color: {CHOCOLATE}; font-weight: bold; margin: 5px 0;")
        layout.addWidget(provider_label)
        
        provider_input = QLineEdit()
        provider_input.setStyleSheet(f"background: {WHITE}; border: 2px solid {BARNEY}; border-radius: 8px; padding: 8px; font-size: 14px; color: black;")
        layout.addWidget(provider_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Delete Provider")
        delete_btn.setStyleSheet(f"background: {CHOCOLATE}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        delete_btn.clicked.connect(lambda: self.submit_delete_provider(provider_input.text().strip(), dialog))
        button_layout.addWidget(delete_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"background: {BARNEY}; color: {WHITE}; font-weight: bold; border-radius: 8px; padding: 10px 20px;")
        cancel_btn.clicked.connect(dialog.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.show()

    def submit_delete_provider(self, provider_id, dialog):
        if not provider_id:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Please enter a provider ID.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Find provider
        provider = data_manager.get_provider(provider_id)
        
        if not provider:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(f"Provider with ID '{provider_id}' not found.")
            msg.setStyleSheet("""
                QLabel { color: black; }
                QPushButton { color: black; }
            """)
            msg.exec()
            return
        
        # Confirm deletion
        confirm_msg = QMessageBox(self)
        confirm_msg.setIcon(QMessageBox.Question)
        confirm_msg.setWindowTitle("Confirm Deletion")
        confirm_msg.setText(f"Are you sure you want to delete this provider?\n\nProvider ID: {provider_id}\nName: {provider['name']}\n\nThis action cannot be undone.")
        confirm_msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_msg.setStyleSheet("""
            QLabel { color: black; }
            QPushButton { color: black; }
        """)
        
        if confirm_msg.exec() == QMessageBox.Yes:
            # Delete provider using data manager
            if data_manager.delete_provider(provider_id):
                # Show success message
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Success")
                msg.setText(f"Provider deleted successfully!\n\nProvider ID: {provider_id}\nName: {provider['name']}\n\nProvider has been removed from the system.")
                msg.setStyleSheet("""
                    QLabel { color: black; }
                    QPushButton { color: black; }
                """)
                msg.exec()
                
                dialog.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chocoholics Anonymous Data Processing System")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet(f"background: {LAVENDER};")
        
        # Set custom window icon
        icon = QPixmap("choco.png")
        if not icon.isNull():
            icon = icon.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setWindowIcon(QIcon(icon))
        
        self.current_user = None
        self.stack = QStackedWidget()
        # Load Pacifico font
        font_id = QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        if font_id != -1:
            self.pacifico_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            self.pacifico_family = "Comic Sans MS"  # fallback
        self.pages = {
            "signin": SignInPage(self, self.pacifico_family),
            "manager_menu": ManagerMenuPage(self),
            "provider_menu": ProviderMenuPage(self),
            "add_provider": AddProviderPage(self),
            "forgot": ForgotPage(self),
            "verify_member": VerifyMemberPage(self),
            "service_claim": ServiceClaimPage(self),
            "manage_members": ManageMembersPage(self),
            "manage_providers": ManageProvidersPage(self),
            # Add more pages as needed
        }
        # Provider directory pages (created dynamically)
        self.provider_directory_claim = None
        self.provider_directory_menu = None
        for page in self.pages.values():
            self.stack.addWidget(page)
        self.setCentralWidget(self.stack)
        self.goto_page("signin")

    def goto_page(self, page_name):
        page = self.pages[page_name]
        self.stack.setCurrentWidget(page)
        
        # Refresh provider list when returning to manage_providers page
        if page_name == "manage_providers" and hasattr(page, 'refresh_providers'):
            page.refresh_providers()
        
        # Refresh member list when returning to manage_members page
        if page_name == "manage_members" and hasattr(page, 'refresh_members'):
            page.refresh_members()

    def goto_provider_directory(self, return_to_claim=False, is_manager=False):
        if return_to_claim:
            # Always recreate the claim page to ensure correct parameters
            if self.provider_directory_claim is not None:
                self.stack.removeWidget(self.provider_directory_claim)
                self.provider_directory_claim.deleteLater()
            self.provider_directory_claim = ProviderDirectoryPage(self, return_to_claim=True, is_manager=is_manager)
            self.stack.addWidget(self.provider_directory_claim)
            self.stack.setCurrentWidget(self.provider_directory_claim)
        else:
            # Always recreate the menu page to ensure correct parameters
            if self.provider_directory_menu is not None:
                self.stack.removeWidget(self.provider_directory_menu)
                self.provider_directory_menu.deleteLater()
            self.provider_directory_menu = ProviderDirectoryPage(self, return_to_claim=False, is_manager=is_manager)
            self.stack.addWidget(self.provider_directory_menu)
            self.stack.setCurrentWidget(self.provider_directory_menu)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
