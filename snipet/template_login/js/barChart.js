// chart.js
function drawBarChart(chart_id, data){
    // CSV状のデータを改行を区切りに1次元配列に割る
    var csvData = [];
    var lines = data.split("\n");
    for (var i = 0; i<lines.length; ++i){
        var cells = lines[i].split(",");
        csvData.push(cells);
    }
    // ラベル用とデータ用の配列に割る
    var temp = {label: [], data: []};
    for (var row in csvData){
        temp.label.push(csvData[row][0]);
        temp.data.push(csvData[row][1]);
    }
    var ctx = document.getElementById(chart_id).getContext("2d");
    var cht = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: temp.label,
            datasets: [{
                data: temp.data
            }]
        },
        options: {
            responsive: false,
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    gridLines: {
                        display: false
                    }
                }],
                yAxes: [{
                    gridLines: {
                        borderDash: [5, 5]
                    }
                }],
            }
        }
    });
}