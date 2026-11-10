from typing import Callable, Dict, List, Optional, Type
from queue import Queue
from collections import defaultdict

from .task_queue import TaskQueue

class EventType:
    TASK_ADDED = "task_added"
    TASK_REMOVED = "task_removed"
    TASK_PROGRESS = "task_progress"

class EventEmitter:
    def __init__(self, task_queue: TaskQueue):
        self._task_queue = task_queue
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)

    def on(self, event_type: str, listener: Callable) -> None:
        """
        Attach a listener to an event.

        :param event_type: The name of the event.
        :param listener: The callable to invoke when the event occurs.
        """
        self._listeners[event_type].append(listener)

    def emit(self, event_type: str, *args, **kwargs) -> None:
        """
        Publish an event and invoke all attached listeners.

        :param event_type: The name of the event.
        :param args: Positional arguments to pass to listeners.
        :param kwargs: Keyword arguments to pass to listeners.
        """
        for listener in self._listeners.get(event_type, []):
            listener(*args, **kwargs)

    def _on_task_added(self, task) -> None:
        self.emit(EventType.TASK_ADDED, task)

    def _on_task_removed(self, task) -> None:
        self.emit(EventType.TASK_REMOVED, task)

    def _on_task_progress(self, task, progress) -> None:
        self.emit(EventType.TASK_PROGRESS, task, progress)

def _setup_event_emitter(task_queue: TaskQueue) -> EventEmitter:
    event_emitter = EventEmitter(task_queue)

    def _wrap_task_add(task: TaskQueue.Item) -> None:
        event_emitter._on_task_added(task)

    def _wrap_task_remove(task: TaskQueue.Item) -> None:
        event_emitter._on_task_removed(task)

    def _wrap_task_progress(task: TaskQueue.Item, progress: float) -> None:
        event_emitter._on_task_progress(task, progress)

    task_queue.register_on_task_add(_wrap_task_add)
    task_queue.register_on_task_remove(_wrap_task_remove)
    task_queue.register_on_task_progress(_wrap_task_progress)

    return event_emitter
