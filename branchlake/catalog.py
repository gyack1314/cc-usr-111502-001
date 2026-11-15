"""分支引用与代号。"""
from threading import RLock

class Catalog:
    def __init__(self, graph):
        self.graph = graph
        self._refs = {}
        self._lock = RLock()

    def create(self, name, token):
        self.graph.get(token)
        with self._lock:
            if name in self._refs:
                raise ValueError('分支已存在')
            self._refs[name] = (0, token)

    def head(self, name):
        with self._lock:
            return self._refs[name]

    def advance(self, name, expected, token):
        self.graph.get(token)
        with self._lock:
            old = self._refs[name]
            if old != tuple(expected):
                raise ValueError('分支代号冲突')
            if old[1] not in self.graph.ancestors(token):
                raise ValueError('提交不是当前头的后代')
            self._refs[name] = (old[0] + 1, token)
            return self._refs[name]
