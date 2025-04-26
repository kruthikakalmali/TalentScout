import aioredis
from app.config import REDIS_URL

redis = aioredis.from_url(REDIS_URL, decode_responses=True)

async def create_session(session_id: str):
    await redis.hset(session_id, mapping={"context": ""})

async def update_session(session_id: str, field: str, value: str):
    await redis.hset(session_id, field, value)

async def get_session(session_id: str):
    return await redis.hgetall(session_id)

async def delete_session(session_id: str):
    await redis.delete(session_id)
