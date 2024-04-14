"""
Import app data from a csv file

Classes:
    DataIngestor: takes a csv file, ingests it and offers methods to get the data
"""

import csv

DATA_VALUE_KEY = 'Data_Value'
QUESTION_KEY = 'Question'
STATE_KEY = 'LocationDesc'
STRATIFICATION_KEY = 'Stratification1'
STRATIFICATION_CATEGORY_KEY = 'StratificationCategory1'


class DataIngestor:
    """Ingests data from csv file"""
    def __init__(self, csv_path: str):
        self.data = []
        with open(csv_path, 'r', encoding='utf-8') as data_file:
            csv_reader = csv.DictReader(data_file)
            for row in csv_reader:
                self.data.append(
                    DataEntry(
                        row[DATA_VALUE_KEY],
                        row[QUESTION_KEY],
                        row[STATE_KEY],
                        row[STRATIFICATION_CATEGORY_KEY],
                        row[STRATIFICATION_KEY])
                )

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def data_for_question(self, question):
        """
        Get all data entries for a given question
        :param question: searched question
        :return: list of DataEntry objects
        """
        return list(filter(lambda item: item.question == question, self.data))

    def data_for_question_in_state(self, question, state):
        """
        Get all data entries for a given question in a state
        :param question: searched question
        :param state: state to search in
        :return: list of DataEntry objects
        """
        return list(filter(lambda item: item.question == question and item.state == state, self.data))

    def states_averages_for_question(self, question):
        """
        Get an average of all entries for a given question for each state in the DataIngestor
        that has an entry for that question
        :param question: searched question
        :return: a dictionary with state names as keys and averages as values
        """
        data = self.data_for_question(question)
        states = self.get_states()

        values = {state: 0 for state in states}
        nr_entries = values.copy()

        for entry in data:
            state = entry.state
            values[state] += entry.data_value
            nr_entries[state] += 1

        means = {state: values[state] / nr_entries[state] for state in states if nr_entries[state] > 0}
        return means

    def get_states(self):
        """Get a list of all states in the DataIngestor"""
        return set(map(lambda item: item.state, self.data))


class DataEntry:
    """Holds information for a single entry from the dataset"""
    def __init__(self, data_value, question, state, strat_category, strat):
        self.data_value = float(data_value)
        self.question = question
        self.state = state
        self.strat_category = strat_category
        self.strat = strat
