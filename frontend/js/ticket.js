// // Function to handle ticket purchase
// function buyTicket(eventId) {
//     const userId = getUserId(); // Assuming the user is already logged in

//     if (!userId) {
//         alert("Please login to purchase a ticket.");
//         window.location.href = 'login.html';
//         return;
//     }

//     fetch('http://localhost:3000/api/tickets/purchase', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ userId, eventId })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.error) {
//             alert(`Error purchasing ticket: ${data.error}`);
//         } else {
//             alert('Ticket purchased successfully!');
//             // Optionally redirect or update UI here
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('Error purchasing ticket.');
//     });
// }

// // Helper function to get logged-in user ID from local storage or cookies
// function getUserId() {
//     // Replace this with the actual method of storing user data (e.g., from a JWT token or session)
//     return localStorage.getItem('userId');
// }
