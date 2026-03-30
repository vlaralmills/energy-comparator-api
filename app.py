from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)

CORS(app, origins=[
    "https://ecogreenpower.gr",
    "https://www.ecogreenpower.gr",
    "http://localhost:5050",
    "http://127.0.0.1:5500",
    "null"
])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRICES_FILE = os.path.join(BASE_DIR, "prices.json")


def load_prices():
    with open(PRICES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ─── ENDPOINTS ────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "service": "Energy Comparator API"})


@app.route("/widget", methods=["GET"])
def widget():
    """Σερβίρει το frontend widget — embed ως iframe στο WordPress."""
    return render_template("widget.html")


@app.route("/api/prices", methods=["GET"])
def get_prices():
    data = load_prices()
    return jsonify(data)


@app.route("/api/compare", methods=["POST"])
def compare():
    body = request.get_json()
    category = body.get("category", "G1")
    day_kwh = float(body.get("day_kwh", 0))
    night_kwh = float(body.get("night_kwh", 0))
    has_night = bool(body.get("has_night", False))

    data = load_prices()
    results = []

    for provider in data["providers"]:
        tariff = provider.get(category, {})
        if not tariff:
            continue
        energy_cost = day_kwh * tariff["day"]
        if has_night:
            energy_cost += night_kwh * tariff["night"]
        monthly = energy_cost + tariff["fixed_monthly"]
        annual = monthly * 12
        results.append({
            "id": provider["id"],
            "name": provider["name"],
            "color": provider["color"],
            "website": provider["website"],
            "annual": round(annual, 2),
            "monthly": round(monthly, 2),
            "tariff": tariff,
        })

    results.sort(key=lambda x: x["annual"])
    cheapest = results[0]["annual"]
    for r in results:
        r["savings_vs_cheapest"] = round(r["annual"] - cheapest, 2)

    return jsonify({
        "category": category,
        "day_kwh": day_kwh,
        "night_kwh": night_kwh if has_night else 0,
        "last_updated": data["last_updated"],
        "results": results,
        "max_savings": round(results[-1]["annual"] - cheapest, 2),
    })


@app.route("/api/update_price", methods=["POST"])
def update_price():
    body = request.get_json()
    provider_id = body.get("provider_id")
    category = body.get("category")
    data = load_prices()
    updated = False
    for provider in data["providers"]:
        if provider["id"] == provider_id:
            provider[category] = {
                "day": body["day"],
                "night": body["night"],
                "fixed_monthly": body["fixed_monthly"],
            }
            updated = True
            break
    if updated:
        data["last_updated"] = datetime.today().strftime("%Y-%m-%d")
        with open(PRICES_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({"success": True, "message": f"Ενημερώθηκε: {provider_id} / {category}"})
    return jsonify({"success": False, "message": "Provider not found"}), 404


@app.route("/api/health", methods=["GET"])
def health():
    data = load_prices()
    return jsonify({
        "status": "ok",
        "last_updated": data["last_updated"],
        "providers_count": len(data["providers"]),
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=False, host="0.0.0.0", port=port)
