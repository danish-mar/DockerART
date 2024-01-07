from flask import Flask, render_template, jsonify
import psutil
import docker

def get_running_containers():
    # Connect to the Docker daemon
    client = docker.from_env()

    # List all running containers
    running_containers = client.containers.list(filters={'status': 'running'})

    return running_containers

app = Flask(__name__)

# Sample Docker and Server Information (replace with your actual data)
docker_info = {
    'running_containers': get_running_containers(),
    'current_images': 10,
    'total_containers': 20,
}

@app.route('/')
def index():
    return render_template('index.html', docker_info=docker_info)

@app.route('/api/docker-info', methods=['GET'])
def get_docker_info():
    return jsonify(docker_info)

@app.route('/api/server-info', methods=['GET'])
def get_server_info():
    # Get CPU and RAM usage
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    return jsonify({'cpu_usage': cpu_usage, 'ram_usage': ram_usage})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
