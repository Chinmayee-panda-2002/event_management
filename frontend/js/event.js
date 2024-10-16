// Add event listener for the event form submission
document.getElementById('eventForm')?.addEventListener('submit', function (e) {
    e.preventDefault();

    const eventId = document.getElementById('event-id').value;
    const event = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        location: document.getElementById('location').value,
        price: document.getElementById('price').value
    };

    const url = eventId
        ? `http://localhost:5000/events/${eventId}`
        : 'http://localhost:5000/create';

    const method = eventId ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(event)
    })
        .then(response => response.json())
        .then(data => {
            alert(eventId ? 'Event updated successfully!' : 'Event created successfully!');
            window.location.href = 'dashboard.html'; // Redirect to dashboard after successful operation
        })
        .catch(error => console.error('Error:', error));
});

// Global variables to hold fetched events and purchased events
let events = [];
let purchasedEvents = [];

// Load events from the server and then fetch purchased tickets
function loadEvents() {
    const userId = localStorage.getItem('userId');
    if (!userId) {
        console.error('No user ID found in local storage. User might not be logged in.');
        return;
    }

    Promise.all([
        fetch('http://localhost:5000/events').then(response => response.json()),
        fetch(`http://127.0.0.1:5000/user/${userId}/tickets`).then(response => response.json())
    ])
    .then(([eventsData, purchasedEventsData]) => {
        events = eventsData;
        purchasedEvents = purchasedEventsData;
        displayEvents(events);
        displayPurchasedEvents();
    })
    .catch(error => console.error('Error loading data:', error));
}

// Display all events on the page
function displayEvents(eventsToDisplay) {
    const eventList = document.getElementById('dashboard');
    eventList.innerHTML = ''; // Clear existing content

    eventsToDisplay.forEach(event => {
        const eventCard = createEventCard(event);
        eventList.appendChild(eventCard);
    });
}

// Display purchased events
function displayPurchasedEvents() {
    const purchasedEventsList = document.getElementById('purchased-events');
    purchasedEventsList.innerHTML = ''; // Reset content

    if (purchasedEvents.length === 0) {
        purchasedEventsList.innerHTML = '<p>No purchased events yet.</p>';
    } else {
        purchasedEvents.forEach(event => {
            const eventCard = createEventCard(event, true);
            purchasedEventsList.appendChild(eventCard);
        });
    }
}

// Create an event card
function createEventCard(event, isPurchased = false) {
    const eventCard = document.createElement('div');
    eventCard.className = 'event-card';
    eventCard.setAttribute('data-event-id', event.id);

    eventCard.innerHTML = `
        
        <div class="event-content">
            <h3 class="event-title">${event.title}</h3>
            <p class="event-date">Date: ${event.date}</p>
            <p class="event-time">Time: ${event.time}</p>
            <p class="event-location">Location: ${event.location}</p>
            <p class="event-price">Price: $${event.price}</p>
            <p class="event-description">${event.description}</p>
            ${isPurchased ?
                '<p class="purchase-status">Purchased</p>' :
                `<a href="#" class="event-button" data-event-id="${event.id}">Buy Ticket</a>`
            }
        </div>
    `;

    if (!isPurchased) {
        const buyTicketButton = eventCard.querySelector('.event-button');
        buyTicketButton.addEventListener('click', (e) => {
            e.preventDefault();
            buyTicket(event.id, event.price);
        });
    }

    return eventCard;
}

// Filter events based on search input
function filterEvents() {
    const searchTerm = document.getElementById('search-bar').value.toLowerCase();
    const filteredEvents = events.filter(event => {
        return (
            event.title.toLowerCase().includes(searchTerm) ||
            event.description.toLowerCase().includes(searchTerm) ||
            event.location.toLowerCase().includes(searchTerm)
        );
    });
    displayEvents(filteredEvents);
}

// Function to buy a ticket for a specific event
function buyTicket(eventId, price) {
    const userId = localStorage.getItem('userId');

    if (!userId) {
        alert('You must be logged in to purchase a ticket.');
        return;
    }

    const ticketData = {
        event_id: eventId,
        user_id: userId,
        price: price,
        status: 'booked'
    };

    fetch('http://127.0.0.1:5000/tickets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(ticketData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Ticket purchased successfully!');
            loadEvents();
        } else {
            if (data.error === 'duplicate_ticket') {
                alert('You have already purchased a ticket for this event.');
            } else {
                alert('Failed to purchase ticket: ' + data.message);
            }
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while purchasing the ticket. Please try again.');
    });
}


document.addEventListener('DOMContentLoaded', loadEvents);


document.getElementById('search-bar').addEventListener('keyup', filterEvents);