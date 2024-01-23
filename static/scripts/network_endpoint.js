// JavaScript for dynamically populating network details
function populateNetworkTable(networks) {
  const tableBody = document.getElementById('networkTableBody');

  networks.forEach(network => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${network.network_name}</td>
      <td>${network.driver}</td>
      <td>${network.connected_containers.join(', ')}</td>
      <td>
        <button class="btn btn-danger" onclick="deleteNetwork('${network.network_id}')">
          <i class="fa-solid fa-trash"></i> Delete
        </button>
        <button class="btn btn-primary" onclick="inspectNetwork('${network.network_id}')">
          <i class="fa-solid fa-eye"></i> Inspect
        </button>
        <button class="btn btn-success" onclick="openAddContainerModal('${network.network_id}')">
          <i class="fa-solid fa-plus"></i> Add Container
        </button>
      </td>
    `;

    tableBody.appendChild(row);
  });
}

// JavaScript for dynamically populating container dropdown in the add container modal
function populateContainerDropdown(containers) {

  

  const containerDropdown = document.getElementById('containerDropdown');


    containerDropdown.innerHTML = '';


  containers.forEach(container => {
    const option = document.createElement('option');
    option.value = container.Name;
    option.textContent = container.Name;
    containerDropdown.appendChild(option);
  });
}

// JavaScript for opening the add container modal
function openAddContainerModal(networkId) {
  // Fetch container list from /api/docker-manage/list
  fetch('/api/docker-manage/list')
    .then(response => response.json())
    .then(containers => {
      // Populate the container dropdown in the modal
      populateContainerDropdown(containers);

      // Open the add container modal
      $('#addContainerModal').modal('show');

      // Set the networkId in a hidden field for reference
      document.getElementById('selectedNetworkId').value = networkId;
    })
    .catch(error => console.error('Error fetching container list:', error));
}

function addContainerToNetwork() {
  const containerName = document.getElementById('containerDropdown').value;
  const networkId = document.getElementById('selectedNetworkId').value;

  // Make a POST request to connect the container to the network
  fetch('/api/docker-manage/network/connect-container', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      container_name: containerName,
      network_name: networkId,
    }),
  })
    .then(response => response.json())
    .then(result => {
      // Close the modal
      $('#addContainerModal').modal('hide');

      // Display a toast with the result
      showColorPaletteToast(result.message, 'success');
    })
    .catch(error => {
      // Handle error and show error toast
      console.error('Error adding container to network:', error);
      showColorPaletteToast('Error adding container to network', 'error');
    });
}

function showColorPaletteToast(message, type) {
  // Define color palette
  const colorPalette = ["#141827", "#36406B", "#BDBCC8", "#857891"];

  // Use the color corresponding to the type
  const color = type === 'success' ? colorPalette[0] : colorPalette[1];

  // Show the toast
  toastr.options = {
    closeButton: true,
    positionClass: 'toast-bottom-right',
    showDuration: '300',
    hideDuration: '1000',
    timeOut: '5000',
    extendedTimeOut: '1000',
    backgroundColor: color,  // Fix the typo: 'backgroundcolor' to 'backgroundColor'
  };

  toastr[type](message);
}

// JavaScript for dynamically populating network inspection modal
function populateNetworkInspectModal(networkDetails, netID) {
const modalContent = document.getElementById('networkInspectContent');
modalContent.innerHTML = `
  <p><strong><i class="fa-solid fa-pencil"></i> Network Name:</strong> ${networkDetails.network_name}</p>
  <p><strong><i class="fa-solid fa-fingerprint"></i> Network ID:</strong> ${netID}</p>
  <p><strong><i class="fa-solid fa-subscript"></i> Network Subnet:</strong> ${networkDetails.network_subnet}</p>
  <p><strong><i class="fa-solid fa-route"></i> Network Gateway:</strong> ${networkDetails.network_gateway}</p>
  <p><strong><i class="fa-solid fa-cubes-stacked"></i> Connected Containers:</strong></p>
  <ul>
    ${networkDetails.connected_containers.map(container => `
      <li>
        <strong>Container Name:</strong> ${container.container_name}<br>

        <strong>MAC Address:</strong> ${container.mac_address}<br>
        <strong>IPv4 Address:</strong> ${container.ipv4_address || 'None'}<br>
        <strong>IPv6 Address:</strong> ${container.ipv6_address || 'None'}
      </li>

      <button class="btn btn-danger" onclick="disconnectContainer('${container.container_name}', '${networkDetails.network_name}')">
        <i class="fa-solid fa-unlink"></i> Unlink
      </button><br>
      <hr>
    `).join('')}
  </ul>
`;
}


// Function to inspect a network
function inspectNetwork(networkId) {
  // Fetch network details using AJAX or fetch API
  fetch('/api/docker-manage/network/getNetworkDetail', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ network_id: networkId }),
  })
  .then(response => response.json())
  .then(data => {
    // Populate the network inspection modal
    populateNetworkInspectModal(data,networkId);
    // Show the modal
    $('#networkInspectModal').modal('show');
  })
  .catch(error => console.error('Error:', error));
}

// Function to delete a network
function deleteNetwork(networkId) {
  // Implement network deletion logic here
  console.log('Deleting network with ID:', networkId);
}

// Function to disconnect a container from a network
function disconnectContainer(containerName, networkName) {
  // Implement container disconnection logic here
  console.log(`Disconnecting container ${containerName} from network ${networkName}`);
}

// Fetch and populate network details on page load
fetch('/api/docker-manage/network/getDetailedNetwork')
  .then(response => response.json())
  .then(data => populateNetworkTable(data))
  .catch(error => console.error('Error:', error));

  function disconnectContainer(containerName, networkName) {
    // Create a payload for the API request
    const payload = {
      container_name: containerName,
      network_name: networkName,
    };
  
    // Make a POST request to your API endpoint
    fetch('/api/docker-manage/network/disconnect-container', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          // Show a success toast
          showColorPaletteToast('Container disconnected successfully!', 'success');
        } else {
          // Show an error toast
          showColorPaletteToast(`Error disconnecting container: ${data.message}`, 'error');
        }
      })
      .catch(error => {
        // Show an error toast for network/API errors
        showColorPaletteToast(`Error disconnecting container: ${error}`, 'error');
      });
  }

  function showColorPaletteToast(message, type) {
    // Define color palette
    const colorPalette = ["#141827", "#36406B", "#BDBCC8", "#857891"];
  
    // Use the color corresponding to the type
    const color = type === 'success' ? colorPalette[0] : colorPalette[1];
  
    // Show the toast
    toastr.options = {
      closeButton: true,
      positionClass: 'toast-bottom-right',
      showDuration: '300',
      hideDuration: '1000',
      timeOut: '5000',
      extendedTimeOut: '1000',
      backgroundcolor: color,  // Set background color based on type
    };
  
    toastr[type](message);
  }

  
  

  // Function to delete a Docker network with confirmation
function deleteNetwork(networkID) {
// Show a confirmation dialog using SweetAlert2
Swal.fire({
  title: 'Are you sure?',
  text: 'This action cannot be undone!',
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Yes, delete it!'
}).then((result) => {
  if (result.isConfirmed) {
    // User confirmed, proceed with the deletion
    performNetworkDeletion(networkID);
  }
});
}

// Function to actually perform the network deletion after confirmation
function performNetworkDeletion(networkID) {
// Create a payload for the API request
const payload = {
  network_id: networkID,
};

// Make a POST request to your API endpoint
fetch('/api/docker-manage/network/delete', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload),
})
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // Show a success toast
      showColorPaletteToast('Network deleted successfully!', 'success');
    } else {
      // Show an error toast
      showColorPaletteToast(`Error deleting network: ${data.message}`, 'error');
    }
  })
  .catch(error => {
    // Show an error toast for network/API errors
    showColorPaletteToast(`Error deleting network: ${error}`, 'error');
  });
}

// Example usage
// Call this function when you want to delete a network
// deleteNetwork('networkID');


function addNetwork() {
const networkName = document.getElementById('networkName').value;
const subnet = document.getElementById('subnet').value;
const gateway = document.getElementById('gateway').value;
const internal = document.getElementById('internal').checked;
const driver = document.getElementById('driver').value;

// Build the ipam_config based on provided values
const ipam_config = {
    Driver: 'default',
    Options: {},
    Config: [],
};

if (subnet && gateway) {
    ipam_config.Config.push({
        Subnet: subnet,
        Gateway: gateway,
    });
}

// Make a POST request to create the network
fetch('/api/docker-manage/network/create', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        network_name: networkName,
        ipam_config: ipam_config,
        internal: internal,
        driver: driver,
    }),
})
    .then(response => response.json())
    .then(result => {
        // Close the modal
        $('#addNetworkModal').modal('hide');
      // Force a complete refresh, fetching the latest content from the server


        // Display a toast with the result
        showColorPaletteToast(result.network_id ? 'Network added successfully' : result.error, result.network_id ? 'success' : 'error');

      })
    .catch(error => {
        console.error('Error adding network:', error);
        showColorPaletteToast('Error adding network. Please try again.', 'error');
    });
}

