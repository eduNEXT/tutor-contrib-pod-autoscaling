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

- ``POD_AUTOSCALING_LMS_HPA`` (default: ``true``): Enables/disables HPA for LMS deployment.
- ``POD_AUTOSCALING_LMS_AVG_CPU`` (default: ``300``): defines the CPU consumption to keep in the HPA, expressed as a percentage.
- ``POD_AUTOSCALING_LMS_AVG_MEMORY`` (default: ``""``): defines the memory consumption to keep in the HPA, expressed as a memory value (e.g. "750Mi"). **For now, we suggest keeping this value empty.**
- ``POD_AUTOSCALING_LMS_CPU_LIMIT`` (default: ``1``): sets the maximum CPU consumption of a LMS pod.
- ``POD_AUTOSCALING_LMS_CPU_REQUEST`` (default: ``0.25``): sets the minimum CPU reserved for a new LMS pod.
- ``POD_AUTOSCALING_LMS_MAX_REPLICAS`` (default: ``4``): the HPA will scale up to this maximum number of replicas
- ``POD_AUTOSCALING_LMS_MEMORY_LIMIT`` (default: ``"1400Mi"``): sets the maximum memory consumption of a LMS pod.
- ``POD_AUTOSCALING_LMS_MEMORY_REQUEST`` (default: ``"350Mi"``): sets the minimum memory reserved for a new LMS pod.
- ``POD_AUTOSCALING_LMS_MIN_REPLICAS`` (default: ``1``): The HPA will not scale below this minimum number of replicas.

- ``POD_AUTOSCALING_LMS_WORKER_HPA`` (default: ``true``)
- ``POD_AUTOSCALING_LMS_WORKER_AVG_CPU`` (default: ``400``)
- ``POD_AUTOSCALING_LMS_WORKER_AVG_MEMORY`` (default: ``""``)
- ``POD_AUTOSCALING_LMS_WORKER_CPU_LIMIT`` (default: ``1``)
- ``POD_AUTOSCALING_LMS_WORKER_CPU_REQUEST`` (default: ``0.175``)
- ``POD_AUTOSCALING_LMS_WORKER_MAX_REPLICAS`` (default: ``6``)
- ``POD_AUTOSCALING_LMS_WORKER_MEMORY_LIMIT`` (default: ``"3000Mi"``)
- ``POD_AUTOSCALING_LMS_WORKER_MEMORY_REQUEST`` (default: ``"750Mi"``)
- ``POD_AUTOSCALING_LMS_WORKER_MIN_REPLICAS`` (default: ``1``)

To configure CMS variables, just change "LMS" in the variables above by "CMS" (CMS variables have the same defaults).

VPA
^^^

VPA components can be enabled/disabled for the **LMS**, **CMS**, **LMS_WORKER** and **CMS_WORKER** deployments. The VPA's are configured with the **UpdateMode** mode disabled, so they don't modify Pod resources automatically. Instead, they work as a dry-run, setting the recommended resources for the deployments in every VPA object.

- ``POD_AUTOSCALING_LMS_VPA`` (default: ``false``)
- ``POD_AUTOSCALING_LMS_WORKER_VPA`` (default: ``false``)
- ``POD_AUTOSCALING_CMS_VPA`` (default: ``false``)
- ``POD_AUTOSCALING_CMS_WORKER_VPA`` (default: ``false``)

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
