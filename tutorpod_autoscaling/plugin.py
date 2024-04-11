from __future__ import annotations

import os
import os.path
from glob import glob

import importlib_resources
from tutor import hooks

from .__about__ import __version__

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

config = {
    "defaults": {
        "VERSION": __version__,
        "CMS_MEMORY_REQUEST": f"{CMS_MEMORY_REQUEST_MB}Mi",
        "LMS_MEMORY_REQUEST": f"{LMS_MEMORY_REQUEST_MB}Mi",
        # Kubernetes HPA autoscaling settings
        "CMS_HPA": True,
        "CMS_AVG_CPU": 300,
        "CMS_AVG_MEMORY": "",
        "CMS_CPU_LIMIT": 1,
        "CMS_CPU_REQUEST": 0.25,
        "CMS_MAX_REPLICAS": CMS_MAX_REPLICAS,
        "CMS_MEMORY_LIMIT": f"{CMS_MEMORY_REQUEST_MB * 4}Mi",
        "CMS_MIN_REPLICAS": 1,
        "CMS_WORKER_HPA": True,
        "CMS_WORKER_AVG_CPU": 400,
        "CMS_WORKER_AVG_MEMORY": "",  # Disable memory-based autoscaling
        "CMS_WORKER_CPU_LIMIT": 1,
        "CMS_WORKER_CPU_REQUEST": 0.175,
        "CMS_WORKER_MAX_REPLICAS": CMS_MAX_REPLICAS * 1.5,
        "CMS_WORKER_MEMORY_LIMIT": f"{CMS_WORKER_MEMORY_REQUEST_MB * 4}Mi",
        "CMS_WORKER_MEMORY_REQUEST": f"{CMS_WORKER_MEMORY_REQUEST_MB}Mi",
        "CMS_WORKER_MIN_REPLICAS": 1,
        "LMS_HPA": True,
        "LMS_AVG_CPU": 300,
        "LMS_AVG_MEMORY": "",
        "LMS_CPU_LIMIT": 1,
        "LMS_CPU_REQUEST": 0.25,
        "LMS_MAX_REPLICAS": LMS_MAX_REPLICAS,
        "LMS_MEMORY_LIMIT": f"{LMS_MEMORY_REQUEST_MB * 4}Mi",
        "LMS_MIN_REPLICAS": 1,
        "LMS_WORKER_HPA": True,
        "LMS_WORKER_AVG_CPU": 400,
        "LMS_WORKER_AVG_MEMORY": "",  # Disable memory-based autoscaling
        "LMS_WORKER_CPU_LIMIT": 1,
        "LMS_WORKER_CPU_REQUEST": 0.175,
        "LMS_WORKER_MAX_REPLICAS": LMS_MAX_REPLICAS * 1.5,
        "LMS_WORKER_MEMORY_LIMIT": f"{LMS_WORKER_MEMORY_REQUEST_MB * 4}Mi",
        "LMS_WORKER_MEMORY_REQUEST": f"{LMS_WORKER_MEMORY_REQUEST_MB}Mi",
        "LMS_WORKER_MIN_REPLICAS": 1,
        # Kubernetes VPA autoscaling settings
        "LMS_VPA": False,
        "LMS_WORKER_VPA": False,
        "CMS_VPA": False,
        "CMS_WORKER_VPA": False,
    },
    "unique": {},
    "overrides": {},
}

# Add configuration entries
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"POD_AUTOSCALING_{key}", value) for key, value in config["defaults"].items()]
)
hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"POD_AUTOSCALING_{key}", value) for key, value in config["unique"].items()]
)
hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))


# Add the "templates" folder as a template root
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("tutorpod_autoscaling") / "templates")
)
# Render the "build" and "apps" folders
hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("pod-autoscaling/build", "plugins"),
        ("pod-autoscaling/apps", "plugins"),
        ("pod-autoscaling/k8s", "plugins"),
    ],
)

# Load patches from files
for path in glob(str(importlib_resources.files("tutorpod_autoscaling") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
