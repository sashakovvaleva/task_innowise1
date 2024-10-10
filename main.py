import argparse
from data_loader.loader import DataLoader
from db.db import Database
from output.formatter import Formatter


def main():
    parser = argparse.ArgumentParser(description='Загрузка данных о студентах и комнатах')
    parser.add_argument('--students', required=True, help='Путь к файлу студентов')
    parser.add_argument('--rooms', required=True, help='Путь к файлу комнат')
    parser.add_argument('--format', choices=['json', 'xml'], required=True, help='Ожидаемый формат вывода')
    parser.add_argument('--queries', nargs='+', choices=['count_of_students', '5rooms_min_age', '5rooms_max_age_diff', 'rooms_mixed_gender'], 
                        required=True, help='Запросы для выполнения: get_room_student_count, get_min_rooms, get_max_age_diff_rooms, get_gender_rooms')

    args = parser.parse_args()

    db_params = {
        'dbname': 'rooms',
        'user': 'shemerei',
        'password': 'qwsdxc09',
        'host': 'localhost',
        'port': '5433'                 
    }

    db = Database(db_params)
    db.create_tables()  
    db.create_indexes()
   
    loader = DataLoader(db)
    loader.load_rooms(args.rooms)
    loader.load_students(args.students)

    result = {}
    if 'count_of_students' in args.queries:
        result["count_of_students"] = db.get_room_student_count()

    if '5rooms_min_age' in args.queries:
        result["'5rooms_min_age'"] = db.get_min_rooms()

    if '5rooms_max_age_diff' in args.queries:
        result["5rooms_max_age_diff"] = db.get_max_age_diff_rooms()

    if 'rooms_mixed_gender' in args.queries:
        result["5rooms_mixed_gender"] = db.get_gender_rooms()

    formatter = Formatter(args.format)
    formatter.export(result)

    db.close()

if __name__ == '__main__':
    main()

