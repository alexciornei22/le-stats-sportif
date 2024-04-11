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
