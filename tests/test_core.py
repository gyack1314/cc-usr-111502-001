import unittest
from branchlake.graph import Graph
from branchlake.catalog import Catalog
from branchlake.reader import Reader

class CoreTests(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.tables = {'visits': {'fields': {'venue': 1, 'amount': 2}, 'rows': [{'row_id': 'r1', '1': '运河', '2': 80}]}}
        self.first = self.graph.append(self.tables)

    def test_fixed_reader_and_defensive_copy(self):
        reader = Reader(self.graph, self.first)
        self.tables['visits']['rows'][0]['2'] = 90
        second = self.graph.append(self.tables, [self.first])
        self.assertEqual(list(reader.rows('visits'))[0]['amount'], 80)
        self.assertEqual(list(Reader(self.graph, second).rows('visits'))[0]['amount'], 90)

    def test_reference_aba_generation(self):
        cat = Catalog(self.graph)
        cat.create('main', self.first)
        old = cat.head('main')
        second = self.graph.append(self.tables, [self.first])
        cat.advance('main', old, second)
        with self.assertRaisesRegex(ValueError, '代号'):
            cat.advance('main', old, second)

    def test_bad_graph_or_duplicate_identity(self):
        with self.assertRaises(ValueError):
            self.graph.append(self.tables, ['missing'])
        self.tables['visits']['rows'] *= 2
        with self.assertRaises(ValueError):
            self.graph.append(self.tables)

    def test_ancestry(self):
        child = self.graph.append(self.tables, [self.first])
        self.assertEqual(self.graph.ancestors(child), {self.first, child})
