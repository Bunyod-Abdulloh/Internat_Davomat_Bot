from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST,
                                              database=config.DB_NAME)

    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False,
                      execute: bool = False):

        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # ============================ ADMIN COMMANDS ============================
    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Admins (
        telegram_id BIGINT UNIQUE NOT NULL,
        bot_on BOOLEAN DEFAULT TRUE        
        );
        """
        await self.execute(sql, execute=True)

    async def add_admin(self, telegram_id):
        sql = "INSERT INTO Admins (telegram_id) VALUES($1) returning *"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def update_admin(self, bot_on: bool):
        sql = f"UPDATE Admins SET bot_on='{bot_on}'"
        return await self.execute(sql, execute=True)

    async def select_admins(self):
        sql = f"SELECT bot_on FROM Admins"
        return await self.execute(sql, fetchrow=True)

    async def drop_table_admins(self):
        await self.execute("DROP TABLE Admins", execute=True)

    # ============================ TABLE EMPLOYEES ============================
    async def create_table_employees(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Employees (
        id SERIAL PRIMARY KEY,
        telegram_id BIGINT NULL,
        level VARCHAR(10) NOT NULL,
        fullname VARCHAR(100) NULL,
        position VARCHAR(50) NULL,
        first_phone VARCHAR(15) NULL,
        second_phone VARCHAR(15) NULL,
        access BOOLEAN DEFAULT FALSE                 
        );
        """
        await self.execute(sql, execute=True)

    async def add_class_employees(self, level):
        sql = "INSERT INTO Employees (level) VALUES($1) returning *"
        return await self.execute(sql, level, fetchrow=True)

    async def add_employee(self, telegram_id, level):
        sql = f"INSERT INTO Employees (telegram_id, level) VALUES($1, $2) returning*"
        return await self.execute(sql, telegram_id, level, fetchrow=True)

    async def update_employee_fullname(self, fullname, position, telegram_id):
        sql = f"UPDATE Employees SET fullname=$1, position=$2 WHERE telegram_id=$3"
        return await self.execute(sql, fullname, position, telegram_id, execute=True)

    async def update_employee_first_phone(self, first_phone, telegram_id):
        sql = f"UPDATE Employees SET first_phone='{first_phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_employee_second_phone(self, second_phone, telegram_id):
        sql = f"UPDATE Employees SET second_phone='{second_phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_employee_access(self, access, telegram_id):
        sql = f"UPDATE Employees SET access='{access}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def select_all_employees(self):
        sql = "SELECT * FROM Employees"
        return await self.execute(sql, fetch=True)

    async def select_new_employees(self, access):
        sql = f"SELECT * FROM Employees WHERE access='{access}'"
        return await self.execute(sql, fetch=True)

    async def select_employee(self, telegram_id):
        sql = f"SELECT level, access, id FROM Employees WHERE telegram_id='{telegram_id}' ORDER BY level"
        return await self.execute(sql, fetchrow=True)

    async def select_employee_level(self, telegram_id, level):
        sql = f"SELECT * FROM Employees WHERE telegram_id='{telegram_id}' AND level='{level}'"
        return await self.execute(sql, fetchrow=True)

    async def select_employee_return_list(self, telegram_id):
        sql = f"SELECT level, id FROM Employees WHERE telegram_id='{telegram_id}' ORDER BY level"
        return await self.execute(sql, fetch=True)

    async def select_teacher_id(self, position, level):
        sql = f"SELECT telegram_id FROM Employees WHERE position='{position}' AND level='{level}'"
        return await self.execute(sql, fetchrow=True)

    async def delete_employees_class(self, telegram_id, level):
        await self.execute(f"DELETE FROM Employees WHERE telegram_id='{telegram_id}' AND level='{level}'",
                           execute=True)

    async def delete_employees(self, telegram_id):
        await self.execute(f"DELETE FROM Employees WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_employees(self):
        await self.execute("DROP TABLE Employees", execute=True)

    # ============================ ATTENDANCE ============================
    async def create_table_attendance(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Attendance (        
        checked_date DATE DEFAULT CURRENT_DATE,                
        level VARCHAR(10) NULL,        
        student_id INTEGER NULL,
        educator_morning INTEGER NULL,
        check_morning VARCHAR(5) DEFAULT '☑️',
        teacher_id INTEGER NULL,
        check_teacher VARCHAR(5) DEFAULT '☑️',
        educator_night INTEGER NULL,
        check_night VARCHAR(5) DEFAULT '☑️'                       
        );        
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_educator(self, educator_morning, level):
        sql = "INSERT INTO Attendance (educator_morning, level) VALUES($1, $2) returning *"
        return await self.execute(sql, educator_morning, level, fetchrow=True)

    async def add_morning_students(self, educator_morning, level, student_id, check_morning):
        sql = ("INSERT INTO Attendance (educator_morning, level, student_id, check_morning) "
               "VALUES($1, $2, $3, $4) returning *")
        return await self.execute(sql, educator_morning, level, student_id, check_morning, fetchrow=True)

    async def get_all_attendance(self):
        sql = "SELECT * FROM Attendance"
        return await self.execute(sql, fetch=True)

    async def get_educator_morning(self, educator_id):
        sql = f"SELECT * FROM Attendance WHERE educator_morning='{educator_id}'"
        return await self.execute(sql, fetch=True)

    async def get_employee_attendance(self, educator_id, level):
        sql = f"SELECT level FROM Attendance WHERE educator_morning='{educator_id}' AND level='{level}'"
        return await self.execute(sql, fetch=True)

    async def drop_table_attendance(self):
        await self.execute("DROP TABLE Attendance", execute=True)

    # ============================ STUDENTS ============================
    async def create_table_students(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Students (
        id SERIAL PRIMARY KEY,        
        level VARCHAR(20) NOT NULL,        
        fullname VARCHAR(100) NULL,        
        morning_check VARCHAR(5) DEFAULT '☑️',        
        night_check VARCHAR(5) DEFAULT '☑️'        
        );        
        """
        await self.execute(sql, execute=True)

    async def add_student(self, level, fullname):
        sql = "INSERT INTO Students (level, fullname) VALUES($1, $2) returning *"
        return await self.execute(sql, level, fullname, fetchrow=True)

    # ========== Students Morning ========== #
    async def update_morning_student(self, morning_check, id_number):
        sql = f"UPDATE Students SET morning_check='{morning_check}' WHERE id='{id_number}'"
        return await self.execute(sql, execute=True)

    async def get_morning(self, level):
        sql = (f"SELECT id, fullname, morning_check FROM Students WHERE level='{level}' "
               f"ORDER BY fullname")
        return await self.execute(sql, fetch=True)

    async def get_morning_attendance(self, level):
        sql = f"SELECT id, morning_check FROM Students WHERE level='{level}'"
        return await self.execute(sql, fetch=True)

    async def count_morning_check(self, level, morning_check):
        sql = f"SELECT COUNT(morning_check) FROM Students WHERE level='{level}' AND morning_check='{morning_check}'"
        return await self.execute(sql, fetchval=True)

    async def morning_report(self, first_value, second_value, morning_check):
        sql = (f"SELECT COUNT(*) FROM Students WHERE SUBSTRING(level FROM '([0-9]+)')::INTEGER BETWEEN {first_value} "
               f"AND {second_value} AND morning_check='{morning_check}'")
        return await self.execute(sql, fetchval=True)

    # ========== Students Night ========== #
    async def update_night_student(self, night_check, id_number):
        sql = f"UPDATE Students SET night_check='{night_check}' WHERE id='{id_number}'"
        return await self.execute(sql, execute=True)

    async def get_night(self, level):
        sql = (f"SELECT id, fullname, night_check FROM Students "
               f"WHERE level='{level}' ORDER BY fullname")
        return await self.execute(sql, fetch=True)

    async def count_night_check(self, level, night_check):
        sql = (f"SELECT COUNT(night_check) FROM Students WHERE level='{level}' "
               f"AND night_check='{night_check}'")
        return await self.execute(sql, fetchval=True)

    # ========== Students All ========== #

    async def select_all_classes(self):
        sql = "SELECT DISTINCT level FROM Students ORDER BY level"
        return await self.execute(sql, fetch=True)

    async def get_student_id(self, id_number):
        sql = f"SELECT id, morning_check, night_check, level FROM Students WHERE id='{id_number}'"
        return await self.execute(sql, fetchrow=True)

    async def get_classes_students(self, select_all=False):
        if select_all:
            sql = f"SELECT * FROM Students"
        else:
            sql = f"SELECT DISTINCT level, mark FROM Students ORDER BY level"
        return await self.execute(sql, fetch=True)

    async def get_class_students(self, level):
        sql = f"SELECT level FROM Students WHERE level='{level}'"
        return await self.execute(sql, fetch=True)

    async def delete_class_students(self, level):
        await self.execute(f"DELETE FROM Students WHERE level='{level}'", execute=True)

    async def drop_table_students(self):
        await self.execute("DROP TABLE Students", execute=True)

    async def create_table_teachers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Teachers (
        id SERIAL,        
        level VARCHAR(20) NULL,
        fullname VARCHAR(100) NULL,
        language VARCHAR(10) NULL,
        lesson_name VARCHAR(50),
        telegram_id BIGINT NOT NULL,
        mark VARCHAR(10) DEFAULT '🔘'       
        );
        """
        await self.execute(sql, execute=True)

    async def add_teacher(self, fullname, telegram_id):
        sql = "INSERT INTO Teachers (fullname, telegram_id) VALUES($1, $2) returning *"
        return await self.execute(sql, fullname, telegram_id, fetchrow=True)

    async def get_teacher(self, telegram_id):
        sql = f"SELECT id, lesson_name, mark FROM Teachers WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def update_lesson_name(self, mark, lesson_name, telegram_id):
        sql = f"UPDATE Teachers SET mark=$1, lesson_name=$2 WHERE telegram_id=$3"
        return await self.execute(sql, mark, lesson_name, telegram_id, execute=True)

    async def drop_table_teachers(self):
        await self.execute("DROP TABLE Teachers", execute=True)
