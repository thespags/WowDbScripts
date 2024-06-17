local lib = LibStub("LibInstances")

if 4 < LE_EXPANSION_LEVEL_CURRENT 
    and 4 > LE_EXPANSION_LEVEL_CURRENT
then
    return
end

lib:addInstance(
    43,
    {
        activities = { [1] = 1, },
        encounters = { "Lady Anacondra", "Lord Cobrahn", "Kresh", "Lord Pythas", "Skum", "Lord Serpentis", "Verdan the Everliving", "Mutanus the Devourer" },
        expansion = 0,
        lastBossIndex = 8,
        maxLevel = 25,
        minLevel = 17,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    289,
    {
        activities = { [1] = 2, },
        encounters = { "Darkmaster Gandling", "Doctor Theolen Krastinov", "Instructor Malicia", "Jandice Barov", "Kirtonos", "Lady Illucia Barov", "Lord Alexei Barov", "Lorekeeper Polkelt", "Marduk Blackpool", "Ras Frostwhisperer", "Rattlegore", "The Ravenian", "Vectus" },
        expansion = 0,
        lastBossIndex = 13,
        maxLevel = 48,
        minLevel = 38,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    389,
    {
        activities = { [1] = 4, },
        encounters = { "Oggleflint", "Jergosh the Invoker", "Bazzalan", "Taragaman the Hungerer" },
        expansion = 0,
        lastBossIndex = 4,
        maxLevel = 20,
        minLevel = 15,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    36,
    {
        activities = { [1] = 6, [12] = 326, },
        encounters = { "Glubtok", "Helix Gearbreaker", "Foe Reaper 5000", "Admiral Ripsnarl", "\"Captain\" Cookie", "Vanessa VanCleef" },
        expansion = 3,
        lastBossIndex = 6,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    33,
    {
        activities = { [1] = 8, [11] = 288, [12] = 327, },
        encounters = { "Baron Ashbury", "Baron Silverlaine", "Commander Springvale", "Lord Walden", "Lord Godfrey" },
        expansion = 3,
        lastBossIndex = 5,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    48,
    {
        activities = { [1] = 10, },
        encounters = { "Ghamoo-ra", "Lady Sarevess", "Gelihast", "Lorgus Jett", "Old Serra'kis", "Twilight Lord Kelris", "Aku'mai" },
        expansion = 0,
        lastBossIndex = 7,
        maxLevel = 30,
        minLevel = 20,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    34,
    {
        activities = { [1] = 12, },
        encounters = { "Targorr the Dread", "Hogger", "Lord Overheat", "Randolph Moloch", "Bazil Thredd" },
        expansion = 0,
        lastBossIndex = 5,
        maxLevel = 30,
        minLevel = 22,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    90,
    {
        activities = { [1] = 14, },
        encounters = { "Grubbis", "Viscous Fallout", "Electrocutioner 6000", "Crowd Pummeler 9-60", "Mekgineer Thermaplugg" },
        expansion = 0,
        lastBossIndex = 5,
        maxLevel = 34,
        minLevel = 24,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    47,
    {
        activities = { [1] = 16, },
        encounters = { "Roogug", "Death Speaker Jargba", "Aggem Thorncurse", "Overlord Ramtusk", "Agathelos the Raging", "Charlga Razorflank" },
        expansion = 0,
        lastBossIndex = 6,
        maxLevel = 40,
        minLevel = 30,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    189,
    {
        activities = { [1] = 165, [11] = 285, },
        encounters = { "Interrogator Vishas", "Bloodmage Thalnos", "Houndmaster Loksey", "Arcanist Doan", "Herod", "High Inquisitor Fairbanks", "High Inquisitor Whitemane" },
        expansion = 0,
        lastBossIndex = 7,
        maxLevel = 85,
        minLevel = 84,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    129,
    {
        activities = { [1] = 20, },
        encounters = { "Tuten'kash", "Mordresh Fire Eye", "Glutton", "Amnennar the Coldbringer" },
        expansion = 0,
        lastBossIndex = 4,
        maxLevel = 50,
        minLevel = 40,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    70,
    {
        activities = { [1] = 22, },
        encounters = { "Revelosh", "The Lost Dwarves", "Ironaya", "Ancient Stone Keeper", "Galgann Firehammer", "Grimlok", "Archaedas" },
        expansion = 0,
        lastBossIndex = 7,
        maxLevel = 45,
        minLevel = 37,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    209,
    {
        activities = { [1] = 24, [11] = 306, },
        encounters = { "Hydromancer Velratha", "Ghaz'rilla", "Antu'sul", "Theka the Martyr", "Witch Doctor Zum'rah", "Nekrum Gutchewer", "Shadowpriest Sezz'ziz", "Chief Ukorz Sandscalp" },
        expansion = 0,
        lastBossIndex = 8,
        maxLevel = 85,
        minLevel = 78,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    349,
    {
        activities = { [1] = 273, [11] = 309, },
        encounters = { "Noxxion", "Razorlash", "Tinkerer Gizlock", "Lord Vyletongue", "Celebras the Cursed", "Landslide", "Rotgrip", "Princess Theradras" },
        expansion = 0,
        lastBossIndex = 8,
        maxLevel = 85,
        minLevel = 78,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    109,
    {
        activities = { [1] = 28, },
        encounters = { "Avatar of Hakkar", "Jammal'an the Prophet", "Dreamscythe", "Weaver", "Morphaz", "Hazzas", "Shade of Eranikus" },
        expansion = 0,
        lastBossIndex = 7,
        maxLevel = 60,
        minLevel = 50,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    230,
    {
        activities = { [1] = 276, [11] = 308, },
        encounters = { "High Interrogator Gerstahn", "Lord Roccor", "Houndmaster Grebmar", "Ring of Law", "Pyromancer Loregrain", "Lord Incendius", "Warder Stilgiss", "Fineous Darkvire", "Bael'Gar", "General Angerforge", "Golem Lord Argelmach", "Hurley Blackbreath", "Phalanx", "Ribbly Screwspigot", "Plugger Spazzring", "Ambassador Flamelash", "The Seven", "Magmus", "Emperor Dagran Thaurissan" },
        expansion = 0,
        lastBossIndex = 19,
        maxLevel = 85,
        minLevel = 84,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    229,
    {
        activities = { [1] = 330, },
        encounters = { "Highlord Omokk", "Shadow Hunter Vosh'gajin", "War Master Voone", "Mother Smolderweb", "Urok Doomhowl", "Quartermaster Zigris", "Halycon", "Gizrul the Slavener", "Overlord Wyrmthalak", "Pyroguard Emberseer", "Solakar Flamewreath", "Warchief Rend Blackhand", "The Beast", "General Drakkisath" },
        expansion = 0,
        lastBossIndex = 14,
        maxLevel = 65,
        minLevel = 58,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    429,
    {
        activities = { [1] = 38, },
        encounters = { "Zevrim Thornhoof", "Hydrospawn", "Lethtendris", "Alzzin the Wildshaper", "Tendris Warpwood", "Illyanna Ravenoak", "Magister Kalendris", "Immol'thar", "Prince Tortheldrin", "Guard Mol'dar", "Stomper Kreeg", "Guard Fengus", "Guard Slip'kik", "Captain Kromcrush", "Cho'Rush the Observer", "King Gordok" },
        expansion = 0,
        lastBossIndex = 16,
        maxLevel = 52,
        minLevel = 42,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    329,
    {
        activities = { [1] = 274, },
        encounters = { "Hearthsinger Forresten", "Timmy the Cruel", "Commander Malor", "Willey Hopebreaker", "Instructor Galford", "Balnazzar", "The Unforgiven", "Baroness Anastari", "Nerub'enkan", "Maleki the Pallid", "Magistrate Barthilas", "Ramstein the Gorger", "Lord Aurius Rivendare" },
        expansion = 0,
        lastBossIndex = 13,
        maxLevel = 56,
        minLevel = 46,
        resets = {},
        sizes = {},
    }
)
lib:addInstance(
    249,
    {
        activities = { [8] = 46, [9] = 257, },
        encounters = { "Onyxia" },
        expansion = 2,
        lastBossIndex = 1,
        legacy = { expansion = 0, size = 40, },
        maxLevel = 83,
        minLevel = 80,
        resets = { [10] = 7, [25] = 7, [40] = 5, },
        sizes = { 10, 25, 40 },
    }
)
lib:addInstance(
    409,
    {
        activities = { [6] = 48, },
        encounters = { "Lucifron", "Magmadar", "Gehennas", "Garr", "Shazzrah", "Baron Geddon", "Sulfuron Harbinger", "Golemagg the Incinerator", "Majordomo Executus", "Ragnaros" },
        expansion = 0,
        lastBossIndex = 10,
        maxLevel = 60,
        minLevel = 60,
        resets = { [40] = 7, },
        sizes = { 40 },
    }
)
lib:addInstance(
    469,
    {
        activities = { [6] = 50, },
        encounters = { "Razorgore the Untamed", "Vaelastrasz the Corrupt", "Broodlord Lashlayer", "Firemaw", "Ebonroc", "Flamegor", "Chromaggus", "Nefarian" },
        expansion = 0,
        lastBossIndex = 8,
        maxLevel = 60,
        minLevel = 60,
        resets = { [40] = 7, },
        sizes = { 40 },
    }
)
lib:addInstance(
    543,
    {
        activities = { [2] = 136, [3] = 188, },
        encounters = { "Omor the Unscarred", "Vazruden the Herald", "Watchkeeper Gargolmar" },
        expansion = 1,
        lastBossIndex = 3,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    542,
    {
        activities = { [2] = 137, [3] = 187, },
        encounters = { "The Maker", "Keli'dan the Breaker", "Broggok" },
        expansion = 1,
        lastBossIndex = 3,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    540,
    {
        activities = { [2] = 138, [3] = 189, },
        encounters = { "Blood Guard Porung", "Grand Warlock Nethekurse", "Warbringer O'mrogg", "Warchief Kargath Bladefist" },
        expansion = 1,
        lastBossIndex = 4,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    547,
    {
        activities = { [2] = 140, [3] = 184, [11] = 286, },
        encounters = { "Mennu the Betrayer", "Quagmirran", "Rokmar the Crackler" },
        expansion = 1,
        lastBossIndex = 3,
        maxLevel = 85,
        minLevel = 84,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    546,
    {
        activities = { [2] = 146, [3] = 186, },
        encounters = { "Ghaz'an", "Hungarfen", "Swamplord Musel'ek", "The Black Stalker" },
        expansion = 1,
        lastBossIndex = 4,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    545,
    {
        activities = { [2] = 147, [3] = 185, },
        encounters = { "Hydromancer Thespia", "Mekgineer Steamrigger", "Warlord Kalithresh" },
        expansion = 1,
        lastBossIndex = 3,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    557,
    {
        activities = { [2] = 148, [3] = 179, },
        encounters = { "Nexus-Prince Shaffar", "Pandemonius", "Yor", "Tavarok" },
        expansion = 1,
        lastBossIndex = 4,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    558,
    {
        activities = { [2] = 149, [3] = 178, },
        encounters = { "Exarch Maladaar", "Shirrak the Dead Watcher" },
        expansion = 1,
        lastBossIndex = 2,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    556,
    {
        activities = { [2] = 150, [3] = 180, },
        encounters = { "Talon King Ikiss", "Darkweaver Syth", "Anzu" },
        expansion = 1,
        lastBossIndex = 3,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    555,
    {
        activities = { [2] = 151, [3] = 181, },
        encounters = { "Ambassador Hellmaw", "Blackheart the Inciter", "Murmur", "Grandmaster Vorpil" },
        expansion = 1,
        lastBossIndex = 4,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    533,
    {
        activities = { [8] = 159, [9] = 227, },
        encounters = { "Anub'Rekhan", "Grand Widow Faerlina", "Maexxna", "Noth the Plaguebringer", "Heigan the Unclean", "Loatheb", "Instructor Razuvious", "Gothik the Harvester", "The Four Horsemen", "Patchwerk", "Grobbulus", "Gluth", "Thaddius", "Sapphiron", "Kel'Thuzad" },
        expansion = 2,
        lastBossIndex = 15,
        maxLevel = 83,
        minLevel = 80,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    509,
    {
        activities = { [6] = 160, },
        encounters = { "Kurinnaxx", "General Rajaxx", "Moam", "Buru the Gorger", "Ayamiss the Hunter", "Ossirian the Unscarred" },
        expansion = 0,
        lastBossIndex = 6,
        maxLevel = 60,
        minLevel = 60,
        resets = { [20] = 3, },
        sizes = { 20 },
    }
)
lib:addInstance(
    531,
    {
        activities = { [6] = 161, },
        encounters = { "The Prophet Skeram", "Silithid Royalty", "Battleguard Sartura", "Fankriss the Unyielding", "Viscidus", "Princess Huhuran", "Twin Emperors", "Ouro", "C'thun" },
        expansion = 0,
        lastBossIndex = 9,
        maxLevel = 60,
        minLevel = 60,
        resets = { [40] = 7, },
        sizes = { 40 },
    }
)
lib:addInstance(
    560,
    {
        activities = { [2] = 170, [3] = 183, },
        encounters = { "Lieutenant Drake", "Epoch Hunter", "Captain Skarloc" },
        expansion = 1,
        lastBossIndex = 3,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    269,
    {
        activities = { [2] = 171, [3] = 182, },
        encounters = { "Aeonus", "Chrono Lord Deja", "Temporus" },
        expansion = 1,
        lastBossIndex = 3,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    554,
    {
        activities = { [2] = 172, [3] = 192, },
        encounters = { "Nethermancer Sepethrea", "Pathaleon the Calculator", "Mechano-Lord Capacitus", "Gatewatcher Gyro-Kill", "Gatewatcher Iron-Hand" },
        expansion = 1,
        lastBossIndex = 5,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    553,
    {
        activities = { [2] = 173, [3] = 191, },
        encounters = { "Commander Sarannis", "High Botanist Freywinn", "Laj", "Thorngrin the Tender", "Warp Splinter" },
        expansion = 1,
        lastBossIndex = 5,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    552,
    {
        activities = { [2] = 174, [3] = 190, },
        encounters = { "Dalliah the Doomsayer", "Harbinger Skyriss", "Wrath-Scryer Soccothrates", "Zereketh the Unbound" },
        expansion = 1,
        lastBossIndex = 4,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    532,
    {
        activities = { [7] = 175, },
        encounters = { "Attumen the Huntsman", "Moroes", "Maiden of Virtue", "Opera Hall", "The Curator", "Terestian Illhoof", "Shade of Aran", "Netherspite", "Chess Event", "Prince Malchezaar", "Nightbane" },
        expansion = 1,
        lastBossIndex = 11,
        maxLevel = 70,
        minLevel = 70,
        resets = { [10] = 7, },
        sizes = { 10 },
    }
)
lib:addInstance(
    544,
    {
        activities = { [7] = 176, },
        encounters = { "Magtheridon" },
        expansion = 1,
        lastBossIndex = 1,
        maxLevel = 70,
        minLevel = 70,
        resets = { [25] = 7, },
        sizes = { 25 },
    }
)
lib:addInstance(
    565,
    {
        activities = { [7] = 177, },
        encounters = { "High King Maulgar", "Gruul the Dragonkiller" },
        expansion = 1,
        lastBossIndex = 2,
        maxLevel = 70,
        minLevel = 70,
        resets = { [25] = 7, },
        sizes = { 25 },
    }
)
lib:addInstance(
    550,
    {
        activities = { [7] = 193, },
        encounters = { "Al'ar", "Void Reaver", "High Astromancer Solarian", "Kael'thas Sunstrider" },
        expansion = 1,
        lastBossIndex = 4,
        maxLevel = 70,
        minLevel = 70,
        resets = { [25] = 7, },
        sizes = { 25 },
    }
)
lib:addInstance(
    548,
    {
        activities = { [7] = 194, },
        encounters = { "Hydross the Unstable", "The Lurker Below", "Leotheras the Blind", "Fathom-Lord Karathress", "Morogrim Tidewalker", "Lady Vashj" },
        expansion = 1,
        lastBossIndex = 6,
        maxLevel = 70,
        minLevel = 70,
        resets = { [25] = 7, },
        sizes = { 25 },
    }
)
lib:addInstance(
    534,
    {
        activities = { [7] = 195, },
        encounters = { "Rage Winterchill", "Anetheron", "Kaz'rogal", "Azgalor", "Archimonde" },
        expansion = 1,
        lastBossIndex = 5,
        maxLevel = 70,
        minLevel = 70,
        resets = { [25] = 7, },
        sizes = { 25 },
    }
)
lib:addInstance(
    564,
    {
        activities = { [7] = 196, },
        encounters = { "High Warlord Naj'entus", "Supremus", "Shade of Akama", "Teron Gorefiend", "Gurtogg Bloodboil", "Reliquary of Souls", "Mother Shahraz", "The Illidari Council", "Illidan Stormrage" },
        expansion = 1,
        lastBossIndex = 9,
        maxLevel = 70,
        minLevel = 70,
        resets = { [25] = 7, },
        sizes = { 25 },
    }
)
lib:addInstance(
    585,
    {
        activities = { [2] = 198, [3] = 201, },
        encounters = { "Kael'thas Sunstrider", "Priestess Delrissa", "Selin Fireheart", "Vexallus" },
        expansion = 1,
        lastBossIndex = 4,
        maxLevel = 75,
        minLevel = 70,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    580,
    {
        activities = { [7] = 199, },
        encounters = { "Kalecgos", "Brutallus", "Felmyst", "Eredar Twins", "M'uru", "Kil'jaeden" },
        expansion = 1,
        lastBossIndex = 6,
        maxLevel = 70,
        minLevel = 70,
        resets = { [25] = 7, },
        sizes = { 25 },
    }
)
lib:addInstance(
    574,
    {
        activities = { [4] = 202, [5] = 242, [174] = 2448, [175] = 2474, [176] = 2491, },
        encounters = { "Prince Keleseth", "Skarvold & Dalronn", "Ingvar the Plunderer" },
        expansion = 2,
        lastBossIndex = 3,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    575,
    {
        activities = { [4] = 203, [5] = 205, [174] = 2453, [175] = 2479, [176] = 2489, },
        encounters = { "Svala Sorrowgrave", "Gortok Palehoof", "Skadi the Ruthless", "King Ymiron" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    601,
    {
        activities = { [4] = 204, [5] = 241, [174] = 2456, [175] = 2483, [176] = 2494, },
        encounters = { "Krik'thir the Gatewatcher", "Hadronox", "Anub'arak" },
        expansion = 2,
        lastBossIndex = 3,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    578,
    {
        activities = { [4] = 206, [5] = 211, [174] = 2451, [175] = 2482, [176] = 2497, },
        encounters = { "Drakos the Interrogator", "Varos Cloudstrider", "Mage-Lord Urom", "Ley-Guardian Eregos" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    602,
    {
        activities = { [4] = 207, [5] = 212, [174] = 2459, [175] = 2480, [176] = 2487, },
        encounters = { "General Bjarngrim", "Volkhan", "Ionar", "Loken" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    599,
    {
        activities = { [4] = 208, [5] = 213, [174] = 2460, [175] = 2473, [176] = 2488, },
        encounters = { "Krystallus", "Maiden of Grief", "Tribunal of Ages", "Sjonnir the Ironshaper" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    595,
    {
        activities = { [4] = 209, [5] = 210, [174] = 2449, [175] = 2472, [176] = 2493, },
        encounters = { "Meathook", "Salram the Fleshcrafter", "Chrono-Lord Epoch", "Mal'ganis" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    600,
    {
        activities = { [4] = 214, [5] = 215, [174] = 2457, [175] = 2481, [176] = 2496, },
        encounters = { "Trollgore", "Novos the Summoner", "King Dred", "The Prophet Tharon'ja" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    604,
    {
        activities = { [4] = 216, [5] = 217, [174] = 2458, [175] = 2478, [176] = 2490, },
        encounters = { "Slad'ran", "Drakkari Colossus", "Moorabi", "Gal'darah", "Eck the Ferocious" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    619,
    {
        activities = { [4] = 218, [5] = 219, [174] = 2455, [175] = 2476, [176] = 2486, },
        encounters = { "Elder Nadox", "Prince Taldaram", "Jedoga Shadowseeker", "Herald Volazj", "Amanitar" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    608,
    {
        activities = { [4] = 220, [5] = 221, [174] = 2454, [175] = 2475, [176] = 2495, },
        encounters = { "First Prisoner", "Second Prisoner", "Cyanigosa" },
        expansion = 2,
        lastBossIndex = 3,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    616,
    {
        activities = { [8] = 223, [9] = 237, },
        encounters = { "Malygos" },
        expansion = 2,
        lastBossIndex = 1,
        maxLevel = 83,
        minLevel = 80,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    615,
    {
        activities = { [8] = 224, [9] = 238, },
        encounters = { "Vesperon", "Tenebron", "Shadron", "Sartharion" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    576,
    {
        activities = { [4] = 225, [5] = 226, [174] = 2450, [175] = 2477, [176] = 2492, },
        encounters = { "Grand Magus Telestra", "Anomalus", "Ormorok the Tree-Shaper", "Keristrasza" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    624,
    {
        activities = { [8] = 239, [9] = 240, },
        encounters = { "Archavon the Stone Watcher", "Emalon the Storm Watcher", "Koralon the Flame Watcher", "Toravon the Ice Watcher" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    603,
    {
        activities = { [8] = 243, [9] = 244, },
        encounters = { "Flame Leviathan", "Ignis the Furnace Master", "Razorscale", "XT-002 Deconstructor", "The Assembly of Iron", "Kologarn", "Auriaya", "Hodir", "Thorim", "Elder Brightleaf", "Elder Ironbranch", "Elder Stonebark", "Freya", "Mimiron", "General Vezax", "Yogg-Saron", "Algalon the Observer" },
        expansion = 2,
        lastBossIndex = 17,
        maxLevel = 83,
        minLevel = 80,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    650,
    {
        activities = { [4] = 245, [5] = 249, [174] = 2452, [175] = 2471, },
        encounters = { "Grand Champions", "Argent Champion", "The Black Knight" },
        expansion = 2,
        lastBossIndex = 3,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    649,
    {
        activities = { [8] = 247, [9] = 250, },
        encounters = { "Northrend Beasts", "Lord Jaraxxus", "Faction Champions", "Val'kyr Twins", "Anub'arak" },
        expansion = 2,
        lastBossIndex = 5,
        maxLevel = 83,
        minLevel = 80,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    632,
    {
        activities = { [4] = 251, [5] = 252, [174] = 2463, },
        encounters = { "Bronjahm", "Devourer of Souls" },
        expansion = 2,
        lastBossIndex = 2,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    658,
    {
        activities = { [4] = 253, [5] = 254, [174] = 2462, },
        encounters = { "Forgemaster Garfrost", "Krick", "Scourgelord Tyrannus" },
        expansion = 2,
        lastBossIndex = 3,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    668,
    {
        activities = { [4] = 255, [5] = 256, [174] = 2461, },
        encounters = { "Falric", "Marwyn", "Escaped from Arthas" },
        expansion = 2,
        lastBossIndex = 3,
        maxLevel = 83,
        minLevel = 80,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    631,
    {
        activities = { [8] = 279, [9] = 280, },
        encounters = { "Lord Marrowgar", "Lady Deathwhisper", "Icecrown Gunship Battle", "Deathbringer Saurfang", "Rotface", "Festergut", "Professor Putricide", "Blood Council", "Queen Lana'thel", "Valithria Dreamwalker", "Sindragosa", "The Lich King" },
        expansion = 2,
        lastBossIndex = 12,
        maxLevel = 83,
        minLevel = 80,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    724,
    {
        activities = { [8] = 293, [9] = 294, },
        encounters = { "Baltharus the Warborn", "Saviana Ragefire", "General Zarithrian", "Halion" },
        expansion = 2,
        lastBossIndex = 4,
        maxLevel = 83,
        minLevel = 80,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    643,
    {
        activities = { [12] = 324, [13] = 302, },
        encounters = { "Lady Naz'jar", "Commander Ulthok", "Mindbender Ghur'sha", "Ozumat" },
        expansion = 3,
        lastBossIndex = 4,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    645,
    {
        activities = { [12] = 323, [13] = 303, },
        encounters = { "Rom'ogg Bonecrusher", "Corla, Herald of Twilight", "Karsh Steelbender", "Beauty", "Ascendant Lord Obsidius" },
        expansion = 3,
        lastBossIndex = 5,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    670,
    {
        activities = { [12] = 322, [13] = 304, },
        encounters = { "General Umbriss", "Forgemaster Throngus", "Drahga Shadowburner", "Erudax" },
        expansion = 3,
        lastBossIndex = 4,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    644,
    {
        activities = { [12] = 321, [13] = 305, },
        encounters = { "Temple Guardian Anhuur", "Earthrager Ptah", "Anraphet", "Isiset", "Ammunae", "Setesh", "Rajh" },
        expansion = 3,
        lastBossIndex = 7,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    725,
    {
        activities = { [12] = 320, [13] = 307, },
        encounters = { "Corborus", "Slabhide", "Ozruk", "High Priestess Azil" },
        expansion = 3,
        lastBossIndex = 4,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    657,
    {
        activities = { [12] = 319, [13] = 311, },
        encounters = { "Grand Vizier Ertan", "Altairus", "Asaad" },
        expansion = 3,
        lastBossIndex = 3,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    755,
    {
        activities = { [12] = 325, [13] = 312, },
        encounters = { "General Husam", "High Prophet Barim", "Lockmaw", "Siamat" },
        expansion = 3,
        lastBossIndex = 4,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    669,
    {
        activities = { [14] = 314, [15] = 313, },
        encounters = { "Omnotron Defense System", "Magmaw", "Atramedes", "Chimaeron", "Maloriak", "Nefarian's End" },
        expansion = 3,
        lastBossIndex = 6,
        maxLevel = 85,
        minLevel = 85,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    671,
    {
        activities = { [14] = 316, [15] = 315, },
        encounters = { "Halfus Wyrmbreaker", "Theralion and Valiona", "Ascendant Council", "Cho'gall", "Sinestra" },
        expansion = 3,
        lastBossIndex = 5,
        maxLevel = 85,
        minLevel = 85,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    754,
    {
        activities = { [14] = 318, [15] = 317, },
        encounters = { "Conclave of Wind", "Al'Akir" },
        expansion = 3,
        lastBossIndex = 2,
        maxLevel = 85,
        minLevel = 85,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    757,
    {
        activities = { [14] = 329, [15] = 328, },
        encounters = { "Argaloth", "Occu'thar", "Alizabal" },
        expansion = 3,
        lastBossIndex = 3,
        maxLevel = 85,
        minLevel = 85,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    859,
    {
        activities = { [12] = 334, },
        encounters = { "High Priest Venoxis", "Bloodlord Mandokir", "Cache of Madness", "High Priestess Kilnara", "Zanzil", "Jin'do the Godbreaker" },
        expansion = 3,
        lastBossIndex = 6,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    568,
    {
        activities = { [12] = 340, },
        encounters = { "Akil'zon", "Nalorakk", "Jan'alai", "Halazzi", "Hex Lord Malacrass", "Daakara" },
        expansion = 3,
        lastBossIndex = 6,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, [10] = 7, },
        sizes = { 5, 10 },
    }
)
lib:addInstance(
    720,
    {
        activities = { [14] = 362, [15] = 361, },
        encounters = { "Beth'tilac", "Lord Rhyolith", "Shannox", "Alysrazor", "Baleroc", "Majordomo Staghelm", "Ragnaros" },
        expansion = 3,
        lastBossIndex = 7,
        maxLevel = 85,
        minLevel = 85,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    967,
    {
        activities = { [0] = 417, [14] = 448, [15] = 447, },
        encounters = { "Morchok", "Warlord Zon'ozz", "Yor'sahj the Unsleeping", "Hagara", "Ultraxion", "Warmaster Blackhorn", "Spine of Deathwing", "Madness of Deathwing" },
        expansion = 3,
        lastBossIndex = 8,
        maxLevel = 85,
        minLevel = 85,
        resets = { [10] = 7, [25] = 7, },
        sizes = { 10, 25 },
    }
)
lib:addInstance(
    938,
    {
        activities = { [12] = 435, [33] = 436, },
        encounters = { "First Echo", "Second Echo", "Murozond" },
        expansion = 3,
        lastBossIndex = 3,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    939,
    {
        activities = { [12] = 437, [33] = 438, },
        encounters = { "Peroth'arn", "Queen Azshara", "Mannoroth" },
        expansion = 3,
        lastBossIndex = 3,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)
lib:addInstance(
    940,
    {
        activities = { [12] = 439, [33] = 440, },
        encounters = { "Arcurion", "Asira Dawnslayer", "Archbishop Benedictus" },
        expansion = 3,
        lastBossIndex = 3,
        maxLevel = 85,
        minLevel = 85,
        resets = { [5] = 1, },
        sizes = { 5 },
    }
)