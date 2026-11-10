from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

import swarmforge.timestamp as ts

class RoleState(Enum):
    UNINIT = "UNINIT"
    ASSIGNED = "ASSIGNED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class RoleStateMachine(ABC):
    @abstractmethod
    def __init__(self, role: str):
        self._role = role
        self._state = RoleState.UNINIT

    @property
    def role(self) -> str:
        return self._role

    @property
    def state(self) -> RoleState:
        return self._state

    @abstractmethod
    def assign_role(self) -> None:
        pass

    @abstractmethod
    def activate_role(self) -> None:
        pass

    @abstractmethod
    def deactivate_role(self) -> None:
        pass

    @abstractmethod
    def status(self) -> str:
        pass

@dataclass
class SimpleRoleStateMachine(RoleStateMachine):
    def __init__(self, role: str):
        super().__init__(role)

    def assign_role(self) -> None:
        self._state = RoleState.ASSIGNED

    def activate_role(self) -> None:
        self._state = RoleState.ACTIVE

    def deactivate_role(self) -> None:
        self._state = RoleState.INACTIVE

    def status(self) -> str:
        return f"{self._role}: {self._state.value} at {ts.now()}"
