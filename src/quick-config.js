// quick-config.js - Instant social setup

// Instagram Content Calendar - Next 4 weeks
const socialCalendar = {
    week1: [
        {
            day: 'Sunday',
            type: 'care_guide',
            content: {
                title: "Monstera Swiss Cheese Care Guide",
                caption: "🌱 Monstera Swiss Cheese Care Guide ✨\n\n📸 Save this for perfect plant parenting!\n\nLIGHT: Bright indirect ☀️\nWATER: Let soil dry 2-3 inches 🌊\nHUMIDITY: 60-80% for best fenestrations 💨\n\n💡 Pro tip: Yellowing? Check humidity first!\n\n📱 Order via WhatsApp: gumfound.com\n\n#MonsteraCare #PlantTips #PinkLeafStore",
                hashtags: ['#MonsteraCare', '#PlantTips', '#HousePlants', '#PinkLeafStore', '#SwissCheesePlant'],
                image_style: 'care infographic',
                posting_schedule: '2026-03-01 09:00 AM IST'
            }
        },
        {
            day: 'Wednesday', 
            type: 'before_after',
            content: {
                title: "3 Week Growth Progress",
                caption: "3 weeks apart! Look at these fenestrations 🌿\n\nFrom: Small rooted cutting\nTo: Gigantic split leaves!\n\n💰 Price: ₪75 MK\n📦 Stock: 3 left MK\n📲 WhatsApp: gumfound.com\n\n#PlantProgress #MonsteraMagic #PinkLeafStore",
                hashtags: ['#PlantProgress', '#GrowingTogether', '#BeforeAfter']
            }
        },
        {
            day: 'Friday',
            type: 'product_spotlight',
            content: {
                title: "Weekend Plant Spotlight",
                caption: "🎯 WEEKEND SPOTLIGHT: Monstera Swiss Cheese\n\nThe Instagram-famous plant that everyone needs!\n\nPerfect for: \n🏡 Corner statement piece\n🌬️ Air purification\n📈 Fast growth (20cm/month)\n\n💰 MK₪75\n🚀 Free delivery in Tel Aviv\n📱 WhatsApp: gumfound.com\n\n#WeekendSpotlight #MonsteraLovers #PinkLeafStore",
                call_to_action: "DM us on WhatsApp!"
            }
        }
    ],
    
    week2: [
        // Snake Plant Guides
    ],
    
    week3: [
        // Fiddle Leaf Fig Guides
    ],
    
    week4: [
        // Pothos and Trailing Plants
    ]
};

// Google Sheets Integration Template
const gSheetSyncTemplate = `
=CONCATENATE(
    "Instagram Post", CHAR(10),
    "Plant:", plant, CHAR(10),
    "Caption:", description_en, CHAR(10),
    "Hebrew Caption:", description_he, CHAR(10),
    "Image URL:", image_url, CHAR(10),
    "Price:", price, CHAR(10),
    "Stock:", stock_total, CHAR(10),
    "360 Barcode:", barcode_360,
    "WhatsApp Link:", CONCATENATE("https://wa.me/972559116990?text=למוצר", plant)
)
`.trim();

// Quick HTML Integration Snippets
const integrationSnippets = {
    
    // Instagram embed on any page
    instagram_embed: `
        <div class="instagram-feed">
            <a href="https://www.instagram.com/pinkleaf.store/" target="_blank">
                📸 Follow us @pinkleaf.store
            </a>
            <!-- Embed actual feed via later embedding -->
        </div>
    `,
    
    // WhatsApp floating action button
    whatsapp_fab: `
        <div class="whatsapp-float" onclick="shareToWhatsApp()">
            <svg viewBox="0 0 24 24" fill="#fff">
                <path d="M20.5 3.4A11.9 11.9 0 0 0 12.2 0C5.5 0 0 5.5 0 12.2c0 2.1.6 4.2 1.7 6L0 24l6.3-1.7c1.9 1.1 4 1.7 6 1.7 6.7 0 12.2-5.5 12.2-12.2 0-3.2-1.2-6.2-3.5-8.5zM12.2 22c-1.7 0-3.4-.4-4.9-1.2l-2.8.8.8-2.7c-.8-1.5-1.2-3.2-1.2-4.9 0-5.5 4.5-10 10-10s10 4.5 10 10-4.5 10-10 10z"/>
            </svg>
        </div>
    `,
    
    // Instagram sharing functionality
    instagram_sharing: `
        <button onclick="shareToInstagram(postContent)" class="insta-share">
            Share to Instagram 📸
        </button>
        
        <script>
        function shareToInstagram(content) {
            const postText = encodeURIComponent(content.caption);
            const url = 'https://www.instagram.com/create/upload/normal';
            // This would integrate with Instagram Graph API
            // For now, create Facebook URL scheme:
            window.open(url, '_blank');
        }
        </script>
    `
};

// SEO Export Functions
window.exportSEOData = (plants) => {
    return plants.map(plant => ({
        plant: plant.en.name,
        url: `https://pinkleaf.co.il/encyclopedia.html#${plant.id}`,
        seo_title: `${plant.en.name} Care Guide | מדריך טיפוח ${plant.he.name}`,
        meta_description: `Complete care guide for ${plant.en.name} - lighting, water, humidity requirements. בית צמח מושלם במחיר ₪${plant.price}`,
        og_image: plant.images.main,
        ig_caption: socialCalendar.week1[0].content.caption,
        whatsapp_price: `₪${plant.price}`,
        availability: plant.stock.total > 0 ? 'In Stock' : 'Sold Out'
    }));
};

// Quick integration for existing site
window.addInstagramIntegration = () => {
    const footer = document.getElementById('footer') || document.createElement('footer');
    footer.innerHTML += `
        <div class="social-links">
            <a href="https://www.instagram.com/pinkleaf.store/" target="_blank">📸 @pinkleaf.store</a>
            <a href="https://wa.me/972559116990" target="_blank">📱 WhatsApp Orders</a>
        </div>
    `;
    document.body.appendChild(footer);
};

// Social media system ready. Use window.exportSEOData(plants) for instant integration.