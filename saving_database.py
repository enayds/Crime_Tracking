import sqlite3

connection = sqlite3.connect('C:/Users/EGBUNA/police_database.db')
cursor = connection.cursor()

# creating tables for the database 

try:
    cursor.execute("""
    create table if not exists criminal_info (
    criminal_id int auto_increment unique primary key ,
    f_name varchar(15) not null,
    l_name varcha(15) not null,
    sex varchar(7) not null,
    age integer(2) not null,
    state_of_origin varchar(20) not null,
    LGA varchar(15) not null,
    address varchar(50) not null,
    case_no int,
    cell_no int,
    case_type varchar(20),
    date_arrested varchar(10) not null,
    conviction_date varchar(10),
    IPO_name varchar(20) not null,
    court varchar(20) not null,
    town varchar(20) not null,
    verdict varchar(50) not null
    );

    """)
    print('table1 creation success')
except sqlite3.Error as error:
    print('table creation failed', error)



connection.commit()
connection.close()
