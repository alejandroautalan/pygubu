from types import SimpleNamespace


class walkns:
    """Return namespace path as string."""

    def __init__(self, node: SimpleNamespace, prefix=None):
        self.node = node
        node_ns = getattr(node, "_name")
        self.prefix = f"{node_ns}" if prefix is None else f"{prefix}.{node_ns}"

    def __getattr__(self, key):
        value = getattr(self.node, key)
        if isinstance(value, SimpleNamespace):
            value = walkns(value, self.prefix)
        else:
            value = f"{self.prefix}.{key}"
        return value


SN = SimpleNamespace
