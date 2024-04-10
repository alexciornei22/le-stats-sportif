import csv

DATA_VALUE_KEY = 'Data_Value'
QUESTION_KEY = 'Question'
STATE_KEY = 'LocationDesc'
STRATIFICATION_KEY = 'Stratification1'
STRATIFICATION_CATEGORY_KEY = 'StratificationCategory1'


class DataIngestor:
    def __init__(self, csv_path: str):
        self.data = []
        with open(csv_path) as data_file:
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

    def get_data_for_question(self, question):
        return list(filter(lambda item: item.question == question, self.data))

    def get_data_for_question_state(self, question, state):
        return list(filter(lambda item: item.question == question and item.state == state, self.data))

    def get_states(self):
        return set(map(lambda item: item.state, self.data))


class DataEntry:
    def __init__(self, data_value, question, state, strat_category, strat):
        self.data_value = float(data_value)
        self.question = question
        self.state = state
        self.strat_category = strat_category
        self.strat = strat
