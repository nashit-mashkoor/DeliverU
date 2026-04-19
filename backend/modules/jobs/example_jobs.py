"""Example TaskIQ jobs"""

import asyncio
from typing import Any, Dict

from backend.services.runtime.broker import broker
from backend.utils.logging import Logging

logging_instance = Logging()
logger = logging_instance.get_logger()


@broker.task(
    task_name="example_task",
    retry_on_error=True,
    max_retries=3,
    timeout=300,  # 5 minute timeout
)
async def example_task(task_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example background task.

    Args:
        task_id: Unique identifier for this task
        data: Task data to process

    Returns:
        Dictionary with processing results
    """
    logger.info(f"Starting example task {task_id}")

    try:
        # Simulate some work
        await asyncio.sleep(2)

        result = {
            "task_id": task_id,
            "status": "completed",
            "processed_data": data,
        }

        logger.info(f"Example task {task_id} completed successfully")
        return result

    except Exception as e:
        logger.error(f"Example task {task_id} failed: {e}")
        raise


@broker.task(task_name="send_notification")
async def send_notification(user_id: int, message: str) -> Dict[str, Any]:
    """
    Example notification task.

    Args:
        user_id: User to notify
        message: Notification message

    Returns:
        Status of notification
    """
    logger.info(f"Sending notification to user {user_id}")

    # In a real app, this would send an email, push notification, etc.
    await asyncio.sleep(0.5)

    return {
        "user_id": user_id,
        "message": message,
        "status": "sent",
    }
