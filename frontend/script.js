const API_URL = "http://127.0.0.1:8000";

let energyChart = null;


// =================================================
// Load Latest Data
// =================================================

async function loadLatestData() {

    try {

        const response = await fetch(
            `${API_URL}/readings`
        );

        if (!response.ok) {
            throw new Error("Failed to fetch energy data");
        }

        const readings = await response.json();

        if (readings.length === 0) {
            console.log("No energy readings available.");
            return;
        }

        const latest = readings[0];


        // =================================================
        // Current Dashboard
        // =================================================

        document.getElementById("windSpeed").textContent =
            `${Number(latest.wind_speed).toFixed(2)} m/s`;

        document.getElementById("generatedPower").textContent =
            `${Number(latest.generated_power).toFixed(2)} W`;

        document.getElementById("batteryLevel").textContent =
            `${Number(latest.battery_level).toFixed(0)}%`;

        document.getElementById("temperature").textContent =
            `${Number(latest.temperature).toFixed(2)} °C`;

        document.getElementById("efficiency").textContent =
            `${Number(latest.efficiency).toFixed(0)}%`;

        document.getElementById("loadStatus").textContent =
            latest.load_status;


        // =================================================
        // Flap Angles
        // =================================================

        document.getElementById("flap1").textContent =
            `${Number(latest.flap_1_angle).toFixed(0)}°`;

        document.getElementById("flap2").textContent =
            `${Number(latest.flap_2_angle).toFixed(0)}°`;

        document.getElementById("flap3").textContent =
            `${Number(latest.flap_3_angle).toFixed(0)}°`;


        // =================================================
        // Recommendation
        // =================================================

        document.getElementById("recommendation").textContent =
            latest.recommendation;


        // =================================================
        // Smart Alert
        // =================================================

        updateSystemAlert(latest);


        // =================================================
        // Historical Graph
        // =================================================

        createEnergyChart(readings);


        // =================================================
        // AI Prediction
        // =================================================

        await loadAIPrediction();


        // =================================================
        // AI Model Performance
        // =================================================

        await loadAIPerformance();

    }

    catch (error) {

        console.error(
            "Error loading energy data:",
            error
        );

    }
}



// =================================================
// Smart System Alerts
// =================================================

function updateSystemAlert(data) {

    const alertElement =
        document.getElementById("systemAlert");

    if (!alertElement) {
        return;
    }


    const battery =
        Number(data.battery_level);

    const temperature =
        Number(data.temperature);

    const windSpeed =
        Number(data.wind_speed);


    if (battery < 20) {

        alertElement.textContent =
            "🔴 Critical: Battery level is very low.";

    }

    else if (temperature > 45) {

        alertElement.textContent =
            "🌡️ Warning: High temperature detected.";

    }

    else if (windSpeed < 3) {

        alertElement.textContent =
            "⚠️ Low wind speed: Power generation may be low.";

    }

    else {

        alertElement.textContent =
            "✅ System operating normally.";

    }

}



// =================================================
// AI Power Prediction
// =================================================

async function loadAIPrediction() {

    try {

        const response = await fetch(
            `${API_URL}/ai-prediction`
        );

        if (!response.ok) {
            throw new Error(
                "Failed to fetch AI prediction"
            );
        }

        const data = await response.json();


        const predictionElement =
            document.getElementById(
                "predictedPower"
            );


        if (!predictionElement) {
            return;
        }


        if (data.error) {

            predictionElement.textContent =
                "AI prediction unavailable.";

            return;
        }


        predictionElement.textContent =
            `${Number(data.predicted_power).toFixed(2)} W`;

    }

    catch (error) {

        console.error(
            "AI prediction error:",
            error
        );

    }

}



// =================================================
// AI Model Performance
// =================================================

async function loadAIPerformance() {

    try {

        const response = await fetch(
            `${API_URL}/ai-performance`
        );

        if (!response.ok) {

            throw new Error(
                "Failed to fetch AI model performance"
            );

        }


        const data = await response.json();


        if (data.error) {

            console.error(
                "AI performance error:",
                data.error
            );

            return;

        }


        // AI Model

        const modelElement =
            document.getElementById(
                "aiModel"
            );

        if (modelElement) {

            modelElement.textContent =
                data.model;

        }


        // Training Samples

        const trainingElement =
            document.getElementById(
                "trainingSamples"
            );

        if (trainingElement) {

            trainingElement.textContent =
                data.training_samples;

        }


        // Test Samples

        const testElement =
            document.getElementById(
                "testSamples"
            );

        if (testElement) {

            testElement.textContent =
                data.test_samples;

        }


        // MAE

        const maeElement =
            document.getElementById(
                "mae"
            );

        if (maeElement) {

            maeElement.textContent =
                `${Number(
                    data.mean_absolute_error
                ).toFixed(2)} W`;

        }


        // R² Score

        const r2Element =
            document.getElementById(
                "r2Score"
            );

        if (r2Element) {

            r2Element.textContent =
                Number(
                    data.r2_score
                ).toFixed(2);

        }

    }

    catch (error) {

        console.error(
            "AI performance error:",
            error
        );

    }

}



// =================================================
// Energy Performance Chart
// =================================================

function createEnergyChart(readings) {

    const canvas =
        document.getElementById(
            "energyChart"
        );

    if (!canvas) {
        return;
    }


    // Oldest → newest

    const chartReadings =
        [...readings].reverse();


    const labels =
        chartReadings.map(
            (reading, index) =>
                `Reading ${index + 1}`
        );


    const powerData =
        chartReadings.map(
            reading =>
                Number(
                    reading.generated_power
                )
        );


    const windData =
        chartReadings.map(
            reading =>
                Number(
                    reading.wind_speed
                )
        );


    const batteryData =
        chartReadings.map(
            reading =>
                Number(
                    reading.battery_level
                )
        );


    const efficiencyData =
        chartReadings.map(
            reading =>
                Number(
                    reading.efficiency
                )
        );


    // Destroy old chart

    if (energyChart !== null) {

        energyChart.destroy();

    }


    // Create chart

    energyChart =
        new Chart(
            canvas,
            {

                type: "line",

                data: {

                    labels: labels,

                    datasets: [

                        {

                            label:
                                "Generated Power (W)",

                            data:
                                powerData,

                            tension:
                                0.3,

                            borderWidth:
                                2

                        },


                        {

                            label:
                                "Wind Speed (m/s)",

                            data:
                                windData,

                            tension:
                                0.3,

                            borderWidth:
                                2

                        },


                        {

                            label:
                                "Battery Level (%)",

                            data:
                                batteryData,

                            tension:
                                0.3,

                            borderWidth:
                                2

                        },


                        {

                            label:
                                "Efficiency (%)",

                            data:
                                efficiencyData,

                            tension:
                                0.3,

                            borderWidth:
                                2

                        }

                    ]

                },


                options: {

                    responsive:
                        true,

                    maintainAspectRatio:
                        false,

                    interaction: {

                        mode:
                            "index",

                        intersect:
                            false

                    },


                    plugins: {

                        legend: {

                            display:
                                true

                        }

                    },


                    scales: {

                        x: {

                            title: {

                                display:
                                    true,

                                text:
                                    "Readings"

                            }

                        },


                        y: {

                            beginAtZero:
                                true,

                            title: {

                                display:
                                    true,

                                text:
                                    "Energy Data"

                            }

                        }

                    }

                }

            }
        );

}



// =================================================
// Initial Load
// =================================================

window.onload =
    loadLatestData;



// =================================================
// LIVE UPDATE EVERY 3 SECONDS
// =================================================

setInterval(
    loadLatestData,
    3000
);