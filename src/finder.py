from mamba import repoquery
from pathlib import Path
import os
import json

libraries = []
dlls = []
conda_path = Path(os.environ.get("CONDA_PREFIX")).joinpath('conda-meta')
file_list = os.listdir(conda_path)
exclude = ["vc", "vs2015_runtime"]


# iterate through dependencies and get all libraries referenced
def get_deps(d):
    dep_name = d.get("name")
    print(dep_name)
    libraries.append(dep_name)
    sub_depspec = repoquery.depends(dep_name)
    for sub_dep in sub_depspec.get("result").get("pkgs"):
        if sub_dep.get('name') != dep_name and not sub_dep.get('name') in exclude and not sub_dep.get('name') in libraries :
            get_deps(sub_dep)

# parse the conda environment and get dependency list for libgdal

depspec = repoquery.depends("libgdal")
deps = depspec.get("result").get("pkgs")

for dep in deps:
    if dep.get('name') != "libgdal":
        print(dep)
        get_deps(dep)

#for each package - get dlls

for lib in libraries:
    file = [ file for file in file_list if lib in file]
    file_handle = conda_path.joinpath(file[0])
    with open(file_handle) as f:
        spec =  json.load(f)
        dlls += ([file for file in spec.get("files") if ".dll" in file and not "api-ms" in file])

print([conda_path.joinpath(file) for file in set(dlls)])