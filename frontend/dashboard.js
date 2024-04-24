let parsedData;

// Fetch CSV data
fetch('http://localhost:3000/customer_review')
    .then(response => response.json())
    .then(data => {
        const reviews = data.map((item) => {
            const { score, content, date, sentiment, keywords, generatedReply } = item;
    
            const formattedKeywords = keywords ? keywords.split(" ").join(", ") : "";
            const dateObj = new Date(date);

            const formattedDate = `${dateObj.getFullYear()}-${String(dateObj.getMonth() + 1).padStart(2, "0")}`;

            return {
              score,
              content,
              date : formattedDate,
              sentiment,
              keywords: formattedKeywords,
              generatedReply,
            };
          });

        // Process initial data for charts
        updateCharts(reviews);
        updateCount(reviews.length);
    })
    .catch(error => console.error('Error fetching CSV:', error));

fetch('http://localhost:3000/summary')
    .then(response => response.json())
    .then(data => {
        const scores = data.map((item) => {
            const { netSentiment } = item;

            return {netSentiment};
        });
        
        const score = scores.length > 1 ? scores[0].netSentiment : 0;
        updateNetSentimentScore(score);
    })
    .catch(error => console.error('Error fetching CSV:', error));

// Function to update charts with data
function updateCharts(data) {
    // Process data for sentiment chart
    const sentimentLabels = ['POSITIVE', 'NEGATIVE'];
    const sentimentData = {
        'POSITIVE': 0,
        'NEGATIVE': 0
    };

    // Process data for date-based sentiment chart
    const dateSentimentData = {};

    data.forEach(entry => {
        const sentiment = entry.sentiment;
        const date = entry.date;

        // Count sentiment occurrences
        if (sentiment === 'POSITIVE') {
            sentimentData['POSITIVE']++;
        } else if (sentiment === 'NEGATIVE') {
            sentimentData['NEGATIVE']++;
        }

        // Extract year and month from date
        const [year, month] = date.split('-');
        const formattedDate = `${year}-${month}`;

        // Group sentiment by year and month
        if (!dateSentimentData[formattedDate]) {
            dateSentimentData[formattedDate] = {
                'POSITIVE': 0,
                'NEGATIVE': 0
            };
        }

        dateSentimentData[formattedDate][sentiment]++;
    });

    // Sort dates in ascending order
    const sortedDates = Object.keys(dateSentimentData).sort();

    // Update sentiment chart with data
    const sentimentChartDiv = document.getElementById('bar-chart');
    const sentimentChart = new Chart(sentimentChartDiv, {
        type: 'bar',
        data: {
            labels: sortedDates,
            datasets: sentimentLabels.map(label => ({
                label: label,
                data: sortedDates.map(date => dateSentimentData[date][label]),
                backgroundColor: label === 'NEGATIVE' ? 'rgba(255, 99, 132, 0.5)' : 'rgba(54, 162, 235, 0.5)',
                borderColor: label === 'NEGATIVE' ? 'rgba(255, 99, 132, 1)' : 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }))
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Process data for pie chart (scores)
    const scoreLabels = [];
    const scoreData = {};

    data.forEach(entry => {
        const score = entry.score;
        if (!scoreData[score]) {
            scoreData[score] = 1;
        } else {
            scoreData[score]++;
        }
    });

    // Update pie chart with data
    const scoreChartDiv = document.getElementById('pie-chart');
    const scoreChart = new Chart(scoreChartDiv, {
        type: 'pie',
        data: {
            labels: Object.keys(scoreData),
            datasets: [{
                data: Object.values(scoreData),
                backgroundColor: [
                    'rgba(255, 9, 9, 0.9)',
                    'rgba(255, 78, 17, 1)',
                    'rgba(255, 142, 21, 1)',
                    'rgba(250, 183, 51, 1)',
                    'rgba(172, 179, 52, 1)',
                ]
            }]
        }
    });
}

function updateCount(count){
    const element = document.querySelector(".review-count"); 
    element.textContent = count;
}

function updateNetSentimentScore(score){
    const element = document.querySelector(".sentiment-score"); 
    element.textContent = parseFloat(score.toFixed(2));;
}