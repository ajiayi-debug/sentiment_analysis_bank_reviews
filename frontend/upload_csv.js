function displayFileName() {
  const fileInput = document.getElementById('csvFileInput');
  const selectedFileName = document.getElementById('selectedFileName');
  
  if (fileInput.files.length > 0) {
    selectedFileName.textContent = fileInput.files[0].name;
  } else {
    selectedFileName.textContent = "";
  }
}

function uploadCSV() {
  const fileInput = document.getElementById('csvFileInput');

  if (fileInput.files.length === 0) {
    alert('Please select a file.');
    return;
  }  

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('csvFile', file);

  // Show the loading indicator
  // const loadingIndicator = document.getElementById('loadingIndicator');
  // loadingIndicator.style.display = 'block';

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
      console.error('There was a problem:', error);
      alert('An error occurred during the process.');
  })
  // .finally(() => {
  //     // Hide the loading indicator regardless of success or error
  //     loadingIndicator.style.display = 'none';
  // });
}

