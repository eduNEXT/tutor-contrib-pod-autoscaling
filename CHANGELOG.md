# CHANGELOG


## v18.0.1 (2024-10-22)

### Bug Fixes

* fix: adjust default values for requests and scaling targets (#17)

An scaling target over 100% can be unreliable in case of CPU starvation
caused by other workloads. Instead we should to keep the value <= 100
and adjust requests accordingly.

This also increases the LMS and CMS memory requests to 800Mi considering
that each uWSGI worker consumes around 350Mi and tutor defaults to two
of them. ([`eabe761`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/eabe761ae14100763839fd7563b3fd987ccf2b8e))


## v18.0.0 (2024-06-20)

### Unknown

* Redwood upgrade (#12)

* feat: add AUTOSCALING_APPS filter

refactor: move all hpa/vpa settings to the filter

chore: applying fixes to make the plugin work properly

fix: comments with MFE references

fix: variable name

chore: use typed dict

chore: only return enabled hpa/vpa

chore: use tutor's lru_cache

fix: don't call lru_cache

chore: bump version to v17.1.0

* fix: tests

* feat: add support for POD_AUTOSCALING_EXTRA_SERVICES setting

* chore: enriching docs and adding small template fix

* feat: upgrade to Redwood

* fix: docs

---------

Co-authored-by: Cristhian Garcia <crisgarta8@gmail.com> ([`8ce5444`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/8ce54445375d6ff2d6b8bf2e4f467b005af7b6a7))


## v17.0.1 (2024-06-13)

### Bug Fixes

* fix: remove cms_worker values in cms deployment (#13) ([`51b48dc`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/51b48dc66686fb3ec1fd60937c02a171a0fc9be0))

* fix: remove pkg_resources for compatibility with python 3.12 (#9)

* fix: remove pkg_resources for compatibility with python 3.12

* feat: running github actions test

* fix: tests

* chore: add type annotations

---------

Co-authored-by: jfavellar90 <jhony.avella@edunext.co> ([`d2d330f`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/d2d330f6801885694b4e374185ee8fbf40d09d7a))

### Unknown

* v17.0.1 ([`8cba77a`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/8cba77aa879a490bac4050dd09c86df30d1a91c4))


## v17.0.0 (2023-12-14)

### Unknown

* Upgrade to Quince (#6)

* feat: upgrade to Quince

* chore: mark compatibility with python 3.12 ([`43ebfcc`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/43ebfcc3aff31746d8f577d399adff5499b43e31))


## v16.1.0 (2023-10-25)

### Bug Fixes

* fix: better overrides and K8S resources Syntax
This change fixes an issue in the plugin where all HPA resources are disabled. This makes the Kustomization build to fail ([`16505a7`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/16505a751e6cc5700637bc90511ce3eac4d7c134))

### Unknown

* v16.1.0 ([`009d498`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/009d498bbdaa676dbfa27f04faa7dd97ff7c8607))


## v16.0.1 (2023-09-18)

### Bug Fixes

* fix: tutor versioning (#4)

* fix: tutor palm version set for required packages.

each tutor plugin with numbered tags, should have tutor version installed as a requirement and the tags should match.

* chore: minor typo fixed.

* chore: Remove commented out code and improve styling ([`ad04286`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/ad04286f27c10a565175636b5163167d8dba8d33))

### Unknown

* v16.0.1 ([`d360da9`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/d360da9ff3988643ef1d0c28935c915512be68b2))


## v16.0.0 (2023-07-19)

### Unknown

* Upgrade to Palm (#3)

* fix: removing deprecated Tutor variables

* feat: bumping version to match tutor version

* chore: dropping Python 3.7 support ([`081b35c`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/081b35c14078f018c432df9f14478edc53a431d7))


## v15.0.1 (2023-07-19)

### Features

* feat: bumping version to match tutor version ([`c721a36`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/c721a36fe16f00fed6d25f67275d68be467bc606))


## v15.0.0 (2023-03-07)

### Bug Fixes

* fix: template spaces ([`1d6fd55`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/1d6fd55f333bee9df5b56a6d3bb08f52c34e7b31))

### Features

* feat: updating Readme ([`d98d228`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/d98d22862a1863c9f4c467d479e74e52f0987d92))

* feat: adding patches to support HPA and VPA resources extension ([`e316ed1`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/e316ed109e6ac2fa789f3d6c5f44ca2d040c37ef))

* feat: changing the variable names to distinguish between HPA y VPA ([`010c00e`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/010c00e5931047d6b50e6012b6fd4a13c714b4ae))

* feat: adding VPA support ([`8f0a804`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/8f0a80461e39792c55c4108aefc5fd5888d66e1e))

* feat: first plugin approach supporting HPA ([`f062998`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/f06299849bbfec7ce09a68c51f48885bae34d2b0))

* feat: plugin structure ([`ed761f8`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/ed761f85623ad3a4b55c0c7dda54f9f09c65b7b8))

### Unknown

* Initial commit ([`f824301`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/f8243015459fd45af7249198910ebafd47b3d226))
