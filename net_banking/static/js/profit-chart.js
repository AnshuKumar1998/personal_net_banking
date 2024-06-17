document.addEventListener('DOMContentLoaded', (event) => {
    fetch('/api/profit-data/')
        .then(response => response.json())
        .then(data => {
            const months = data.map(item => item.month);
            const profits = data.map(item => item.profit);

            const ctx = document.getElementById('profitChart').getContext('2d');
            const profitChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Profit',
                        data: profits,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)', // Line fill color
                        borderWidth: 2,
                        fill: true, // Fill the area under the line
                        pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                callback: function(value) {
                                    return '₹ ' + value;
                                },
                                color: '#ecf0f1'
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: '#ecf0f1'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#ecf0f1'
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    label += '₹ ' + context.parsed.y;
                                    return label;
                                }
                            }
                        }
                    },
                    elements: {
                        point: {
                            radius: 5,
                            hoverRadius: 7
                        }
                    }
                }
            });
        });
});
