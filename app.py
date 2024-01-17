import os
import subprocess
from flask import Flask, render_template, jsonify, request, Response, redirect, url_for, session

import random
import docker

from docker_info import *
import psutil
import randomname
import json


import json

def load_config():
    try:
        with open('config/config.json', 'r') as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print("Error: Config file not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON in config file.")
        return None

def get_username_password():
    config_data = load_config()

    if config_data:
        username = config_data.get('username')
        password = config_data.get('password')

        if username and password:
            return username, password
        else:
            print("Error: Username or password not found in config file.")
            return None, None
    else:
        return None, None

# Example usage:
username, password = get_username_password()

# if username and password:
#     print(f"Username: {username}")
#     print(f"Password: {password}")
# else:
#     print("Failed to retrieve username and password.")



def get_cpu_and_memory_usage():
    # Get CPU and memory usage using 'ps' command
    try:
        ps_output = subprocess.check_output(["ps", "-p", str(os.getpid()), "-o", "%cpu,%mem"])
        lines = ps_output.decode().split('\n')[1:-1]
        cpu_mem_values = lines[0].strip().split()

        cpu_usage, mem_usage = map(float, cpu_mem_values[:2])

        return cpu_usage, mem_usage
    except subprocess.CalledProcessError:
        return None, None

app = Flask(__name__)
app.secret_key = "kequeen"

def check_session():
    # Check if the session token is present in the session
    return 'session_token' in session


from flask import redirect, url_for, session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Render the login page
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()

        # Check if the username and password match (replace with your actual authentication logic)
        if data.get('username') == username and data.get('password') == password:
            # Set a session variable with a random session token
            session['session_token'] = str(random.randint(1, 1000000))
            session['user_id'] = 'keqing'  # Use a unique identifier for the user

            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401




@app.route("/logout", methods=['GET'])
def logout():
    session.clear()

    return redirect(url_for('index'))
# dashboard routes 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/container')
def docker():
    if check_session():
        return render_template('container.html')
    else:
        return redirect(url_for('login'))


@app.route('/images')
def imageRoute():
    if check_session():
        return render_template('images.html')
    else:
        return redirect(url_for('login'))

@app.route('/api/docker-info', methods=['GET'])
def get_docker_info():
    docker_info = {
    'running_containers': get_running_containers_count(),
    'current_images': get_installed_images(),
    'total_containers': get_all_containers_count(),
    }
    return jsonify(docker_info)


@app.route('/api/server-info', methods=['GET'])
def get_server_info():
    # Get CPU and RAM usage
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    return jsonify({'cpu_usage': cpu_usage, 'ram_usage': ram_usage})



#docker container management routes 


@app.route('/api/docker-manage/list', methods=['GET'])
def docker_manage_list():
    container_list = get_container_info()
    return jsonify(container_list)                                                                                                                                                                                                                           

@app.route('/api/docker-manage/startcontainer', methods=['POST'])
def start_container_route():
    # Get the JSON data from the request
    data = request.get_json()

    # Check if the 'containerID' key exists in the JSON data
    if 'containerID' in data:
        container_id = data['containerID']
        result = start_container(container_id)

        # Return a response, for example, a JSON response
        if("successfully" in result):
            return jsonify({'status': 'success', 'message': result})
        else:
            return jsonify({'status': 'error', 'message': result})
            
    else:
        # If 'containerID' is not provided in the JSON data, return an error response
        return jsonify({'status': 'error', 'message': 'Container ID not provided'}), 400

@app.route('/api/docker-manage/stopcontainer', methods=['POST'])
def stop_container_route():
    data = request.get_json()

    if 'containerID' in data:
        container_id = data['containerID']
        result = stop_container(container_id)

        if("successfully" in result):
            return jsonify({'status': 'success', 'message': result})
        else:
            return jsonify({'status': 'error', 'message': result})
            
    else:
        # If 'containerID' is not provided in the JSON data, return an error response
        return jsonify({'status': 'error', 'message': 'Container ID not provided'}), 400


@app.route('/api/docker-manage/createcontainer', methods=['POST'])
def create_docker_container_route():
    data = request.get_json()

    if 'container_image' in data and 'container_name' in data:
        container_name = data['container_name']
        container_image = data['container_image']
        container_daemon = data.get('run_as_daemon', False)  # Default to False if not provided
        print("-----> ", container_daemon)

        # Optional parameters
        xcommand = data.get('command', None)
        print("---->", xcommand)
        auto_removal = data.get('auto_removal', False)  # Default to True if not provided
        hostname = data.get('hostname', container_name)  # Default to containerName if not provided
        memory_limit = data.get('memory_limit', None)  # Default to None if not provided
        ports = data.get('ports', None)  # Default to None if not provided
        volumes = data.get('volumes', None)  # Default to None if not provided

        if 'container_attach_to_network' in data:
            container_network = data['container_network']
            result = create_docker_container(container_image, container_name, network=container_network, 
                                            command=xcommand, auto_removal=auto_removal, hostname=hostname,
                                            memory_limit=memory_limit, ports=ports, volumes=volumes, daemon=container_daemon, startImmediate=True)

        else:
            result = create_docker_container(container_image, container_name, network=container_network, 
                                            command=xcommand, auto_removal=auto_removal, hostname=hostname,
                                            memory_limit=memory_limit, ports=ports, volumes=volumes, daemon=container_daemon, startImmediate=True)


        if "created" and "started" in result:
            return jsonify({'status': 'Success', 'message': result})
        else:
            return jsonify({'status': 'error', 'message': result})

    else:
        return jsonify({'status': 'error', 'message': 'Error in payload'}), 400



@app.route('/api/docker-manage/deletecontainer', methods=['POST'])
def delete_docker_container_route():
    data = request.get_json()

    if 'container_id' in data:

        container_id = data['container_id']
        result = delete_docker_container(container_id)
        if("successfully" in result):
            return jsonify({'status': 'success', 'message': result})
        else:
            return jsonify({'status': 'error', 'message': result})

    else:
        # If 'containerID' is not provided in the JSON data, return an error response
        return jsonify({'status': 'error', 'message': 'Container ID not provided'}), 400



@app.route('/api/docker-manage/createNetwork', methods=['POST'])
def create_docker_network_route():
    data = request.get_json()

    # Extract parameters from the request data
    network_name = data.get('network_name')
    containers_to_attach = data.get('containers_to_attach', [])

    # Call the create_docker_network function
    network_id = create_docker_network(network_name, containers_to_attach)

    return jsonify({"network_id": network_id, "message": "Docker network created successfully."})


@app.route('/api/docker-manage/searchImage', methods=['GET'])
def search_docker_images():
    # Get the query parameter from the request
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Query parameter is missing"}), 400

    # Docker Hub API URL for image search
    api_url = f'https://hub.docker.com/v2/search/repositories/?query={query}&page_size=10'

    try:
        # Make a request to the Docker Hub API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses

        # Parse the JSON response
        result = response.json()

        # Extract image names from the response
        image_names = [repo['repo_name'] for repo in result.get('results', [])]

        return jsonify({"images": image_names})

    except requests.RequestException as e:
        return jsonify({"error": f"Error searching Docker images: {e}"}), 500


@app.route('/api/docker-manage/pullImage', methods=['GET'])
def pull_docker_image_route():
    # Get the image_name parameter from the query string
    image_name = request.args.get('image_name')

    # Check if 'image_name' is provided
    if image_name:
        tag = request.args.get('tag', 'latest')  # Default to 'latest' if 'tag' is not provided

        # Use Response to stream SSE to the client
        return Response(pull_docker_image(image_name, tag), content_type='text/event-stream')

    else:
        # If 'image_name' is not provided in the query string, return an error response
        return jsonify({'status': 'error', 'message': 'Image name not provided'}), 400


@app.route('/api/docker-manage/installedImages/list', methods=['GET'])
def get_installed_images_route():
    images = get_installed_images_list_dropdown()
    return jsonify(images)

@app.route('/api/docker-manage/network/getNetworks', methods=['GET'])
def get_docker_networks_route():
    network_list = get_docker_networks_list_dropdown()
    return jsonify(network_list)


@app.route('/api/misc/random-name', methods=['GET'])
def get_random_name():
    name = randomname.generate()
    return jsonify({"random_name": name})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
