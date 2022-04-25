import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  port='33306',
  user="automation",
  # password="Fej1chahgheebohxohxi",  # Production
  password="ue1roo0uawechai5nieg1B",  # Testing
  database="timebank"
)

mycursor = mydb.cursor()

sql1 = "DROP TABLE IF EXISTS Serviceregister, Service, User"

mycursor.execute(sql1)

sql2 = "CREATE TABLE User" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "phone VARCHAR(30) NOT NULL," \
       "password VARCHAR(200)," \
       "user_name VARCHAR(30) NOT NULL," \
       "time_account INT NOT NULL," \
       "UNIQUE (phone), UNIQUE (user_name));"

mycursor.execute(sql2)

sql3 = "CREATE TABLE Service" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "title VARCHAR(200) NOT NULL," \
       "user_id INT NOT NULL," \
       "CONSTRAINT `fk_service_user`FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE ON UPDATE RESTRICT);"

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
       "end_time DATE);"

mycursor.execute(sql4)

sql5 = "INSERT INTO User (phone, user_name, time_account)" \
       "VALUES ('+421 905 111222', 'Obi-wan Kenobi', '1');"

sql6 = "INSERT INTO User (phone, user_name, time_account)"\
       "VALUES ('+421 905 333444', 'Darth Vader', '1');"

sql7 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Pokosim travnik', '1');"

sql8 = "INSERT INTO Serviceregister (service_id, consumer_id,service_status)" \
       "VALUES ('1', '2', 'inprogress');"

mycursor.execute(sql5)
mycursor.execute(sql6)
mycursor.execute(sql7)
mycursor.execute(sql8)
mydb.commit()
