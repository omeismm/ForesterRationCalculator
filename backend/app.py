# backend/app.py
from flask import Flask, jsonify, send_from_directory
import requests
import pandas as pd
import webbrowser
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'Table.html')

@app.route('/calculate')
def calculate():
    headers = {"User-Agent": "ForesterRationsCalculator/2.0 - Github repo by omeismm"}
    
    try:
        mapping_data = requests.get("https://prices.runescape.wiki/api/v1/osrs/mapping", headers=headers).json()
        prices_data = requests.get("https://prices.runescape.wiki/api/v1/osrs/latest", headers=headers).json()["data"]
        
        # Leaves to base rations mapping
        leaves_to_rations = {
            "Leaves": 2,
            "Oak leaves": 4,
            "Willow leaves": 6,
            "Maple leaves": 8,
            "Yew leaves": 10,
            "Magic leaves": 12
        }

        # Cooking level to multiplier mapping
        cooking_multiplier = [
            (1, 29, 1),
            (30, 69, 2),
            (70, 99, 3)
        ]

        # Cooked food cooking levels
        cooked_food = {
            "Shrimps": 1,
            "Anchovies": 1,
            "Sardine": 1,
            "Chicken": 2,
            "Meat": 2,
            "Herring": 5,
            "Trout": 15,
            "Pike": 15,
            "Cod": 18,
            "Salmon": 25,
            "Slimy eel": 28,
            "Tuna": 30,
            "Karambwan": 30,
            "Rainbow fish": 35,
            "Cave eel": 35,
            "Lobster": 40,
            "Bass": 43,
            "Swordfish": 45,
            "Monkfish": 62,
            "Shark": 80,
            "Sea turtle": 82,
            "Anglerfish": 84,
            "Dark crab": 90,
            "Manta ray": 91
        }

        # Map item names to IDs from the mapping data
        name_to_id = {item["name"]: item["id"] for item in mapping_data}

        # Get average price for each item, handling None values
        id_to_price = {}
        for item_id, data in prices_data.items():
            high = data.get("high")
            low = data.get("low")
            if high is not None and low is not None:  # Ensure valid price data
                id_to_price[int(item_id)] = (high + low) / 2
            else:
                id_to_price[int(item_id)] = None  # Mark as unavailable

        # Get Forester's Rations price
        rations_price_id = name_to_id.get("Forester's ration")
        rations_price = id_to_price.get(rations_price_id, None)

        if rations_price is None:
            raise ValueError("Could not fetch Forester's Rations price from the API!")

        # Calculate profit for each combination
        results = []
        for leaf, base_rations in leaves_to_rations.items():
            leaf_id = name_to_id.get(leaf)
            leaf_price = id_to_price.get(leaf_id, None)

            if leaf_price is None:
                continue  # Skip leaves without valid prices

            for food, level in cooked_food.items():
                food_id = name_to_id.get(food)
                food_price = id_to_price.get(food_id, None)

                if food_price is None:
                    continue  # Skip foods without valid prices

                # Determine rations created
                multiplier = next(m for min_lvl, max_lvl, m in cooking_multiplier if min_lvl <= level <= max_lvl)
                rations_created = base_rations * multiplier

                # Calculate profit
                total_cost = leaf_price + food_price
                revenue = rations_created * rations_price
                profit = revenue - total_cost

                results.append({
                    "Leaf": leaf,
                    "Food": food,
                    "Profit": profit,
                    "Rations Created": rations_created,
                    "Leaf Price": leaf_price,
                    "Food Price": food_price,
                    "Rations Price": rations_price
                })
        
        top_10 = sorted(results, key=lambda x: x["Profit"], reverse=True)[:10]
        # Convert to a DataFrame for better presentation
        top_10_df = pd.DataFrame(top_10)
        print(top_10_df)
        return jsonify([{
            "Leaf": item["Leaf"],
            "Food": item["Food"],
            "Profit": item["Profit"],
            "Rations_Created": item["Rations Created"],
            "Leaf_Price": item["Leaf Price"],
            "Food_Price": item["Food Price"]
        } for item in top_10])
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        webbrowser.open_new('http://localhost:5000')
    app.run(debug=True)