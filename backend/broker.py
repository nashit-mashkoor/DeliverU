from taskiq import SimpleRetryMiddleware
from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

from backend.constants import REDIS_URL
from backend.utils.logging import Logging

logging_instance = Logging()
logger = logging_instance.get_logger()

# Create result backend
result_backend: RedisAsyncResultBackend = RedisAsyncResultBackend(redis_url=REDIS_URL)

# Create broker with Redis Stream
broker = (
    RedisStreamBroker(REDIS_URL, queue_name="app_stream", consumer_group_name="app_group", mkstream=True)
    .with_result_backend(result_backend)
    .with_middlewares(
        SimpleRetryMiddleware(default_retry_count=3),
    )
)


@broker.on_event("startup")
async def startup() -> None:
    """Broker startup hook"""
    logger.info("TaskIQ broker starting up")


@broker.on_event("shutdown")
async def shutdown() -> None:
    """Broker shutdown hook"""
    logger.info("TaskIQ broker shutting down")

