// Initialise Word Cloud
async function initWordCloud() {
  const scores = await fetchSummary();
  
  const chart = anychart.tagCloud(scores.map(word => ({
    x: word.text,
    value: word.size,
    category: word.category
  })));

  let palette = anychart.palettes.distinctColors();
  palette.items(
      ["#ff0000", "#00FF00"]
  );

  // Set chart container
  chart.background({fill: "#490c56"})
  chart.container('word-cloud');
  chart.angles([0])
  chart.palette(palette);
  chart.colorRange(true);
  chart.colorRange().length('80%');

  // Draw the chart
  chart.draw();
}

// Function to fetch summary data from the server and process it into a word map
async function fetchSummary() {
const response = await fetch('http://localhost:3000/summary');
const data = await response.json();

const wordMap = {};

data.forEach((item) => {
  const { keyword, count, sentiment } = item;
  const keywordList = keyword.split(" ");

  keywordList.forEach((word) => {
    if (word.trim() !== "") {
      const cleanedWord = word.trim().toLowerCase(); 

      if (wordMap[cleanedWord]) {
        wordMap[cleanedWord].size += count; 
      } else {
        wordMap[cleanedWord] = { text: cleanedWord, size: count, category: sentiment };
      }
    }
  });
});

const scores = Object.values(wordMap);

return scores;
}

// Call initialise Word Cloud function
anychart.onDocumentReady(() => {
initWordCloud(); 
});