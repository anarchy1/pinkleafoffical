// encyclopedia.js - Bilingual Plant Encyclopedia
class Encyclopedia {
    constructor() {
        this.currentLang = 'en';
        this.plants = [];
        this.filteredPlants = [];
        this.init();
    }

    async init() {
        await this.loadPlants();
        this.renderPlants();
        this.setupEventListeners();
    }

    async loadPlants() {
        try {
            const response = await fetch('./src/data/entries.json');
            const data = await response.json();
            this.plants = data.plants || [];
            this.filteredPlants = [...this.plants];
        } catch (error) {
            console.error('Error loading plants:', error);
            this.showError();
        }
    }

    renderPlants() {
        const grid = document.getElementById('plantsGrid');
        const content = this.filteredPlants.map(plant => 
            this.createPlantCard(plant)
        ).join('');
        grid.innerHTML = content;
    }

    createPlantCard(plant) {
        const lang = plant[this.currentLang];
        const instaShare = this.generateInstaShare(plant);
        
        return `
            <article class="plant-card" data-difficulty="${lang.difficulty}">
                <div class="plant-image">
                    <img src="${plant.images.main}" alt="${lang.name}" loading="lazy">
                    <div class="social-share">
                        <button onclick="shareToInstagram('${instaShare}')" title="Share to Instagram">
                            📸 IG
                        </button>
                        <button onclick="shareProduct('${plant.id}')" title="WhatsApp Checkout">
                            📱 הזמנה ב-WhatsApp
                        </button>
                    </div>
                </div>
                
                <h3>${lang.name}</h3>
                <em>${lang.scientific}</em>
                
                <div class="care-summary">
                    <span class="difficulty-badge" data-difficulty="${lang.difficulty}">
                        ${lang.difficulty}
                    </span>
                    <span class="price">₪${plant.price}</span>
                </div>
                
                <p>${lang.description}</p>
                
                <div class="care-details">
                    <h4>${this.currentLang === 'en' ? 'Care Tips' : 'טיפים לטיפוח'}:</h4>
                    <ul>
                        <li>🌞 ${lang.care.light}</li>
                        <li>💧 ${lang.care.water}</li>
                        <li>🌡️ ${lang.care.humidity}</li>
                        <li>🌡️ ${lang.care.temperature}</li>
                    </ul>
                </div>

                <div class="availability">
                    ${this.renderStock(plant.stock)}
                </div>
            </article>
        `;
    }

    generateInstaShare(plant) {
        const lang = plant[this.currentLang];
        return {
            image: plant.images.main,
            caption: `${lang.name}
${lang.description}
💡 ${this.currentLang === 'en' ? 
    'Swipe for care tips →' : 
    'החלק לטיפים →'}
📱 Order via WhatsApp: gumfound.com

${lang.benefits.map(b => `#${b.replace(/\s+/g, '')}`).join(' ')}
#PinkLeafPlants #HousePlants #PlantLover #${lang.name.replace(/\s+/g, '')}`
        };
    }

    renderStock(stock) {
        let availabilityText = '';
        let urgencyClass = '';

        const total = Object.values(stock).reduce((a,b) => a+b, 0);
        if (total === 0) {
            availabilityText = '🔴 SOLD OUT | אזל במלאי';
            urgencyClass = 'sold-out';
        } else if (total < 3) {
            availabilityText = '⚠️ LOW STOCK | מעט במלאי';
            urgencyClass = 'low-stock';
        } else {
            availabilityText = '✅ IN STOCK | במלאי';
            urgencyClass = 'in-stock';
        }

        return `<span class="${urgencyClass}">${availabilityText}</span>`;
    }

    // Instagram Integration
    async scheduleInstagramPost(plantId, caption, schedule) {
        // This will integrate with Instagram Graph API
        // For now, creates content ready for scheduling
        const plant = this.plants.find(p => p.id === plantId);
        if (!plant) return null;

        return {
            platform: 'instagram',
            type: 'post',
            image: plant.images.main,
            caption: caption,
            hashtags: plant[this.currentLang].benefits.map(b => 
                `#${b.replace(/\s+/g, '')}`
            ).join(' '),
            schedule: schedule,
            url: `https://pinkleaf.netlify.app/encyclopedia.html#${plantId}`
        };
    }

    // Filter Logic
    filterPlants(searchTerm = '') {
        const term = searchTerm.toLowerCase();
        this.filteredPlants = this.plants.filter(plant => {
            const lang = plant[this.currentLang];
            return lang.name.toLowerCase().includes(term) ||
                   lang.scientific.toLowerCase().includes(term);
        });
        this.renderPlants();
    }

    setLanguage(lang) {
        this.currentLang = lang;
        document.documentElement.lang = lang;
        document.documentElement.dir = lang === 'he' ? 'rtl' : 'ltr';
        this.renderPlants();
    }

    filterDifficulty(difficulty) {
        if (difficulty === 'all') {
            this.filteredPlants = [...this.plants];
        } else {
            this.filteredPlants = this.plants.filter(plant => 
                plant[this.currentLang].difficulty === difficulty
            );
        }
        this.renderPlants();
    }

    setupEventListeners() {
        window.setLanguage = (lang) => this.setLanguage(lang);
        window.filterDifficulty = (diff) => this.filterDifficulty(diff);
        window.filterPlants = () => {
            const searchTerm = document.getElementById('plantSearch').value;
            this.filterPlants(searchTerm);
        };
        
        // WhatsApp integration
        window.shareProduct = (plantId) => {
            const url = `https://wa.me/972XXXXXXXX?text=למוצר: ${plantId}`;
            window.open(url, '_blank');
        };
    }
}

// Instagram scheduling system
class InstagramScheduler {
    constructor() {
        this.contentQueue = [];
        this.postingSchedule = [
            'Sun 9:00 AM',  // Growing tips
            'Wed 6:00 PM',  // Care guides  
            'Fri 11:00 AM'  // New plant spotlight
        ];
    }

    generateWeeklyContent(plants) {
        const weeklyPosts = [];
        
        plants.forEach((plant, index) => {
            if (index < 3) { // Create posts for first 3 plants
                const scheduleDate = this.postingSchedule[index % 3];
                weeklyPosts.push({
                    plant: plant,
                    schedule: scheduleDate,
                    ...new Encyclopedia().generateInstaShare(plant)
                });
            }
        });

        return weeklyPosts;
    }
}

// SEO Schema Generator
class SEOStructuredData {
    static generateBreadcrumb() {
        return {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://pinkleaf.netlify.app/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Encyclopedia",
                    "item": "https://pinkleaf.netlify.app/encyclopedia.html"
                }
            ]
        };
    }
    
    static generatePlantSchema(plant, currentLang) {
        const lang = plant[currentLang];
        return {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": lang.name,
            "description": lang.description,
            "image": plant.images.main,
            "url": `https://pinkleaf.netlify.app/encyclopedia.html#${plant.id}`,
            "offers": {
                "@type": "Offer",
                "price": plant.price,
                "priceCurrency": "ILS",
                "availability": plant.stock.total > 0 ? "https://schema.org/InStock" : "https://schema.org/OutOfStock"
            }
        };
    }
}

// Initialize Encyclopedia
const encyclopedia = new Encyclopedia();
const instagramScheduler = new InstagramScheduler();

// Export for social media use
window.InstagramScheduler = InstagramScheduler;
window.encyclopediaInstance = encyclopedia;