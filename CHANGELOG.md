# CHANGELOG

<!--
All enhancements and changes will be documented in this file.  It adheres to
the structure of http://keepachangelog.com/ ,

This project adheres to Semantic Versioning (http://semver.org/).
-->

## Unreleased

See the fragment files in the [changelog.d/ directory](./changelog.d).

<!-- scriv-insert-here -->

<a id='changelog-21.0.0'></a>
## 21.0.0 — 2026-01-28

### Added

- Support for the Ulmo release

<a id='changelog-20.0.0'></a>
## v20.0.0 (2025-07-02)

### Added

- Support for the Teak release.

## v19.0.0 (2024-12-17)

### Features

- Sumac release ([#18](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/pull/18),
  [`d7dfa58`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/d7dfa58219d55aa2c3fe797bdd412be24ca2698c))


## v18.0.1 (2024-10-22)

### Bug Fixes

- Adjust default values for requests and scaling targets
  ([#17](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/pull/17),
  [`eabe761`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/eabe761ae14100763839fd7563b3fd987ccf2b8e))

An scaling target over 100% can be unreliable in case of CPU starvation caused by other workloads.
  Instead we should to keep the value <= 100 and adjust requests accordingly.

This also increases the LMS and CMS memory requests to 800Mi considering that each uWSGI worker
  consumes around 350Mi and tutor defaults to two of them.

### Chores

- **release**: Preparing 18.0.1
  ([`808149b`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/808149b2515417b90aee800082258bca1cb9de6b))


## v18.0.0 (2024-06-20)


## v17.0.1 (2024-06-13)

### Bug Fixes

- Remove cms_worker values in cms deployment
  ([#13](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/pull/13),
  [`51b48dc`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/51b48dc66686fb3ec1fd60937c02a171a0fc9be0))

- Remove pkg_resources for compatibility with python 3.12
  ([#9](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/pull/9),
  [`d2d330f`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/d2d330f6801885694b4e374185ee8fbf40d09d7a))

* fix: remove pkg_resources for compatibility with python 3.12

* feat: running github actions test

* fix: tests

* chore: add type annotations

---------

Co-authored-by: jfavellar90 <jhony.avella@edunext.co>


## v17.0.0 (2023-12-14)


## v16.1.0 (2023-10-25)

### Bug Fixes

- Better overrides and K8S resources Syntax
  ([`16505a7`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/16505a751e6cc5700637bc90511ce3eac4d7c134))


## v16.0.1 (2023-09-18)

### Bug Fixes

- Tutor versioning ([#4](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/pull/4),
  [`ad04286`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/ad04286f27c10a565175636b5163167d8dba8d33))

* fix: tutor palm version set for required packages.

each tutor plugin with numbered tags, should have tutor version installed as a requirement and the
  tags should match.

* chore: minor typo fixed.

* chore: Remove commented out code and improve styling


## v16.0.0 (2023-07-19)


## v15.0.1 (2023-07-19)

### Features

- Bumping version to match tutor version
  ([`c721a36`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/c721a36fe16f00fed6d25f67275d68be467bc606))


## v15.0.0 (2023-03-07)

### Bug Fixes

- Template spaces
  ([`1d6fd55`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/1d6fd55f333bee9df5b56a6d3bb08f52c34e7b31))

### Features

- Adding patches to support HPA and VPA resources extension
  ([`e316ed1`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/e316ed109e6ac2fa789f3d6c5f44ca2d040c37ef))

- Adding VPA support
  ([`8f0a804`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/8f0a80461e39792c55c4108aefc5fd5888d66e1e))

- Changing the variable names to distinguish between HPA y VPA
  ([`010c00e`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/010c00e5931047d6b50e6012b6fd4a13c714b4ae))

- First plugin approach supporting HPA
  ([`f062998`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/f06299849bbfec7ce09a68c51f48885bae34d2b0))

- Plugin structure
  ([`ed761f8`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/ed761f85623ad3a4b55c0c7dda54f9f09c65b7b8))

- Updating Readme
  ([`d98d228`](https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/commit/d98d22862a1863c9f4c467d479e74e52f0987d92))
