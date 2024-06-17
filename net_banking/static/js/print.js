function printTable() {
    var printContents = document.getElementById('transaction-table').outerHTML;
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = `
        <html>
            <head>
                <title>Print Transaction Statement</title>
                <style>
                    @media print {
                        @page {
                            size: landscape;
                        }
                        body {
                            font-family: Arial, sans-serif;
                            margin: 20px;
                        }
                        table {
                            width: 100%;
                            border-collapse: collapse;
                        }
                        table, th, td {
                            border: 1px solid black;
                        }
                        th, td {
                            padding: 8px;
                            text-align: left;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                    }
                </style>
            </head>
            <body>
                <h4>Transaction History</h4>
                ${printContents}
            </body>
        </html>`;

    window.print();
    document.body.innerHTML = originalContents;
}

