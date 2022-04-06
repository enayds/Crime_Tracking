import sys
from PyQt5.QtSql import *
from PyQt5.QtWidgets import QWidget, QScrollBar, QMessageBox, QTableWidget, QTableWidgetItem, QApplication, QDateEdit, QFormLayout, QTextEdit, QVBoxLayout, QLabel, QStackedWidget, QLineEdit, QHBoxLayout, QPushButton, QComboBox
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
import sqlite3 as sql


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        
        self.database_path = 'C:/Users/EGBUNA/police_database.db'

        self.setFixedWidth(1200)
        self.setWindowTitle('Police Software for Crime Checking')
        
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        self.Login_Page()
        self.Information_Page()
        self.Report_Page()
        

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.Stack)
        self.setLayout(main_layout)


        #---------------getting the index of the last value in the database-------------------
    def database_row_count(self):
        connection = sql.connect(self.database_path)
        cursor = connection.cursor()
        row_count = cursor.execute("SELECT COUNT(*) FROM criminal_info").fetchone()[0]
        connection.close()
        return row_count + 1

    ## working with the update function
    def update_func(self):
        print(self.table.currentRow())

    #-------------------function for grabbing data from the database----------------------------------
    def GrabData(self):
        connection = sql.connect(self.database_path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM criminal_info')
        self.table.setRowCount(self.database_row_count())
        row = 0
        for data in cursor.fetchall():
            for col in range(17):
                self.table.setItem(row,col, QTableWidgetItem(str(data[col])))
            row += 1

        connection.close()

    def Search(self):

        connection = sql.connect(self.database_path)
        cursor = connection.cursor()
        if len(self.search_input.text()) == 0:
            print('Please enter a value')

        elif self.choice.currentIndex() == 0:
            cursor.execute("SELECT * FROM criminal_info WHERE criminal_id = :value", 
                    {
                        'value': self.search_input.text()
                    }
                    )
        elif self.choice.currentIndex() == 1:
            cursor.execute("SELECT * FROM criminal_info WHERE f_name = :value", 
                    {
                        'value': self.search_input.text()
                    }
                    )
        elif self.choice.currentIndex() == 2:
            cursor.execute("SELECT * FROM criminal_info WHERE l_name = :value", 
                    {
                        'value': self.search_input.text()
                    }
                    )
        elif self.choice.currentIndex() == 3:
            cursor.execute("SELECT * FROM criminal_info WHERE state_of_origin = :value", 
                    {
                        'value': self.search_input.text()
                    }
                    )
        elif self.choice.currentIndex() == 4:
            cursor.execute("SELECT * FROM criminal_info WHERE IPO_name = :value", 
                    {
                        'value': self.search_input.text()
                    }
                    )
        else:
            cursor.execute("SELECT * FROM criminal_info WHERE sex = :value", 
                    {
                        'value': self.search_input.text()
                    }
                    )
        results = cursor.fetchall()

        if len(results) < 1:
            self.table.clearContents()
            err_msg = QMessageBox()
            err_msg.setIcon(QMessageBox.Critical)
            err_msg.setText('Not Found')
            err_msg.setInformativeText('no record match your search')
            err_msg.setStandardButtons(QMessageBox.Ok)
            retval = err_msg.exec_()
            
            
        else:
            self.table.setRowCount(len(results))
            row = 0
            for data in results:
                for col in range(17):
                    self.table.setItem(row,col, QTableWidgetItem(str(data[col])))
                row += 1

        connection.close()






#----------------------------------Save Function to save into the database -------------------
    def Save_Msg(self, i):
        if i.text() == 'OK':
            self.criminal_id = self.database_row_count()
            connection = sql.connect(self.database_path)
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    INSERT INTO criminal_info VALUES(:criminal_id,
                    :f_name, :l_name, :sex, :age, :state, :lga, :address,
                    :case_no, :cell_no, :case_type, :arrest_date, :convict_date, :ipo,
                    :court, :town, :verdict
                    )
                    ;""", 
                    {
                        'criminal_id': self.criminal_id, 'f_name': self.f_name.text(), 'l_name': self.l_name.text(),
                        'sex': self.sex.currentText(), 'age': int(self.age.text()),
                        'state': self.state_of_origin.currentText(), 'lga': self.LGA.text(),
                        'address': self.address.toPlainText(),
                        'case_no': int(self.case_no.text()), 'cell_no': int(self.cell_no.text()),
                        'case_type': self.case_type.currentText(),
                        'arrest_date': str(self.date_arrested.date())[19:-1],
                        'convict_date': str(self.date_of_conviction.date())[19:-1],
                        'ipo': self.IPO_name.text(),
                        'court': self.court.text(),
                        'town': self.town.text(),
                        'verdict': self.verdict.text()
                    }
                    )
                connection.commit()
                print('insertion succesful')
                connection.close()
                    
            except (ValueError, sql.Error) as error:
                err_msg = QMessageBox()
                err_msg.setIcon(QMessageBox.Critical)
                err_msg.setText('Error, Please Try Again')
                err_msg.setInformativeText(str(error))
                err_msg.setStandardButtons(QMessageBox.Ok)
                retval = err_msg.exec_()
                connection.close()

        else:
            self.Stack.setCurrentIndex(1)


    # --------------------inserting data into the database-------------------------------
    def InsertIntoDB(self):
        msg = QMessageBox()
        msg.setInformativeText('Do you want save to database?! ')
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = msg.buttonClicked.connect(self.Save_Msg)
        retval = msg.exec_()
        

        
    #---------------------functions for the buttons to function-----------------

    
#----------------- Preview box ----------------------------------   
    def Preview(self):
        self.preview_box.clear()
        self.preview_box.insertPlainText("\t" + "----------Preview----------" + '\n' + '\n')
        self.preview_box.insertPlainText("Criminal Id => " + str(self.database_row_count()) + '\n')
        self.preview_box.insertPlainText("First Name => " + self.f_name.text() + '\n')
        self.preview_box.insertPlainText("Last Name => " + self.l_name.text() + '\n')
        self.preview_box.insertPlainText("Sex => " + self.sex.currentText() + '\n')
        self.preview_box.insertPlainText("Age => " + self.age.text() + '\n')
        self.preview_box.insertPlainText("Address => " + self.address.toPlainText() + '\n')
        self.preview_box.insertPlainText("State of Origin => " + self.state_of_origin.currentText() + '\n')
        self.preview_box.insertPlainText("Local Government => " + self.LGA.text() + '\n')
        self.preview_box.insertPlainText("Date Arrested => " + str(self.date_arrested.date())[19:-1] + '\n')
        self.preview_box.insertPlainText("Date of Conviction => " + str(self.date_of_conviction.date())[19:-1] + '\n')
        self.preview_box.insertPlainText("IPO Name => " + self.IPO_name.text() + '\n')
        self.preview_box.insertPlainText("Case Type => " + self.case_type.currentText() + '\n')
        self.preview_box.insertPlainText("Cell Number => " + self.cell_no.text() + '\n')
        self.preview_box.insertPlainText("Case Number => " + self.case_no.text() + '\n')
        self.preview_box.insertPlainText("Verdict => " + self.verdict.text() + '\n')
        self.preview_box.insertPlainText("Town => " + self.town.text() + '\n')
        self.preview_box.insertPlainText("Court => " + self.court.text() + '\n')
        self.preview_box.setAlignment(QtCore.Qt.AlignJustify)
        self.save_button.setEnabled(True)


        #------------------------ clear function for the reset buttons -------------------------------
    def Clear_Screen(self):
        self.preview_box.clear()
        self.preview_box.insertPlainText(("\t" + "----------Preview----------" + '\n' + '\n'))
        ## clear every textbox so the user can start all over again
        self.preview_box.setAlignment(QtCore.Qt.AlignJustify)
        self.f_name.clear()
        self.l_name.clear()
        self.sex.setCurrentText('Male')
        self.age.clear()
        self.address.clear()
        self.state_of_origin.setCurrentIndex(0)
        self.LGA.clear()
        self.date_arrested.setDate(QDate.currentDate())
        self.IPO_name.clear()
        self.case_type.clear()
        self.case_no.clear()
        self.date_of_conviction.setDate(QDate.currentDate())
        self.town.clear()
        self.court.clear()
        self.verdict.clear()
        self.save_button.setEnabled(False)


#-------------------------------Login Page UI -----------------------------------------------------
    def Login_Page(self):
        layout = QHBoxLayout()
        image = QPixmap('C:/Users/EGBUNA/PyQt5 Folder/bird_log.png')
        logo = QLabel()
        logo.setPixmap(image)
        
        greetings = QLabel('Welcome, Please Login to continue')
        greetings.setStyleSheet(
        'font-size:30px;' + 'color: white'
        )
        greetings.setAlignment(QtCore.Qt.AlignCenter)
        
        username = QLineEdit('Username')
        username.setStyleSheet(
        'font-size:30px;' + 'color: white;' + 'background-color: transparent;' + 
        'border-radius: 15px;' + 'margin-left:150px;' + 'margin-right:150px;' + "border: 4px solid 'yellow';" +
        'padding: 10px;' + 'margin-top: 50px'
        )

        password = QLineEdit('Password')
        password.setStyleSheet(
        'font-size:30px;' + 'color: white;' + 'background-color: transparent;' + 
        'border-radius: 15px;' + 'margin-left:150px;' + 'margin-right:150px;' + "border: 4px solid 'yellow';" + 
        'padding: 10px;' + 'margin-top: 20px'
        )
        password.setEchoMode(QLineEdit.Password)
        
        login_button = QPushButton('LOGIN')
        login_button.setStyleSheet("*{border: 4px solid '#BC006C';" +
                        "font-size: 16px;" +
                        "color: 'white'; " +
                        "padding: 15px 0;" +
                        'margin-left:200px;' + 
                        'margin-right:200px;' +
                        "margin-top: 50px;" +
                        "border-radius: 25px;}" +
                        "*:hover{background: #BC006C;}")
        
        login_button.clicked.connect(lambda x: self.Stack.setCurrentIndex(1))


        
        hbox = QVBoxLayout()
        hbox.addWidget(greetings)
        hbox.addWidget(username)
        hbox.addWidget(password)
        hbox.addWidget(login_button)
        hbox.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(logo)
        layout.addLayout(hbox)
        self.stack1.setLayout(layout)
        self.stack1.setStyleSheet('background: "#00002f"')
        
    def Information_Page(self):
        States = """Abia, Adamawa, Akwa Ibom, Anambra, Bauchi, Bayelsa, Benue,
        Borno, Cross River, Delta, Ebonyi, Edo, Ekiti, Enugu,
        Federal Capital Territory, Gombe, Imo, Jigawa, Kaduna,
        Kano, Katsina, Kebbi, Kogi, Kwara, Lagos, Nasarawa, Niger,
        Ogun, Ondo, Osun, Oyo, Plateau, Rivers, Sokoto, Taraba, Yobe, Zamfara""".split(', ')
        
        self.criminal_id  = QLineEdit()
        self.criminal_id.setStyleSheet('margin:10px;')
        self.criminal_id.setText(str(self.database_row_count()))
        self.criminal_id.setEnabled(False)
        self.f_name = QLineEdit()
        self.f_name.setStyleSheet('margin:10px')
        self.l_name = QLineEdit()
        self.l_name.setStyleSheet('margin:10px')
        self.sex = QComboBox()
        self.sex.setStyleSheet('margin:10px')
        self.sex.addItem('Male')
        self.sex.addItem('Female')
        self.age = QLineEdit()
        self.age.setStyleSheet('margin:10px')
        self.address = QTextEdit()
        self.address.setStyleSheet('margin:10px')
        self.state_of_origin = QComboBox()
        self.state_of_origin.addItems(States)
        self.state_of_origin.setStyleSheet('margin:10px')
        self.LGA = QLineEdit()
        self.LGA.setStyleSheet('margin:10px')

        form1 = QFormLayout()
        form1.addRow(QLabel('Criminal Id'), self.criminal_id)
        form1.addRow(QLabel('First Name'), self.f_name)
        form1.addRow(QLabel('Last Name'), self.l_name)
        form1.addRow(QLabel('Sex'), self.sex)
        form1.addRow(QLabel('Age'), self.age)
        form1.addRow(QLabel('Address'), self.address)
        form1.addRow(QLabel('State Of Origin'), self.state_of_origin)
        form1.addRow(QLabel('LGA'), self.LGA)
        

        self.date_arrested = QDateEdit(self)
        d = QDate.currentDate()
        self.date_arrested.setDate(d)
        self.date_arrested.setStyleSheet('margin:10px')
        self.IPO_name = QLineEdit()
        self.IPO_name.setStyleSheet('margin:10px')
        self.case_type = QComboBox()
        self.case_type.setStyleSheet('margin:10px')
        self.case_type.addItems(['Murder', 'Fraud', 'Robbery'])
        self.cell_no = QLineEdit()
        self.cell_no.setStyleSheet('margin:10px')
        self.case_no = QLineEdit()
        self.case_no.setStyleSheet('margin:10px')
        self.verdict = QLineEdit()
        self.verdict.setStyleSheet('margin:10px')
        self.date_of_conviction = QDateEdit()
        self.date_of_conviction.setDate(d)
        self.date_of_conviction.setStyleSheet('margin:10px')
        self.town = QLineEdit()
        self.town.setStyleSheet('margin:10px')
        self.court = QLineEdit()
        self.court.setStyleSheet('margin:10px')
    
        form2 = QFormLayout()
        form2.addRow("Date arrested", self.date_arrested)
        form2.addRow(QLabel('IPO Name'), self.IPO_name)
        form2.addRow(QLabel('Case Type'), self.case_type)
        form2.addRow(QLabel('Cell No'), self.cell_no)
        form2.addRow(QLabel('Case No'), self.case_no)
     
        form2.addRow(QLabel('Verdict'), self.verdict)
        form2.addRow(QLabel('Conviction Date'), self.date_of_conviction)
        form2.addRow(QLabel('Town'), self.town)
        form2.addRow(QLabel('Court'), self.court)
        
        self.preview_box = QTextEdit("\t" + "----------Preview----------" + '\n' + '\n')
        self.preview_box.setReadOnly(True)
        self.preview_box.setStyleSheet('background-color: white;' + 'color: black;')

        self.preview_button = QPushButton('Preview')
        self.preview_button.clicked.connect(self.Preview)
        self.save_button = QPushButton('Save')
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.InsertIntoDB)
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.Clear_Screen)
        self.update_button = QPushButton('Update')
        self.update_button.setEnabled(False)
        self.exit_button = QPushButton('Exit')
        self.exit_button.clicked.connect(lambda : self.Stack.setCurrentIndex(0))
        self.report_page = QPushButton('Report Page')
        self.report_page.clicked.connect(lambda x: self.Stack.setCurrentIndex(2))

        hbox = QHBoxLayout()
        hbox.addLayout(form1)
        hbox.addLayout(form2)
        hbox.addWidget(self.preview_box)
        
        settings_layout = QHBoxLayout()
        settings_layout.addWidget(self.preview_button)
        settings_layout.addWidget(self.save_button)
        settings_layout.addWidget(self.reset_button)
        settings_layout.addWidget(self.update_button)
        settings_layout.addWidget(self.exit_button)
        settings_layout.addWidget(self.report_page)
        layout = QVBoxLayout()
        layout.addLayout(hbox)
        layout.addLayout(settings_layout)
        self.stack2.setLayout(layout)
        self.stack2.setStyleSheet('background: "#7d5300";' + 'color: "#aaaaff";' + 'font-size:18px')

#------------------------------------------Report Layout-------------------------------------------------
    def Report_Page(self):
        heading = QLabel('Report Page')
        heading.setStyleSheet('color:black;' + 'font-size: 45px;' + 'margin:20px;' + 'padding:5px')
        heading.setAlignment(QtCore.Qt.AlignCenter)

        self.choice = QComboBox()
        self.choice.addItems(['Criminal ID', 'First Name', 'Last Name', 'State Of Origin', 'IPO Name', 'sex'])
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("background-color: white;" + "color:blue;")
        self.get_button = QPushButton('Get results')
        self.get_button.clicked.connect(self.Search)
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.choice)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.get_button)

        
        self.table = QTableWidget()
        self.table.setColumnCount(17)
        self.table.resizeColumnToContents(0)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(7, 150)
        self.table.setColumnWidth(13, 250)
        self.table.setColumnWidth(16, 350)
        column_headers = ['Id', 'First Name', 'Last Name', 'Sex', 'Age', 'State of Origin', 'LGA', 'Address', 
                            'Case No', 'Cell No', 'Case Type', 'Date Arrested', 'Conviction Date', 'IPO Name', 
                             'Court' ,'Town', 'Verdict']
        
        self.table.setHorizontalHeaderLabels(column_headers)
        self.table.resizeRowsToContents()
        self.table.setStyleSheet('background-color:white;' + 'font-size:15px;')

        
  
  

        self.show_all = QPushButton('Show All')
        self.show_all.clicked.connect(self.GrabData)
        self.update_rec = QPushButton('Update Record')
        self.update_rec.clicked.connect(self.update_func)
        self.delete = QPushButton('Delete Record')
        self.exit = QPushButton('Exit')
        self.exit.clicked.connect(lambda : self.Stack.setCurrentIndex(0))
        


        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.show_all)
        buttons_layout.addWidget(self.update_rec)
        buttons_layout.addWidget(self.delete)
        buttons_layout.addWidget(self.exit)

        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addLayout(search_layout)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)
        self.stack3.setStyleSheet('background-color:"#00002f";' + "color:red")
        self.stack3.setLayout(layout)
        




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
    
    
    
    
    
    
    
    