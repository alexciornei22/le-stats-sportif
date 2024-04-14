"""Defines the routes used by the API and their corresponding methods"""
import json
from flask import request, jsonify
from app import queries, webserver


@webserver.route('/api/get_results/<int:job_id>', methods=['GET'])
def get_response(job_id):
    """Get the response for a given job"""
    future = webserver.futures[job_id]

    if future is None:
        return jsonify({'error': 'Invalid job_id'})
    if not future.done():
        return jsonify({'status': 'running'})

    with open(f'results/{job_id}.json', 'r', encoding='utf-8') as file:
        result = json.load(file)
    return jsonify({'status': 'done', 'data': result})


@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get the statuses of all jobs submitted to the ThreadPoolExecutor"""
    jobs = [{job: 'done' if f.done() else 'running'} for job, f in webserver.futures.items()]
    return jsonify({'status': 'done', 'data': jobs})


@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """Get the number of jobs currently running"""
    count = len(list(filter(lambda f: not f.done(), webserver.futures.values())))
    return jsonify({'status': 'done', 'data': count})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """Get the mean for each state for a given question"""
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_states_mean, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """Get the mean for a single state for a given question"""
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_state_mean, data['question'], data['state'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """Get the best 5 performing states for a question metric"""
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_best5, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """Get the worst 5 performing states for a question metric"""
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_worst5, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """Get the mean for all entries in all states regarding a question"""
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_global_mean, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """Get each state mean's deviation from the global mean for a given question"""
    data = request.get_json()

    job_id = submit_job_to_executor(queries.get_diff_from_mean, data['question'])

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """Get one state mean's deviation from the global mean for a given question"""
    data = request.get_json()
    question = data['question']
    state = data['state']

    job_id = submit_job_to_executor(queries.get_state_diff_from_mean, question, state)

    return jsonify({"job_id": job_id})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Get the mean for all entries for a given question grouped by stratification categories"""
    data = request.get_json()
    question = data['question']

    job_id = submit_job_to_executor(queries.get_mean_by_category, question)

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    Get the mean for all entries for a given question in a given state
    grouped by stratification categories
    """
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
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs.join(f"<p>{route}</p>")

    msg += paragraphs
    return msg


def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes


def submit_job_to_executor(job, *args):
    """
    Submits a job to the ThreadPoolExecutor, increases the job counter
    and returns the submitted job's ID
    """
    job_id = webserver.job_counter
    future = webserver.tasks_runner.submit(queries.job_wrapper, job, job_id, args)
    webserver.futures[job_id] = future
    webserver.job_counter += 1
    return job_id
