// data.js - The Master Archive
const PLANT_DB = {
    "PV1": "Epipremnum Giganteum aurea var", "PV2": "Epipremnum Giganteum mint var", "PV3": "Ficus lyrata variegated", "PV4": "Epipremum pinnatum Aurea Var",
    "PV5": "Monstera delisiosa green snow", "PV6": "Monstera legacy", "PV7": "Monstera Thai Constellation var", "PV8": "Monstera deliciosa 'Yellow Marilyn'",
    "PV9": "Monstera deliciosa aurea", "PV10": "Monstera Mint var", "PV11": "Monstera deliciosa 'White Monster'", "PV12": "Monstera cream brulee",
    "PV13": "Raphidophora Tetrasperma Var", "PV14": "Alocasia Dragon Scale mint var", "PV15": "Alocasia 'Dragon Scale' white var", "PV16": "Alocasia frydek var",
    "PV17": "Alocasia Green Bambino variegata", "PV18": "Alocasia wentii variegated", "PV19": "Alocasia Polly pink var", "PV20": "Alocasia Bambino Arrow variegata",
    "PV21": "Alocasia Bambino aurea variegata", "PV22": "Alocasia Black Velvet pink Variegata", "PV23": "Alocasia Black Velvet Aurea Variegata",
    "PV24": "Alocasia odora var", "PV25": "Alocasia macrorrhizos variegata", "PV26": "Alocasia longiloba Variegated", "PV27": "Syngonium Podophyllum albo Var",
    "PV28": "Anthurium crassinervium Variegata", "PV29": "Anthurium clarinerviu var", "PV30": "Alocasia zebrina mint var", "PV31": "Alocasia zebrina aurea var",
    "PV32": "Alocasia Nairobi Nights var", "PV33": "Xanthosoma sagittifolium frozen planet var", "PV34": "Alocasia lauterbachiana var", "PV35": "Alocasia Jacklyn aurea var",
    "PV36": "Alocasia Yucatanense variegata", "PV37": "Alocasia Silver Dragon aurea var", "PV38": "Alocasia Silver Dragon albo Var", "PV39": "Alocasia Sinuata aurea var",
    "PV40": "Alocasia ninja albo var", "PV41": "Alocasia odora Okinawa Silver white var", "PV42": "Alocasia odora Orkinawa Silver yellow var", "PV43": "Alocasia Regal Shield albo var",
    "PV44": "Alocasia 'Pink Dragon' Albo/Pink", "PV45": "Alocasia sarian albo var", "PV46": "Elephant ear Var", "PV47": "Philodendron bipinnatifidum var",
    "PV48": "Philodendron Jose Buono var", "PV49": "Philodendron Burle Marx Albo variegata", "PV50": "Philodendron Micans Variegated", "PV51": "Philodendron Florida beauty variegata",
    "PV52": "Philodendron Strawberry Shake variegata", "PV53": "Philodendron domesticum variegated", "PV54": "Philodendron Giganteum Blizzard variegata", "PV55": "Philodendron White Knight var",
    "PV56": "Philodendron forest of white var", "PV57": "Philodendron White Princess variegata", "PV58": "Philodendron White Wizard variegata", "PV59": "Philodendron Pink Princess Marble",
    "PV60": "Philodendron caramel Marble var", "PV61": "Philodendron Ring of Fire", "PV62": "Philodendron Melanochrysum pink var", "PV63": "Philodendron billietiae 'Variegata'",
    "PV64": "Philodendron Gloriosum variegata", "PV65": "Philodendron erubescens 'Green Emerald' var", "PV66": "Philodendron tortum var", "PV67": "Philodendron olympaid var",
    "PV68": "Homalomena rubwscend aurea variegata", "PV69": "Homalomena rubwscend mint variegata", "PV70": "Homalomena Snowflakes Var", "PV71": "Musa 'AeAe' florida Variegata",
    "PV72": "Musa Nono Variegated pink", "PV73": "Alocasia cuprea Red Secret var", "PV74": "Alocasia Stingray var", "PV75": "Alocasia macrorrhizos Shock Treatment",
    "PV76": "Alocasia Watsoniana pink shiny var", "PV77": "Alocasia watsoniana doff pink var", "PV78": "Alocasia Simpo white var", "PV79": "Alocasia Nobilis Pink Variegated",
    "PV80": "Alocasia Scalprum white var", "PV81": "Alocasia heart balloon variegated", "PV82": "Alocasia Azlanii white Variegated", "PV83": "Alocasia Psuedo sanderiana AureaVariegated",
    "PV84": "Alocasia Psuedo sanderiana Pink Variegated", "PV85": "Alocasia nebula aurea var", "PV86": "Alocasia nebula albo var", "PV87": "Alocasia Maharani Variegated",
    "PV88": "Caladium lindenii var", "PV89": "Alocasia 'Melo' white var"
};

const STORE_LIST = ["PV22", "PV19", "PV20"]; // Only the store items

let xp = parseInt(localStorage.getItem('pl_xp')) || 0;
let streak = 0;
