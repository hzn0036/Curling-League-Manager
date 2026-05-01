class IdentifiedObject:
    """An abstract base class that provides an object id."""

    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid

    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        return self.oid == other.oid

    def __hash__(self):
        return hash(self.oid)