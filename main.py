import requests
import time
import random
import sys

# ======= Section 1: Utility functions =======

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner(text):
    print("\n" + "=" * (len(text) + 10))
    print(f"     {text}")
    print("=" * (len(text) + 10))

def show_loading(message="Loading", dots=3, delay=0.5):
    for _ in range(dots):
        print(message + "." * (_+1), end="\r")
        time.sleep(delay)
    print()

# ======= Section 2: Weather Fetch Function =======

def get_weather(city, api_key):
    show_loading("Fetching weather")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data['main']['temp']
        weather = data['weather'][0]['main']
        return temp, weather
    else:
        slow_print("❌ City not found or API error!")
        return None, None

# ======= Section 3: Outfit Data =======

outfits = {
    "cold": [
        {"title": "Cozy Casual", "items": ["Wool Coat", "Blue Jeans", "Sweater"]},
        {"title": "Layered Look", "items": ["Puffer Jacket", "Thermal Leggings", "Flannel Shirt"]},
        {"title": "Classic Winter", "items": ["Trench Coat", "Corduroy Pants", "Turtleneck"]},
        {"title": "Snow Day", "items": ["Parkha", "Wool Pants", "Thermal Innerwear"]},
        {"title": "Evening Chill", "items": ["Peacoat", "Dress Slacks", "Knitted Sweater"]}
    ],
    "moderate": [
        {"title": "Smart Casual", "items": ["Long Sleeve Shirt", "Chinos", "Light Sweater"]},
        {"title": "Light Layers", "items": ["Denim Jacket", "T-shirt", "Stretch Jeans"]},
        {"title": "Relaxed Style", "items": ["Henley Shirt", "Khaki Pants", "Light Hoodie"]},
        {"title": "Weekend Wear", "items": ["Checkered Shirt", "Slim Fit Jeans", "Cardigan"]},
        {"title": "Urban Mix", "items": ["Bomber Jacket", "Joggers", "Graphic Tee"]}
    ],
    "hot": [
        {"title": "Cool & Comfy", "items": ["Cotton T-Shirt", "Shorts"]},
        {"title": "Summer Breeze", "items": ["Sleeveless Top", "Light Joggers"]},
        {"title": "Beach Day", "items": ["Tank Top", "Swim Shorts"]},
        {"title": "Outdoor Vibe", "items": ["Dry-fit Tee", "Sports Shorts"]},
        {"title": "Casual Noon", "items": ["Hawaiian Shirt", "Linen Pants"]}
    ]
}

accessories = {
    "cold": ["Woolen Scarf", "Gloves", "Beanie", "Fingerless Gloves", "Knitted Hat", "Earmuffs", "Neck Warmer"],
    "moderate": ["Leather Belt", "Watch", "Cap", "Simple Chain", "Bracelet", "Sunglasses", "Snapback Hat"],
    "hot": ["Sunglasses", "Baseball Cap", "Bucket Hat", "Beaded Necklace", "Wristband", "Cooling Towel", "Bandana"]
}

shoes = {
    "cold": ["Leather Boots", "Snow Boots", "Chelsea Boots", "High Tops", "Insulated Sneakers"],
    "moderate": ["Sneakers", "Canvas Shoes", "Loafers", "Desert Boots", "Walking Shoes"],
    "hot": ["Sneakers", "Flip-Flops", "Sandals", "Sliders", "Crocs"]
}

# ======= Section 4: Outfit Recommendation Logic =======

def recommend_outfit(temp, condition):
    # Determine temperature category
    if temp < 15:
        temp_cat = "cold"
    elif 15 <= temp <= 25:
        temp_cat = "moderate"
    else:
        temp_cat = "hot"

    # Rain warning
    if "rain" in condition.lower():
        slow_print("\n☔ It's rainy — don't forget an umbrella or raincoat!", 0.04)

    # Step 1: Choose outfit
    banner("👗 Outfit Styles")
    for i, outfit in enumerate(outfits[temp_cat], 1):
        slow_print(f"{i}. {outfit['title']} - Includes: {', '.join(outfit['items'])}")

    selected_outfit = get_choice("Select an outfit style", len(outfits[temp_cat]))
    
    # Step 2: Choose accessory
    banner("🎒 Accessories")
    for i, acc in enumerate(accessories[temp_cat], 1):
        slow_print(f"{i}. {acc}")
    
    selected_accessory = get_choice("Select an accessory", len(accessories[temp_cat]))

    # Step 3: Choose shoes
    banner("👟 Shoes")
    for i, shoe in enumerate(shoes[temp_cat], 1):
        slow_print(f"{i}. {shoe}")

    selected_shoe = get_choice("Select a shoe", len(shoes[temp_cat]))

    # Final Summary
    banner("✅ Your Final Recommended Outfit")
    outfit = outfits[temp_cat][selected_outfit]
    acc = accessories[temp_cat][selected_accessory]
    shoe = shoes[temp_cat][selected_shoe]

    print(f"\n🧥 Outfit Style: {outfit['title']}")
    print("👕 Clothes:")
    for item in outfit['items']:
        print(f"   - {item}")
    print(f"🎀 Accessory: {acc}")
    print(f"🥾 Shoes: {shoe}")
    print("\n🎉 Have a stylish day ahead!")

# ======= Section 5: Choice Function =======

def get_choice(prompt, max_value):
    while True:
        choice = input(f"{prompt} (1-{max_value}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= max_value:
            return int(choice) - 1
        else:
            print(f"Please enter a number between 1 and {max_value}.")

# ======= Section 6: Program Main Loop =======

def main():
    api_key = "c44576f39b5066de0f7214c50941cb24"

    banner("🌤️ Weather-Based Outfit Recommender")
    slow_print("👋 Welcome! This smart assistant helps you choose what to wear based on real-time weather data.\n", 0.04)

    while True:
        city = input("📍 Enter your city: ").strip()
        temp, condition = get_weather(city, api_key)

        if temp is not None:
            print(f"\n🌡️ Temperature: {temp}°C")
            print(f"☁️ Weather Condition: {condition}")
            recommend_outfit(temp, condition)

        again = input("\n🔁 Would you like to check another city? (y/n): ").lower()
        if again != 'y':
            break

    slow_print("\n👋 Thank you for using the Outfit Recommender. Stay stylish!", 0.03)

# ======= Entry Point =======
if __name__ == "__main__":
    main()
