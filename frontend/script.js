const API_BASE = "http://127.0.0.1:8000/planner";

async function getExtendedPlan() {
    const origin = document.getElementById("origin").value;
    const destination = document.getElementById("destination").value;
    const start_date = document.getElementById("start_date").value;
    const nights = parseInt(document.getElementById("nights").value);
    const travelers = parseInt(document.getElementById("travelers").value);

    const body = { origin, destination, start_date, nights, travelers, preferences: {} };

    const errorEl = document.getElementById("error");
    const itineraryEl = document.getElementById("itinerary");
    const weatherEl = document.getElementById("weather");
    const flightsEl = document.getElementById("flights");
    const aiEl = document.getElementById("ai_text");

    // Clear previous results
    errorEl.textContent = "";
    itineraryEl.innerHTML = "";
    weatherEl.innerHTML = "";
    flightsEl.innerHTML = "";
    aiEl.innerHTML = "";

    try {
        const res = await fetch(`${API_BASE}/plan_extended`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (!res.ok) {
            const errorData = await res.json();
            errorEl.textContent = `Error ${res.status}: ${errorData.detail || res.statusText}`;
            return;
        }

        const data = await res.json();

        // Itinerary
        itineraryEl.innerHTML = `<h3>Itinerary</h3><ul>${data.itinerary.map(item => `<li>${item}</li>`).join('')}</ul>`;

        // Weather
        if (data.weather && data.weather.current) {
            weatherEl.innerHTML = `
                <h3>Weather in ${destination}</h3>
                <p>${data.weather.current.temp_c}°C, ${data.weather.current.condition.text}</p>
                <img src="${data.weather.current.condition.icon}" alt="weather icon">
            `;
        }

        // Flights
        if (data.flights && Array.isArray(data.flights)) {
            let flightRows = data.flights.map(f => `
                <tr>
                    <td>${f.itineraries[0].segments[0].departure.iataCode}</td>
                    <td>${f.itineraries[0].segments[0].arrival.iataCode}</td>
                    <td>${f.itineraries[0].segments[0].carrierCode}</td>
                    <td>${f.price.total} ${f.price.currency}</td>
                </tr>
            `).join('');
            flightsEl.innerHTML = `
                <h3>Flights</h3>
                <table>
                    <tr><th>From</th><th>To</th><th>Airline</th><th>Price</th></tr>
                    ${flightRows}
                </table>
            `;
        }

        // AI suggestions
        aiEl.innerHTML = `<h3>AI Suggestions</h3><p>${data.ai_text}</p>`;

    } catch (err) {
        errorEl.textContent = "Network error: " + err.message;
    }
}
