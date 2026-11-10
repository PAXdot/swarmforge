from typing import Dict, Any, Union

import attr
from pydantic import BaseModel, root_validator, PositiveInt, Optional

@attr.s(auto_attribs=True)
class BackoffPolicy:
    type: str
    initial_delay: PositiveInt = 1
    multiplier: PositiveInt = 2
    maximum_delay: Optional[PositiveInt] = None

    @root_validator
    def validate_maximum_delay(cls, values):
        initial_delay = values.get('initial_delay')
        maximum_delay = values.get('maximum_delay')

        if maximum_delay is not None and maximum_delay < initial_delay:
            raise ValueError("Maximum delay cannot be less than initial delay")

        return values

@attr.s(auto_attribs=True)
class SwarmLevelMetrics:
    success_rate: float
    failure_rate: float
    average_throughput: float
    response_time: Optional[float] = None

    @root_validator
    def validate_metrics(cls, values):
        success_rate = values.get('success_rate')
        failure_rate = values.get('failure_rate')

        if success_rate + failure_rate != 1.0:
            raise ValueError("Success rate and failure rate must add up to 1.0")

        return values

class BackoffPoliciesAndMetricsConfig(BaseModel):
    backoff_policies: Dict[str, BackoffPolicy]
    swarm_level_metrics: SwarmLevelMetrics
