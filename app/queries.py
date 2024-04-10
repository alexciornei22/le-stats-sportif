from app import data_ingestor


def states_mean(question):
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
