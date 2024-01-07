// script.js

function createDockerContainer(containerImage, containerName, containerNetwork = null, runAsDaemon = null) {
    const data = {
        container_image: containerImage,
        container_name: containerName,
        container_run_as_daemon: runAsDaemon
    };

    // Check if containerNetwork is provided
    if (containerNetwork) {
        data.container_network = containerNetwork;
    }

    // Make a POST request to the Flask server
    fetch('/api/docker-manage/createcontainer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        // Handle the result, you can log it or perform any additional actions
        console.log(result);

        // You can also update the container list or perform other actions here
        // updateContainerList();

        return result;
    })
    .catch(error => console.error('Error creating Docker container:', error));
}

function commit_and_create() {
    // Get values from form elements
    const dockerImage = document.getElementById('dockerImage').value;
    const containerName = document.getElementById('containerName').value;
    const containerNetwork = document.getElementById('containerNetwork').value;
    const runAsDaemon = document.getElementById('runAsDaemon').checked;
    const maxMemory = document.getElementById('maxMemory').value;
    const disksToConnect = document.getElementById('disksToConnect').value;

    // Prepare data for the POST request
    const data = {
        container_image: dockerImage,
        container_name: containerName,
        container_network: containerNetwork,
        container_attach_to_network: containerNetwork !== 'None', // Check if a network is selected
        run_as_daemon: runAsDaemon,
        max_memory: maxMemory,
        disks_to_connect: disksToConnect,
    };

    // Make a POST request to the Flask server
    fetch('/api/docker-manage/createcontainer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        // Handle the result, you can log it or perform any additional actions
        console.log(result);

        // Close the form after submission
        form_hide_create_docker_container();
        fetchContainerData();
    })
    .catch(error => console.error('Error creating container:', error));
}

// function getRandomName() {
//     fetch('/api/misc/random-name')
//     .then(response => response.json())
//     .then(data => {
//         // Use querySelector to get the first element with class 'xs'
//         const container_name = document.querySelector('.xs');
//         container_name.value = data['random_name'];
//     })
// }



document.addEventListener('DOMContentLoaded', function () {
    // Fetch Docker networks from Flask server
    fetch('/api/docker-manage/network/getNetworks')
        .then(response => response.json())
        .then(data => {
            // Update the dropdown options
            fillDropdown('containerNetwork', data);
        })
        .catch(error => console.error('Error fetching Docker networks:', error));
});

    document.addEventListener('DOMContentLoaded', function () {
        // Fetch Docker images from Flask server
        fetch('/api/docker-manage/installedImages/list')
            .then(response => response.json())
            .then(data => {
                // Update the dropdown options
                fillDropdown('dockerImage', data);
            })
            .catch(error => console.error('Error fetching Docker images:', error));
    });

    function fillDropdown(dropdownId, options) {
        // Get the dropdown element
        const dropdown = document.getElementById(dropdownId);

        // Clear existing options
        dropdown.innerHTML = '';

        // Add new options
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.text = option;
            dropdown.appendChild(optionElement);
        });
    }



function fetchContainerData() {
    fetch('/api/docker-manage/list')
        .then(response => response.json())
        .then(data => {
            // Update the container list on the webpage
            updateContainerList(data);
        })
        .catch(error => console.error('Error fetching container data:', error));
}

document.addEventListener("DOMContentLoaded", fetchContainerData);


function getLogoClass(imageName) {
    // Check the image name to determine the appropriate logo class
    if (imageName.includes('ubuntu')) {
        return 'fa-ubuntu';
    } else if (imageName.includes('arch')) {
        return 'fa-linux';
    } else if (imageName.includes('mysql')) {
        return 'fa-database';
    } else if (imageName.includes('nginx')) {
        return 'fa-server';
    } else {
        return 'fa-docker'; // Use a default logo for unrecognized images
    }
}

function startContainer(containerId) {
    // Prepare the data to be sent in the POST request
    const data = {
        containerID: containerId
    };

    // Make a POST request to the Flask server
    fetch('/api/docker-manage/startcontainer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        // Handle the result, you can log it or perform any additional actions


        // Update the container list after starting the container
        fetchContainerData();

        return(result);
    })
    .catch(error => console.error('Error starting container:', error));
}

function stopContainer(container_id) {
    const data = {
        containerID: container_id
    };

    fetch('/api/docker-manage/stopcontainer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        // Introduce a delay of 2 seconds (2000 milliseconds)
            fetchContainerData();
        return result;
    })
    .catch(error => console.error('Error stopping container:', error));
}


function deleteContainer(containerId) {
    // Prepare the data to be sent in the POST request
    const data = {
        container_id: containerId
    };

    // Make a POST request to the Flask server
    fetch('/api/docker-manage/deletecontainer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        // Handle the result, you can log it or perform any additional actions
        console.log(result);

        // Update the container list after deleting the container
        fetchContainerData();
    })
    .catch(error => console.error('Error deleting container:', error));
}



function updateContainerList(containerData) {
    const containerList = document.getElementById('containerList');

    // Clear the existing container list
    containerList.innerHTML = '';

    // Loop through the container data and create list items
    containerData.forEach(container => {
        const listItem = document.createElement('div');
        listItem.classList.add('col-md-4', 'mb-4');

        const card = document.createElement('div');
        card.classList.add('card', 'tpcard');

        // Check if the image name contains 'Ubuntu' to determine the logo
        const logoClass = getLogoClass(container.Image);

        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body', 'text-center');

        const logo = document.createElement('i');
        logo.classList.add('fa-brands', logoClass, 'fa-3x', 'mb-3');

        const title = document.createElement('h5');
        title.classList.add('card-title');
        title.innerText = container.Name;

        const status = document.createElement('p');
        status.classList.add('card-text');
        if (container.Running) {
            status.innerText = 'Running: Yes';
        } else {
            status.innerText = 'Running: No';
        }

        const container_id = document.createElement('p');
        container_id.classList.add('lg');
        container_id.innerHTML = `ID : ${container.id}`;

        // Create the button element
        const containerButton = document.createElement('button');
        containerButton.classList.add('container-button');

        if(container.Running){
            containerButton.classList.add('stopped');
            logo.classList.add('fa-fade')
            containerButton.innerHTML = '<i class="fas fa-stop"></i> Stop';
        }else{
            containerButton.classList.add('running');
            containerButton.innerHTML = '<i class="fas fa-play"></i> Start';
        }

        // Add click event listener to the button
        containerButton.addEventListener('click', () => {
            if (container.Running) {
                stopContainer(container.id);
                containerButton.classList.remove('running');
                containerButton.classList.add('stopped');
                containerButton.innerHTML = '<i class="fas fa-stop"></i> Stop';
            } else {
                startContainer(container.id);
                containerButton.classList.remove('stopped');
                containerButton.classList.add('running');
                containerButton.innerHTML = '<i class="fas fa-play"></i> Start';
            }
        });

        // Create the delete button element
        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete-button');
        deleteButton.innerHTML = '<i class="fas fa-times"></i>';

        // Add click event listener to the delete button
        deleteButton.addEventListener('click', () => {
            // Show confirmation dialog before deleting
            const shouldDelete = confirm(`Are you sure you want to delete container ${container.Name}?`);
            if (shouldDelete) {
                // Call a function to handle the deletion
                deleteContainer(container.id);
            }
        });

        // Append delete button to the card body
        cardBody.appendChild(deleteButton);

        // Append elements to the card body
        cardBody.appendChild(logo);
        cardBody.appendChild(title);
        cardBody.appendChild(status);
        cardBody.appendChild(container_id);
        cardBody.appendChild(containerButton);

        // Append card body to the card
        card.appendChild(cardBody);

        // Append card to the list item
        listItem.appendChild(card);

        // Append list item to the container list
        containerList.appendChild(listItem);
    });
}




function submitForm() {
    // Implement your form submission logic here
    alert('Form submitted!');
}

