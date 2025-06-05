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


    
// ANSI color codes for colorful terminal output
#define GREEN   "\033[1;32m"
#define BLUE    "\033[1;34m"
#define CYAN    "\033[1;36m"
#define RED     "\033[1;31m"
#define YELLOW  "\033[1;33m"
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
    {"Frosty Fashion", {"Puffer Jacket", "Thermal Leggings", "Wool Shirt"}},
    {"Cozy Layers", {"Wool Coat", "Blue Jeans", "Sweater"}}
};





// Outfit options for moderate weather
Outfit moderate_outfits[NUM_OUTFITS] = {
    {"Smart Casual", {"Long Sleeve Shirt", "Chinos", "Light Sweater"}},
    {"Relaxed Style", {"Henley Shirt", "Khaki Pants", "Light Hoodie"}},
    {"Urban Mix", {"Bomber Jacket", "Joggers", "Graphic Tee"}}
};





// Outfit options for hot weather
Outfit hot_outfits[NUM_OUTFITS] = {
    {"Cool & Comfy", {"Cotton T-Shirt", "Shorts", "Cap"}},
    {"Beach Day", {"Tank Top", "Swim Shorts", "Flip-Flops"}},
    {"Summer Breeze", {"Sleeveless Top", "Linen Pants", "Sun Hat"}}
};






// Accessory suggestions
char cold_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Woolen Scarf", "Gloves", "Beanie", "Knitted Hat", "Earmuffs"
};

char moderate_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Cap", "Watch", "Leather Belt", "Sunglasses", "Snapback Hat"
};

char hot_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Baseball Cap", "Bandana", "Wristband", "Cooling Towel", "Bucket Hat"
};





// Shoe suggestions
char cold_shoes[NUM_SHOES][MAX_LEN] = {
    "Snow Boots", "Leather Boots", "Chelsea Boots", "Insulated Sneakers", "High Tops"
};

char moderate_shoes[NUM_SHOES][MAX_LEN] = {
    "Sneakers", "Canvas Shoes", "Loafers", "Desert Boots", "Walking Shoes"
};

char hot_shoes[NUM_SHOES][MAX_LEN] = {
    "Flip-Flops", "Sandals", "Crocs", "Sliders", "Light Sneakers"
};





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




// =============================
// UTILITY FUNCTIONS
// =============================


    // Print program banner with formatting
void print_banner() {
    printf(GREEN);
    printf("\n==========================================\n");
    printf("    Weather-Based Outfit Recommender    \n");
    printf("==========================================\n" RESET);
}

// Remove newline character from string
void strip_newline(char *str) {
    size_t len = strlen(str);
    if (len && str[len - 1] == '\n') str[len - 1] = '\0';
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
            printf(RED "Invalid input. Try again.\n" RESET);
            while (getchar() != '\n');
        }
    }
}

// Simulate loading animation with message
void simulate_loading(const char *msg) {
    printf(CYAN "%s", msg);
    for (int i = 0; i < 3; i++) {
        printf(".");
        fflush(stdout);
        for (volatile long j = 0; j < 50000000; j++);
    }
    printf(RESET "\n");
}

// Display outfit titles and their items
void display_outfits(Outfit outfits[], int size) {
    for (int i = 0; i < size; i++) {
        printf(BLUE "%d. %s\n" RESET, i + 1, outfits[i].title);
        for (int j = 0; j < NUM_ITEMS; j++) {
            printf("   - %s\n", outfits[i].items[j]);
        }
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
    if (temp < 15.0) return "cold";
    else if (temp <= 25.0) return "moderate";
    else return "hot";
}

// Take user input for weather details
void get_weather_input(Weather *weather) {
    printf("Enter your city: ");
    fgets(weather->city, MAX_LEN, stdin);
    strip_newline(weather->city);

    printf("Enter temperature (°C): ");
    scanf("%f", &weather->temp);
    getchar();

    printf("Enter weather condition (e.g., Rain, Clear): ");
    fgets(weather->condition, MAX_LEN, stdin);
    strip_newline(weather->condition);
}






// Recommend outfit based on weather input
void recommend_outfit(const Weather *weather) {
    const char *category = get_category(weather->temp);
    Outfit *chosen_outfit;
    char (*acc)[MAX_LEN];
    char (*shoe)[MAX_LEN];

    if (strstr(weather->condition, "rain") || strstr(weather->condition, "Rain")) {
        printf(RED "\n☔ It's rainy — carry an umbrella or raincoat!\n" RESET);
    }

    printf("\n👕 Choose an outfit style:\n");
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

    printf("\n🎒 Choose an accessory:\n");
    display_options(acc, NUM_ACCESSORIES);
    int acc_choice = get_valid_choice(NUM_ACCESSORIES) - 1;

    printf("\n👟 Choose a shoe type:\n");
    display_options(shoe, NUM_SHOES);
    int shoe_choice = get_valid_choice(NUM_SHOES) - 1;

    // Final outfit display
    printf(GREEN "\n✅ Final Outfit Recommendation:\n" RESET);
    printf("Style: %s\n", chosen_outfit->title);
    for (int i = 0; i < NUM_ITEMS; i++) {
        printf(" - %s\n", chosen_outfit->items[i]);
    }
    printf("Accessory: %s\n", acc[acc_choice]);
    printf("Footwear: %s\n", shoe[shoe_choice]);
}





// Prompt for user to continue
void wait_for_user() {
    printf(YELLOW "\nPress Enter to continue..." RESET);
    while (getchar() != '\n');
}

// Print a divider between sections
void print_divider() {
    printf("\n-------------------------------------------\n");
}

// Ask user whether to repeat
void repeat_menu() {
    printf("\nWould you like to try another city?\n1. Yes\n2. No\n");
}

// Print exit message
void farewell() {
    printf(GREEN "\nThank you for using the Weather-Based Outfit Recommender! Stay stylish!\n" RESET);
}

// =============================
// MAIN FUNCTION
// =============================

int main() {
    while (1) {
        Weather current_weather;
        print_banner();               // Display welcome banner
        get_weather_input(&current_weather);  // Get weather input from user
        simulate_loading("\nFetching recommendations"); // Simulate delay
        recommend_outfit(&current_weather);    // Suggest outfit
        print_divider();             // Print divider
        repeat_menu();              // Ask for retry
        int choice = get_valid_choice(2);     // Get choice
        if (choice == 2) break;               // Exit if user chooses no
    }
    farewell(); // Goodbye message
    return 0;
}
