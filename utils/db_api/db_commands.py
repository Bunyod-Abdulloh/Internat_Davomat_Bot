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

    # ============================ ADD CLASSES ============================
    async def create_table_classes(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Classes (
        id SERIAL PRIMARY KEY,
        class_number VARCHAR(10) NOT NULL,
        mark VARCHAR(10) DEFAULT '🔘' 
        );
        """
        await self.execute(sql, execute=True)

    async def add_class(self, class_number):
        sql = "INSERT INTO Classes (class_number) VALUES($1) returning *"
        return await self.execute(sql, class_number, fetchrow=True)

    async def select_all_classes(self):
        sql = "SELECT class_number, mark FROM Classes"
        return await self.execute(sql, fetch=True)

    async def select_class(self, class_number):
        sql = "SELECT class_number, mark FROM Classes WHERE class_number=$1"
        return await self.execute(sql, class_number, fetch=True)

    async def update_class_mark(self, mark, class_number):
        sql = f"UPDATE Classes SET mark=$1 WHERE class_number=$2"
        return await self.execute(sql, mark, class_number, execute=True)

    async def update_class_name(self, class_number, id_number):
        sql = f"UPDATE Classes SET class_number=$1 WHERE id=$2"
        return await self.execute(sql, class_number, id_number, execute=True)

    async def delete_class(self, id_number):
        await self.execute(f"DELETE FROM Classes WHERE id='{id_number}'", execute=True)

    async def drop_table_classes(self):
        await self.execute("DROP TABLE Classes", execute=True)

    # ============================ EDUCATORS ============================
    async def create_table_educators(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Educators (
        id SERIAL,        
        fullname VARCHAR(255) NULL,        
        first_phone VARCHAR(20) NULL,
        second_phone VARCHAR(20) NULL,
        class_number VARCHAR(20) NULL,                        
        telegram_id BIGINT NULL,
        mark VARCHAR(10) DEFAULT '🔘',
        access BOOLEAN DEFAULT FALSE,
        morning BOOLEAN DEFAULT FALSE,
        day BOOLEAN DEFAULT FALSE 
        );        
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_educators_class(self, class_number):
        sql = "INSERT INTO Educators (class_number) VALUES($1) returning *"
        return await self.execute(sql, class_number, fetchrow=True)

    async def add_educator_new(self, telegram_id, mark, class_number):
        sql = f"UPDATE Educators SET telegram_id='{telegram_id}', mark='{mark}' WHERE class_number='{class_number}'"
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

    # async def off_morning_educators(self, mark):
    #     sql = f"UPDATE Educators SET morning='{mark}'"
    #     return await self.execute(sql, execute=True)

    # async def update_educator_day(self, day, telegram_id):
    #     sql = f"UPDATE Educators SET day='{day}' WHERE telegram_id='{telegram_id}'"
    #     return await self.execute(sql, execute=True)

    async def update_educator_mark(self, mark, telegram_id, class_number):
        sql = f"UPDATE Educators SET mark=$1 WHERE telegram_id=$2 AND class_number=$3"
        return await self.execute(sql, mark, telegram_id, class_number, execute=True)

    async def update_educator_telegram(self, telegram_id, mark, class_number):
        sql = (f"UPDATE Educators SET telegram_id=NULL, mark='{mark}' WHERE class_number='{class_number}' AND "
               f"telegram_id='{telegram_id}'")
        return await self.execute(sql, execute=True)

    # async def update_educator_(self, telegram_id, class_number):
    #         sql = (f"UPDATE Educators SET telegram_id = NULL WHERE class_number='{class_number}' AND "
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

    # async def update_educator_class_number(self, class_number, mark, telegram_id):
    #     sql = f"UPDATE Educators SET class_number='{class_number}' WHERE ='{id_number}'"
    #     return await self.execute(sql, execute=True)
    async def update_educator_work_day(self, work_day, telegram_id):
        sql = f"UPDATE Educators SET work_day='{work_day}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_access(self, access: bool, telegram_id: int):
        sql = f"UPDATE Educators SET access='{access}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def select_all_educators(self, morning=None, day=None):
        if morning:
            sql = f"SELECT * FROM Educators WHERE morning='{morning}'"
        else:
            sql = f"SELECT * FROM Educators WHERE day='{day}'"
        return await self.execute(sql, fetch=True)

    async def select_educator(self, telegram_id, onerow=False):
        sql = f"SELECT * FROM Educators WHERE telegram_id='{telegram_id}'"
        if onerow:
            return await self.execute(sql, fetchrow=True)
        else:
            return await self.execute(sql, fetch=True)

    async def select_educator_distinct(self, telegram_id):
        sql = f"SELECT DISTINCT * FROM Educators WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def select_educator_mark(self, telegram_id, class_number):
        sql = f"SELECT mark FROM Educators WHERE telegram_id='{telegram_id}' AND class_number='{class_number}'"
        return await self.execute(sql, fetchrow=True)

    async def get_educators_class(self):
        sql = f"SELECT class_number, mark FROM Educators ORDER BY id"
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
        class_number VARCHAR(15) NOT NULL,
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
        class_number VARCHAR(20) NOT NULL,
        educator VARCHAR(100) NULL,
        fullname VARCHAR(100) NULL,        
        morning_check VARCHAR(15) DEFAULT '🔘',        
        night_check VARCHAR(15) DEFAULT '🔘'
        );        
        """
        await self.execute(sql, execute=True)

    async def add_student(self, class_number, fullname):
        sql = "INSERT INTO Students (class_number, fullname) VALUES($1, $2) returning *"
        return await self.execute(sql, class_number, fullname, fetchrow=True)

    # ========== Students Morning ========== #
    async def update_morning_student(self, morning_check, id_number):
        sql = f"UPDATE Students SET morning_check='{morning_check}' WHERE id='{id_number}'"
        return await self.execute(sql, execute=True)

    async def get_morning(self, class_number):
        sql = (f"SELECT id, fullname, morning_check FROM Students WHERE class_number='{class_number}' "
               f"ORDER BY fullname")
        return await self.execute(sql, fetch=True)

    async def count_morning_check(self, class_number, morning_check):
        sql = f"SELECT COUNT(morning_check) FROM Students WHERE class_number='{class_number}' AND morning_check='{morning_check}'"
        return await self.execute(sql, fetchval=True)

    # ========== Students Night ========== #
    async def update_night_student(self, night_check, id_number):
        sql = f"UPDATE Students SET night_check='{night_check}' WHERE id='{id_number}'"
        return await self.execute(sql, execute=True)

    async def get_night(self, class_number):
        sql = (f"SELECT id, fullname, night_check FROM Students "
               f"WHERE class_number='{class_number}' ORDER BY fullname")
        return await self.execute(sql, fetch=True)

    async def count_night_check(self, class_number, night_check):
        sql = (f"SELECT COUNT(night_check) FROM Students WHERE class_number='{class_number}' "
               f"AND night_check='{night_check}'")
        return await self.execute(sql, fetchval=True)

    # ========== Students All ========== #
    async def get_student_id(self, id_number):
        sql = f"SELECT morning_check, night_check, class_number FROM Students WHERE id='{id_number}'"
        return await self.execute(sql, fetchrow=True)

    async def drop_table_students(self):
        await self.execute("DROP TABLE Students", execute=True)

    async def create_table_check(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Check (        
        date DATE DEFAULT CURRENT_DATE,
        educator_id INTEGER NULL
        student_id INTEGER NULL,
        class_number VARCHAR(10) NULL,        
        morning_check VARCHAR(10) DEFAULT '🔘',
        check_day VARCHAR(10) DEFAULT '🔘',
        check_night VARCHAR(10) DEFAULT '🔘'        
        );
        """
        await self.execute(sql, execute=True)

    async def add_morning_check(self, educator_id, student_id, class_number, fullname, morning_check):
        sql = ("INSERT INTO Check (educator_id, student_id, class_number, fullname, morning_check) "
               "VALUES ($1, $2, $3, $4, $5) returning *")
        return await self.execute(sql, educator_id, student_id, class_number, fullname, morning_check,
                                  fetchrow=True)

    async def drop_table_check(self):
        await self.execute("DROP TABLE Check", execute=True)

    async def create_table_lessons(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Lessons (
        id SERIAL,        
        class_number VARCHAR(20) NULL,
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
        class_number VARCHAR(20) NULL,
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
