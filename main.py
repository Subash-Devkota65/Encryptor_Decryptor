#a simple encryption/decryption program 
import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLabel,QLineEdit,QFileDialog,QComboBox,
                             QVBoxLayout,QHBoxLayout,QFrame,QButtonGroup)
from PyQt5.QtGui import QIcon,QDesktopServices
import string
import json
from PyQt5.QtCore import Qt,QUrl
class endec(QWidget):
    def __init__(self):
        super().__init__()
        self.all_chars_list=list(string.ascii_letters+" "+string.punctuation+string.digits+"\n"+"\t")
        self.file_label=QLabel("File",self)
        self.file_name_label=QLabel("No file selected",self)
        self.browse_btn=QPushButton("Browse...",self)
        self.channel_label=QLabel("Channel",self)
        self.channel_dropdown=QComboBox(self)
        self.action_label=QLabel("Action",self)
        self.encrypt_btn=QPushButton("Encrypt",self)
        self.decrypt_btn=QPushButton("Decrypt",self)
        self.conform_msg_label=QLabel("Ready. Choose a file to begain.")
        self.proceed_btn=QPushButton("Proceed",self)
        self.encrypt_btn.setCheckable(True)
        self.decrypt_btn.setCheckable(True)
        self.proceed_btn.setEnabled(False)
        self.inUI()
        self.dropdown_options()
        self.btnFunctionality()
        self.get_action_type("Encrypt")
        self.get_channel_no()

    def inUI(self):
        self.setWindowTitle("Endec")
        self.setWindowIcon(QIcon("endec_logo.png"))
        self.setGeometry(700,300,900,600)

        #all the UI stuff
        ## hboxs and vboxs
        ###hbox
        title_hbox=QHBoxLayout()
        title_frame=QFrame()
        title_frame.setLayout(title_hbox)
        file_hbox=QHBoxLayout()
        file_hbox.addWidget(self.file_name_label,3)
        file_hbox.addWidget(self.browse_btn,1)
        action_hbox=QHBoxLayout()
        action_hbox.addWidget(self.encrypt_btn)
        action_hbox.addWidget(self.decrypt_btn)
        final_hbox=QHBoxLayout()
        final_hbox.addWidget(self.conform_msg_label,3)
        final_hbox.addWidget(self.proceed_btn,1)
        ###hbox
        vbox=QVBoxLayout(self)
        vbox.addWidget(title_frame)
        body_vbox=QVBoxLayout()

        file_vbox=QVBoxLayout()
        file_vbox.addWidget(self.file_label)
        file_vbox.addLayout(file_hbox)
        body_vbox.addLayout(file_vbox)

        channel_vbox=QVBoxLayout()
        channel_vbox.addWidget(self.channel_label)
        channel_vbox.addWidget(self.channel_dropdown)
        body_vbox.addLayout(channel_vbox)

        action_vbox=QVBoxLayout()
        action_vbox.addWidget(self.action_label)
        action_vbox.addLayout(action_hbox)
        body_vbox.addLayout(action_vbox)

        body_vbox.addStretch()
        body_vbox.addLayout(final_hbox)
        vbox.addLayout(body_vbox)
        ##actual UI
        ###naming_stuff(i hate it)
        title_frame.setObjectName("Title")
        self.file_name_label.setObjectName("file_name")
        self.browse_btn.setObjectName("browse_btn")
        self.encrypt_btn.setObjectName("encrypt_btn")
        self.decrypt_btn.setObjectName("decrypt_btn")
        self.proceed_btn.setObjectName("proceed_btn")
        self.channel_dropdown.setObjectName("channel_dropdown")
        self.conform_msg_label.setObjectName("conform_msg")
        ###CSS
        title_frame.setFixedHeight(50)
        self.channel_dropdown.setFixedHeight(50)
        self.encrypt_btn.setFixedHeight(60)
        self.decrypt_btn.setFixedHeight(60)
        self.proceed_btn.setFixedHeight(60)

        vbox.setContentsMargins(0,0,0,30)
        body_vbox.setContentsMargins(40,25,40,10)

        body_vbox.setSpacing(25)
        file_vbox.setSpacing(5)
        channel_vbox.setSpacing(5)
        action_vbox.setSpacing(5)
        file_hbox.setSpacing(15)

        vbox.setAlignment(Qt.AlignTop)
        #makes it unable to have both btn checked
        action_btns=QButtonGroup(self)
        action_btns.setExclusive(True)
        action_btns.addButton(self.encrypt_btn)
        action_btns.addButton(self.decrypt_btn)
        self.encrypt_btn.setChecked(True)
        #Real CSS
        self.setStyleSheet("""
        QLabel,QPushButton,QComboBox{
        font-size:18px;
        font-family:Segoe UI;
        }
        QFrame#Title{
        background-color:#0F5C5C;
        }
        QLabel#file_name{
        color#97a6ba;
        background-color:white;
        border:2px solid #a2a5a8;
        border-radius:10px;
        padding:10px;     
        }
        QPushButton#browse_btn{
        font-size:20px;
        font-family:Segoe UI;
        border:2px solid #0F5C5C;
        border-radius:10px;
        padding:15px; 
        }
        QComboBox#channel_dropdown{
        border:2px solid #a2a5a8;
        border-radius:6px;
        padding-left:10px;
        }
        QPushButton#encrypt_btn,QPushButton#decrypt_btn,QPushButton#proceed_btn
        {
        font-size:20px;
        font-family:Segoe UI;
        border-radius:8px;
        }
        QPushButton#encrypt_btn,QPushButton#decrypt_btn{
        border:2px solid #AAB2BD
        }
        QPushButton#proceed_btn{
        background-color:#0F5C5C;
        color:white;
        }
       QPushButton#browse_btn:hover,QPushButton#proceed_btn:hover{
        font-size:22px
        } 
        QPushButton#encrypt_btn:checked, QPushButton#decrypt_btn:checked{
        background-color:#0F5C5C;
        color:white;
        border:2px solid #0F5C5C
        }
        QPushButton#proceed_btn:disabled{
        background: #e4e8ed;
        color: #9AA3AF;
        border-color: #D5DAE0;
        }
        QLabel#conform_msg{
        font-size:22px;
        font-family:Segoe UI;
        }
        """)
    
    def dropdown_options(self):
        channels_list=[f"Channel {x}" for x in range(1,101)]
        self.channel_dropdown.addItems(channels_list)
    def btnFunctionality(self):
        self.browse_btn.clicked.connect(self.browse_file)
        self.encrypt_btn.clicked.connect(lambda: self.get_action_type("Encrypt"))
        self.decrypt_btn.clicked.connect(lambda: self.get_action_type("Decrypt"))
        self.channel_dropdown.currentTextChanged.connect(self.get_channel_no)
        self.proceed_btn.clicked.connect(self.perform_action)
    def browse_file(self):
        self.file_path,_=QFileDialog.getOpenFileName(self,"Select a file","","Text Files (*.txt)")
        self.file_name_label.setText(self.file_path)
        self.proceed_btn.setEnabled(True)
        self.update_confirmation_message()
    def get_action_type(self,action):
        self.mode=action
        if self.proceed_btn.isEnabled():
            self.update_confirmation_message()
    def get_channel_no(self):
        self.channel_name=self.channel_dropdown.currentText()
        if self.proceed_btn.isEnabled():
            self.update_confirmation_message()   
    def update_confirmation_message(self):
        #acessing the file name from its path
        file_name_list=[]
        for letter in reversed(self.file_path):
            if not letter == "/":
                file_name_list.append(letter)
            else:
                break
        file_name_list.reverse()
        file_name=("").join(file_name_list)
        self.conform_msg_label.setText(f"{self.mode} '{file_name}' via {self.channel_name}")
    def perform_action(self):
        with open("encryption_keys.json","r") as json_file:
            key_dict=json.load(json_file)
            current_key=key_dict[str(int(self.channel_name[8:])-1)]
        if self.mode=="Encrypt":
            self.perform_encrypt(current_key)
        elif self.mode=="Decrypt":
            self.perform_decrypt(current_key)
    def perform_encrypt(self,key):
        with open(self.file_path,"r") as plane_file:
            plane_text=plane_file.read()
            cipher_text=""
            for letter in plane_text:
                    cipher_text+=key[self.all_chars_list.index(letter)]
        with open (self.file_path,"w") as encrypted_file:
            encrypted_file.write(cipher_text)
        self.encrypt_btn.setEnabled(False)
        self.decrypt_btn.setEnabled(True)
        self.open_notepad()
    def perform_decrypt(self,key):
        with open(self.file_path,"r") as encrypted_file:
            cipher_text=encrypted_file.read()
            plane_text=""
            for letter in cipher_text:
                plane_text+=self.all_chars_list[key.index(letter)]
        with open (self.file_path,"w") as plane_file:
            plane_file.write(plane_text)
        self.decrypt_btn.setEnabled(False)
        self.encrypt_btn.setEnabled(True)
        self.open_notepad()

    def open_notepad(self):
        self.conform_msg_label.setText(f"File has been {self.mode}ed.")
        
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.file_path))


if __name__=="__main__":
    app=QApplication(sys.argv)
    endecWindow=endec()
    endecWindow.show()
    sys.exit(app.exec_())
