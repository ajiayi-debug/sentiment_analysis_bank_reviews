fetch('http://localhost:3000/')
  .then(response => response.json())
  .then(data => {
    // Parse CSV data
    // const rows = data.split('\n').slice(1); // Skip header row
    // const reviews = rows.map(row => {
    //   const [score, content, date, score_sentiment] = row.split(',');
    //   return { score, content, date, score_sentiment };
    // });

    // Populate table with reviews
    const tableBody = document.querySelector('#csvTable tbody');
    data.forEach(review => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${review.score}</td>
        <td>${review.content}</td>
        <td>${review.date}</td>
        <td>${review.score_sentiment}</td>
        <td>${review.replyContent}</td>
      `;
      tableBody.appendChild(row);
    });
  })
  .catch(error => console.error('Error fetching data:', error));

  