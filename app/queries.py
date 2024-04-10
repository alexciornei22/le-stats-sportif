from functools import reduce
from app import data_ingestor


def states_mean(args):
    question, = args

    data = data_ingestor.get_data_for_question(question)
    states = data_ingestor.get_states()

    values = {state: 0 for state in states}
    nr_entries = values.copy()

    for entry in data:
        state = entry.state
        values[state] += entry.data_value
        nr_entries[state] += 1

    means = {state: values[state] / nr_entries[state] for state in states if nr_entries[state] > 0}
    return dict(sorted(means.items(), key=lambda x: x[1]))


def state_mean(args):
    question, state = args
    data = data_ingestor.get_data_for_question_state(question, state)

    mean = reduce(lambda a, x: a + x.data_value, data, 0) / len(data)
    return {state: mean}
