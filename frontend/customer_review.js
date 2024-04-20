// Fetch data from customer.csv
fetch('customer.csv')
  .then(response => response.text())
  .then(data => {
    // Parse CSV data
    const rows = data.split('\n').slice(1); // Skip header row
    const reviews = rows.map(row => {
      const [score, content, date, score_sentiment, keywords, generatedReply] = row.split(',');
      return { score, content, date, score_sentiment, keywords, generatedReply };
    });

// Function to filter data based on selected criteria
function filter(data) {
  const keywordInput = document.querySelector('#keywordInput').value.trim().toLowerCase();
  const selectedScores = Array.from(document.querySelectorAll('.scoreButton.selected')).map(button => button.dataset.score);

  const startDateInput = document.querySelector('#startDateInput').value.trim();
  const endDateInput = document.querySelector('#endDateInput').value.trim();

  return data.filter(entry => {
    let passesFilter = true;

    if (keywordInput) {
      passesFilter = passesFilter && filterByKeyword([entry], keywordInput).length > 0;
    }

    if (selectedScores.length > 0 && !selectedScores.includes(entry.score)) {
      passesFilter = false;
    }

    if (startDateInput && endDateInput) {
      const entryDate = new Date(entry.date);
      const startDate = new Date(startDateInput);
      const endDate = new Date(endDateInput);

      passesFilter = passesFilter && entryDate >= startDate && entryDate <= endDate;
    }

    return passesFilter;
  });
}

// Function to filter data by keywords
function filterByKeyword(data, keyword) {
  const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(escapedKeyword, 'i');
  return data.filter(entry => regex.test(entry.content));
}


// Function to populate table with reviews
function populateTable(data) {
  const tableBody = document.querySelector('#csvTable tbody');
  tableBody.innerHTML = ''; // Clear previous content
  data.forEach(review => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${review.score}</td>
      <td>${review.content}</td>
      <td>${review.date}</td>
      <td>${review.score_sentiment}</td>
      <td>${review.keywords}</td>
      <td>${review.generatedReply}</td>
    `;
    tableBody.appendChild(row);
  });
}

// Populate table with reviews initially
populateTable(reviews);

// Function to handle filter option clicks
document.querySelectorAll('.filter-option').forEach(option => {
  option.addEventListener('input', handleFiltering);
});

// Function to handle dynamic filtering
function handleFiltering() {
  const filteredData = filter(reviews);
  populateTable(filteredData);
}

// Function to handle score button clicks
document.querySelectorAll('.scoreButton').forEach(button => {
  button.addEventListener('click', () => {
    button.classList.toggle('selected');
    handleFiltering();
  });
});

// Add event listener to clear keyword button
document.querySelector('#clearKeywordButton').addEventListener('click', () => {
document.querySelector('#keywordInput').value = ''; // Clear keyword input
handleFiltering(); // Apply filtering
});
})

  .catch(error => console.error('Error fetching data:', error));