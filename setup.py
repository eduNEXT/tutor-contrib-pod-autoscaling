import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "tutorpod_autoscaling", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-contrib-pod-autoscaling",
    version=ABOUT["__version__"],
    url="https://github.com/eduNEXT/tutor-contrib-pod-autoscaling",
    project_urls={
        "Code": "https://github.com/eduNEXT/tutor-contrib-pod-autoscaling",
        "Issue tracker": "https://github.com/eduNEXT/tutor-contrib-pod-autoscaling/issues",
    },
    license="AGPLv3",
    author="Jhony Avella",
    description="pod-autoscaling plugin for Tutor",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["tutor>=17.0.0,<18.0.0"],
    entry_points={
        "tutor.plugin.v1": [
            "pod-autoscaling = tutorpod_autoscaling.plugin"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
