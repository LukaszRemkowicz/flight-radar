from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "flights" ADD "local_arrival" VARCHAR(1024) NOT NULL;
        ALTER TABLE "flights" ADD "local_departure" VARCHAR(1024) NOT NULL;
        ALTER TABLE "flights" DROP COLUMN "route";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "flights" ADD "route" JSONB NOT NULL;
        ALTER TABLE "flights" DROP COLUMN "local_arrival";
        ALTER TABLE "flights" DROP COLUMN "local_departure";"""
