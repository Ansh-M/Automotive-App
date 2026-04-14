from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

CARS = [
    {
        "id": 1,
        "name": "BMW M4 Competition",
        "brand": "BMW",
        "category": "Sports",
        "year": 2024,
        "price": "₹1,42,00,000",
        "engine": "3.0L Twin-Turbo I6",
        "horsepower": "503 hp",
        "torque": "650 Nm",
        "transmission": "8-Speed M Steptronic",
        "drivetrain": "RWD",
        "top_speed": "290 km/h",
        "acceleration": "3.9s (0–100)",
        "fuel_type": "Petrol",
        "color": "Isle of Man Green",
        "image": "bmw_m4",
        "badge": "Track Beast",
        "description": "The definitive driver's car — raw, aggressive, and utterly addictive on both road and track."
    },
    {
        "id": 2,
        "name": "Mercedes-AMG GT 63",
        "brand": "Mercedes",
        "category": "Luxury",
        "year": 2024,
        "price": "₹2,57,00,000",
        "engine": "4.0L Biturbo V8",
        "horsepower": "630 hp",
        "torque": "900 Nm",
        "transmission": "9-Speed MCT",
        "drivetrain": "AWD",
        "top_speed": "315 km/h",
        "acceleration": "3.2s (0–100)",
        "fuel_type": "Petrol",
        "color": "Obsidian Black",
        "image": "amg_gt",
        "badge": "Grand Tourer",
        "description": "Where opulence meets ferocity. A four-door GT that devours autobahns without breaking a sweat."
    },
    {
        "id": 3,
        "name": "Porsche 911 GT3 RS",
        "brand": "Porsche",
        "category": "Sports",
        "year": 2024,
        "price": "₹3,25,00,000",
        "engine": "4.0L Naturally Aspirated Flat-6",
        "horsepower": "525 hp",
        "torque": "465 Nm",
        "transmission": "7-Speed PDK",
        "drivetrain": "RWD",
        "top_speed": "296 km/h",
        "acceleration": "3.2s (0–100)",
        "fuel_type": "Petrol",
        "color": "Guards Red",
        "image": "911_gt3",
        "badge": "Apex Predator",
        "description": "A racing car with number plates. The GT3 RS is the purest expression of what a sports car should be."
    },
    {
        "id": 4,
        "name": "Tesla Model S Plaid",
        "brand": "Tesla",
        "category": "Electric",
        "year": 2024,
        "price": "₹1,89,00,000",
        "engine": "Tri-Motor Electric",
        "horsepower": "1,020 hp",
        "torque": "1,420 Nm",
        "transmission": "Single-Speed Direct Drive",
        "drivetrain": "AWD",
        "top_speed": "322 km/h",
        "acceleration": "1.99s (0–100)",
        "fuel_type": "Electric",
        "color": "Midnight Silver",
        "image": "tesla_plaid",
        "badge": "Ludicrous",
        "description": "The fastest production sedan ever built. Redefines what electric performance means, from 0 to terrifying."
    },
    {
        "id": 5,
        "name": "Lamborghini Urus S",
        "brand": "Lamborghini",
        "category": "SUV",
        "year": 2024,
        "price": "₹4,22,00,000",
        "engine": "4.0L Twin-Turbo V8",
        "horsepower": "666 hp",
        "torque": "850 Nm",
        "transmission": "8-Speed Automatic",
        "drivetrain": "AWD",
        "top_speed": "305 km/h",
        "acceleration": "3.5s (0–100)",
        "fuel_type": "Petrol",
        "color": "Arancio Borealis",
        "image": "urus_s",
        "badge": "Super SUV",
        "description": "The world's first super SUV just got angrier. School runs will never be the same again."
    },
    {
        "id": 6,
        "name": "Audi RS e-tron GT",
        "brand": "Audi",
        "category": "Electric",
        "year": 2024,
        "price": "₹1,99,00,000",
        "engine": "Dual-Motor Electric",
        "horsepower": "637 hp",
        "torque": "830 Nm",
        "transmission": "2-Speed Automatic",
        "drivetrain": "AWD",
        "top_speed": "250 km/h",
        "acceleration": "3.3s (0–100)",
        "fuel_type": "Electric",
        "color": "Kemora Grey",
        "image": "rs_etron",
        "badge": "Electric Grand Tourer",
        "description": "Sculpted like a concept car, quick like a supercar, silent like a secret. The future of the GT."
    },
    {
        "id": 7,
        "name": "Ford Mustang GT500",
        "brand": "Ford",
        "category": "Muscle",
        "year": 2024,
        "price": "₹89,00,000",
        "engine": "5.2L Supercharged V8",
        "horsepower": "760 hp",
        "torque": "847 Nm",
        "transmission": "7-Speed Tremec DCT",
        "drivetrain": "RWD",
        "top_speed": "290 km/h",
        "acceleration": "3.3s (0–100)",
        "fuel_type": "Petrol",
        "color": "Grabber Blue",
        "image": "gt500",
        "badge": "American Icon",
        "description": "The most powerful street-legal Mustang ever. All-American brute force wrapped in iconic muscle car DNA."
    },
    {
        "id": 8,
        "name": "Range Rover Sport SVR",
        "brand": "Land Rover",
        "category": "SUV",
        "year": 2024,
        "price": "₹2,34,00,000",
        "engine": "5.0L Supercharged V8",
        "horsepower": "575 hp",
        "torque": "700 Nm",
        "transmission": "8-Speed Automatic",
        "drivetrain": "AWD",
        "top_speed": "280 km/h",
        "acceleration": "4.3s (0–100)",
        "fuel_type": "Petrol",
        "color": "Santorini Black",
        "image": "rr_sport",
        "badge": "Luxury Offroader",
        "description": "British refinement meets off-road royalty. Goes anywhere, arrives everywhere, apologises to nobody."
    }
]

@app.route('/')
def index():
    categories = list(set(car['category'] for car in CARS))
    return render_template('index.html', cars=CARS, categories=sorted(categories))

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = next((c for c in CARS if c['id'] == car_id), None)
    if not car:
        return "Car not found", 404
    return render_template('detail.html', car=car)

@app.route('/api/cars')
def api_cars():
    category = request.args.get('category', '')
    search = request.args.get('search', '').lower()
    filtered = CARS
    if category and category != 'All':
        filtered = [c for c in filtered if c['category'] == category]
    if search:
        filtered = [c for c in filtered if search in c['name'].lower() or search in c['brand'].lower()]
    return jsonify(filtered)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
