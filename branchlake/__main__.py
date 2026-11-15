import json
from pathlib import Path
from .graph import Graph
from .catalog import Catalog
from .reader import Reader
data = json.loads(Path('data/sample.json').read_text())
graph = Graph()
token = graph.append(data['tables'])
catalog = Catalog(graph)
catalog.create('main', token)
print(json.dumps({'head': catalog.head('main'), 'rows': list(Reader(graph, token).rows('visits'))}, ensure_ascii=False))
