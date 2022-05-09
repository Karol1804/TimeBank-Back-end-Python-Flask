# Subor na handlovanie testovacej a produkcnej databazy
import mysql.connector

mydb = mysql.connector.connect(
       # host="127.0.0.1",  # Localhost
       host="157.245.27.101",  # Testing
       # host="157.230.79.85",  # Production
       port='33306',
       user="automation",
       password="ue1roo0uawechai5nieg1B",  # Testing
       # password="Fej1chahgheebohxohxi",  # Production
       database="timebank",
)

mycursor = mydb.cursor()

sql1 = "DROP TABLE IF EXISTS Serviceregister, Service, User"

mycursor.execute(sql1)

sql2 = "CREATE TABLE User" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "phone VARCHAR(30) NOT NULL," \
       "password VARCHAR(200) NOT NULL," \
       "user_name VARCHAR(30) NOT NULL," \
       "time_account INT NOT NULL," \
       "UNIQUE (phone));"

mycursor.execute(sql2)

sql3 = "CREATE TABLE Service" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "title VARCHAR(1000) NOT NULL," \
       "user_id INT NOT NULL," \
       "CONSTRAINT `fk_service_user`FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE ON UPDATE RESTRICT," \
       "estimate INT," \
       "avg_rating INT);"

mycursor.execute(sql3)

sql4 = "CREATE TABLE Serviceregister" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "service_id INT NOT NULL," \
       "CONSTRAINT `fk_serviceregister_service`FOREIGN KEY (service_id)" \
       "REFERENCES Service (id) ON DELETE CASCADE ON UPDATE RESTRICT," \
       "consumer_id INT NOT NULL," \
       "CONSTRAINT `fk_serviceregister_consumer`FOREIGN KEY (consumer_id)" \
       "REFERENCES User (id) ON DELETE CASCADE ON UPDATE RESTRICT," \
       "hours INT," \
       "service_status ENUM ('inprogress','ended') NOT NULL," \
       "end_time DATE," \
       "rating INT);"

mycursor.execute(sql4)

sql5 = "INSERT INTO User (phone, user_name, time_account, password)" \
       "VALUES ('+421 905 111222', 'Obi-wan Kenobi', '0', 'pbkdf2:sha256:" \
       "260000$yogvVRpbV5xHD8VJ$7c4cc8e3f54988c81a175afad559b08b06ec1f35c7063898dba674929ce9f9d2');"

sql6 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 333444', 'Darth Vader', '0', 'pbkdf2:sha256:" \
       "260000$FnLSMwPNR4A9quhV$cde29184e427e545ed22a4e8f3f5317f0d21060f2fd7d75b785acdf211e0d031');"

sql7 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 555666', 'Qui-gon Jinn', '0', 'pbkdf2:sha256:" \
       "260000$z1GFAnU3lDWIgreH$19ac07dacedcba5192b1b73e37897a6adf2443964f46f8b109f3fa19c33b588d');"

sql8 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 777888', 'Darth Maul', '0', 'pbkdf2:sha256:" \
       "260000$3b6IHlTVpWvJ3BnF$c3ad0843372b546e72dfd4e487f6d648cd7c52a4883e1470068d9c5310fde2a0');"

sql9 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 999000', 'Ahsoka Tano', '0', 'pbkdf2:sha256:" \
       "260000$AIZ5s2wXaMb1ra8K$89f4fe4c1847290eeb163dec27629da5a1309028f6935abae81b9cfa13a95eb3');"

sql10 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Pokosim travnik', '1');"

sql11 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Vypalim palenku', '2');"

sql12 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Bonznem roztlieskavacku', '3');"

sql13 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Pozehlim pradlo', '4');"

sql14 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Namontujem bojler', '5');"
#
sql15 = "INSERT INTO Serviceregister (service_id, consumer_id,service_status)" \
       "VALUES ('1', '2', 'inprogress');"

sql16 = "INSERT INTO Serviceregister (service_id, consumer_id,service_status)" \
       "VALUES ('2', '3', 'inprogress');"

sql17 = "INSERT INTO Serviceregister (service_id, consumer_id,service_status)" \
       "VALUES ('3', '4', 'inprogress');"

sql18 = "INSERT INTO Serviceregister (service_id, consumer_id,service_status)" \
       "VALUES ('4', '5', 'inprogress');"

sql19 = "INSERT INTO Serviceregister (service_id, consumer_id,service_status)" \
       "VALUES ('5', '1', 'inprogress');"


mycursor.execute(sql5)
mycursor.execute(sql6)
mycursor.execute(sql7)
mycursor.execute(sql8)
mycursor.execute(sql9)
mycursor.execute(sql10)
mycursor.execute(sql11)
mycursor.execute(sql12)
mycursor.execute(sql13)
mycursor.execute(sql14)
mycursor.execute(sql15)
mycursor.execute(sql16)
mycursor.execute(sql17)
mycursor.execute(sql18)
mycursor.execute(sql19)

mydb.commit()
