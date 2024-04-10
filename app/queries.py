from functools import reduce
from app import data_ingestor


def states_mean(args):
    question, = args

    means = data_ingestor.get_averages_for_question(question)

    return dict(sorted(means.items(), key=lambda x: x[1]))


def state_mean(args):
    question, state = args
    data = data_ingestor.get_data_for_question_state(question, state)

    mean = reduce(lambda a, x: a + x.data_value, data, 0) / len(data)
    return {state: mean}


def best5(args):
    question, = args

    means = data_ingestor.get_averages_for_question(question)

    reverse = question in data_ingestor.questions_best_is_max
    means = sorted(means.items(), key=lambda x: x[1], reverse=reverse)
    return dict(means[0:5])


def worst5(args):
    question, = args

    means = data_ingestor.get_averages_for_question(question)

    reverse = question in data_ingestor.questions_best_is_min
    means = sorted(means.items(), key=lambda x: x[1], reverse=reverse)
    return dict(means[0:5])


def global_mean(args):
    question, = args

    data = data_ingestor.get_data_for_question(question)
    mean = reduce(lambda a, x: a + x.data_value, data, 0) / len(data)
    return {'global_mean': mean}
