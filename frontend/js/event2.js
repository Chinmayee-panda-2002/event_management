function loadEvents() {
    fetch('http://localhost:5000/events')
        .then(response => response.json())
        .then(events => {
            const dashboard = document.getElementById('dashboard');
            dashboard.innerHTML = ''; // Clear any existing content

            events.forEach(event => {
                const eventCard = document.createElement('div');
                eventCard.className = 'event-card';
                eventCard.innerHTML = `
                    
                    <div class="event-content">
                        <h2 class="event-title">${event.title}</h2>
                        <p class="event-date">Date: ${event.date}</p>
                        <p class="event-time">Time: ${event.time}</p>
                        <p class="event-location">Location: ${event.location}</p>
                        <p class="event-price">Price: $${event.price}</p>
                        <p class="event-description">${event.description}</p>
                        <button onclick="editEvent(${event.id}, '${encodeURIComponent(event.title)}', '${encodeURIComponent(event.description)}', '${event.date}', '${event.time}', '${encodeURIComponent(event.location)}', ${event.price})">Edit</button>
                        <button onclick="deleteEvent(${event.id})">Delete</button>
                    </div>
                `;
                dashboard.appendChild(eventCard);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Add the editEvent function here
function editEvent(id, title, description, date, time, location, price) {
    const url = `create-event.html?id=${id}&title=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}&date=${date}&time=${time}&location=${encodeURIComponent(location)}&price=${price}`;
    window.location.href = url;
}

function deleteEvent(eventId) {
    console.log('Attempting to delete event with ID:', eventId);
    console.log('Type of eventId:', typeof eventId);

    if (!eventId && eventId !== 0) {
        console.error('Event ID is undefined or null');
        alert('Cannot delete event: Invalid event ID');
        return;
    }

    const payload = { event_id: eventId };
    const stringifiedPayload = JSON.stringify(payload);

    fetch('http://localhost:5000/events', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: stringifiedPayload
    })
    .then(async response => {
        console.log('Response status:', response.status);
        const textResponse = await response.text();
        console.log('Response text:', textResponse);

        let jsonResponse;
        try {
            jsonResponse = JSON.parse(textResponse);
        } catch (e) {
            throw new Error(`Server response was not JSON: ${textResponse}`);
        }

        if (!response.ok) {
            throw new Error(jsonResponse.message || 'Unknown error occurred');
        }

        alert('Event deleted successfully');
        loadEvents();
    })
    .catch(error => {
        console.error('Error deleting event:', error);
        alert(`Error deleting event: ${error.message}`);
    });
}
// Initialize event fetching
document.addEventListener('DOMContentLoaded', loadEvents);
