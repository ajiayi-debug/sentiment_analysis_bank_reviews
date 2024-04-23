// Function to fetch data from the API
function fetchCustomerReviews() {
  return fetch("http://localhost:3000/customer_review")
    .then((response) => response.json())
    .then((data) => {
      const reviews = data.map((row) => {
        const { score, content, date, sentiment, keywords, replyContent, generatedReply } = row;
        
        const formattedKeywords = keywords ? keywords.split(" ").join(", ") : keywords;

        return {
          score,
          content,
          date,
          sentiment,
          keywords : formattedKeywords,
          replyContent,
          generatedReply,
        };
      });

      return reviews;
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
      return [];
    });
}

// Function to filter data based on selected criteria
function filter(data) {
  const keywordInput = document.querySelector("#keywordInput").value.trim().toLowerCase();
  const replyKeywordInput = document.querySelector("#replyKeywordInput").value.trim().toLowerCase();
  const selectedScores = Array.from(document.querySelectorAll(".scoreButton.selected")).map((button) => button.dataset.score);

  const startDateInput = document.querySelector("#startDateInput").value.trim();
  const endDateInput = document.querySelector("#endDateInput").value.trim();

  return data.filter((entry) => {
    let passesFilter = true;

    // Keyword filter
    if (keywordInput) {
      passesFilter = passesFilter && filterByKeyword([entry], keywordInput).length > 0;
    }

    if (replyKeywordInput) {
      passesFilter = passesFilter && filterByReplyKeyword([entry], replyKeywordInput).length > 0;
    }

    // Score filter
    if (selectedScores.length > 0 && !selectedScores.includes(entry.score)) {
      const entryScore = String(entry.score); 
      passesFilter = passesFilter && selectedScores.includes(entryScore);
    }

    // Date filter
    if (startDateInput && endDateInput) {
      const entryDate = new Date(entry.date);
      const startDate = new Date(startDateInput);
      const endDate = new Date(endDateInput);
      endDate.setDate(endDate.getDate() + 1);

      passesFilter = passesFilter && entryDate >= startDate && entryDate <= endDate;
    }

    return passesFilter;
  });
}

// Function to filter data by keywords
function filterByKeyword(data, keyword) {
  const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(escapedKeyword, "i");
  return data.filter((entry) => regex.test(entry.keywords));
}

function filterByReplyKeyword(data, keyword) {
  const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(escapedKeyword, "i");
  return data.filter((entry) => regex.test(entry.generatedReply));
}

// Function to populate a table with reviews
function populateTable(data) {
  const tableBody = document.querySelector("#csvTable tbody");
  tableBody.innerHTML = ""; // Clear previous content
  data.forEach((review) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${review.score}</td>
      <td>${review.content}</td>
      <td>${review.date}</td>
      <td>${review.sentiment}</td>
      <td>${review.keywords}</td>
      <td>${review.replyContent}</td>
      <td>${review.generatedReply}</td>
    `;
    tableBody.appendChild(row);
  });
}

// Initial setup to fetch and display reviews
fetchCustomerReviews().then((reviews) => {
  // Populate the table with reviews
  populateTable(reviews);

  // Event listeners for filtering and other interactions
  document.querySelectorAll(".filter-option").forEach((option) => {
    option.addEventListener("input", () => {
      const filteredData = filter(reviews);
      populateTable(filteredData);
    });
  });

  document.querySelectorAll(".scoreButton").forEach((button) => {
    button.addEventListener("click", () => {
      button.classList.toggle("selected");
      const filteredData = filter(reviews);
      populateTable(filteredData);
    });
  });

  document.querySelector("#clearKeywordButton").addEventListener("click", () => {
    document.querySelector("#keywordInput").value = "";
    const filteredData = filter(reviews);
    populateTable(filteredData);
  });
});
