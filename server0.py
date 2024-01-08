import os
import subprocess
from flask import Flask, render_template, jsonify, request, Response
import docker
from docker_info import *
import psutil
import randomname
import json


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

# Sample Docker and Server Information (replace with your actual data)
def get_container_info():
    # Connect to the Docker daemon
    client = docker.from_env()

    # List all containers
    containers = client.containers.list(all=True)

    # Prepare container information
    container_info = []
    for container in containers:
        info = {
            'id' : container.id,
            'Name': container.name,
            'Image': container.image.tags[0],
            'Running': container.status == 'running'
        }
        container_info.append(info)

    return container_info


# dashboard routes 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docker')
def server():
    return render_template('docker.html')

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
        container_daemon = data['run_as_daemon']
        if 'container_attach_to_network' in data:
            container_network = data['container_network']
            result = create_docker_container(container_image, container_name, container_network,container_daemon)
        else:
            result = create_docker_container(container_image, container_name, network=None)
        
        if "created" and "started" in result:
            return jsonify({'status': 'Success', 'message': result})
        else:
            return jsonify({'status':'error', 'message' : result})
    
    else:
        return jsonify({'status':'error', 'message':'Error in payload'}), 400
        
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
