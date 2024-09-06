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

This plugin implements a `filter <https://docs.tutor.edly.io/reference/api/hooks/filters.html>`_ called **AUTOSCALING_CONFIG** (``tutorpod_autoscaling.hooks.AUTOSCALING_CONFIG``) which allow to add/modify pod autoscaling configuration for different OpenedX services. The plugin by itself uses the **AUTOSCALING_CONFIG** filter to add default autoscaling configuration (HPA and VPA) for the **LMS**, **CMS**, **LMS_WORKER** and **CMS_WORKER** deployments based on **CPU** and **MEMORY** metrics (check the ``CORE_AUTOSCALING_CONFIG`` variable in the ``plugin.py`` file).

Adding/changing HPA/VPA configuration for OpenedX services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Operators can take advantage of this plugin to configure their HPA/VPA settings for different services. There are 2 mechanisms to do so:

1. Create a Tutor plugin and add your HPA/VPA configuration to the ``tutorpod_autoscaling.hooks.AUTOSCALING_CONFIG`` filter. For instance, to add HPA support to the forum deployment:

.. code-block:: python

    from tutorpod_autoscaling.hooks import AUTOSCALING_CONFIG

    @AUTOSCALING_CONFIG.add()
    def _add_my_autoscaling(autoscaling_config):
        autoscaling_config["forum"] = {
            "enable_hpa": True,
            "memory_request": "300Mi",
            "cpu_request": 0.25,
            "memory_limit": "1200Mi",
            "cpu_limit": 1,
            "min_replicas": 1,
            "max_replicas": 10,
            "avg_cpu": 300,
            "avg_memory": "",
            "enable_vpa": False,
        }
        return autoscaling_config

.. note::
    - The key used for the new autoscaling item (in this case "forum") must match the name of the deployment you are adding HPA/VPA support to.

You can also override the HPA/VPA configuration for any of the services supported by default, for instance, LMS:

.. code-block:: python

    from tutorpod_autoscaling.hooks import AUTOSCALING_CONFIG

    @AUTOSCALING_CONFIG.add()
    def _add_my_autoscaling(autoscaling_config):
        autoscaling_config["lms"] = {
            "enable_hpa": True,
            "memory_request": "1Gi",
            "cpu_request": 0.4,
            "memory_limit": "2Gi",
            "cpu_limit": 1,
            "min_replicas": 5,
            "max_replicas": 20,
            "avg_cpu": 70,
            "avg_memory": "",
            "enable_vpa": False,
        }
        return autoscaling_config

2. Set the ``POD_AUTOSCALING_EXTRA_SERVICES`` variable to extend HPA/VPA support to different services of modify default ones:

.. code-block:: yaml

    POD_AUTOSCALING_EXTRA_SERVICES:
        forum:
            enable_hpa: true
            memory_request: 300Mi
            cpu_request: 0.25
            memory_limit: 1200Mi
            cpu_limit: 1
            min_replicas: 1
            max_replicas: 10
            avg_cpu: 300
            avg_memory: ''
            enable_vpa: true
        lms:
            enable_hpa: true
            memory_request: 1Gi
            cpu_request: 0.4
            memory_limit: 2Gi
            cpu_limit: 1
            min_replicas: 5
            max_replicas: 20
            avg_cpu: 70
            avg_memory: ''
            enable_vpa: true

.. note::
    - The main reason why 2 alternatives were provided to alter the HPA/VPA configuration is to enable operators to decide what alternative better suits their needs. In some cases, reducing the plugin dependency chain is desirable, thus using the plugin setting is a good alternative.
    - The configuration defined through the **POD_AUTOSCALING_EXTRA_SERVICES** plugin setting will have precedence over the **AUTOSCALING_CONFIG** filter final configuration.
    - Using only one of the 2 mechanisms available is strongly recommended to prevent potential misconfiguration.
    - VPA components can be enabled/disabled for different deployments thanks to the ``enable_vpa`` key defined on every configured service. The VPAs are configured with the **UpdateMode** mode disabled, so they don't modify Pod resources automatically. Instead, they work as a dry-run, setting the recommended resources for the deployments in every VPA object.

3. In case you want to disable resource limits you can use the following setting: `POD_AUTOSCALING_ENABLE_RESOURCE_MANAGEMENT: false`

Migrating to Redwood version (18.x.x)
-------------------------------------

In versions prior to Redwood, the plugin used multiple configurations and a couple of patches to provide HPA/VPA support. Let's suppose you want to migrate to version 18.x.x and you have the following configuration in your ``config.yml`` for the LMS HPA/VPA support:

.. code-block:: yaml

    POD_AUTOSCALING_LMS_HPA: true
    POD_AUTOSCALING_LMS_MEMORY_REQUEST: "350Mi"
    POD_AUTOSCALING_LMS_CPU_REQUEST: 0.25
    POD_AUTOSCALING_LMS_MEMORY_LIMIT: "1400Mi"
    POD_AUTOSCALING_LMS_CPU_LIMIT: 1
    POD_AUTOSCALING_LMS_MIN_REPLICAS: 1
    POD_AUTOSCALING_LMS_MAX_REPLICAS: 4
    POD_AUTOSCALING_LMS_AVG_CPU: 300
    POD_AUTOSCALING_LMS_AVG_MEMORY: ""
    POD_AUTOSCALING_LMS_VPA: false

The equivalent configuration for the 18.x.x version using the **AUTOSCALING_CONFIG** filter would be like this:

.. code-block:: python

    from tutorpod_autoscaling.hooks import AUTOSCALING_CONFIG

    @AUTOSCALING_CONFIG.add()
    def _add_my_autoscaling(autoscaling_config):
        autoscaling_config["lms"] = {
            "enable_hpa": True,
            "memory_request": "350Mi",
            "cpu_request": 0.25,
            "memory_limit": "1400Mi",
            "cpu_limit": 1,
            "min_replicas": 1,
            "max_replicas": 4,
            "avg_cpu": 300,
            "avg_memory": "",
            "enable_vpa": False,
        }
        return autoscaling_config

The migration of other services follows the same logic.

It is important to mention that ``pod-autoscaling-hpa`` and ``pod-autoscaling-vpa`` patches were removed in the Redwood release since they are longer required in the HPA/VPA configuration model.

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
