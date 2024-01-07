import docker


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

    return installed_images

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
def start_container(container_id):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Get the container object
        container = client.containers.get(container_id)

        # Start the container
        container.start()

        return(f"Container {container_id} started successfully.")
    except docker.errors.APIError as e:
        return (f"Error starting container {container_id}: {e}")
    except docker.errors.NotFound:
        return(f"Container {container_id} not found.")

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
def create_docker_container(container_image, container_name, network):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()

        # Define container configurations
        container_config = {
            'image': container_image,
            'name': container_name,
            'network': network,
            # Add more configurations as needed
        }

        # Create the Docker container
        container = client.containers.create(**container_config)

        # Start the created container
        container.start()

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
