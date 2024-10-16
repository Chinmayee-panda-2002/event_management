from flask import request, jsonify
from models import Event,Ticket  
from db import db  

def create_event():
    data = request.json  

 
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')
    time = data.get('time')
    location = data.get('location')
    price = data.get('price')

   
    new_event = Event(title=title, description=description, date=date, time=time, location=location, price=price)
    db.session.add(new_event)
    db.session.commit()

    return jsonify({"message": "Event created successfully", "event_id": new_event.id}), 201


def get_all_events():
    events = Event.query.all()  
    return jsonify([{
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.date.isoformat(),  
        "time": event.time.isoformat(),  
        "location": event.location,
        "price": event.price
    } for event in events]), 200



def delete_event():
    print("Received DELETE request")
    print("Request headers:", dict(request.headers))

    try:
        data = request.get_json(silent=True)
        print("Received data:", data)

        if not data:
            print("No JSON data received")
            return jsonify({"message": "No JSON data received"}), 400

        if 'event_id' not in data:
            print("No event_id in data")
            return jsonify({"message": "Missing event_id in request"}), 400

        event_id = data.get('event_id')
        print(f"Attempting to delete event with ID: {event_id}")

      
        event = Event.query.get(event_id)
        if not event:
            print(f"Event with id {event_id} not found")
            return jsonify({"message": f"Event with id {event_id} not found"}), 404

        db.session.delete(event)
        db.session.commit()
        print(f"Successfully deleted event {event_id}")
        return jsonify({"message": "Event deleted successfully"}), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        db.session.rollback()
        return jsonify({"message": f"Error deleting event: {str(e)}"}), 500


def edit_event(event_id):
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": f"Event with id {event_id} not found"}), 404

        data = request.get_json()

       
        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'date' in data:
            event.date = data['date']
        if 'time' in data:
            event.time = data['time']
        if 'location' in data:
            event.location = data['location']
        if 'price' in data:
            event.price = data['price']

        db.session.commit()

        
        return jsonify({
            "message": "Event updated successfully",
            "event": {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date,
                "time": event.time,
                "location": event.location,
                "price": event.price
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating event: {str(e)}"}), 500




def create_ticket():
    data = request.json
    event_id = data.get('event_id')
    user_id = data.get('user_id')
    price = data.get('price')

  
    existing_ticket = Ticket.query.filter_by(event_id=event_id, user_id=user_id).first()
    if existing_ticket:
        return jsonify({'success': False, 'message': 'Event already purchased', 'error': 'duplicate_ticket'}), 400

    new_ticket = Ticket(event_id=event_id, user_id=user_id, price=price, status='booked')

    try:
        db.session.add(new_ticket)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Ticket booked successfully!', 'ticket_id': new_ticket.id})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error booking ticket', 'error': 'database_error'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e), 'error': 'unknown_error'}), 500

def get_purchased_tickets(user_id):
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    purchased_event_ids = [ticket.event_id for ticket in tickets]

    
    purchased_events = Event.query.filter(Event.id.in_(purchased_event_ids)).all()

    
    events_data = []
    for event in purchased_events:
        events_data.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'), 
            'time': event.time.strftime('%H:%M'),     
            'location': event.location,
            'price': float(event.price), 

        })

    return jsonify(events_data)
