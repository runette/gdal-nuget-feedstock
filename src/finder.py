from mamba import repoquery
from pathlib import Path
import os

libraries = []


# iterate through dependencies and get all libraries referenced
def get_deps(d):
    print(d.get("name"))
    libraries.append(d.get("name"))
    sub_depspec = repoquery.depends(d.get('name'))
    for sub_dep in sub_depspec.get("result").get("pkgs"):
        print(sub_dep)
        get_deps(sub_dep)

# parse the conda environment and get dependency list for libgdal

depspec = repoquery.depends("libgdal")
deps = depspec.get("result").get("pkgs")

for dep in deps:
    get_deps(dep)

print(libraries)