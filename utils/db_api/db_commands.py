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

    # ============================ EDUCATORS ============================
    async def create_table_educators(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Educators (
        id SERIAL,        
        fullname VARCHAR(255) NULL,        
        first_phone VARCHAR(20) NULL,
        second_phone VARCHAR(20) NULL,
        class_number VARCHAR(20) NULL,        
        work_day BOOLEAN NULL DEFAULT FALSE,                
        telegram_id BIGINT NULL,
        access BOOLEAN NULL DEFAULT FALSE 
        );        
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    # async def add_educator(self, telegram_id, class_number):
    #     sql = "INSERT INTO Educators (fullname, telegram_id) VALUES($1, $2) returning *"
    #     return await self.execute(sql, telegram_id fetchrow=True)

    async def add_educator_(self, telegram_id, class_number):
        sql = f"UPDATE Educators SET telegram_id='{telegram_id}' WHERE class_number='{class_number}'"
        return await self.execute(sql, execute=True)

    async def add_educators_class(self, class_number):
        sql = "INSERT INTO Educators (class_number) VALUES($1) returning *"
        return await self.execute(sql, class_number, fetchrow=True)

    async def update_educator_telegram(self, telegram_id, class_number):
        sql = (f"UPDATE Educators SET telegram_id = NULL WHERE class_number='{class_number}' AND "
               f"telegram_id='{telegram_id}'")
        return await self.execute(sql, execute=True)

    async def update_educator_fullname(self, fullname, class_number, telegram_id):
        sql = (f"UPDATE Educators SET fullname='{fullname}' WHERE telegram_id='{telegram_id}' "
               f"AND class_number='{class_number}'")
        return await self.execute(sql, execute=True)

    async def update_educator_first_phone(self, first_phone, telegram_id):
        sql = f"UPDATE Educators SET first_phone='{first_phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_second_phone(self, second_phone, telegram_id):
        sql = f"UPDATE Educators SET second_phone='{second_phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_class_number(self, class_number, id_number):
        sql = f"UPDATE Educators SET class_number='{class_number}' WHERE id='{id_number}'"
        return await self.execute(sql, execute=True)

    async def update_educator_work_day(self, work_day, telegram_id):
        sql = f"UPDATE Educators SET work_day='{work_day}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_access(self, access: bool, telegram_id: int):
        sql = f"UPDATE Educators SET access='{access}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def select_all_educators(self):
        sql = "SELECT * FROM Educators"
        return await self.execute(sql, fetch=True)

    async def select_educator(self, telegram_id):
        sql = f"SELECT * FROM Educators WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetchrow=True)

    async def select_educator_(self, telegram_id, class_number):
        sql = f"SELECT DISTINCT * FROM Educators WHERE telegram_id='{telegram_id}' AND class_number='{class_number}'"
        return await self.execute(sql, fetchrow=True)

    async def get_educators_class(self):
        sql = f"SELECT class_number FROM Educators ORDER BY id"
        return await self.execute(sql, fetch=True)

    async def select_by_id(self, id_number):
        sql = f"SELECT * FROM Educators WHERE id='{id_number}'"
        return await self.execute(sql, fetchrow=True)

    async def count_educators(self):
        sql = "SELECT COUNT(*) FROM Educators"
        return await self.execute(sql, fetchval=True)

    async def delete_educators(self, telegram_id):
        await self.execute(f"DELETE FROM Educators WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_educators(self):
        await self.execute("DROP TABLE Educators", execute=True)

    # ============================ STUDENTS ============================
    async def create_table_students(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Students (
        id SERIAL PRIMARY KEY,        
        class_number VARCHAR(20) NOT NULL,
        fullname VARCHAR(255) NULL,
        language VARCHAR(10) NULL,
        morning_check VARCHAR(5) DEFAULT '🔘',
        day_check VARCHAR(5) DEFAULT '🔘',
        night_check VARCHAR(5) DEFAULT '🔘'
        );        
        """
        await self.execute(sql, execute=True)

    async def add_student(self, class_number, language, fullname):
        sql = ("INSERT INTO Students (class_number, language, fullname) "
               "VALUES($1, $2, $3) returning *")
        return await self.execute(sql, class_number, language, fullname, fetchrow=True)

    async def update_student(self, old_class, old_fullname, new_class, new_fullname):
        sql = (f"UPDATE Students SET class_number='{new_class}', fullname='{new_fullname}'"
               f" WHERE class_number='{old_class}' AND fullname='{old_fullname}'")
        return await self.execute(sql, execute=True)

    async def update_morning_student(self, morning_check, id_number):
        sql = f"UPDATE Students SET morning_check='{morning_check}' WHERE id='{id_number}'"
        return await self.execute(sql, execute=True)

    async def get_students(self, class_number):
        sql = (f"SELECT id, class_number, fullname, morning_check FROM Students "
               f"WHERE class_number='{class_number}' ORDER BY fullname")
        return await self.execute(sql, fetch=True)

    async def get_student(self, class_number, fullname):
        sql = f"SELECT * FROM Students WHERE class_number='{class_number}' AND fullname='{fullname}'"
        return await self.execute(sql, fetchrow=True)

    async def get_student_id(self, id_number):
        sql = f"SELECT morning_check, day_check, night_check FROM Students WHERE id='{id_number}'"
        return await self.execute(sql, fetchrow=True)

    async def count_morning_check(self, class_number, morning_check):
        sql = f"SELECT COUNT(morning_check) FROM Students WHERE class_number='{class_number}' AND morning_check='{morning_check}'"
        return await self.execute(sql, fetchval=True)

    async def delete_student(self, id_number):
        await self.execute(f"DELETE FROM Students WHERE id='{id_number}'", execute=True)

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
