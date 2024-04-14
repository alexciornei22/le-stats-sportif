import unittest

from app import DataIngestor


class TestDataIngestor(unittest.TestCase):
    def setUp(self):
        self.data_ingestor = DataIngestor('./nutrition_activity_obesity_usa_subset.csv')

    def test_data_size(self):
        self.assertEqual(len(self.data_ingestor.data), 18650, 'Data size incorrect')

    def test_data_for_question(self):
        di = self.data_ingestor
        self.assertIsNotNone(
            di.data_for_question('Percent of adults aged 18 years and older who have obesity'),
            'Data for question failed'
        )

    def test_get_states_nr(self):
        self.assertGreater(len(self.data_ingestor.get_states()), 50, 'Incorrect state number')

    def test_states_averages_for_question(self):
        means = self.data_ingestor.states_averages_for_question('Percent of adults aged 18 years and older who have obesity')
        for state, mean in means.items():
            self.assertGreater(mean, 0.0, 'Incorrect average')
            self.assertTrue(state in self.data_ingestor.get_states(), 'Invalid state name')


if __name__ == '__main__':
    unittest.main()
