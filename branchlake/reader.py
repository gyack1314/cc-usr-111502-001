"""固定提交的多表读句柄。"""
from copy import deepcopy

class Reader:
    def __init__(self, graph, token):
        self.token = token
        self.tables = graph.get(token)['tables']

    def rows(self, name):
        table = self.tables[name]
        names = {str(value): key for key, value in table['fields'].items()}
        for row in table['rows']:
            yield {'row_id': row['row_id'], **{names[key]: deepcopy(value) for key, value in row.items() if key != 'row_id'}}
