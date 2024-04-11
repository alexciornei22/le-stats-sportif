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


def states_mean(question):
    means = data_ingestor.states_averages_for_question(question)

    return dict(sorted(means.items(), key=lambda x: x[1]))


def state_mean(question, state):
    data = data_ingestor.data_for_question_in_state(question, state)

    mean = reduce(lambda a, x: a + x.data_value, data, 0) / len(data)
    return {state: mean}


def best5(question):
    means = data_ingestor.states_averages_for_question(question)

    reverse = question in data_ingestor.questions_best_is_max
    means = sorted(means.items(), key=lambda x: x[1], reverse=reverse)
    return dict(means[0:5])


def worst5(question):
    means = data_ingestor.states_averages_for_question(question)

    reverse = question in data_ingestor.questions_best_is_min
    means = sorted(means.items(), key=lambda x: x[1], reverse=reverse)
    return dict(means[0:5])


def global_mean(question):
    data = data_ingestor.data_for_question(question)
    mean = reduce(lambda a, x: a + x.data_value, data, 0) / len(data)
    return {'global_mean': mean}
