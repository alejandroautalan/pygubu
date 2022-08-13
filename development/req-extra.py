import io
import re
from collections import defaultdict
from pprint import pp

extra_requirements = """
# FORMAT
# Put your extra requirements here in the following format
#
# package[version_required]: tag1, tag2, ...

ttkwidgets: ttkwidgets
tksheet: tksheet
tkinterweb: tkinterweb
tkintertable: tkintertable
tkcalendar: tkcalendar
AwesomeTkinter: awesometkinter
"""


def get_extra_requires(add_all=True):
    ifile = io.StringIO(extra_requirements)
    with ifile as fp:
        extra_deps = defaultdict(set)
        for k in fp:
            if k.strip() and not k.startswith("#"):
                tags = set()
                if ":" in k:
                    k, v = k.split(":")
                    tags.update(vv.strip() for vv in v.split(","))
                # tags.add(re.split("[<=>]", k)[0])
                for t in tags:
                    extra_deps[t].add(k)
        # add tag `all` at the end
        if add_all:
            extra_deps["all"] = set(vv for v in extra_deps.values() for vv in v)

    return extra_deps


if __name__ == "__main__":
    requires = get_extra_requires()
    for key, dep in requires.items():
        print(f"{key} = {list(dep)}")
