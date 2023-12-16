from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "requestmodel" ALTER COLUMN "user_id" TYPE INT USING "user_id"::INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "requestmodel" ALTER COLUMN "user_id" TYPE VARCHAR(124) USING "user_id"::VARCHAR(124);"""
