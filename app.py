import os
from tavily import TavilyClient
from groq import Groq
from flask import Flask, render_template, request, jsonify, Response
import requests as http_requests
from data.cars import CARS
from services.image_service import get_car_search_term, get_wiki_image_url


# v2 - automated deploy
app = Flask(__name__)


# ── Helpers ───────────────────────────────────────────────────────────────

def get_car_by_id(car_id: int):
    return next((c for c in CARS if c["id"] == car_id), None)


def search_cars(query: str, category: str = "", origin: str = ""):
    query = query.lower().strip()
    results = CARS

    if category and category != "All":
        results = [c for c in results if c["category"] == category]

    if origin and origin not in ("", "all"):
        results = [c for c in results if c.get("origin") == origin]

    if query:
        results = [c for c in results if
                   query in c["name"].lower() or
                   query in c["brand"].lower() or
                   query in c["category"].lower()]
    return results


# ── Page Routes ───────────────────────────────────────────────────────────

@app.route("/")
def index():
    categories = sorted(set(car["category"] for car in CARS))
    return render_template("index.html", cars=CARS, categories=categories)


@app.route("/car/<int:car_id>")
def car_detail(car_id):
    car = get_car_by_id(car_id)
    if not car:
        return "Car not found", 404
    return render_template("detail.html", car=car)


@app.route("/search")
def search_page():
    return render_template("search.html")


# ── API Routes ────────────────────────────────────────────────────────────

@app.route("/api/cars")
def api_cars():
    category = request.args.get("category", "")
    search   = request.args.get("search", "")
    origin   = request.args.get("origin", "")
    return jsonify(search_cars(search, category, origin))


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Please enter a car name or brand"}), 400

    # Score and rank results
    scored = []
    for car in CARS:
        q = query.lower()
        score = 0
        if q in car["name"].lower():      score += 3
        if q in car["brand"].lower():     score += 2
        if q in car["category"].lower():  score += 1
        if score > 0:
            scored.append({**car, "match_score": score})

    scored.sort(key=lambda x: x["match_score"], reverse=True)

    if not scored:
        try:
            api_key = os.environ.get("TAVILY_API_KEY")
            if not api_key:
                raise ValueError("Tavily key not set")
            tavily = TavilyClient(api_key=api_key)
            results = tavily.search(query=f"{query} car specs price India")
            
            structured = structure_with_groq(results["results"])
            if structured:
                return jsonify(structured)

            return jsonify({
                "source": "tavily",
                "results": results["results"][:3]
            })
        except Exception:
            return jsonify({
                "error": f'No results for "{query}". Try: BMW, Tata, Mahindra, SUV, Electric...'
            }), 404

    return jsonify(scored[:3])


@app.route("/api/generate-image/<int:car_id>")
def api_generate_image(car_id):
    """
    Fetches the real Wikipedia photo for this car via Wikipedia's public API,
    then proxies the image bytes back to avoid browser CORS issues.
    """
    car = get_car_by_id(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404

    search_term = get_car_search_term(car["name"], car["brand"], car["category"])
    try:
        # Use a session so both Wikipedia API calls share a TCP connection
        with http_requests.Session() as session:
            image_url = get_wiki_image_url(search_term, session)
            if not image_url:
                return jsonify({"error": "No image found on Wikipedia"}), 404
            resp = session.get(image_url, timeout=10, headers={"User-Agent": "AutoverseApp/1.0 (car-catalog project) python-requests/2.x"})
            content_type = resp.headers.get("Content-Type", "image/jpeg")
            if not content_type.startswith("image/"):
                raise ValueError(f"Non-image response: {content_type}")
            return Response(resp.content, content_type=content_type)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

@app.route("/api/generate-image-by-name")
def api_generate_image_by_name():
    name = request.args.get("name", "").strip()
    brand = request.args.get("brand", "").strip()
    category = request.args.get("category", "").strip()
    if not name:
        return jsonify({"error": "No name provided"}), 400
    search_term = get_car_search_term(name, brand, category)
    try:
        with http_requests.Session() as session:
            image_url = get_wiki_image_url(search_term, session)
            if not image_url:
                return jsonify({"error": "No image found"}), 404
            resp = session.get(image_url, timeout=10, headers={"User-Agent": "AutoverseApp/1.0"})
            content_type = resp.headers.get("Content-Type", "image/jpeg")
            return Response(resp.content, content_type=content_type)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def structure_with_groq(raw_results):
    try:
        api_key = os.environ.get("GROQ_API_KEY")
            
        if not api_key:
            return None
            
        client = Groq(api_key=api_key)
        content = "\n".join([r.get("content", "") for r in raw_results])
        prompt = f""" You are a car data extractor. Based on this web content, 
        extract car information and return ONLY a JSON array with this exact structure, 
        no explanation:
        [{{
            "id": 9999,
            "name": "Full Car Name",
            "brand": "Brand",
            "badge": "CATEGORY",
            "category": "SUV/Sedan/Hatchback/etc",
            "origin": "india or global",
            "description": "2 sentence description",
            "engine": "engine spec",
            "horsepower": "XXX hp",
            "acceleration": "X.X s",
            "top_speed": "XXX km/h",
            "fuel_type": "Petrol/Diesel/Electric",
            "drivetrain": "FWD/RWD/AWD",
            "price": "₹XX.XX Lakh"      
        }}]

        Web content: {content}
        """
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
        
    except Exception:
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)