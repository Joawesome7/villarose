from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATA")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Admin credentials from environment variables
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

# Database Model
class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    checkin = db.Column(db.String(50), nullable=False)
    checkout = db.Column(db.String(50), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    requests = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'guests': self.guests,
            'checkin': self.checkin,
            'checkout': self.checkout,
            'room_type': self.room_type,
            'requests': self.requests,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else ''
        }

# Helper functions
def load_bookings():
    """Load all bookings from database"""
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return [b.to_dict() for b in bookings]

def save_booking(booking_data):
    """Save new booking to database"""
    booking = Booking(
        name=booking_data['name'],
        email=booking_data['email'],
        phone=booking_data['phone'],
        guests=booking_data['guests'],
        checkin=booking_data['checkin'],
        checkout=booking_data['checkout'],
        room_type=booking_data['room_type'],
        requests=booking_data.get('requests', ''),
        status=booking_data.get('status', 'pending')
    )
    db.session.add(booking)
    db.session.commit()
    return booking.to_dict()

ROOM_PRICES = {
    'deluxe': 3500,
    'suite': 4500,
    'executive': 4000,
    'family': 4000,
    'deluxe-2': 3500
}

DISCOUNT_RATE = 0.40  # 40% off
DISCOUNT_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday']

# Room data
ROOMS = [
    {
        'id': 1,
        'name': 'Deluxe',
        'price': f'Php. {ROOM_PRICES["deluxe"]:,.2f}',
        'capacity': '4 Pax',
        'bed': '1 Queen size W/ Pull Out Bed',
        'amenities': ['Shared toilet bath room', '2nd Floor Level With Plated Breakfast', 'Full Ocean View', 'Nature View'],
        'image': 'https://placehold.co/400x300?text=Deluxe+Room',
    },
    {
        'id': 2,
        'name': 'Suite',
        'price': f'Php. {ROOM_PRICES["suite"]:,.2f}',
        'capacity': '2 Pax',
        'bed': '1 King Size Bed',
        'amenities': ['2nd Floor Level With Plated Breakfast', 'Ocean View / Pool View', 'Toilet and Bath w/bath thub'],
        'image': 'https://placehold.co/400x300?text=Suite+Room',
    },
    {
        'id': 3,
        'name': 'Executive',
        'price': f'Php. {ROOM_PRICES["executive"]:,.2f}',
        'capacity': '2-3 Pax',
        'bed': 'Queen Size Bed W/Pull Out Bed',
        'amenities': ['Ocean View / Pool View', 'Toilet & Bath', 'Ground Floor Level With Plated Breakfast'],
        'image': 'https://placehold.co/400x300?text=Executive+Room',
    },
    {
        'id': 4,
        'name': 'Family',
        'price': f'Php. {ROOM_PRICES["family"]:,.2f}',
        'capacity': '4 Pax',
        'bed': '2 Bunk Bed',
        'amenities': ['Shared Toilet & Bath', 'With Plated Breakfast'],
        'image': 'https://placehold.co/400x300?text=Family+Room',
    },
    {
        'id': 5,
        'name': 'Deluxe 2',
        'price': f'Php. {ROOM_PRICES["deluxe-2"]:,.2f}',
        'capacity': '2-3 Pax',
        'bed': 'Queen Size and Twin Size Bed',
        'amenities': ['Shared Toilet & Bath', 'With Plated Breakfast'],
        'image': 'https://placehold.co/400x300?text=Deluxe-02+Room',
    },
]

AMENITIES = [
    {'name': 'Swimming Pool', 'icon': '🏊'},
    {'name': 'Playground', 'icon': '🛝'},
    {'name': 'Bar and Restaurant', 'icon': '🍽️'},
    {'name': 'Hunay Wellness & Spa', 'icon': '💆'},
]

ACTIVITIES = [
    {'name': 'Jetski', 'icon': '🚤'},
    {'name': 'Kayak', 'icon': '🛶'},
    {'name': 'Bonfire', 'icon': '🔥'},
    {'name': 'LandTour', 'icon': '🚗'},
    {'name': 'Snorkelling', 'icon': '🤿'},
    {'name': 'Bangka Island Hopping', 'icon': '⛵'},
    {'name': 'Banana Boating', 'icon': '🍌'},
]

ESCAPE_PACKAGE = {
    'title': 'Bungalow Escape',
    'days': 'Monday to Thursday Only',
    'swimming_fee': '₱550 per person',
    'entrance_fee': '₱500 Fully consumable at our restaurant',
    'description': 'Come on over for a refreshing swim! Our pool is open from Monday to Thursday, with a fee of ₱550 per person. To ensure a pleasant experience for all, we kindly ask that guests wear proper swimming attire, such as a dry-fit swimsuit or rash guard. Please note that pool access may be limited or unavailable on some days due to private events or scheduled maintenance. We recommend contacting us ahead of your visit to confirm availability. We can\'t wait to see you!',
}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tab/<tab_name>')
def load_tab(tab_name):
    if tab_name == 'rooms':
        return render_template('partials/rooms.html', rooms=ROOMS)
    elif tab_name == 'amenities':
        return render_template('partials/amenities.html', 
                             amenities=AMENITIES, 
                             activities=ACTIVITIES)
    elif tab_name == 'escape':
        return render_template('partials/escape.html', 
                             package=ESCAPE_PACKAGE)
    return 'Tab not found', 404

@app.route('/booking', methods=['POST'])
def booking():
    return render_template('partials/booking_form.html')

@app.route('/check-availability', methods=['POST'])
def check_availability():
    """Check which rooms are available for given dates"""
    checkin = request.json.get('checkin')
    checkout = request.json.get('checkout')
    
    if not checkin or not checkout:
        return jsonify({'error': 'Dates required'}), 400
    
    # Get all bookings
    bookings = load_bookings()
    
    # Room types
    room_types = ['executive', 'family', 'junior', 'premier']
    availability = {}
    
    for room_type in room_types:
        available = True
        conflicting_booking = None
        
        for booking in bookings:
            # Skip cancelled bookings
            if booking['status'] == 'cancelled':
                continue
                
            # Check if same room type
            if booking['room_type'] == room_type:
                existing_checkin = booking['checkin']
                existing_checkout = booking['checkout']
                
                # Check if dates overlap
                if not (checkout <= existing_checkin or checkin >= existing_checkout):
                    available = False
                    conflicting_booking = {
                        'checkin': existing_checkin,
                        'checkout': existing_checkout,
                        'name': booking.get('name', 'Guest')
                    }
                    break
        
        availability[room_type] = {
            'available': available,
            'conflict': conflicting_booking
        }
    
    return jsonify(availability)

@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    # Get form data
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')
    room_type = request.form.get('room_type')
    
    # Check for date conflicts
    bookings = load_bookings()
    for booking in bookings:
        # Skip cancelled bookings
        if booking['status'] == 'cancelled':
            continue
            
        # Check if same room type
        if booking['room_type'] == room_type:
            # Check if dates overlap
            existing_checkin = booking['checkin']
            existing_checkout = booking['checkout']
            
            # Date overlap logic
            if not (checkout <= existing_checkin or checkin >= existing_checkout):
                # Dates overlap - room not available
                error_msg = f"Sorry! This room is already booked from {existing_checkin} to {existing_checkout}. Please choose different dates or another room."
                return render_template('partials/booking_error.html', error=error_msg, booking_data=request.form)
    
    # No conflicts - proceed with booking
    booking_data = {
        'name': request.form.get('name'),
        'email': request.form.get('email'),
        'phone': request.form.get('phone'),
        'guests': request.form.get('guests'),
        'checkin': checkin,
        'checkout': checkout,
        'room_type': room_type,
        'requests': request.form.get('requests', ''),
        'status': 'pending'
    }
    
    # Save to database
    saved_booking = save_booking(booking_data)
    
    return render_template('partials/booking_success.html', booking=saved_booking)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin/login.html', error='Invalid credentials')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    bookings = load_bookings()
    return render_template('admin/dashboard.html', bookings=bookings)

@app.route('/admin/api/bookings')
def get_bookings():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    bookings = load_bookings()
    return jsonify(bookings)

@app.route('/admin/api/booking/<int:booking_id>/status', methods=['POST'])
def update_booking_status(booking_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    status = request.json.get('status')
    booking = Booking.query.get(booking_id)
    
    if booking:
        booking.status = status
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'error': 'Booking not found'}), 404

@app.route('/admin/api/booking/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'error': 'Booking not found'}), 404

# Initialize database
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created!")
    
    # Run app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)