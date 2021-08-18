from model.project import Project
import string
import random


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def random_status():
    statuses = ["development", "release", "stable", "obsolete"]
    i = random.randrange(len(statuses))
    return statuses[i]


def random_view():
    statuses = ["public", "private"]
    i = random.randrange(len(statuses))
    return statuses[i]


testdata = [
    Project(name=random_string("pr-name", 10), status=random_status(), enabled='', view_status=random_view(),
            description=random_string("Description", 20)) for i in range(2)
]
