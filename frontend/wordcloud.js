// word cloud
async function initWordCloud() {
    //sample data
    const scores = await fetchSummary();
    
    const words = [
        { text: "easy", size: 21 ,category: "positive"},
        { text: "unable", size: 17 ,category: "negative" },
        { text: "savings", size: 10, category: "positive" },
        { text: "friendly", size: 8 , category: "positive"},
        { text: "singpass", size: 17, category: "negative"},
        { text: "fast", size: 5 , category: "positive"},
        { text: "error", size: 6, category: "negative"},
        { text: "waste", size: 3, category: "negative"},
        { text: "stuck", size: 4, category: "negative"}
  
    ];
    const chart = anychart.tagCloud(scores.map(word => ({
      x: word.text,
      value: word.size,
      category: word.category
    })));
  
    let palette = anychart.palettes.distinctColors();
    palette.items(
        ["#00FF00", "#ff0000", "#ffffff"]
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

anychart.onDocumentReady(() => {
  initWordCloud(); 
});