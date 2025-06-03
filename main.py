import requests

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data['main']['temp']
        weather = data['weather'][0]['main']
        return temp, weather
    else:
        print("City not found or API error!")
        return None, None

def recommend_outfit(temp, condition):
    # Data structured by temperature range
    outfits = {
        "cold": [
            {"title": "Cozy Casual", "items": ["Wool Coat", "Blue Jeans", "Sweater"]},
            {"title": "Layered Look", "items": ["Puffer Jacket", "Thermal Leggings", "Flannel Shirt"]},
            {"title": "Classic Winter", "items": ["Trench Coat", "Corduroy Pants", "Turtleneck"]}
        ],
        "moderate": [
            {"title": "Smart Casual", "items": ["Long Sleeve Shirt", "Chinos", "Light Sweater"]},
            {"title": "Light Layers", "items": ["Denim Jacket", "T-shirt", "Stretch Jeans"]},
            {"title": "Relaxed Style", "items": ["Henley Shirt", "Khaki Pants", "Light Hoodie"]}
        ],
        "hot": [
            {"title": "Cool & Comfy", "items": ["Cotton T-Shirt", "Shorts"]},
            {"title": "Summer Breeze", "items": ["Sleeveless Top", "Light Joggers"]},
            {"title": "Beach Day", "items": ["Tank Top", "Swim Shorts"]}
        ]
    }

    accessories = {
        "cold": ["Woolen Scarf", "Gloves", "Beanie", "Fingerless Gloves", "Knitted Hat"],
        "moderate": ["Leather Belt", "Watch", "Cap", "Simple Chain", "Bracelet", "Sunglasses"],
        "hot": ["Sunglasses", "Baseball Cap", "Bucket Hat", "Beaded Necklace", "Wristband"]
    }

    shoes = {
        "cold": ["Leather Boots", "Snow Boots", "Chelsea Boots"],
        "moderate": ["Sneakers", "Canvas Shoes", "Loafers"],
        "hot": ["Sneakers", "Flip-Flops", "Sandals"]
    }

    # Determine temperature category
    if temp < 15:
        temp_cat = "cold"
    elif 15 <= temp <= 25:
        temp_cat = "moderate"
    else:
        temp_cat = "hot"

    if "rain" in condition.lower():
        print("\n☔ It's rainy — don't forget an umbrella or raincoat!")

    # Step 1: Choose outfit
    print("\n👗 Outfit Styles:")
    for i, outfit in enumerate(outfits[temp_cat], 1):
        print(f"{i}. {outfit['title']} - Includes: {', '.join(outfit['items'])}")

    while True:
        outfit_choice = input("Select an outfit style (1-3): ").strip()
        if outfit_choice in ['1', '2', '3']:
            outfit_choice = int(outfit_choice) - 1
            selected_outfit = outfits[temp_cat][outfit_choice]
            break
        else:
            print("Please enter 1, 2, or 3.")

    # Step 2: Choose accessory
    print("\n🎒 Accessories:")
    for i, acc in enumerate(accessories[temp_cat], 1):
        print(f"{i}. {acc}")

    while True:
        acc_choice = input(f"Select an accessory (1-{len(accessories[temp_cat])}): ").strip()
        if acc_choice.isdigit() and 1 <= int(acc_choice) <= len(accessories[temp_cat]):
            acc_choice = int(acc_choice) - 1
            selected_accessory = accessories[temp_cat][acc_choice]
            break
        else:
            print(f"Please enter a number between 1 and {len(accessories[temp_cat])}.")

    # Step 3: Choose shoes
    print("\n👟 Shoes:")
    for i, shoe in enumerate(shoes[temp_cat], 1):
        print(f"{i}. {shoe}")

    while True:
        shoe_choice = input(f"Select a shoe (1-{len(shoes[temp_cat])}): ").strip()
        if shoe_choice.isdigit() and 1 <= int(shoe_choice) <= len(shoes[temp_cat]):
            shoe_choice = int(shoe_choice) - 1
            selected_shoe = shoes[temp_cat][shoe_choice]
            break
        else:
            print(f"Please enter a number between 1 and {len(shoes[temp_cat])}.")

    # Final summary
    print("\n✅ Your final recommended outfit:")
    print(f"Outfit Style: {selected_outfit['title']}")
    print("Clothes:")
    for item in selected_outfit['items']:
        print(f" - {item}")
    print(f"Accessory: {selected_accessory}")
    print(f"Shoes: {selected_shoe}")

# ====== MAIN PROGRAM ======
api_key = "c44576f39b5066de0f7214c50941cb24" 

city = input("Enter your city: ").strip()
temperature, condition = get_weather(city, api_key)

if temperature is not None:
    print(f"\n🌡️ Temperature: {temperature}°C")
    print(f"☁️ Condition: {condition}")
    recommend_outfit(temperature, condition)
