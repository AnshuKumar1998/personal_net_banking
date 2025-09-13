document.addEventListener('DOMContentLoaded', () => {
    const ctxEl = document.getElementById('profitChart');

    if (!ctxEl) {
        console.warn('profitChart canvas not found, chart will not render');
        return;
    }

    // Set canvas height manually
    ctxEl.height = 300; // adjust as needed

    // Show loader
    if (typeof dvloader === 'function') dvloader('show');

    fetch('/api/profit-data/')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (!data || !Array.isArray(data) || data.length === 0) {
                console.warn('No profit data available');
                alert('No profit data available to display.');
                return;
            }

            const months = data.map(item => item.month);
            const profits = data.map(item => item.profit);

            const ctx = ctxEl.getContext('2d');

            if (ctxEl.chartInstance) ctxEl.chartInstance.destroy();

            ctxEl.chartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Profit',
                        data: profits,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderWidth: 2,
                        fill: true,
                        pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: value => '₹ ' + value,
                                color: '#fff' // white text
                            },
                            grid: { color: 'rgba(255,255,255,0.2)' }
                        },
                        x: {
                            ticks: { color: '#fff' }, // white text
                            grid: { color: 'rgba(255,255,255,0.2)' }
                        }
                    },
                    plugins: {
                        legend: { labels: { color: '#fff' } }, // white legend
                        tooltip: {
                            callbacks: {
                                label: context => {
                                    let label = context.dataset.label || '';
                                    if (label) label += ': ';
                                    label += '₹ ' + context.parsed.y;
                                    return label;
                                }
                            }
                        }
                    },
                    elements: {
                        point: { radius: 5, hoverRadius: 7 }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching profit data:', error);
            alert('Unable to load profit chart data.');
        })
        .finally(() => {
            if (typeof dvloader === 'function') dvloader('hide');
        });
});
