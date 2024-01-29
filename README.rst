Pod-autoscaling plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This plugin enables Pod-Autoscaling strategies for instances deployed **in Kubernetes** with Tutor. Inspired by the implementation of HPA from https://gitlab.com/opencraft/dev/tutor-contrib-grove (thanks @gabor-boros) The strategies offered by the plugin are:

1. `HPA <https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/>`_ (Horizontal Pod Autoscaler): this mechanism adds or removes pods based on a defined metric **threshold** (For instance CPU or memory consumption).
2. `VPA <https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler>`_ (Vertical Pod Autoscaler): this strategy aims to stabilize the consumption and resources of every pod, so they're kept between `limits and requests <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits>`_ that were specified in the initial pod configuration.

Requirements
------------

1. To use HPA, the installation of `metrics-server <https://github.com/kubernetes-sigs/metrics-server>`_ is required.
2. To use VPA, the installation of `Vertical Pod Autoscaler <https://github.com/cowboysysop/charts/tree/master/charts/vertical-pod-autoscaler>`_ is required.

Installation
------------

::

    pip install git+https://github.com/eduNEXT/tutor-contrib-pod-autoscaling

Configuration
-------------

HPA
^^^

This plugin allows to configure HPA's for the **LMS**, **CMS**, **LMS_WORKER** and **CMS_WORKER** deployments based on **CPU** and **MEMORY** metrics

VPA
^^^

VPA components can be enabled/disabled for the **LMS**, **CMS**, **LMS_WORKER** and **CMS_WORKER** deployments. The VPA's are configured with the **UpdateMode** mode disabled, so they don't modify Pod resources automatically. Instead, they work as a dry-run, setting the recommended resources for the deployments in every VPA object.

HPA - VPA Management
^^^^^^^^^^^^^^^^^^^^

Other plugin developers can take advantage of this plugin to configure they HPA/HPA settings. To declare a new HPA, create a Tutor plugin
and add your autoscaling configuration to the ``tutorpod_autoscaling.hooks.AUTOSCALING_CONFIG`` filter. For example::

    from tutorpod_autoscaling import AUTOSCALING_CONFIG

    @AUTOSCALING_CONFIG.add()
    def _add_my_autoscaling(autoscaling_config):
        autoscaling_config["service"] = {
            "enable_hpa": True,
            "memory_request": "300Mi",
            "cpu_request": 0.25,
            "memory_limit": "1200Mi",
            "cpu_limit": 1,
            "min_replicas": 1,
            "max_replicas": 10,
            "avg_cpu": 300,
            "avg_memory": "",
            "enable_vpa": True,
        }
        return autoscaling_config

The following services are pre-configured in the plugin:

- lms
- cms
- lms-worker
- cms-worker

You can update the configuration for any of these services by updating the autoscaling_config dictionary in the filter function.


**Notes** to take in mind when using this plugin:

- The default values for HPA in this plugin can work OK for small installations. However, according to your use case, you'll need to tune the values in order to get the best performance.
- The VPA entities are configured to just display suggestions on the right amount of resources to allocate for every workload, and not to go directly and modify the resources allocated for a workload. This is because using HPA and VPA in **automatic UpdateMode** is **not recommended**. The best practice is to get the suggestions from the VPA and based on those suggestions, adjust the HPA values for the workloads in order to get the most value out of these autoscaling tools.

Usage
-----

::

    tutor plugins enable pod-autoscaling


License
-------

This software is licensed under the terms of the AGPLv3.
