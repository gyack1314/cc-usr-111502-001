"""不可变提交图及祖先访问。"""
from copy import deepcopy
import hashlib
import json

def digest(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()

class Graph:
    def __init__(self):
        self._nodes = {}

    def append(self, tables, parents=()):
        parents = tuple(parents)
        if len(parents) > 1:
            raise ValueError('现有发布入口仅接受单父提交')
        if any(parent not in self._nodes for parent in parents):
            raise ValueError('父提交不存在')
        for name, table in tables.items():
            ids = [row['row_id'] for row in table['rows']]
            if len(ids) != len(set(ids)):
                raise ValueError('表内行身份重复')
            fields = table['fields']
            if len(set(fields.values())) != len(fields):
                raise ValueError('字段身份重复')
        node = {'parents': list(parents), 'tables': deepcopy(tables)}
        token = digest(node)
        self._nodes[token] = node
        return token

    def get(self, token):
        node = deepcopy(self._nodes[token])
        if digest(node) != token:
            raise ValueError('提交摘要不符')
        return node

    def ancestors(self, token):
        found = set()
        pending = [token]
        while pending:
            current = pending.pop()
            if current not in found:
                found.add(current)
                pending.extend(self.get(current)['parents'])
        return frozenset(found)
