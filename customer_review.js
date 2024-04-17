// JavaScript for fetching data from customer_review.csv and populating the table

// Fetch data from customer_review.csv
fetch('customer_reviews.csv')
  .then(response => response.text())
  .then(data => {
    // Parse CSV data
    const rows = data.split('\n').slice(1); // Skip header row
    const reviews = rows.map(row => {
      const [score, content, date, score_sentiment] = row.split(',');
      return { score, content, date, score_sentiment };
    });

    // Populate table with reviews
    const tableBody = document.querySelector('#csvTable tbody');
    reviews.forEach(review => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${review.score}</td>
        <td>${review.content}</td>
        <td>${review.date}</td>
        <td>${review.score_sentiment}</td>
      `;
      tableBody.appendChild(row);
    });
  })
  .catch(error => console.error('Error fetching data:', error));

  