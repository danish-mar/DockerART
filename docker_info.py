import docker
import json
from flask import jsonify, Response
import requests
from datetime import datetime

# ... rest of your code ...

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

#returns the running containers count
def get_running_containers_count():
    # Connect to the Docker daemon
    client = docker.from_env()

    # Count the number of running containers
    running_containers_count = len(client.containers.list(filters={'status': 'running'}))

    return running_containers_count

#Gets the already installed images
def get_installed_images():
    client = docker.from_env()

    # List all images
    installed_images = client.images.list()

    # Return the count of images
    return len(installed_images)


#gets the installed images list
def get_installed_images_list():
    client = docker.from_env()

    installed_images = client.images.list()

    return installed_images

#gets the installed images list
def get_installed_images_list_dropdown():

    client = docker.from_env()
    images = client.images.list()
    return [image.tags[0] for image in images if image.tags]

    return images

def get_docker_networks_list_dropdown():
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Get a list of Docker networks
        networks = client.networks.list()

        # Extract relevant information about each network
        network_info = []
        for network in networks:
            info = {
                'name': network.name,
                # Add more information as needed
            }
            network_info.append(info)

        return network_info

    except docker.errors.APIError as e:
        return f"Error retrieving Docker networks: {str(e)}"




#gets the all container count even tho the stopped and the running container as well
def get_all_containers_count():
    client = docker.from_env()
    all_containers = len(client.containers.list(all=True))

    return all_containers


#gets contaienr info NON_ABSTRACT
def print_container_info():
    # Connect to the Docker daemon
    client = docker.from_env()

    # List all containers
    containers = client.containers.list(all=True)

    # Print container information
    print("Name\t\tImage\t\tRunning")
    for container in containers:
        print(f"{container.id[:12]}\t{container.name}\t{container.image.tags[0]}\t{container.status}")


#@params : container_ID | starts a container
def start_container(container_id,command=None):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Get the container object
        container = client.containers.get(container_id)

        # Start the container
        if command:
            container.run(command)
        else:
            container.start()

        return(f"Container {container_id} started successfully.")
    except docker.errors.APIError as e:
        return (f"Error starting container {container_id}: {e}")
    except docker.errors.NotFound:
        return(f"Container {container_id} not found.")

# def start_container(container_id,command):
#     try:
#         # Connect to the Docker daemon
#         client = docker.from_env()

#         # Get the container object
#         container = client.containers.get(container_id)

#         # Start the container
#         container.run(container, command)

#         return(f"Container {container_id} started successfully.")
#     except docker.errors.APIError as e:
#         return (f"Error starting container {container_id}: {e}")
#     except docker.errors.NotFound:
#         return(f"Container {container_id} not found.")

#@params : container_ID | stops a container
def stop_container(container_id):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Get the container object
        container = client.containers.get(container_id)

        # Start the container
        container.stop()

        return (f"Container {container_id} stopped successfully.")

    except docker.errors.APIError as e:
        return (f"Error stopping container {container_id}: {e}")
    except docker.errors.NotFound:
        return (f"Container {container_id} not found.")

import docker


#@params container_image, container_name, network | creates a docker container on the following arguments
def create_docker_container_gen2(container_image, container_name, network=None,
                            command=None, auto_removal=False, hostname=None, memory_limit=None,
                            ports=None, volumes=None, daemon=False, startImmediate=True):

    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Define container configurations
        container_config = {
            'image': container_image,
            'name': container_name,
            'network': network,
            'detach': daemon,
            'auto_remove': auto_removal,
            'hostname': hostname,
            'mem_limit': memory_limit,
            'ports': ports,
            'volumes': volumes,
            # Add more configurations as needed
        }

        if startImmediate:
            start_container(container_name,command)

        # Create the Docker container
        container = client.containers.create(**container_config)

        return f"Container '{container_name}' created and started successfully."

    except docker.errors.APIError as e:
        return f"Error creating or starting container '{container_name}': {str(e)}"






def create_docker_container(container_image, container_name, network, run_as_daemon=False):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Define container configurations
        container_config = {
            'image': container_image,
            'name': container_name,
            'network': network,
            'detach': run_as_daemon,
            # Add more configurations as needed
        }

        # Create the Docker container
        container = client.containers.create(**container_config)

        if not run_as_daemon:
            # Start the created container
            container.start()
        else:
            # Run the '/bin/bash' command and detach
            exec_command = ['/bin/bash']
            exec_result = container.exec_run(exec_command, detach=True)
            # Check exec_result for success or handle errors

        return f"Container '{container_name}' created and {'started' if not run_as_daemon else 'running as daemon'} successfully."

    except docker.errors.APIError as e:
        return f"Error creating or starting container '{container_name}': {str(e)}"


#@params container_id | deletes a docker container 
def delete_docker_container(container_id):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Get the container object
        container = client.containers.get(container_id)

        # Stop the container before deleting
        container.stop()

        # Remove the container
        container.remove()

        return (f"Container {container_id} | {container.name} deleted successfully.")
    except docker.errors.APIError as e:
        return (f"Error deleting container {container_id}: {e}")
    except docker.errors.NotFound:
        return (f"Container {container_id} not found.")



#get all the docker network info
def get_docker_networks():
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Get a list of Docker networks
        networks = client.networks.list()

        # Extract relevant information about each network
        network_info = []
        for network in networks:
            info = {
                'id': network.id,
                'name': network.name,
                'driver': network.attrs['Driver'],
                # Add more information as needed
            }
            network_info.append(info)

        return network_info

    except docker.errors.APIError as e:
        return f"Error retrieving Docker networks: {str(e)}"


#@params : network_id | gets the information on the provided contaner id
def get_docker_network_info(network_id):


    """
    

    """


    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Get information about the specified Docker network
        network = client.networks.get(network_id)

        # Extract relevant information about connected containers
        connected_containers = []
        for container_id, container_info in network.attrs['Containers'].items():
            container = client.containers.get(container_id)
            info = {
                'id': container.id,
                'name': container.name,
                'ipv4_address': container_info['IPv4Address'],
                # Add more information as needed
            }
            connected_containers.append(info)

        return connected_containers

    except docker.errors.APIError as e:
        return f"Error retrieving Docker network information: {str(e)}"




def create_docker_network(network_name, list_of_containers_to_attach=None):
    """
    Create a Docker network and optionally attach specified containers.

    Parameters:
    - network_name (str): Name of the Docker network to be created.
    - list_of_containers_to_attach (list): List of container names to attach to the network (default is None).

    Returns:
    - str: The ID of the created network.
    """

    # Initialize the Docker client
    client = docker.from_env()

    # Create the Docker network
    network = client.networks.create(network_name)

    # Attach containers to the network if the list is provided
    if list_of_containers_to_attach:
        for container_name in list_of_containers_to_attach:
            try:
                container = client.containers.get(container_name)
                network.connect(container)
                print(f"Container '{container_name}' attached to network '{network_name}'.")
            except docker.errors.NotFound:
                print(f"Container '{container_name}' not found.")

    return network.id
def create_docker_network(network_name, ipam_config=None, internal=False, driver='bridge'):
    """
    Create a new Docker network.

    Parameters:
    - network_name: Name of the new network.
    - ipam_config: IPAM configuration (subnet, gateway, etc.). Default is None.
    - internal: Whether the network is internal (True or False). Default is False.
    - driver: Network driver to be used. Default is 'bridge'.

    Returns:
    - Dictionary containing information about the created network.
    """
    try:
        client = docker.from_env()

        ipam_config = ipam_config or {
            'Driver': 'default',
            'Options': {},
            'Config': []
        }

        network = client.networks.create(
            name=network_name,
            internal=internal,
            driver=driver,
            ipam=ipam_config
        )

        return {
            'network_id': network.id,
            'network_name': network.name,
            'internal': network.attrs['Internal'],
            'driver': network.attrs['Driver'],
            'ipam_config': network.attrs['IPAM']
        }

    except docker.errors.APIError as e:
        return {'error': f'Docker API error: {e}'}

def connect_containers_to_network(container_names, network_name):
    """
    Connect containers to a Docker network.

    Parameters:
    - container_names: List of container names to be connected.
    - network_name: Name of the network to connect the containers.

    Returns:
    - List of dictionaries containing information about each connection.
    """
    try:
        client = docker.from_env()

        connections = []
        network = client.networks.get(network_name)

        for container_name in container_names:
            try:
                container = client.containers.get(container_name)
                network.connect(container)
                connections.append({
                    'container_name': container_name,
                    'network_name': network_name,
                    'status': 'connected'
                })
            except docker.errors.NotFound:
                connections.append({
                    'container_name': container_name,
                    'network_name': network_name,
                    'status': 'container not found'
                })

        return connections

    except docker.errors.APIError as e:
        return [{'error': f'Docker API error: {e}'} for _ in container_names]





def search_docker_images(query):
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

        return image_names

    except requests.RequestException as e:
        print(f"Error searching Docker images: {e}")
        return None

# ... (existing code)

def pull_docker_image(image_name, tag='latest'):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Use an event stream to get real-time logs during image pull
        stream = client.api.pull(image_name, tag=tag, stream=True, decode=True)

        # Iterate through the stream to get progress information
        for event in stream:
            if 'status' in event and 'id' in event:
                # Send progress information to the client
                progress_data = {'status': event['status'], 'id': event['id']}
                yield f"data: {json.dumps(progress_data)}\n\n"

        # Return a success message when the image pull is complete
        yield f"data: {json.dumps({'status': 'success', 'message': f'Successfully pulled image: {image_name}:{tag}'})}\n\n"

    except docker.errors.APIError as e:
        # Return an error message if there is an issue with the image pull
        yield f"data: {json.dumps({'status': 'error', 'message': f'Error pulling Docker image: {e}'})}\n\n"



#image page functions 

def convert_size_bytes(size_bytes):
    # Convert bytes to megabytes (MB)
    size_mb = size_bytes / (1024 * 1024)

    # Choose appropriate unit (MB, GB, TB, etc.)
    for unit in ['MB', 'GB', 'TB', 'PB']:
        if size_mb < 1024:
            return f"{size_mb:.2f} {unit}"
        size_mb /= 1024

def format_date(created_date):
    # Split the date string into date and time
    date_part, time_part = created_date.split('T')
    
    # Convert Docker date string (date) to datetime object
    date_object = datetime.strptime(date_part, "%Y-%m-%d")
    
    # Format the date as DD-MM-YYYY
    formatted_date = date_object.strftime("%d-%m-%Y")
    return formatted_date


def list_installed_images_detailed():
    try:
        client = docker.from_env()
        images = client.images.list()

        images_info = [{'index': idx,
                        'id': image.short_id[7:],
                        'name': image.tags[0],
                        'size': convert_size_bytes(image.attrs['Size']),
                        'tags': image.tags,
                        'release_date': format_date(image.attrs['Created'])} for idx, image in enumerate(images)]

        return images_info
    except Exception as e:
        return {'error': str(e)}

def delete_image(image_id):
    try:
        client = docker.from_env()
        image = client.images.get(image_id)
        image.remove()
        return f"Image with ID {image_id} successfully deleted."
    except docker.errors.ImageNotFound:
        return f"Image with ID {image_id} not found."
    except docker.errors.APIError as e:
        return {'error': str(e)}

=======


def get_docker_network_details():
    try:
        client = docker.from_env()

        networks = client.networks.list()

        network_details_list = []

        for network in networks:
            connected_containers = get_connected_containers(network.id)
            network_details = {
                'network_name': network.name,
                'network_id': network.id[:12],  # Shortened network ID
                'connected_containers': connected_containers,
                'driver': network.attrs['Driver'],
            }

            network_details_list.append(network_details)

        return network_details_list

    except docker.errors.APIError as e:
        # Handle Docker API errors
        return {'error': f'Docker API error: {e}'}

def get_connected_containers(network_id):
    try:
        client = docker.from_env()

        network = client.networks.get(network_id)
        return [container.name for container in network.containers]

    except docker.errors.APIError as e:
        # Handle Docker API errors
        return []

def get_network_details(network_id):
    try:
        client = docker.from_env()
        network = client.networks.get(network_id)

        network_details = {
            'network_name': network.name,
            'network_subnet': None,
            'network_gateway': None,
            'connected_containers': [],
        }

        if 'IPAM' in network.attrs:
            network_details['network_subnet'] = network.attrs['IPAM']['Config'][0]['Subnet']
            network_details['network_gateway'] = network.attrs['IPAM']['Config'][0]['Gateway']

        for container_id, container_info in network.attrs['Containers'].items():
            container_details = {
                'container_name': client.containers.get(container_id).name,
                'mac_address': container_info['MacAddress'],
                'ipv4_address': container_info['IPv4Address'] if 'IPv4Address' in container_info else None,
                'ipv6_address': container_info['IPv6Address'] if 'IPv6Address' in container_info else None,
            }
            network_details['connected_containers'].append(container_details)

        return network_details

    except docker.errors.APIError as e:
        # Handle Docker API errors
        return {'error': f'Docker API error: {e}'}

# Example usage:
# network_id = '32202c87c156'  # Replace with the short network ID you want to query
# result = get_network_details(network_id)
# print(result)


def delete_docker_network(network_id):
    try:
        client = docker.from_env()
        network = client.networks.get(network_id)
        network.remove()
        return {'status': 'success', 'message': f'Network {network_id} deleted successfully'}
    except docker.errors.APIError as e:
        return {'status': 'error', 'message': f'Docker API error: {e}'}


def disconnect_container_from_network(container_name, network_name):
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)

        # Disconnect the container from the network
        client.api.disconnect_container_from_network(container.id, network_name)

        return {'status': 'success'}

    except docker.errors.APIError as e:
        # Handle Docker API errors
        return {'error': f'Docker API error: {e}'}



def connect_container_to_network(container_name, network_name):
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)

        # Connect the container to the network
        client.api.connect_container_to_network(container.id, network_name)

        return {'status': 'success'}

    except docker.errors.APIError as e:
        # Handle Docker API errors
        return {'error': f'Docker API error: {e}'}

# Example usage:
# disconnect_container_from_network('your_container_name', 'your_network_name')


# ... (existing code)




# Example: Pull the latest nginx image

#print(list_installed_images_detailed())

# Example: Search for images with the query 'nginx


# Example usage:
# Replace 'your_container_id' with the actual container ID you want to start



# Examples of how to use the function

#print(get_all_containers_count())

# print(print_container_info())
# #stop_container("34cda8bd4864")
#print(get_docker_networks())
# print(get_docker_network_info('10d02f2a62b856629168eb82a8b5f2a8ef55ce53dfe19511444a58447ccc600a'))
# #start_container("priceless_kilby")


#print(get_installed_images_list_dropdown())
# #print(create_docker_container("ubuntu:latest","testServer",network=None))
# print(print_container_info())
# print(delete_docker_container("7b323933014c"))
# print(print_container_info())
