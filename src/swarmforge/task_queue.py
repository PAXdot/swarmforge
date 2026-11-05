from collections import deque
from typing import Deque
import uuid
from datetime import datetime

class Task:
    def __init__(self, task_id: uuid.UUID, priority: int, expire: datetime):
        self.task_id = task_id
        self.priority = priority
        self.expire = expire

class TaskQueue:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.tasks: Deque[Task] = deque()

    def add_task(self, priority: int, expire: datetime):
        task_id = uuid.uuid4()
        task = Task(task_id=task_id, priority=priority, expire=expire)
        self.tasks.append(task)
        self._reorder_queue()

    def pop_next_task(self) -> Task:
        if not self.tasks:
            raise IndexError("Pop from empty TaskQueue")

        task = self.tasks.popleft()
        return task

    def _reorder_queue(self):
        self.tasks = deque(sorted(self.tasks, key=lambda x: x.priority))
