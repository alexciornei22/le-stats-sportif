"""Methods for each dataset query used by the API"""
import json
import os
from functools import reduce
from app import data_ingestor


def job_wrapper(query, job_id, args):
    """
    Calls a query method and saves its output as a json file in the results directory
    :param query: method to call
    :param job_id: job id for the current query
    :param args: arguments to be passed to the query
    :return: job result
    """
    result = query(*args)

    if not os.path.exists('results'):
        os.makedirs('results')
    with open(f'results/{job_id}.json', 'w', encoding='utf-8') as result_file:
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


def format_data_for_mean_category(*args):
    return "('"+"', '".join(args)+"')"


def get_mean_by_category(question):
    data = data_ingestor.data_for_question(question)
    states = set(map(lambda x: x.state, data))

    state_data = {state: [entry for entry in data if entry.state == state] for state in states}

    grouped_data = {
        format_data_for_mean_category(state, category, strat):
            [entry for entry in state_data[state] if entry.strat == strat]
        for state in state_data.keys()
        for category in set(map(lambda x: x.strat_category, state_data[state])) if category
        for strat in set(map(
            lambda x: x.strat, filter(lambda x: x.strat_category == category, state_data[state])
        )) if strat
    }
    for key, items in grouped_data.items():
        grouped_data[key] = reduce(lambda a, item: a + item.data_value, items, 0) / len(items)

    return grouped_data


def get_state_mean_by_category(question, state):
    data = data_ingestor.data_for_question_in_state(question, state)

    grouped_data = {
        format_data_for_mean_category(category, strat):
            [entry for entry in data if entry.strat == strat]
        for category in set(map(lambda x: x.strat_category, data)) if category
        for strat in set(map(
            lambda x: x.strat, filter(lambda x: x.strat_category == category, data)
        )) if strat
    }
    for key, items in grouped_data.items():
        grouped_data[key] = reduce(lambda a, item: a + item.data_value, items, 0) / len(items)

    return {state: grouped_data}
