  // Function to display selected file name
  function displayFileName() {
    const fileInput = document.getElementById('csvFileInput');
    const selectedFileName = document.getElementById('selectedFileName');
    
    if (fileInput.files.length > 0) {
      selectedFileName.textContent = fileInput.files[0].name;
    } else {
      selectedFileName.textContent = "";
    }
  }

  // Function to upload CSV file
  function uploadCSV() {
    const fileInput = document.getElementById('csvFileInput');

    if (fileInput.files.length === 0) {
      alert('Please select a file.');
      return;
    }  

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('csvFile', file);

    // Upload the CSV file to the server
    fetch('http://localhost:3000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert('File uploaded successfully:', data);

        return fetch('http://localhost:3000/new_data', { method: 'GET' });
    })
    .then(data => {
        if (data.status === 200) {
            console.log('Data processed successfully:', data);
            alert('Data processed successfully!');
        } else {
            console.error('Data processing failed:', data);
            alert('Data processing failed.');
        }
    })
    .catch(error => {
      console.error('An error occurred during the process:', error);
      if (error.message.includes('Network response was not ok')) {
          alert('The server responded with an error. Please check the server logs for more details.');
      } else if (error.message.includes('Failed to fetch')) {
          alert('Please wait! Data should have loaded once localhost:3000/new_data has loaded.');
      } else {
          alert('An unexpected error occurred. Please try again later.');
      }
    });
  }

