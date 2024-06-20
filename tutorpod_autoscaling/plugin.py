from __future__ import annotations

import os
import os.path
from glob import glob

import importlib_resources
import tutor
from tutor import hooks as tutor_hooks

from typing import Dict, Union

from .__about__ import __version__
from .hooks import AUTOSCALING_ATTRS_TYPE, AUTOSCALING_CONFIG

################# Autoscaling
# Here comes the default common settings for the autoscaling. Some resources
# should not request a specific resources, but rather use as much/as few as
# possible. This is the case for the CPU and memory in the case of workers.
# Hence workers has no "*_MEMORY_REQUEST" but only "*_MEMORY_LIMIT" settings.
# The LMS and CMS (non-worker) memory limits are set to have a small amount of
# overcommitment. This is to prevent the LMS and CMS from being slow for
# learners and instructors, though workers may lag a bit behind with tasks.
CMS_MEMORY_REQUEST_MB = 350
CMS_MAX_REPLICAS = 4
CMS_WORKER_MEMORY_REQUEST_MB = 750

LMS_MEMORY_REQUEST_MB = 350
LMS_MAX_REPLICAS = 4
LMS_WORKER_MEMORY_REQUEST_MB = 750

config: Dict[
    str, Dict[str, Union[bool, str, float, dict[str, AUTOSCALING_ATTRS_TYPE]]]
] = {
    "defaults": {"VERSION": __version__, "EXTRA_SERVICES": {}},
    "unique": {},
    "overrides": {},
}

CORE_AUTOSCALING_CONFIG: dict[str, AUTOSCALING_ATTRS_TYPE] = {
    "lms": {
        "enable_hpa": True,
        "memory_request": f"{LMS_MEMORY_REQUEST_MB}Mi",
        "cpu_request": 0.25,
        "memory_limit": f"{LMS_MEMORY_REQUEST_MB * 4}Mi",
        "cpu_limit": 1,
        "min_replicas": 1,
        "max_replicas": LMS_MAX_REPLICAS,
        "avg_cpu": 300,
        "avg_memory": "",
        "enable_vpa": False,
    },
    "lms-worker": {
        "enable_hpa": True,
        "memory_request": f"{LMS_WORKER_MEMORY_REQUEST_MB}Mi",
        "cpu_request": 0.175,
        "memory_limit": f"{LMS_WORKER_MEMORY_REQUEST_MB * 4}Mi",
        "cpu_limit": 1,
        "min_replicas": 1,
        "max_replicas": int(LMS_MAX_REPLICAS * 1.5),
        "avg_cpu": 400,
        "avg_memory": "",
        "enable_vpa": False,
    },
    "cms": {
        "enable_hpa": True,
        "memory_request": f"{CMS_MEMORY_REQUEST_MB}Mi",
        "cpu_request": 0.25,
        "memory_limit": f"{CMS_MEMORY_REQUEST_MB * 4}Mi",
        "cpu_limit": 1,
        "min_replicas": 1,
        "max_replicas": CMS_MAX_REPLICAS,
        "avg_cpu": 300,
        "avg_memory": "",
        "enable_vpa": False,
    },
    "cms-worker": {
        "enable_hpa": True,
        "memory_request": f"{CMS_WORKER_MEMORY_REQUEST_MB}Mi",
        "cpu_request": 0.175,
        "memory_limit": f"{CMS_WORKER_MEMORY_REQUEST_MB * 4}Mi",
        "cpu_limit": 1,
        "min_replicas": 1,
        "max_replicas": int(CMS_MAX_REPLICAS * 1.5),
        "avg_cpu": 400,
        "avg_memory": "",
        "enable_vpa": False,
    },
}


# The core autoscaling configs are added with a high priority, such that other users can override or
# remove them.
@AUTOSCALING_CONFIG.add(priority=tutor_hooks.priorities.HIGH)
def _add_core_autoscaling_config(
    scaling_config: dict[str, AUTOSCALING_ATTRS_TYPE]
) -> dict[str, AUTOSCALING_ATTRS_TYPE]:
    scaling_config.update(CORE_AUTOSCALING_CONFIG)
    return scaling_config


@tutor.hooks.lru_cache
def get_autoscaling_config() -> dict[str, AUTOSCALING_ATTRS_TYPE]:
    """
    This function is cached for performance.
    """
    return AUTOSCALING_CONFIG.apply({})


def iter_autoscaling_config() -> dict[str, AUTOSCALING_ATTRS_TYPE]:
    """
    Yield:

        (name, dict)
    """
    return {name: config for name, config in get_autoscaling_config().items()}


# Add configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"POD_AUTOSCALING_{key}", value)
        for key, value in config.get("defaults", {}).items()
    ]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"POD_AUTOSCALING_{key}", value)
        for key, value in config.get("unique", {}).items()
    ]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)


# Add the "templates" folder as a template root
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("tutorpod_autoscaling") / "templates")
)
# Render the "build" and "apps" folders
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("pod-autoscaling/build", "plugins"),
        ("pod-autoscaling/apps", "plugins"),
        ("pod-autoscaling/k8s", "plugins"),
    ],
)

# Make the pod-autoscaling hook functions available within templates
tutor_hooks.Filters.ENV_TEMPLATE_VARIABLES.add_items(
    [
        ("iter_autoscaling_config", iter_autoscaling_config),
    ]
)

# Load patches from files
for path in glob(
    str(importlib_resources.files("tutorpod_autoscaling") / "patches" / "*")
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
