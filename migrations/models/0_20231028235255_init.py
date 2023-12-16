from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "requestmodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "request_id" VARCHAR(124) NOT NULL,
    "response" JSONB NOT NULL,
    "requested_flight_to" VARCHAR(124) NOT NULL,
    "requested_flight_from" VARCHAR(124) NOT NULL,
    "user_id" VARCHAR(124) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "requestmodel"."request_id" IS 'Search ID. Example: a4fd41e0-6f06-8de2-b4bc-b5c0440cca0b';
CREATE TABLE IF NOT EXISTS "flights" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "fly_from" VARCHAR(12) NOT NULL,
    "fly_to" VARCHAR(12) NOT NULL,
    "city_from" VARCHAR(124) NOT NULL,
    "city_to" VARCHAR(124) NOT NULL,
    "nights" INT NOT NULL,
    "bags_price" JSONB NOT NULL,
    "bag_limit" JSONB NOT NULL,
    "availability" JSONB NOT NULL,
    "airlines" JSONB NOT NULL,
    "route" JSONB NOT NULL,
    "booking_token" VARCHAR(2048) NOT NULL,
    "deep_link" VARCHAR(2048) NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "price_conversion" JSONB NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "search_id_id" INT REFERENCES "requestmodel" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "flights"."fly_from" IS 'Country to code. Example: PL';
COMMENT ON COLUMN "flights"."fly_to" IS 'Country from code. Example: ES';
COMMENT ON COLUMN "flights"."city_from" IS 'City from. Example: Warsaw';
COMMENT ON COLUMN "flights"."city_to" IS 'City to. Example: Tenerife';
CREATE TABLE IF NOT EXISTS "flight_route" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "city_from" VARCHAR(124) NOT NULL,
    "city_to" VARCHAR(124) NOT NULL,
    "airline" VARCHAR(100) NOT NULL,
    "return_" BOOL NOT NULL,
    "flight_no" VARCHAR(124) NOT NULL,
    "local_arrival" VARCHAR(1024) NOT NULL,
    "local_departure" VARCHAR(1024) NOT NULL,
    "flight_id" INT REFERENCES "flights" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "flight_route"."city_from" IS 'City from. Example: Warsaw';
COMMENT ON COLUMN "flight_route"."city_to" IS 'City to. Example: Tenerife';
COMMENT ON COLUMN "flight_route"."airline" IS 'Airline. Example: Ryanair';
COMMENT ON COLUMN "flight_route"."return_" IS 'Return flight. Example: True';
COMMENT ON COLUMN "flight_route"."flight_no" IS 'Flight number. Example: FR 321';
COMMENT ON COLUMN "flight_route"."local_arrival" IS 'Local arrival time. Example: 2021-07-10T23:10';
COMMENT ON COLUMN "flight_route"."local_departure" IS 'Local departure time. Example: 2021-07-10T23:10';
COMMENT ON TABLE "flight_route" IS 'Stores flight route data (there and back)';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
