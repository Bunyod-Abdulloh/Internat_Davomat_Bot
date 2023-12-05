from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
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

    async def create_table_educators(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Educators (
        id SERIAL,        
        fullname VARCHAR(255) NULL,        
        first_phone VARCHAR(20) NULL,
        second_phone VARCHAR(20) NULL,
        class_number VARCHAR(20) NULL,        
        work_day BOOLEAN NULL DEFAULT FALSE,
        post VARCHAR(50) NULL,        
        telegram_id BIGINT NOT NULL 
        );        
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_educators(self, telegram_id):
        sql = "INSERT INTO Educators (telegram_id) VALUES($1) returning *"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def update_educator_fullname(self, fullname, telegram_id):
        sql = f"UPDATE Educators SET fullname='{fullname}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_first_phone(self, first_phone, telegram_id):
        sql = f"UPDATE Educators SET first_phone='{first_phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_second_phone(self, second_phone, telegram_id):
        sql = f"UPDATE Educators SET second_phone='{second_phone}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_class_number(self, class_number, telegram_id):
        sql = f"UPDATE Educators SET class_number='{class_number}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_work_day(self, work_day, telegram_id):
        sql = f"UPDATE Educators SET work_day='{work_day}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    async def update_educator_post(self, post, telegram_id):
        sql = f"UPDATE Educators SET post='{post}' WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, execute=True)

    # async def add_student(self, student, class_number):
    #     sql = "INSERT INTO Educators (student) VALUES($1) WHERE class_number=$2"
    #     return await self.execute(sql, student, class_number, fetchrow=True)

    async def add_student(self, student_number, student_fullname, class_number, telegram_id):
        sql = (f"UPDATE Educators SET student_number='{student_number}', student_fullname='{student_fullname}'"
               f" WHERE class_number='{class_number}'")
        return await self.execute(sql, execute=True)

    async def select_all_educators(self):
        sql = "SELECT * FROM Educators"
        return await self.execute(sql, fetch=True)

    async def select_educator(self, telegram_id):
        sql = f"SELECT DISTINCT fullname FROM Educators WHERE telegram_id='{telegram_id}'"
        return await self.execute(sql, fetch=True)

    async def select_by_id(self, id_number):
        sql = f"SELECT * FROM Educators WHERE id='{id_number}'"
        return await self.execute(sql, fetchrow=True)

    async def count_educators(self):
        sql = "SELECT COUNT(*) FROM Educators"
        return await self.execute(sql, fetchval=True)

    # async def update_user_username(self, username, telegram_id):
    #     sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
    #     return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_educators(self, telegram_id):
        await self.execute(f"DELETE FROM Educators WHERE telegram_id='{telegram_id}'", execute=True)

    async def drop_table_educators(self):
        await self.execute("DROP TABLE Educators", execute=True)
