var socket = io.connect('http://localhost:5000');
socket.on('connect', function() {
    console.log('Connected to the server');
});

var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Sensor Data',
            data: [],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

socket.on('device-data', function(data) {
    console.log('Received data: ' + data);
    var jsonData = JSON.parse(data);
    console.log(jsonData.value);

    if (chart.data.labels.length >= 20) {
        chart.data.labels.shift(); // remove the first label
        chart.data.datasets[0].data.shift(); // remove the first data point
    }

    // Agrega el valor del sensor a la gráfica
    chart.data.labels.push(new Date().toLocaleTimeString());
    chart.data.datasets[0].data.push(parseFloat(jsonData.value));
    chart.update();
});

function sendMessage() {
    var message = {
        "text": "Hello, world!",
        "timestamp": Date.now()
    };
    socket.emit('message', message);
}