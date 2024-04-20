let parsedData;

// Fetch CSV data
fetch('customer.csv')
    .then(response => response.text())
    .then(data => {
        // Parse CSV data
        const rows = data.trim().split('\n');
        const headers = rows.shift().split(',');
        parsedData = rows.map(row => {
            const values = row.split(',');
            return headers.reduce((object, header, index) => {
                object[header.trim()] = values[index].trim();
                return object;
            }, {});
        });

        // Process initial data for charts
        updateCharts(parsedData);
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
                backgroundColor: label === 'POSITIVE' ? 'rgba(255, 99, 132, 0.5)' : 'rgba(54, 162, 235, 0.5)',
                borderColor: label === 'POSITIVE' ? 'rgba(255, 99, 132, 1)' : 'rgba(54, 162, 235, 1)',
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
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                    'rgba(255, 159, 64, 0.5)'
                ]
            }]
        }
    });
}


