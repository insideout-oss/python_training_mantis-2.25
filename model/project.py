from sys import maxsize


class Project:

    def __init__(self, name=None, status=None, enabled=None, view_status=None, description=None, id=None):
        self.name = name
        # 70 obsolete, 10 development, 30 release, 50 stable
        self.status = status
        self.enabled = enabled
        self.view_status = view_status
        self.description = description
        self.id = id

    def __repr__(self):
        return "%s:%s:%s:%s" % (self.id, self.name, self.status, self.description)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
