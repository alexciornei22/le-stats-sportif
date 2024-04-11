from functools import reduce
from app import data_ingestor
import json
import os

def job_wrapper(query, job_id, args):
    result = query(*args)

    if not os.path.exists('results'):
        os.makedirs('results')
    with open(f'results/{job_id}', 'w') as result_file:
        json.dump(result, result_file)

    return result


def get_states_mean(question):
    means = data_ingestor.states_averages_for_question(question)

    return dict(sorted(means.items(), key=lambda x: x[1]))


def get_state_mean(question, state):
    data = data_ingestor.data_for_question_in_state(question, state)

    mean = reduce(lambda a, x: a + x.data_value, data, 0) / len(data)
    return {state: mean}


def get_best5(question):
    means = data_ingestor.states_averages_for_question(question)

    reverse = question in data_ingestor.questions_best_is_max
    means = sorted(means.items(), key=lambda x: x[1], reverse=reverse)
    return dict(means[0:5])


def get_worst5(question):
    means = data_ingestor.states_averages_for_question(question)

    reverse = question in data_ingestor.questions_best_is_min
    means = sorted(means.items(), key=lambda x: x[1], reverse=reverse)
    return dict(means[0:5])


def get_global_mean(question):
    data = data_ingestor.data_for_question(question)
    mean = reduce(lambda a, x: a + x.data_value, data, 0) / len(data)
    return {'global_mean': mean}


def get_diff_from_mean(question):
    state_means = get_states_mean(question)
    global_mean = get_global_mean(question)['global_mean']

    state_means = {state: global_mean - mean for (state, mean) in state_means.items()}
    return state_means


def get_state_diff_from_mean(question, state):
    state_mean = get_state_mean(question, state)
    global_mean = get_global_mean(question)['global_mean']

    state_mean[state] = global_mean - state_mean[state]
    return state_mean


def get_mean_by_category(question):
    data = data_ingestor.data_for_question(question)
    states = set(map(lambda x: x.state, data))

    state_data = {state: [entry for entry in data if entry.state == state] for state in states}

    grouped_data = {
        "('"+"', '".join((state, category, strat))+"')": [entry for entry in state_data[state] if entry.strat == strat]
        for state in state_data.keys()
        for category in set(map(lambda x: x.strat_category, state_data[state])) if category
        for strat in set(map(
            lambda x: x.strat, filter(lambda x: x.strat_category == category, state_data[state])
        )) if strat
    }
    for key, items in grouped_data.items():
        grouped_data[key] = reduce(lambda a, item: a + item.data_value, items, 0) / len(items)

    return dict(sorted(grouped_data.items()))
