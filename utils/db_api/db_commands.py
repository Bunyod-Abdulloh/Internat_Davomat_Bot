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

    async def select_employee(self, telegram_id, level=False, return_list=False):
        if level:
            sql = f"SELECT * FROM Employees WHERE telegram_id='{telegram_id}' AND level='{level}'"
            return await self.execute(sql, fetchrow=True)
        elif return_list:
            sql = f"SELECT level FROM Employees WHERE telegram_id='{telegram_id}' ORDER BY level"
            return await self.execute(sql, fetch=True)
        else:
            sql = f"SELECT level, access FROM Employees WHERE telegram_id='{telegram_id}' ORDER BY level"
            return await self.execute(sql, fetchrow=True)

    async def delete_employees_class(self, telegram_id, level):
        await self.execute(f"DELETE FROM Employees WHERE telegram_id='{telegram_id}' AND level='{level}'",
                           execute=True)

    async def delete_employees(self, telegram_id):
        await self.execute(f"DELETE FROM Employees WHERE telegram_id='{telegram_id}'", execute=True)

    async def delete_class(self, level):
        await self.execute(f"DELETE FROM Employees WHERE level='{level}'", execute=True)

    async def drop_table_employees(self):
        await self.execute("DROP TABLE Employees", execute=True)

    # ============================ EDUCATORS ============================
    async def create_table_educators(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Educators (
        id SERIAL,
        checked_date DATE DEFAULT DATE NOW(),        
        level VARCHAR(20) NULL,                        
        telegram_id BIGINT NULL,        
        work_time VARCHAR(35) NULL        
        );        
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_educator(self, telegram_id, work_time):
        sql = "INSERT INTO Educators (telegram_id, work_time) VALUES($1, $2) returning *"
        return await self.execute(sql, telegram_id, work_time, fetchrow=True)

    async def add_educator_new(self, telegram_id, mark, level):
        sql = f"UPDATE Educators SET telegram_id='{telegram_id}', mark='{mark}' WHERE level='{level}'"
        return await self.execute(sql, execute=True)

    # Ertalabki tarbiyachilar ishga kelgan kelmaganligini belgilovchi funksiya
    async def update_educators_morning(self, morning):
        sql = f"UPDATE Educators SET morning='{morning}'"
        return await self.execute(sql, execute=True)

    # Kunduzgi tarbiyachilar ishga kelgan kelmaganligini belgilovchi funksiya
    async def update_educators_day(self, day):
        sql = f"UPDATE Educators SET day='{day}'"
        return await self.execute(sql, execute=True)

    # Ertalabki tarbiyachi ishga kelgan kelmaganligini belgilovchi funksiya
    async def update_educator_morning(self, morning, telegram_id):
        sql = f"UPDATE Educators SET morning='{morning}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    # Kunduzgi tarbiyachi ishga kelgan kelmaganligini belgilovchi funksiya
    async def update_educator_day(self, day, telegram_id):
        sql = f"UPDATE Educators SET day='{day}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)


    async def update_educator_mark(self, mark, telegram_id, level):
        sql = f"UPDATE Educators SET mark=$1 WHERE telegram_id=$2 AND level=$3"
        return await self.execute(sql, mark, telegram_id, level, execute=True)

    async def update_educator_telegram(self, telegram_id, mark, level):
        sql = (f"UPDATE Educators SET telegram_id=NULL, mark='{mark}' WHERE level='{level}' AND "
               f"telegram_id='{telegram_id}'")
        return await self.execute(sql, execute=True)

    # async def update_educator_(self, telegram_id, level):
    #         sql = (f"UPDATE Educators SET telegram_id = NULL WHERE level='{level}' AND "
    #                f"telegram_id='{telegram_id}'")
    #         return await self.execute(sql, execute=True)

    async def update_educator_fullname(self, fullname, telegram_id):
        sql = f"UPDATE Educators SET fullname=$1 WHERE telegram_id=$2"
        return await self.execute(sql, fullname, telegram_id, execute=True)

    async def update_educator_first_phone(self, first_phone, telegram_id):
        sql = f"UPDATE Educators SET first_phone='{first_phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_second_phone(self, second_phone, telegram_id):
        sql = f"UPDATE Educators SET second_phone='{second_phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    # async def update_educator_class_number(self, level, mark, telegram_id):
    #     sql = f"UPDATE Educators SET level='{level}' WHERE ='{id_number}'"
    #     return await self.execute(sql, execute=True)

    async def update_educator_access(self, access: bool, telegram_id: int):
        sql = f"UPDATE Educators SET access='{access}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def select_all_educators(self, morning=None, day=None):
        if morning:
            sql = f"SELECT * FROM Educators WHERE morning='{morning}'"
        else:
            sql = f"SELECT * FROM Educators WHERE day='{day}'"
        return await self.execute(sql, fetch=True)

    async def select_educator_distinct(self, telegram_id):
        sql = f"SELECT DISTINCT * FROM Educators WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def select_educator_mark(self, telegram_id, level):
        sql = f"SELECT mark FROM Educators WHERE telegram_id='{telegram_id}' AND level='{level}'"
        return await self.execute(sql, fetchrow=True)

    async def get_educators_class(self):
        sql = f"SELECT level, mark FROM Educators ORDER BY level"
        return await self.execute(sql, fetch=True)

    async def select_by_id(self, id_number):
        sql = f"SELECT * FROM Educators WHERE id='{id_number}'"
        return await self.execute(sql, fetchrow=True)

    async def count_educators(self, all_=False, morning=False, day=False):
        if all_:
            sql = "SELECT COUNT(*) FROM Educators"
            return await self.execute(sql, fetchval=True)
        elif morning:
            sql = f"SELECT COUNT(*) FROM Educators WHERE morning='{morning}'"
            return await self.execute(sql, fetchval=True)
        elif day:
            sql = f"SELECT COUNT(*) FROM Educators WHERE day='{day}'"
            return await self.execute(sql, fetchval=True)

    async def delete_educators(self, telegram_id):
        await self.execute(f"DELETE FROM Educators WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_educators(self):
        await self.execute("DROP TABLE Educators", execute=True)

    # ============================ TABLE MORNING ============================
    async def create_table_attendance(self):
        sql = """
        CREATE TABLE Attendance IF NOT EXISTS (
        id SERIAL PRIMARY KEY,
        level VARCHAR(15) NOT NULL,
        language VARCHAR(10) NULL,
        student_fullname VARCHAR(100) NULL,
        check VARCHAR(30) NULL
        );
        """
        await self.execute(sql, execute=True)

    # ============================ STUDENTS ============================
    async def create_table_students(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Students (
        id SERIAL PRIMARY KEY,        
        level VARCHAR(20) NOT NULL,
        educator VARCHAR(100) NULL,
        fullname VARCHAR(100) NULL,        
        morning_check VARCHAR(15) DEFAULT '🔘',        
        night_check VARCHAR(15) DEFAULT '🔘',
        mark VARCHAR(5) DEFAULT '🔘'
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

    async def count_morning_check(self, level, morning_check):
        sql = f"SELECT COUNT(morning_check) FROM Students WHERE level='{level}' AND morning_check='{morning_check}'"
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
        sql = f"SELECT morning_check, night_check, level FROM Students WHERE id='{id_number}'"
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

    async def create_table_check(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Check (        
        date DATE DEFAULT CURRENT_DATE,
        educator_id INTEGER NULL
        student_id INTEGER NULL,
        level VARCHAR(10) NULL,        
        morning_check VARCHAR(10) DEFAULT '🔘',
        check_day VARCHAR(10) DEFAULT '🔘',
        check_night VARCHAR(10) DEFAULT '🔘'        
        );
        """
        await self.execute(sql, execute=True)

    async def add_morning_check(self, educator_id, student_id, level, fullname, morning_check):
        sql = ("INSERT INTO Check (educator_id, student_id, level, fullname, morning_check) "
               "VALUES ($1, $2, $3, $4, $5) returning *")
        return await self.execute(sql, educator_id, student_id, level, fullname, morning_check,
                                  fetchrow=True)

    async def drop_table_check(self):
        await self.execute("DROP TABLE Check", execute=True)

    async def create_table_lessons(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Lessons (
        id SERIAL,        
        level VARCHAR(20) NULL,
        fullname VARCHAR(60) NULL,
        language VARCHAR(10) NULL,
        lesson_name VARCHAR(50) NOT NULL,
        telegram_id BIGINT NULL,
        mark VARCHAR(10) DEFAULT '🔘'       
        );
        """
        await self.execute(sql, execute=True)

    async def add_lessons(self, lesson_name):
        sql = "INSERT INTO Lessons (lesson_name) VALUES($1) returning *"
        return await self.execute(sql, lesson_name, fetchrow=True)

    async def add_lesson(self, lesson_name):
        sql = "INSERT INTO Lessons (lesson_name) VALUES($1) returning *"
        return await self.execute(sql, lesson_name, fetchrow=True)

    async def get_lessons(self):
        sql = f"SELECT lesson_name, fullname, mark FROM Lessons ORDER BY lesson_name"
        return await self.execute(sql, fetch=True)

    async def drop_table_lessons(self):
        await self.execute("DROP TABLE Lessons", execute=True)

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
