#!/usr/bin/env python3
import csv
import os
from datetime import datetime, timedelta

DATA_FILE = "greenhouse_data.csv"
PORT = 8080

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Greenhouse Monitoring</title>
    <meta http-equiv="refresh" content="300"> <!-- Refresh every 5 minutes -->
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background-color: #f5f5f5;
        }}
        h1, h2, h3 {{ 
            color: #2c3e50; 
            text-align: center; 
        }}
        .container {{ 
            max-width: 900px; 
            margin: 0 auto; 
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .reading-box {{ 
            background-color: #ecf0f1; 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 20px;
            text-align: center;
            font-size: 1.2em;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }}
        .stat-box {{
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #e9ecef;
        }}
        .stat-value {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #7f8c8d;
        }}
        .chart-container {{
            margin: 20px 0;
            height: 300px;
        }}
        .time-selector {{
            text-align: center;
            margin-bottom: 15px;
        }}
        .time-selector button {{
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            padding: 8px 15px;
            margin: 0 5px;
            border-radius: 5px;
            cursor: pointer;
        }}
        .time-selector button.active {{
            background-color: #3498db;
            color: white;
            border-color: #2980b9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .timestamp {{ 
            color: #7f8c8d; 
            text-align: center; 
            margin-top: 20px; 
            font-size: 0.8em; 
        }}
        .temperature {{
            color: #e74c3c;
        }}
        .humidity {{
            color: #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Greenhouse Monitoring Dashboard</h1>
        
        <!-- Current Readings -->
        <h2>Current Conditions</h2>
        <div class="reading-box">
            <div class="temperature">{current_temp_c}°C ({current_temp_f}°F)</div>
            <div class="humidity">Humidity: {current_humidity}%</div>
            <div style="font-size: 0.8em; margin-top: 10px; color: gray;">
                Last reading: {last_reading_time}
            </div>
        </div>
        
        <!-- Charts -->
        <h2>Monitoring Charts</h2>
        <div class="time-selector">
            <button id="btn-12h" onclick="changeTimeframe('12h')" class="active">12 Hours</button>
            <button id="btn-24h" onclick="changeTimeframe('24h')">24 Hours</button>
            <button id="btn-3d" onclick="changeTimeframe('3d')">3 Days</button>
            <button id="btn-7d" onclick="changeTimeframe('7d')">7 Days</button>
            <button id="btn-30d" onclick="changeTimeframe('30d')">30 Days</button>
            <button id="btn-all" onclick="changeTimeframe('all')">All Data</button>
        </div>
        <div class="chart-container">
            <canvas id="tempChart"></canvas>
        </div>
        <div class="chart-container">
            <canvas id="humidityChart"></canvas>
        </div>
        
        <!-- Statistics -->
        <h2>Statistics (Last 24 Hours)</h2>
        <div class="stat-grid">
            <div class="stat-box">
                <div class="stat-value temperature">{min_temp}°C</div>
                <div class="stat-label">Min Temperature</div>
            </div>
            <div class="stat-box">
                <div class="stat-value temperature">{avg_temp}°C</div>
                <div class="stat-label">Avg Temperature</div>
            </div>
            <div class="stat-box">
                <div class="stat-value temperature">{max_temp}°C</div>
                <div class="stat-label">Max Temperature</div>
            </div>
            <div class="stat-box">
                <div class="stat-value humidity">{min_humidity}%</div>
                <div class="stat-label">Min Humidity</div>
            </div>
            <div class="stat-box">
                <div class="stat-value humidity">{avg_humidity}%</div>
                <div class="stat-label">Avg Humidity</div>
            </div>
            <div class="stat-box">
                <div class="stat-value humidity">{max_humidity}%</div>
                <div class="stat-label">Max Humidity</div>
            </div>
        </div>
        
        <!-- Recent Readings Table -->
        <h2>Recent Readings</h2>
        <table>
            <tr>
                <th>Time</th>
                <th>Temperature</th>
                <th>Humidity</th>
            </tr>
            {table_rows}
        </table>
        
        <p class="timestamp">Dashboard updated: {current_time}</p>
    </div>
    
    <script>
        // All the chart data
        const allChartData = {{
            // 12 hour data
            '12h': {{
                labels: {chart_labels_12h},
                tempData: {temp_data_12h},
                humidityData: {humidity_data_12h}
            }},
            // 24 hour data
            '24h': {{
                labels: {chart_labels_24h},
                tempData: {temp_data_24h},
                humidityData: {humidity_data_24h}
            }},
            // 3 day data
            '3d': {{
                labels: {chart_labels_3d},
                tempData: {temp_data_3d},
                humidityData: {humidity_data_3d}
            }},
            // 7 day data
            '7d': {{
                labels: {chart_labels_7d},
                tempData: {temp_data_7d},
                humidityData: {humidity_data_7d}
            }},
            // 30 day data
            '30d': {{
                labels: {chart_labels_30d},
                tempData: {temp_data_30d},
                humidityData: {humidity_data_30d}
            }},
            // All data
            'all': {{
                labels: {chart_labels_all},
                tempData: {temp_data_all},
                humidityData: {humidity_data_all}
            }}
        }};
        
        // Format for X-axis labels based on timeframe
        const timeframeLabelFormats = {{
            '12h': 'HH:MM',
            '24h': 'HH:MM',
            '3d': 'MM-DD HH:MM',
            '7d': 'MM-DD',
            '30d': 'MM-DD',
            'all': 'MM-DD'
        }};
        
        // Create the charts
        let tempChart, humidityChart;
        
        function initCharts() {{
            // Temperature chart
            const tempCtx = document.getElementById('tempChart').getContext('2d');
            tempChart = new Chart(tempCtx, {{
                type: 'line',
                data: {{
                    labels: allChartData['12h'].labels,
                    datasets: [{{
                        label: 'Temperature (°C)',
                        data: allChartData['12h'].tempData,
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'Temperature Over Time (12 Hours)'
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: false,
                            title: {{
                                display: true,
                                text: 'Temperature (°C)'
                            }}
                        }},
                        x: {{
                            title: {{
                                display: true,
                                text: 'Time'
                            }}
                        }}
                    }}
                }}
            }});
            
            // Humidity chart
            const humidityCtx = document.getElementById('humidityChart').getContext('2d');
            humidityChart = new Chart(humidityCtx, {{
                type: 'line',
                data: {{
                    labels: allChartData['12h'].labels,
                    datasets: [{{
                        label: 'Humidity (%)',
                        data: allChartData['12h'].humidityData,
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        title: {{
                            display: true,
                            text: 'Humidity Over Time (12 Hours)'
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: false,
                            title: {{
                                display: true,
                                text: 'Humidity (%)'
                            }}
                        }},
                        x: {{
                            title: {{
                                display: true,
                                text: 'Time'
                            }}
                        }}
                    }}
                }}
            }});
        }}
        
        // Function to change the timeframe
        function changeTimeframe(timeframe) {{
            // Update active button
            document.querySelectorAll('.time-selector button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            document.getElementById(`btn-${{timeframe}}`).classList.add('active');
            
            // Get data for the selected timeframe
            const data = allChartData[timeframe];
            
            // Update temperature chart
            tempChart.data.labels = data.labels;
            tempChart.data.datasets[0].data = data.tempData;
            tempChart.options.plugins.title.text = `Temperature Over Time (${{getTimeframeText(timeframe)}})`;
            tempChart.update();
            
            // Update humidity chart
            humidityChart.data.labels = data.labels;
            humidityChart.data.datasets[0].data = data.humidityData;
            humidityChart.options.plugins.title.text = `Humidity Over Time (${{getTimeframeText(timeframe)}})`;
            humidityChart.update();
        }}
        
        // Helper function to get timeframe text
        function getTimeframeText(timeframe) {{
            switch(timeframe) {{
                case '12h': return '12 Hours';
                case '24h': return '24 Hours';
                case '3d': return '3 Days';
                case '7d': return '7 Days';
                case '30d': return '30 Days';
                case 'all': return 'All Time';
                default: return timeframe;
            }}
        }}
        
        // Initialize charts when the page loads
        window.onload = function() {{
            initCharts();
        }};
    </script>
</body>
</html>
"""

class DataReader:
    @staticmethod
    def read_csv_data(filename):
        """Read data from the CSV file and return as a list of dictionaries"""
        if not os.path.exists(filename):
            return []

        data = []
        try:
            with open(filename, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []

        return data

    @staticmethod
    def get_current_reading(data):
        """Get the most recent reading from the data"""
        if not data:
            return None
        return data[-1]

    @staticmethod
    def parse_timestamp(ts_str):
        """Parse timestamp string to datetime object"""
        try:
            return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.now()

    @staticmethod
    def get_timeframe_data(data, hours=None):
        """Filter data to only include readings from the last n hours, or all if hours is None"""
        if not data or hours is None:
            return data

        now = datetime.now()
        cutoff = now - timedelta(hours=hours)

        return [
            row for row in data if DataReader.parse_timestamp(row["timestamp"]) > cutoff
        ]
