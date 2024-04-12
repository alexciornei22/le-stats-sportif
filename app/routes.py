from app import webserver
from flask import request, jsonify
from app import queries


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    job_id = int(job_id)
    future = webserver.futures[job_id]

    if future is None:
        return jsonify({'error': 'Invalid job_id'})
    if not future.done():
        return jsonify({'status': 'running'})
    else:
        return jsonify({'status': 'done', 'data': future.result()})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_states_mean, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_state_mean, data['question'], data['state'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_best5, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_worst5, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_global_mean, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_diff_from_mean, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    data = request.get_json()
    question = data['question']
    state = data['state']

    job_id = submit_job_to_executor(queries.get_state_diff_from_mean, question, state)

    return jsonify({"job_id": job_id})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    data = request.get_json()
    question = data['question']

    job_id = submit_job_to_executor(queries.get_mean_by_category, question)

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    data = request.get_json()
    question = data['question']
    state = data['state']

    job_id = submit_job_to_executor(queries.get_state_mean_by_category, question, state)

    return jsonify({"job_id": job_id})


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes


def submit_job_to_executor(job, *args):
    job_id = webserver.job_counter
    future = webserver.tasks_runner.submit(queries.job_wrapper, job, job_id, args)
    webserver.futures[job_id] = future
    webserver.job_counter += 1
    return job_id
