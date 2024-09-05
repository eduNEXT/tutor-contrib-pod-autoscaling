"""
These hooks are stored in a separate module. If they were included in plugin.py, then
the pod-autoscaling hooks would be created in the context of some other plugin that imports
them.
"""

from __future__ import annotations

from typing import TypedDict, NotRequired

from tutor.core.hooks import Filter


class AUTOSCALING_ATTRS_TYPE(TypedDict):
    enable_hpa: bool
    memory_limit: str
    memory_request: str
    cpu_limit: float
    cpu_request: float
    min_replicas: int
    max_replicas: int
    avg_cpu: int
    avg_memory: str
    enable_vpa: bool
    list_length: NotRequired[int]
    queue_name: NotRequired[str]
    enable_keda: NotRequired[bool]


AUTOSCALING_CONFIG: Filter[dict[str, AUTOSCALING_ATTRS_TYPE], []] = Filter()
