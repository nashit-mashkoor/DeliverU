from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from backend.constants import REDIS_URL
from backend.utils.logging import Logging

logging_instance = Logging()
logger = logging_instance.get_logger()

if REDIS_URL is None:
    raise RuntimeError("REDIS_URL environment variable is not set")

# Synchronous Redis client
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

# Asynchronous Redis client
async_redis_client = AsyncRedis.from_url(REDIS_URL, decode_responses=True)


def get_redis_client() -> Redis:
    """Get synchronous Redis client instance"""
    return redis_client


def get_async_redis_client() -> AsyncRedis:
    """Get asynchronous Redis client instance"""
    return async_redis_client


async def redis_close() -> None:
    """Close the Redis connections"""
    try:
        await async_redis_client.aclose()
        redis_client.close()
        logger.info("Redis connections closed")
    except Exception as e:
        logger.error(f"Error closing Redis connections: {e}")


async def redis_ping() -> bool:
    """Check if Redis is connected and responsive"""
    try:
        await async_redis_client.ping()
        return True
    except Exception as e:
        logger.error(f"Redis ping failed: {e}")
        return False
