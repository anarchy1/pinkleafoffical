// social-media-content.js - Instagram + Marketing Pipeline
class SocialMediaContent {
    constructor() {
        this.platforms = {
            instagram: {
                postTypes: ['reel', 'carousel', 'story'],
                bestTimes: ['9:00 AM', '6:00 PM', '11:00 AM'],
                frequencies: { seed: 3, small: 2, medium: 1 }
            },
            whatsapp: {
                channel: 'business_catalog',
                quick_replies: ['מחיר', 'זמינות', 'הזמנה']
            }
        };
        this.contentBank = this.loadContentBank();
    }

    generatePlantContent(plant, type, platform = 'instagram') {
        const baseContent = this.createBasePlantPost(plant);
        
        switch(type) {
            case 'care_guides':
                return this.createCareGuide(plant, platform);
            case 'new_arrivals':
                return this.createNewArrival(plant, platform);
            case 'care_tips':
                return this.createCareTip(plant, platform);
            case 'before_after':
                return this.createGrowthStory(plant, platform);
            case 'myth_busting':
                return this.createMythBust(plant, platform);
            default:
                return this.createProductSpotlight(plant, platform);
        }
    }

    createCareGuide(plant) {
        const tips = plant.en.care;
        return {
            image: [plant.images.main, `${plant.id}-care.jpg`],
            caption: `🌱 ${plant.en.name} Care Guide | מדריך טיפוח

Light: ${tips.light} | אור: ${plant.he.care.light}
Water: ${tips.water} | מים: ${plant.he.care.water}
Humidity: ${tips.humidity} | לחות: ${plant.he.care.humidity}

💡 Pro Tip: ${this.getProTip(plant.id)}

📱 Order via WhatsApp - מוזמנים ב-WhatsApp
👉 gumfound.com

#PlantCare #${plant.en.name.replace(/\s+/g, '')} #HousePlants #PinkLeaf #PlantLovers`,
            hashtags: ['#PlantCare', '#HousePlants', '#PlantLover', '#PinkLeaf'],
            mentions: [],
            location: "Tel Aviv, Israel"
        };
    }

    createNewArrival(plant) {
        return {
            image: plant.images.main,
            caption: `🆕 NEW ARRIVAL | הוצאה חדשה!

Meet the stunning ${plant.en.name} ✨

${plant.en.description.substring(0, 100)}...

💰 Price: ₪${plant.price}
📦 In stock: ${this.formatStock(plant.stock)}
📥 WhatsApp: gumfound.com

הזמן עכשיו ב-WhatsApp: gumfound.com

#NewPlant #${plant.en.name.replace(/\s+/g, '')} #PinkLeafStore`,
            story_poll: {
                question: `Would you buy this plant? | האם תקנו את הצמח הזה?`,
                options: ['Absolutely! | בטח!', 'Maybe | אולי', 'Not for me | לא בשבילי']
            },
            product_tag: {
                id: plant.id,
                price: `₪${plant.price}`
            }
        };
    }

    createCareTip(plant) {
        const tip = this.getRandomTip(plant.id);
        return {
            image: [`${plant.id}-tip.jpg`],
            caption: `🧠 Plant Pro Tip | טיפ מקצועי

${tip.text}

For your ${plant.en.name}:
${tip.specific}

Save this post for later 🔖
Tag a friend who needs this! 👥

#PlantTips #${plant.en.name.replace(/\s+/g, '')} #HousePlantCare`,
            instagram_story: {
                interactive_quiz: {
                    question: `What's the best care tip for ${plant.en.name}?`,
                    options: ["Direct sunlight", "Let soil dry", "Daily watering", "Ignore it"]
                }
            }
        };
    }

    createProductSpotlight(plant) {
        return {
            image: { 
                main: plant.images.main,
                detail: `${plant.id}-detail.jpg`,
                room: `${plant.id}-livingroom.jpg`
            },
            caption: `✨ SPOTLIGHT: ${plant.en.name}

Perfect for: ${plant.en.benefits.join(', ')}
Price: ₪${plant.price} | מחיר: ₪${plant.price}

Swipe to see it in different rooms →

📱 Order now: gumfound.com
📞 WhatsApp for details

#PlantSpotlight #${plant.en.name.replace(/\s+/g, '')} #IndoorPlants`,
            carousel_lines: [
                `${plant.en.name} - Perfect corner plant`,
                `Learn care tips →`,
                `See it styled in rooms →`,
                `Price & WhatsApp order →`
            ]
        };
    }

    generateWeeklyContent(plants) {
        const week = [];
        const days = ['Sunday', 'Wednesday', 'Friday'];
        
        plants.forEach((plant, index) => {
            if (index < 3) { // First 3 plants get this week's content
                const day = days[index % 3];
                const post = this.generatePlantContent(plant, 'care_guides');
                
                week.push({
                    day: day,
                    plant: plant,
                    post: post,
                    schedule: `${day} 9:00 AM`
                });
            }
        });

        return week;
    }

    createContentCalendar(plants, weeks = 4) {
        const calendar = [];
        
        for (let week = 1; week <= weeks; week++) {
            const weekContent = [
                // Sunday - Care Guide
                {
                    date: `Week ${week} Sunday`,
                    type: 'care_guide',
                    plant: plants[(week - 1) % plants.length],
                    content: this.generatePlantContent(plants[(week-1) % plants.length], 'care_guid', 'instagram')
                },
                // Wednesday - New Arrival\Tip
                {
                    date: `Week ${week} Wednesday`,
                    type: week % 2 === 0 ? 'new_arrival' : 'care_tips',
                    plant: plants[(week) % plants.length],
                    content: this.generatePlantContent(plants[week % plants.length], 
                      week % 2 === 0 ? 'new_arrival' : 'care_tips')
                },
                // Friday - Product Spotlight
                {
                    date: `Week ${week} Friday`,
                    type: 'spotlight',
                    plant: plants[(week + 1) % plants.length],
                    content: this.generatePlantContent(plants[(week + 1) % plants.length], 'product_spotlight')
                }
            ];
            
            calendar.push({ week, content: weekContent });
        }

        return calendar;
    }

    // WhatsApp Business Integration
    whatsAppCatalog(plants) {
        return plants.map(plant => ({
            name: `${plant.en.name} - ${plant.he.name}`,
            price: `₪${plant.price}`,
            stock: `
✅ Available: ${plant.stock.seed + plant.stock.small + plant.stock.medium + plant.stock.large} units
📦 Stock Breakdown:
• Seeds: ${plant.stock.seed}
• Small: ${plant.stock.small} 
• Medium: ${plant.stock.medium}
• Large: ${plant.stock.large}
            `,
            order_link: `https://wa.me/972XXXXXXXX?text=I'm%20interested%20in%20${plant.en.name}`
        }));
    }

    // SEO & Analytics
    generateSEOMeta(plant) {
        return {
            title: `${plant.en.name} | צמח בית מושלם - Pink Leaf Encyclopedia`,
            description: `${plant.en.description} | ${plant.he.description}`,
            keywords: [
                plant.en.name, plant.he.name, 'house plants', 'צמחי בית',
                'plant care', 'טיפוח צמחים', 'bilingual', 'חלון מידע'
            ]
        };
    }

    // Helper methods
    getProTip(plantId) {
        const tips = {
            'monstera-deliciosa': 'Yellowing? Check for overwatering or low humidity',
            'snake-plant': 'Thrives in low light and survives neglect',
            'fiddle-fig': 'Rotate weekly for even growth'
        };
        return tips[plantId] || 'Observe your plant daily for best care';
    }

    getRandomTip(plantId) {
        const tips = [
            { text: "Less is more with watering", specific: "When soil feels dry 2-3 inches down" },
            { text: "Bright indirect light wins", specific: "East-facing windows are perfect" },
            { text: "Check leaves before watering", specific: "Droopy leaves = thirsty" }
        ];
        return tips[Math.floor(Math.random() * tips.length)];
    }

    formatStock(stock) {
        const total = stock.seed + stock.small + stock.medium + stock.large;
        if (total === 0) return 'אזל במלאי';
        if (total < 5) return `${total} units left`;
        return 'In stock';
    }

    loadContentBank() {
        return {
            plantBenefits: [
                'Air purification | טיהור אוויר',
                'Stress reduction | הפחתת לחץ',
                'Better sleep | שינה טובה',
                'Natural decor | נוי טבעי'
            ],
            seasonalTips: {
                winter: "Reduce watering, keep away from cold drafts",
                spring: "Increase water as growth resumes", 
                summer: "More frequent watering, watch for sunburn",
                fall: "Gradually reduce watering"
            }
        };
    }
}

// Usage Example
const socialMedia = new SocialMediaContent();

// Generate weekly content plan
const weeklyContent = (plants) => {
    return socialMedia.createContentCalendar(plants, 1);
};

// WhatsApp catalog generator
const whatsAppCatalog = (plants) => {
    return socialMedia.whatsAppCatalog(plants);
};

// Connect to Google Sheets inventory sync
const syncSocialInventory = async (inventoryData) => {
    if (!inventoryData) return null;
    
    const updatedPlants = inventoryData.map(row => ({
        ...row, // existing plant data
        social_ready: new SocialMediaContent().generatePlantContent(row, 'product_spotlight')
    }));
    
    return updatedPlants;
};

window.SocialMediaContent = SocialMediaContent;
window.socialScheduler = socialMedia;