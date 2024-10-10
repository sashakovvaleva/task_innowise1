import psycopg2

class Database:
    def __init__(self, db_params):
        self.connection = psycopg2.connect(**db_params)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute("""
        DROP TABLE IF EXISTS students;
        DROP TABLE IF EXISTS rooms;
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INT PRIMARY KEY,
            room_name VARCHAR(100) 
        );
        CREATE TABLE IF NOT EXISTS students (
            birthday TIMESTAMP NOT NULL,
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            room_id INTEGER REFERENCES rooms(room_id),
            sex CHAR(1) CHECK (sex IN ('M', 'F'))
        );
        """)
        self.connection.commit()

    def insert_room(self, room_obj):
        self.cursor.execute(
            "INSERT INTO rooms (room_id, room_name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (room_obj.room_id, room_obj.room_name)
        )
        self.connection.commit()

    def insert_student(self, student_obj):
        self.cursor.execute(
            "INSERT INTO students (id, birthday,name,room_id,sex) VALUES (%s, %s, %s, %s, %s)",
            (student_obj.id, student_obj.birthday, student_obj.name, student_obj.room, student_obj.sex)
        )
        self.connection.commit()

    def get_room_student_count(self):
        self.cursor.execute("""
        SELECT room_name, COUNT(id) AS student_count
        FROM rooms
        LEFT JOIN students
        ON rooms.room_id = students.room_id
        GROUP BY room_name;
        """)
        return self.cursor.fetchall()
    
    def view_data(self):
        print("Rooms data:")
        self.cursor.execute("SELECT * FROM rooms;")
        rooms = self.cursor.fetchall()
        for room in rooms:
            print(f"Room ID: {room[0]}, Room Number: {room[1]}")

        print("\nStudents data:")
        self.cursor.execute("SELECT * FROM students;")
        students = self.cursor.fetchall()
        for student in students:
            print(student[0], student[1], student[2], student[3], student[4])

#5 комнат, где самый маленький средний возраст студентов

    def get_min_rooms(self):
        self.cursor.execute("""
        SELECT room_name, AVG(EXTRACT(YEAR FROM AGE(birthday))) AS age
        FROM rooms
        JOIN students ON rooms.room_id = students.room_id
        GROUP BY room_name
        ORDER BY age 
        LIMIT 5;
        """)
        return self.cursor.fetchall()

#5 комнат с самой большой разницей в возрасте студентов

    def get_max_age_diff_rooms(self):
        self.cursor.execute("""
        SELECT room_name, MAX(EXTRACT(YEAR FROM AGE(birthday))) - MIN(EXTRACT(YEAR FROM AGE(birthday))) AS age_diff
        FROM rooms
        JOIN students ON rooms.room_id = students.room_id
        GROUP BY room_name
        ORDER BY age_diff DESC
        LIMIT 5;
        """)
        return self.cursor.fetchall()

#Список комнат где живут разнополые студенты

    def get_gender_rooms(self):
        self.cursor.execute("""
        SELECT room_name
        FROM rooms
        JOIN students ON rooms.room_id = students.room_id
        GROUP BY room_name
        HAVING COUNT(DISTINCT sex) > 1;
        """)
        return self.cursor.fetchall()
    
    def create_indexes(self):
        self.cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_students_room_id ON students(room_id);
        CREATE INDEX IF NOT EXISTS idx_students_age ON students(birthday);
        CREATE INDEX IF NOT EXISTS idx_students_gender ON students(sex);
        """)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
    























        
