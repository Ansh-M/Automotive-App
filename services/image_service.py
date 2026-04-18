import urllib.parse

# Wikipedia search terms tuned per car for best image match.
# The Flask proxy calls Wikipedia's API live at request time.
WIKI_SEARCH_TERMS = {
    "BMW M4 Competition":       "BMW M4 G82",
    "Mercedes-AMG GT 63":       "Mercedes-AMG GT 63 S",
    "Porsche 911 GT3 RS":       "Porsche 911 GT3 RS 992",
    "Tesla Model S Plaid":      "Tesla Model S Plaid",
    "Lamborghini Urus S":       "Lamborghini Urus",
    "Audi RS e-tron GT":        "Audi RS e-tron GT",
    "Ford Mustang GT500":       "Ford Mustang Shelby GT500",
    "Range Rover Sport SVR":    "Range Rover Sport SVR",
    "Mercedes C-Class India":   "Mercedes-Benz C-Class W206",
    "BMW 3 Series India":       "BMW 3 Series G20",
    "Audi Q5 India":            "Audi Q5 second generation",
    "Mahindra XUV700":          "Mahindra XUV700",
    "Tata Nexon EV":            "Tata Nexon EV",
    "Kia Seltos":               "Kia Seltos",
    "Hyundai Creta":            "Hyundai Creta second generation",
    "Mahindra Scorpio-N":       "Mahindra Scorpio N",
    "Maruti Suzuki Swift":      "Suzuki Swift fourth generation",
    "Tata Punch":               "Tata Punch",
    "Hyundai Grand i10 Nios":   "Hyundai Grand i10 Nios",
}

HEADERS = {
    "User-Agent": "AutoverseApp/1.0 (car-catalog project; contact@autoverse.app) python-requests/2.x"
}


def get_wiki_image_url(search_term: str, session) -> str | None:
    """
    Hits Wikipedia's public API to find the main image for a car article.
    Returns the thumbnail URL or None if not found.
    """
    # Step 1: find the best matching Wikipedia article title
    search_api = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "format": "json",
        "srlimit": "1",
    }
    r1 = session.get(search_api, params=search_params, headers=HEADERS, timeout=8)
    results = r1.json().get("query", {}).get("search", [])
    if not results:
        return None

    title = results[0]["title"]

    # Step 2: get the page's main thumbnail image
    image_params = {
        "action": "query",
        "titles": title,
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": "800",
    }
    r2 = session.get(search_api, params=image_params, headers=HEADERS, timeout=8)
    pages = r2.json().get("query", {}).get("pages", {})
    for page in pages.values():
        src = page.get("thumbnail", {}).get("source")
        if src:
            return src
    return None


def get_car_search_term(car_name: str, brand: str, category: str) -> str:
    """Returns the best Wikipedia search term for this car."""
    return WIKI_SEARCH_TERMS.get(car_name, f"{brand} {car_name}")
