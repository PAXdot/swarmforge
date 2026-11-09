import time
from typing import Optional, Dict, Any

class TaskQueueItem:
    """Represents an item in the task queue."""

    def __init__(self, task_id: str, payload: Dict[str, Any], timestamp: Optional[float] = None):
        """
        Initializes a new TaskQueueItem.

        :param task_id: Unique identifier for the task
        :param payload: Data associated with the task
        :param timestamp: Timestamp when the task was received, defaults to current time if not provided
        """
        self.task_id = task_id
        self.payload = payload
        self.timestamp = timestamp or time.time()

    def __repr__(self) -> str:
        """Returns a string representation of the TaskQueueItem."""
        return f"TaskQueueItem(task_id={self.task_id}, timestamp={self.timestamp})"
