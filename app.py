from flask import Flask, render_template, request

app = Flask(__name__)

# Room data
ROOMS = [
    {
        'id': 1,
        'name': 'Executive',
        'price': 'Php. 12,700.00',
        'capacity': '2 Pax',
        'bed': '1 King size Bed',
        'amenities': ['Breakfast Included', 'Full Ocean View', 'Jacuzzi Access'],
        'image': 'https://placehold.co/400x300?text=Executive+Villa',
    },
    {
        'id': 2,
        'name': 'Family',
        'price': 'Php. 12,700.00',
        'capacity': '2 Pax',
        'bed': '1 King Size Bed with Bunk Beds',
        'amenities': ['Breakfast Included', 'Ocean View', 'Jacuzzi Access'],
        'image': 'https://placehold.co/400x300?text=Family+Villa',
    },
    {
        'id': 3,
        'name': 'Junior',
        'price': 'Php. 10,500.00',
        'capacity': '2 Pax',
        'bed': '2 Double Beds',
        'amenities': ['Breakfast Included', 'Garden View', 'Jacuzzi Access'],
        'image': 'https://placehold.co/400x300?text=Junior+Villa',
    },
    {
        'id': 4,
        'name': 'Premier Deluxe Room',
        'price': 'Php. 7,900.00',
        'capacity': '2 Pax',
        'bed': '2 Queen Size Beds',
        'amenities': ['Breakfast Included', 'Garden View'],
        'image': 'https://placehold.co/400x300?text=Premier+Deluxe',
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
    'title': 'Manggadiwa Escape',
    'days': 'Monday to Thursday Only',
    'swimming_fee': '₱550 per person',
    'entrance_fee': '₱500 Fully consumable at our restaurant',
    'description': 'Come on over for a refreshing swim! Our pool is open from Monday to Thursday, with a fee of ₱550 per person. To ensure a pleasant experience for all, we kindly ask that guests wear proper swimming attire, such as a dry-fit swimsuit or rash guard. Please note that pool access may be limited or unavailable on some days due to private events or scheduled maintenance. We recommend contacting us ahead of your visit to confirm availability. We can\'t wait to see you!',
}

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

if __name__ == '__main__':
    app.run(debug=True)