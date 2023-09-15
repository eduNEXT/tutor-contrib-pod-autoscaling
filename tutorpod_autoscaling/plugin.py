from __future__ import annotations

import os
import os.path
from glob import glob

import click
import pkg_resources
from tutor import hooks

from .__about__ import __version__

################# Autoscaling
# Here comes the default common setttings for the autoscaling. Some resources
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

########################################
# CONFIGURATION
########################################

config = {
    # Add here your new settings
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
        "CMS_WORKER_AVG_MEMORY": "", # Disable memory-based autoscaling
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
        "LMS_WORKER_AVG_MEMORY": "", # Disable memory-based autoscaling
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
        # Services to autoscale
        "SERVICES": {
            "lms": {
                "hpa": {
                    "enabled": "{{ POD_AUTOSCALING_LMS_HPA }}",
                    "avg_cpu": "{{ POD_AUTOSCALING_LMS_AVG_CPU }}",
                    "avg_memory": "{{ POD_AUTOSCALING_LMS_AVG_MEMORY }}",
                    "cpu_limit": "{{ POD_AUTOSCALING_LMS_CPU_LIMIT }}",
                    "cpu_request": "{{ POD_AUTOSCALING_LMS_CPU_REQUEST }}",
                    "max_replicas": "{{ POD_AUTOSCALING_LMS_MAX_REPLICAS }}",
                    "memory_limit": "{{ POD_AUTOSCALING_LMS_MEMORY_LIMIT }}",
                    "memory_request": "{{ POD_AUTOSCALING_LMS_MEMORY_REQUEST }}",
                    "min_replicas": "{{ POD_AUTOSCALING_LMS_MIN_REPLICAS }}",
                },
                "vpa": {
                    "enabled": "{{ POD_AUTOSCALING_LMS_VPA }}",
                },
            },
            "lms-worker": {
                "hpa": {
                    "enabled": "{{ POD_AUTOSCALING_LMS_WORKER_HPA }}",
                    "avg_cpu": "{{ POD_AUTOSCALING_LMS_WORKER_AVG_CPU }}",
                    "avg_memory": "{{ POD_AUTOSCALING_LMS_WORKER_AVG_MEMORY }}",
                    "cpu_limit": "{{ POD_AUTOSCALING_LMS_WORKER_CPU_LIMIT }}",
                    "cpu_request": "{{ POD_AUTOSCALING_LMS_WORKER_CPU_REQUEST }}",
                    "max_replicas": "{{ POD_AUTOSCALING_LMS_WORKER_MAX_REPLICAS }}",
                    "memory_limit": "{{ POD_AUTOSCALING_LMS_WORKER_MEMORY_LIMIT }}",
                    "memory_request": "{{ POD_AUTOSCALING_LMS_WORKER_MEMORY_REQUEST }}",
                    "min_replicas": "{{ POD_AUTOSCALING_LMS_WORKER_MIN_REPLICAS }}",
                },
                "vpa": {
                    "enabled": "{{ POD_AUTOSCALING_LMS_WORKER_VPA }}",
                },
            },
            "cms": {
                "hpa": {
                    "enabled": "{{ POD_AUTOSCALING_CMS_HPA }}",
                    "avg_cpu": "{{ POD_AUTOSCALING_CMS_AVG_CPU }}",
                    "avg_memory": "{{ POD_AUTOSCALING_CMS_AVG_MEMORY }}",
                    "cpu_limit": "{{ POD_AUTOSCALING_CMS_CPU_LIMIT }}",
                    "cpu_request": "{{ POD_AUTOSCALING_CMS_CPU_REQUEST }}",
                    "max_replicas": "{{ POD_AUTOSCALING_CMS_MAX_REPLICAS }}",
                    "memory_limit": "{{ POD_AUTOSCALING_CMS_MEMORY_LIMIT }}",
                    "memory_request": "{{ POD_AUTOSCALING_CMS_MEMORY_REQUEST }}",
                    "min_replicas": "{{ POD_AUTOSCALING_CMS_MIN_REPLICAS }}",
                },
                "vpa": {
                    "enabled": "{{ POD_AUTOSCALING_CMS_VPA }}",
                },
            },
            "cms-worker": {
                "hpa": {
                    "enabled": "{{ POD_AUTOSCALING_CMS_WORKER_HPA }}",
                    "avg_cpu": "{{ POD_AUTOSCALING_CMS_WORKER_AVG_CPU }}",
                    "avg_memory": "{{ POD_AUTOSCALING_CMS_WORKER_AVG_MEMORY }}",
                    "cpu_limit": "{{ POD_AUTOSCALING_CMS_WORKER_CPU_LIMIT }}",
                    "cpu_request": "{{ POD_AUTOSCALING_CMS_WORKER_CPU_REQUEST }}",
                    "max_replicas": "{{ POD_AUTOSCALING_CMS_WORKER_MAX_REPLICAS }}",
                    "memory_limit": "{{ POD_AUTOSCALING_CMS_WORKER_MEMORY_LIMIT }}",
                    "memory_request": "{{ POD_AUTOSCALING_CMS_WORKER_MEMORY_REQUEST }}",
                    "min_replicas": "{{ POD_AUTOSCALING_CMS_WORKER_MIN_REPLICAS }}",
                },
                "vpa": {
                    "enabled": "{{ POD_AUTOSCALING_CMS_WORKER_VPA }}",
                },
            },
        }
    },
    # Add here settings that don't have a reasonable default for all users. For
    # instance: passwords, secret keys, etc.
    "unique": {},
    # Danger zone! Add here values to override settings from Tutor core or other plugins.
    "overrides": {},
}

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"POD_AUTOSCALING_{key}", value)
        for key, value in config["defaults"].items()
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"POD_AUTOSCALING_{key}", value)
        for key, value in config["unique"].items()
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))


########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# tutorpod_autoscaling/templates/pod-autoscaling/jobs/init/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...]]] = [
    # For example, to add LMS initialization steps, you could add the script template at:
    # tutorpod_autoscaling/templates/pod-autoscaling/jobs/init/lms.sh
    # And then add the line:
    ### ("lms", ("pod-autoscaling", "jobs", "init", "lms.sh")),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path in MY_INIT_TASKS:
    full_path: str = pkg_resources.resource_filename(
        "tutorpod_autoscaling", os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        # To build `myimage` with `tutor images build myimage`,
        # you would add a Dockerfile to templates/pod-autoscaling/build/myimage,
        # and then write:
        ### (
        ###     "myimage",
        ###     ("plugins", "pod-autoscaling", "build", "myimage"),
        ###     "docker.io/myimage:{{ POD_AUTOSCALING_VERSION }}",
        ###     (),
        ### ),
    ]
)


# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        # To pull `myimage` with `tutor images pull myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ POD_AUTOSCALING_VERSION }}",
        ### ),
    ]
)


# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        # To push `myimage` with `tutor images push myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ POD_AUTOSCALING_VERSION }}",
        ### ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutorpod_autoscaling", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorpod_autoscaling/templates/pod-autoscaling/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/pod-autoscaling/build``.
    [
        ("pod-autoscaling/build", "plugins"),
        ("pod-autoscaling/apps", "plugins"),
        ("pod-autoscaling/k8s", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorpod_autoscaling/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorpod_autoscaling", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################

# A job is a set of tasks, each of which run inside a certain container.
# Jobs are invoked using the `do` command, for example: `tutor local do importdemocourse`.
# A few jobs are built in to Tutor, such as `init` and `createuser`.
# You can also add your own custom jobs:

# To add a custom job, define a Click command that returns a list of tasks,
# where each task is a pair in the form ("<service>", "<shell_command>").
# For example:
### @click.command()
### @click.option("-n", "--name", default="plugin developer")
### def say_hi(name: str) -> list[tuple[str, str]]:
###     """
###     An example job that just prints 'hello' from within both LMS and CMS.
###     """
###     return [
###         ("lms", f"echo 'Hello from LMS, {name}!'"),
###         ("cms", f"echo 'Hello from CMS, {name}!'"),
###     ]


# Then, add the command function to CLI_DO_COMMANDS:
## hooks.Filters.CLI_DO_COMMANDS.add_item(say_hi)

# Now, you can run your job like this:
#   $ tutor local do say-hi --name="Jhony Avella"


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def pod-autoscaling() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(pod-autoscaling)


# Then, you would add subcommands directly to the Click group, for example:


### @pod-autoscaling.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor pod-autoscaling example-command
