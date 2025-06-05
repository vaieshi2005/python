// =============================
// Weather-Based Outfit Recommender in C
// =============================
// Description:
// This interactive console program allows users to input weather details (temperature and condition)
// and receive customized outfit recommendations based on the weather. It simulates behavior similar
// to a basic AI stylist by suggesting outfit types, accessories, and shoes.

    
    
// =============================


    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <ctype.h>
    #include <time.h>

    
    
    // =============================
   // CONSTANTS AND DEFINITIONS
    // =============================

    
    

#define MAX_LEN 100
#define NUM_OUTFITS 3
#define NUM_ITEMS 3
#define NUM_ACCESSORIES 5
#define NUM_SHOES 5
#define MAX_CITIES 5

// Temperature validation constants
#define MIN_TEMP -50.0
#define MAX_TEMP 50.0

// ANSI color codes for colorful terminal output
#define GREEN   "\033[1;32m"
#define BLUE    "\033[1;34m"
#define CYAN    "\033[1;36m"
#define RED     "\033[1;31m"
#define YELLOW  "\033[1;33m"
#define MAGENTA "\033[1;35m"
#define RESET   "\033[0m"

                   


// =============================
// STRUCTURE DEFINITIONS
// =============================

    
    
// Outfit structure to hold a title and an array of clothing items
typedef struct {
    char title[MAX_LEN];
    char items[NUM_ITEMS][MAX_LEN];
} Outfit;

// Weather structure to hold city name, temperature, and condition
typedef struct {
    char city[MAX_LEN];
    float temp;
    char condition[MAX_LEN];
} Weather;

// =============================
// GLOBAL DATA ARRAYS
// =============================

// Outfit options for cold weather
Outfit cold_outfits[NUM_OUTFITS] = {
    {"Winter Warrior", {"Trench Coat", "Corduroy Pants", "Turtleneck"}},
    {"Arctic Explorer", {"Puffer Jacket", "Thermal Leggings", "Wool Sweater"}},
    {"Cozy Professional", {"Wool Coat", "Dark Jeans", "Cashmere Sweater"}}
};

// Outfit options for moderate weather
Outfit moderate_outfits[NUM_OUTFITS] = {
    {"Smart Casual", {"Long Sleeve Shirt", "Chinos", "Light Cardigan"}},
    {"Weekend Relaxed", {"Henley Shirt", "Khaki Pants", "Zip-up Hoodie"}},
    {"Urban Explorer", {"Denim Jacket", "Joggers", "Graphic Tee"}}
};

// Outfit options for hot weather
Outfit hot_outfits[NUM_OUTFITS] = {
    {"Summer Cool", {"Linen Shirt", "Cotton Shorts", "Baseball Cap"}},
    {"Beach Ready", {"Tank Top", "Board Shorts", "Sun Hat"}},
    {"City Heat", {"Breathable Tee", "Linen Pants", "Cooling Towel"}}
};

// Accessory suggestions
char cold_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Wool Scarf", "Insulated Gloves", "Warm Beanie", "Fleece Headband", "Thermal Socks"
};

char moderate_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Baseball Cap", "Stylish Watch", "Leather Belt", "Sunglasses", "Light Scarf"
};

char hot_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Wide-Brim Hat", "Cooling Bandana", "UV Wristband", "Portable Fan", "Sweat Towel"
};

// Shoe suggestions
char cold_shoes[NUM_SHOES][MAX_LEN] = {
    "Waterproof Boots", "Insulated Sneakers", "Warm Chelsea Boots", "Snow Boots", "Thermal Loafers"
};

char moderate_shoes[NUM_SHOES][MAX_LEN] = {
    "Comfortable Sneakers", "Canvas Shoes", "Casual Loafers", "Walking Boots", "Slip-on Shoes"
};

char hot_shoes[NUM_SHOES][MAX_LEN] = {
    "Breathable Sandals", "Flip-Flops", "Mesh Sneakers", "Water Shoes", "Ventilated Slip-ons"
};

// jackets suggestions
char cold_jackets[NUM_JACKETS][MAX_LEN] = {
    "Waterproof Jackets", "Insulated Jackets", "Warm Chelsea Jackets", "Snow Jackets", "Thermal Jackets"
};

char moderate_jackets[NUM_JACKETS][MAX_LEN] = {
    "Comfortable Jackets", "Leather Jackets", "Casual Jackets", "Thin Jackets", "Sweaters"
};

char hot_jackets[NUM_JACKETS][MAX_LEN] = {
    "Wollen Jackets", "Hoodies", "Mesh Jackets", "Water Jackets", "Ventilated Jackets"
};

// Weather memory
Weather last_weather = {"", 0.0, ""};
int has_last_weather = 0;

// =============================
// FUNCTION DECLARATIONS
// =============================
    
void print_banner();
void strip_newline(char *str);
int get_valid_choice(int max);
void simulate_loading(const char *msg);
void display_outfits(Outfit outfits[], int size);
void display_options(char options[][MAX_LEN], int count);
const char* get_category(float temp);
void get_weather_input(Weather *weather);
void recommend_outfit(const Weather *weather);
void wait_for_user();
void print_divider();
void repeat_menu();
void farewell();
void display_weather_info(const Weather *weather);

// =============================
// UTILITY FUNCTIONS
// =============================

// Print program banner with formatting
void print_banner() {
    printf(GREEN);
    printf("\n==========================================\n");
    printf("   🌤️  Weather-Based Outfit Recommender  👕\n");
    printf("==========================================\n" RESET);
    printf(CYAN "Your personal AI stylist for any weather!\n" RESET);
}

// Remove newline character from string
void strip_newline(char *str) {
    size_t len = strlen(str);
    if (len > 0 && str[len - 1] == '\n') str[len - 1] = '\0';
}

// Get a valid user menu choice within range
int get_valid_choice(int max) {
    int choice;
    while (1) {
        printf(YELLOW "Enter your choice (1-%d): " RESET, max);
        if (scanf("%d", &choice) == 1 && choice >= 1 && choice <= max) {
            while (getchar() != '\n');
            return choice;
        } else {
            printf(RED "❌ Invalid input. Please enter a number between 1 and %d.\n" RESET, max);
            while (getchar() != '\n');
        }
    }
}

// Simulate loading animation with message
void simulate_loading(const char *msg) {
    printf(CYAN "🔄 %s", msg);
    for (int i = 0; i < 4; i++) {
        printf(".");
        fflush(stdout);
        for (volatile long j = 0; j < 40000000; j++);
    }
    printf(" Done!" RESET "\n");
}

// Display outfit titles and their items
void display_outfits(Outfit outfits[], int size) {
    for (int i = 0; i < size; i++) {
        printf(BLUE "%d. %s\n" RESET, i + 1, outfits[i].title);
        for (int j = 0; j < NUM_ITEMS; j++) {
            printf("   • %s\n", outfits[i].items[j]);
        }
        printf("\n");
    }
}

// Display options such as accessories or shoes
void display_options(char options[][MAX_LEN], int count) {
    for (int i = 0; i < count; i++) {
        printf("%d. %s\n", i + 1, options[i]);
    }
}

// Determine weather category based on temperature
const char* get_category(float temp) {
    if (temp < 10.0) return "cold";
    else if (temp <= 25.0) return "moderate";
    else return "hot";
}

// Display current weather information
void display_weather_info(const Weather *weather) {
    printf(MAGENTA "\n🌡️  Weather Summary for %s:\n" RESET, weather->city);
    printf("Temperature: %.1f°C\n", weather->temp);
    printf("Condition: %s\n", weather->condition);
    
    const char *category = get_category(weather->temp);
    if (strcmp(category, "cold") == 0) {
        printf("Category: ❄️  Cold Weather\n");
    } else if (strcmp(category, "moderate") == 0) {
        printf("Category: 🌤️  Moderate Weather\n");
    } else {
        printf("Category: ☀️  Hot Weather\n");
    }
}

// Take user input for weather details
void get_weather_input(Weather *weather) {
    printf("\n📍 Enter your city: ");
    if (has_last_weather) {
        printf("(or press Enter for '%s') ", last_weather.city);
    }
    
    if (fgets(weather->city, MAX_LEN, stdin) == NULL) {
        printf(RED "Error reading city name.\n" RESET);
        exit(1);
    }
    strip_newline(weather->city);
    
    // If user just pressed enter, use last city
    if (strlen(weather->city) == 0 && has_last_weather) {
        strcpy(weather->city, last_weather.city);
        printf("✅ Using previous city: %s\n", weather->city);
    }

    // Temperature input with validation
    while (1) {
        printf("🌡️  Enter temperature (°C): ");
        if (has_last_weather && strlen(weather->city) > 0) {
            printf("(or press Enter for %.1f°C) ", last_weather.temp);
        }
        
        char temp_input[20];
        if (fgets(temp_input, sizeof(temp_input), stdin) != NULL) {
            strip_newline(temp_input);
            
            // Check if user wants to use last temperature
            if (strlen(temp_input) == 0 && has_last_weather) {
                weather->temp = last_weather.temp;
                printf("✅ Using previous temperature: %.1f°C\n", weather->temp);
                break;
            }
            
            if (sscanf(temp_input, "%f", &weather->temp) == 1) {
                if (weather->temp >= MIN_TEMP && weather->temp <= MAX_TEMP) {
                    break;
                }
                printf(RED "❌ Temperature must be between %.1f and %.1f°C.\n" RESET, MIN_TEMP, MAX_TEMP);
            } else {
                printf(RED "❌ Please enter a valid number.\n" RESET);
            }
        }
    }

    printf("🌦️  Enter weather condition (e.g., Sunny, Rainy, Cloudy): ");
    if (fgets(weather->condition, MAX_LEN, stdin) == NULL) {
        printf(RED "Error reading weather condition.\n" RESET);
        exit(1);
    }
    strip_newline(weather->condition);

    // Save current weather as last used
    strcpy(last_weather.city, weather->city);
    last_weather.temp = weather->temp;
    strcpy(last_weather.condition, weather->condition);
    has_last_weather = 1;
}

// Recommend outfit based on weather input
void recommend_outfit(const Weather *weather) {
    display_weather_info(weather);
    
    const char *category = get_category(weather->temp);
    Outfit *chosen_outfit;
    char (*acc)[MAX_LEN];
    char (*shoe)[MAX_LEN];

    // Case-insensitive weather condition check
    char condition_lower[MAX_LEN];
    strcpy(condition_lower, weather->condition);
    for (int i = 0; condition_lower[i]; i++) {
        condition_lower[i] = tolower(condition_lower[i]);
    }

    // Weather-specific advice
    if (strstr(condition_lower, "rain") || strstr(condition_lower, "drizzle")) {
        printf(BLUE "\n☔ Rain detected! Don't forget an umbrella or waterproof jacket!\n" RESET);
    } else if (strstr(condition_lower, "snow")) {
        printf(CYAN "\n❄️ Snowy conditions! Extra layers and waterproof footwear recommended!\n" RESET);
    } else if (strstr(condition_lower, "wind")) {
        printf(YELLOW "\n💨 Windy weather! Consider a windbreaker or secure accessories!\n" RESET);
    }

    printf("\n👔 Choose your outfit style:\n");
    if (strcmp(category, "cold") == 0) {
        display_outfits(cold_outfits, NUM_OUTFITS);
        chosen_outfit = &cold_outfits[get_valid_choice(NUM_OUTFITS) - 1];
        acc = cold_accessories;
        shoe = cold_shoes;
    } else if (strcmp(category, "moderate") == 0) {
        display_outfits(moderate_outfits, NUM_OUTFITS);
        chosen_outfit = &moderate_outfits[get_valid_choice(NUM_OUTFITS) - 1];
        acc = moderate_accessories;
        shoe = moderate_shoes;
    } else {
        display_outfits(hot_outfits, NUM_OUTFITS);
        chosen_outfit = &hot_outfits[get_valid_choice(NUM_OUTFITS) - 1];
        acc = hot_accessories;
        shoe = hot_shoes;
    }

    printf("\n🎒 Choose your accessory:\n");
    display_options(acc, NUM_ACCESSORIES);
    int acc_choice = get_valid_choice(NUM_ACCESSORIES) - 1;

    printf("\n👟 Choose your footwear:\n");
    display_options(shoe, NUM_SHOES);
    int shoe_choice = get_valid_choice(NUM_SHOES) - 1;

    // Final outfit display
    printf(GREEN "\n✨ Your Perfect Outfit Recommendation:\n" RESET);
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf(BLUE "Style: %s\n" RESET, chosen_outfit->title);
    printf("Clothing:\n");
    for (int i = 0; i < NUM_ITEMS; i++) {
        printf("  • %s\n", chosen_outfit->items[i]);
    }
    printf("Accessory: %s\n", acc[acc_choice]);
    printf("Footwear: %s\n", shoe[shoe_choice]);
    printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf(GREEN "Have a stylish day! 😎\n" RESET);
}

// Prompt for user to continue
void wait_for_user() {
    printf(YELLOW "\nPress Enter to continue..." RESET);
    while (getchar() != '\n');
}

// Print a divider between sections
void print_divider() {
    printf("\n" CYAN "═══════════════════════════════════════════\n" RESET);
}

// Ask user whether to repeat
void repeat_menu() {
    printf(YELLOW "\nWould you like to get another outfit recommendation?\n" RESET);
    printf("1. Yes, try another city/weather\n");
    printf("2. No, exit program\n");
}

// Print exit message
void farewell() {
    printf(GREEN "\n🎉 Thank you for using the Weather-Based Outfit Recommender!\n");
    printf("Stay stylish and weather-ready! ✨👗👔\n" RESET);
}

// =============================
// MAIN FUNCTION
// =============================

int main() {
    while (1) {
        Weather current_weather;
        print_banner();
        get_weather_input(&current_weather);
        simulate_loading("Analyzing weather and finding perfect outfits");
        recommend_outfit(&current_weather);
        print_divider();
        repeat_menu();
        int choice = get_valid_choice(2);
        if (choice == 2) break;
    }
    farewell();
    return 0;
}