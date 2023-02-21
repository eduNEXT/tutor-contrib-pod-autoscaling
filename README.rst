Pod-autoscaling plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This plugin enables Pod-Autoscaling strategies for instances deployed with Tutor. The strategies are:

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

Usage
-----

::

    tutor plugins enable pod-autoscaling


License
-------

This software is licensed under the terms of the AGPLv3.
