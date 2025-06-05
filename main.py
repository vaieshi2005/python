#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <ctype.h>



// =================== GLOBALS =====================



#define MAX_LEN 100
#define NUM_OUTFITS 3
#define NUM_ITEMS 3
#define NUM_ACCESSORIES 5
#define NUM_SHOES 5





// ANSI color codes
#define GREEN   "\033[1;32m"
#define BLUE    "\033[1;34m"
#define CYAN    "\033[1;36m"
#define RED     "\033[1;31m"
#define RESET   "\033[0m"

typedef struct {
    char title[MAX_LEN];
    char items[NUM_ITEMS][MAX_LEN];
} Outfit;

// Weather structure (placeholder for real API)
typedef struct {
    char city[MAX_LEN];
    float temp;
    char condition[MAX_LEN];
} Weather;





// =================== OUTFITS =====================

Outfit cold_outfits[NUM_OUTFITS] = {
    {"Winter Warrior", {"Trench Coat", "Corduroy Pants", "Turtleneck"}},
    {"Frosty Fashion", {"Puffer Jacket", "Thermal Leggings", "Wool Shirt"}},
    {"Cozy Layers", {"Wool Coat", "Blue Jeans", "Sweater"}}
};

Outfit moderate_outfits[NUM_OUTFITS] = {
    {"Smart Casual", {"Long Sleeve Shirt", "Chinos", "Light Sweater"}},
    {"Relaxed Style", {"Henley Shirt", "Khaki Pants", "Light Hoodie"}},
    {"Urban Mix", {"Bomber Jacket", "Joggers", "Graphic Tee"}}
};

Outfit hot_outfits[NUM_OUTFITS] = {
    {"Cool & Comfy", {"Cotton T-Shirt", "Shorts", "Cap"}},
    {"Beach Day", {"Tank Top", "Swim Shorts", "Flip-Flops"}},
    {"Summer Breeze", {"Sleeveless Top", "Linen Pants", "Sun Hat"}}
};





// Accessories
char cold_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Woolen Scarf", "Gloves", "Beanie", "Knitted Hat", "Earmuffs"
};
char moderate_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Cap", "Watch", "Leather Belt", "Sunglasses", "Snapback Hat"
};
char hot_accessories[NUM_ACCESSORIES][MAX_LEN] = {
    "Baseball Cap", "Bandana", "Wristband", "Cooling Towel", "Bucket Hat"
};





// Shoes
char cold_shoes[NUM_SHOES][MAX_LEN] = {
    "Snow Boots", "Leather Boots", "Chelsea Boots", "Insulated Sneakers", "High Tops"
};
char moderate_shoes[NUM_SHOES][MAX_LEN] = {
    "Sneakers", "Canvas Shoes", "Loafers", "Desert Boots", "Walking Shoes"
};
char hot_shoes[NUM_SHOES][MAX_LEN] = {
    "Flip-Flops", "Sandals", "Crocs", "Sliders", "Light Sneakers"
};




// =================== UTILITIES =====================




void print_banner() {
    printf(GREEN "\n===============================\n");
    printf(" Weather-Based Outfit Recommender\n");
    printf("===============================\n" RESET);
}

void strip_newline(char *str) {
    size_t len = strlen(str);
    if (len && str[len - 1] == '\n') str[len - 1] = '\0';
}

int get_valid_choice(int max) {
    int choice;
    while (1) {
        printf("Enter your choice (1-%d): ", max);
        if (scanf("%d", &choice) == 1 && choice >= 1 && choice <= max) {
            while (getchar() != '\n');  // flush stdin
            return choice;
        } else {
            printf(RED "Invalid input. Try again.\n" RESET);
            while (getchar() != '\n');
        }
    }
}

void simulate_loading(const char *msg) {
    printf(CYAN "%s", msg);
    for (int i = 0; i < 3; i++) {
        printf(".");
        fflush(stdout);
        for (volatile int j = 0; j < 100000000; j++); // delay
    }
    printf(RESET "\n");
}






// =================== CORE LOGIC =====================

void display_outfits(Outfit outfits[], int size) {
    for (int i = 0; i < size; i++) {
        printf(BLUE "%d. %s\n" RESET, i + 1, outfits[i].title);
        for (int j = 0; j < NUM_ITEMS; j++) {
            printf("   - %s\n", outfits[i].items[j]);
        }
    }
}

void display_options(char options[][MAX_LEN], int count) {
    for (int i = 0; i < count; i++) {
        printf(BLUE "%d. %s\n" RESET, i + 1, options[i]);
    }
}

const char* get_category(float temp) {
    if (temp < 15.0) return "cold";
    else if (temp <= 25.0) return "moderate";
    else return "hot";
}

void get_weather_input(Weather *weather) {
    printf("Enter your city: ");
    fgets(weather->city, MAX_LEN, stdin);
    strip_newline(weather->city);

    printf("Enter temperature (°C): ");
    scanf("%f", &weather->temp);
    getchar(); // consume newline

    printf("Enter weather condition (e.g., Rain, Clear): ");
    fgets(weather->condition, MAX_LEN, stdin);
    strip_newline(weather->condition);
}

void recommend_outfit(const Weather *weather) {
    const char *category = get_category(weather->temp);
    Outfit *chosen_outfit;
    char (*acc)[MAX_LEN];
    char (*shoe)[MAX_LEN];

    if (strstr(weather->condition, "rain") || strstr(weather->condition, "Rain"))
        printf(RED "\n☔ It's rainy — carry an umbrella or raincoat!\n" RESET);

    // Outfit options
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

    // Accessories
    printf("\n🎒 Choose an accessory:\n");
    display_options(acc, NUM_ACCESSORIES);
    int acc_choice = get_valid_choice(NUM_ACCESSORIES) - 1;

    // Shoes
    printf("\n👟 Choose a shoe type:\n");
    display_options(shoe, NUM_SHOES);
    int shoe_choice = get_valid_choice(NUM_SHOES) - 1;

    // Final recommendation
    printf(GREEN "\n✅ Final Outfit Recommendation:\n" RESET);
    printf("Style: %s\n", chosen_outfit->title);
    for (int i = 0; i < NUM_ITEMS; i++) {
        printf(" - %s\n", chosen_outfit->items[i]);
    }
    printf("Accessory: %s\n", acc[acc_choice]);
    printf("Footwear: %s\n", shoe[shoe_choice]);
}





// =================== MAIN =====================

int main() {
    Weather current_weather;

    print_banner();
    get_weather_input(&current_weather);
    simulate_loading("Fetching recommendations");
    recommend_outfit(&current_weather);

    printf(GREEN "\n🎉 Stay stylish and weather-ready!\n\n" RESET);
    return 0;
}
