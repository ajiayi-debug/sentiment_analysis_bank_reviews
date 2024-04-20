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
      console.log('File uploaded successfully:', data);
      // You can do something with the response from the backend here
  })
  .catch(error => {
      console.error('There was a problem with the file upload:', error);
  });
}
