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
       "VALUES ('+421 905 111222', 'Obi-wan Kenobi', '7', 'pbkdf2:sha256:" \
       "260000$yogvVRpbV5xHD8VJ$7c4cc8e3f54988c81a175afad559b08b06ec1f35c7063898dba674929ce9f9d2');"

sql6 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 333444', 'Darth Vader', '0', 'pbkdf2:sha256:" \
       "260000$FnLSMwPNR4A9quhV$cde29184e427e545ed22a4e8f3f5317f0d21060f2fd7d75b785acdf211e0d031');"

sql7 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 555666', 'Qui-gon Jinn', '1', 'pbkdf2:sha256:" \
       "260000$z1GFAnU3lDWIgreH$19ac07dacedcba5192b1b73e37897a6adf2443964f46f8b109f3fa19c33b588d');"

sql8 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 777888', 'Darth Maul', '0', 'pbkdf2:sha256:" \
       "260000$3b6IHlTVpWvJ3BnF$c3ad0843372b546e72dfd4e487f6d648cd7c52a4883e1470068d9c5310fde2a0');"

sql9 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 999000', 'Ahsoka Tano', '7', 'pbkdf2:sha256:" \
       "260000$AIZ5s2wXaMb1ra8K$89f4fe4c1847290eeb163dec27629da5a1309028f6935abae81b9cfa13a95eb3');"

sql10 = "INSERT INTO Service (title, user_id, estimate)" \
       "VALUES ('Pokosim travnik s motorovou kosackou za polnoci za zvuku vytia vlkov', '1', '2');"

sql11 = "INSERT INTO Service (title, user_id, estimate, avg_rating)" \
       "VALUES ('Vypalim palenku', '1', '8', '4');"

sql12 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Pokosim zahradu', '2');"

sql13 = "INSERT INTO Service (title, user_id, estimate)" \
       "VALUES ('Pozehlim pradlo', '3', '1');"

sql14 = "INSERT INTO Service (title, user_id, estimate, avg_rating)" \
       "VALUES ('Vyperiem pradlo', '5', '2', '1');"

sql15 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Postriham kriky', '4');"

sql16 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Vypijem palenku', '2');"

sql17 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Porylujem zahradu', '3');"

sql18 = "INSERT INTO Service (title, user_id, estimate, avg_rating)" \
       "VALUES ('Vymalujem dom', '4', '8', '3');"

sql19 = "INSERT INTO Service (title, user_id, estimate)" \
       "VALUES ('Vynesiem smeti', '5', '1');"

sql20 = "INSERT INTO Service (title, user_id, estimate, avg_rating)" \
       "VALUES ('Vymalujem plot', '1', '4', '4');"

sql21 = "INSERT INTO Service (title, user_id, estimate)" \
       "VALUES ('Vyvolam hadku', '2', '1');"

#
sql22 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('1', '2', 'inprogress');"

sql23 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status, end_time, rating, hours)" \
       "VALUES ('11', '3', 'ended', '2020-05-12', '4', '2');"

sql24 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('3', '2', 'inprogress');"

sql25 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('4', '1', 'inprogress');"

sql26 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status, end_time, rating, hours)" \
       "VALUES ('8', '1', 'ended', '2020-12-15', '3', '1');"

sql27 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('1', '4', 'inprogress');"

sql28 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status, end_time, rating, hours)" \
       "VALUES ('2', '5', 'ended', '2017-04-08', '4', '5');"

sql29 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('3', '1', 'inprogress');"

sql30 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('4', '3', 'inprogress');"

sql31 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status, end_time, rating, hours)" \
       "VALUES ('5', '2', 'ended', '2019-02-01', '1', '7');"

sql32 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('4', '3', 'inprogress');"

sql33 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('5', '2', 'inprogress');"


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
mycursor.execute(sql20)
mycursor.execute(sql21)
mycursor.execute(sql22)
mycursor.execute(sql23)
mycursor.execute(sql24)
mycursor.execute(sql25)
mycursor.execute(sql26)
mycursor.execute(sql27)
mycursor.execute(sql28)
mycursor.execute(sql29)
mycursor.execute(sql30)
mycursor.execute(sql31)
mycursor.execute(sql32)
mycursor.execute(sql33)

mydb.commit()
