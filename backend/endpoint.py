from flask import Blueprint
from sso import signup, login, admin_login,forgot_password
from event import create_event, delete_event, get_all_events, edit_event, create_ticket, get_purchased_tickets

endpoint = Blueprint("endpoint", __name__)

# Authentication
@endpoint.route("/signup", methods=["POST"])
def signupp():
    return signup()

@endpoint.route("/login", methods=["POST"])
def loginn():
    return login()

@endpoint.route("/create", methods=["POST"])
def create():
    return create_event()

@endpoint.route('/events', methods=['DELETE']) # Changed to 'delete'
def delete():

    return delete_event()

@endpoint.route('/events', methods=['GET'])  # Change to 'GET' for retrieving events
def get():
    return get_all_events()


@endpoint.route('/events/<int:event_id>', methods=['PUT']) # Change to 'PUT' for updating
def update(event_id):
    return edit_event(event_id)

@endpoint.route("/admin_login", methods=["POST"])
def adminloginn():
    return admin_login()

@endpoint.route('/forgot-password', methods=['POST'])
def forgot_passwordd():
    return forgot_password()

@endpoint.route('/tickets', methods=['POST'])
def buy_ticket():
    return create_ticket()

@endpoint.route('/user/<int:user_id>/tickets', methods=['GET'])
def get_purchesed_event(user_id):
    print("+++++++++++++++++++++++++++++++")
    return get_purchased_tickets(user_id)