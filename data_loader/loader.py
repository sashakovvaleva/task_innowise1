import json
from models.student import Student
from models.room import Room

class DataLoader:
    def __init__(self, db):
        self.db = db

    def load_students(self, student_file):
        with open(student_file, 'r') as file:
            students = json.load(file)
            for student in students:
                student_obj = Student(
                    birthday = student['birthday'],  
                    id = student['id'],
                    name = student['name'],
                    room = student['room'],
                    sex = student['sex']
                )
                self.db.insert_student(student_obj)

    def load_rooms(self, room_file):
        with open(room_file, 'r') as file:
            rooms = json.load(file)
            for room in rooms:
                room_obj = Room(
                    room_id = room['id'],  
                    room_name = room['name']
                )
                self.db.insert_room(room_obj)