class RaCSave:
    GAMES = ["rac1", "rac2", "rac3", "rac4"]
    LANGUAGES = {"EN": 0, "FR": 2, "DE": 3, "ES": 4 ,"IT": 5}
    VALUE_OFFSET = {"rac1": {"Bolts": [36, 4, 2147483647], "Completed": [48, 1, 255]},
                    "rac2": {"Bolts": [36, 4, 2147483647], "Raritanium": [40, 4, 2147483647], "Completed": [54, 1, 255], "Nanotech": [56, 4, 204778415], "Crystals": [70, 2, 32767], "Moonstones": [72, 2, 65535], "Bolts Multiplier": [94, 1, 255] , "Language": [6264, 1, 5]},
                    "rac3": {"Bolts": [36, 4, 2147483647], "Completed": [86, 1, 255], "Nanotech": [88, 4, 61503510], "Crystals": [102, 2, 32767], "Bolts Multiplier": [126, 1, 255], "Language": [11279, 1, 5]},
                    "rac4": {"Bolts": [36, 4, 2147483647], "Nanotech": [44, 4, 45281245], "Dread Points": [48, 4, 2147483647], "Bolts Multiplier": [66, 1, 255], "Language": [30785, 1, 5]}
                   }
    ITEMS_OFFSET = {"rac1": {"Zoomerator": 88, "Raritanium": 89, "CodeBot": 90, "Heli-Pack": 442, "Thruster-Pack": 443,
                             "Hydro-Pack": 444, "Sonic Summoner": 445, "O2 Mask": 446, "Pilot Helmet": 447, "Suck Cannon": 449,
                             "Devastator": 451, "Swingshot": 452, "Visibomb Gun": 453, "Taunter": 454, "Blaster": 455,
                             "Pyrocitor": 456, "Mine Glove": 457, "Walloper": 458, "Tesla Claw": 459, "Glove of Doom": 460,
                             "Morph-o-ray": 461, "Hydrodisplacer": 462, "RYNO": 463, "Drone Device": 464, "Decoy Glove": 465,
                             "Trespasser": 466, "Metal Detector": 467, "Magneboots": 468, "Grind Boots": 469, "Hoverboard": 470,
                             "Hologuise": 471, "PDA": 472, "Map-o-matic": 473, "Bolt Grabber": 474, "Persuader": 475},
                    "rac2": {"Nanotech Boost 1": 84, "Nanotech Boost 2": 85, "Nanotech Boost 3": 86, "Nanotech Boost 4": 87, "Nanotech Boost 5": 88,
                             "Nanotech Boost 6": 89, "Nanotech Boost 7": 90, "Nanotech Boost 8": 91, "Nanotech Boost 9": 92, "Nanotech Boost 10": 93,
                             "Heli-Pack": 658, "Thruster-Pack": 659, "Hydro-Pack": 660, "Mapper": 661, "Armor Magnetizer": 663,
                             "Levitator": 664, "Clank Zapper": 665, "Bomb Glove": 668, "Swingshot": 669, "Visibomb Gun": 670,
                             "Sheepinator": 672, "Decoy Glove": 673, "Tesla Claw": 674, "Gravity Boots": 675, "Grind Boots": 676,
                             "Glider": 677, "Chopper": 678, "Pulse Rifle": 679, "Seeker Gun": 680, "Hoverbomb Gun": 681,
                             "Blitz Gun": 682, "Minirocket Tube": 683, "Plasma Coil": 684, "Lava Gun": 685, "Synthenoids": 687,
                             "Spiderbot Glove": 688, "Dynamo": 692, "Bouncer": 693, "Electrolyzer": 694, "Thermanator": 695,
                             "Miniturret Glove": 697, "Zodiac": 699, "RYNO II": 700, "Shield Charger": 701, "Tractor Beam": 702,
                             "Biker Helmet": 704, "Quark Statuette": 705, "Box Breaker": 706, "Infiltrator": 707, "Walloper": 709,
                             "Charge Boots": 710, "Hypnomatic": 711},
                    "rac3": {"Heli-Pack": 1194, "Thruster-Pack": 1195, "Hydro-Pack": 1196, "Map-o-matic": 1197, "Bolt Grabber": 1199,
                             "Hypershot": 1203, "Gravity Boots": 1205, "Plasma Coil": 1208, "Lava Gun": 1209, "Refractor": 1210,
                             "Bouncer": 1211, "Hacker": 1212, "Miniturret Glove": 1213, "Shield Charger": 1214, "Charge Boots": 1221,
                             "Thyrraguise": 1222, "Warp Pad": 1223, "Nano Pak": 1224, "Star Map": 1225, "Master Plan": 1226,
                             "PDA": 1227, "Shock Blaster": 1231, "N60 Storm": 1239, "Infector": 1247, "Annihilator": 1255,
                             "Spitting Hydra": 1263, "Disc Blade Gun": 1271, "Glove of Doom": 1279, "Rift Inducer": 1287, "Holoshield Glove": 1295,
                             "Flux Rifle": 1303, "Nitro Launcher": 1311, "Plasma Whip": 1319, "Suck Cannon": 1327, "Qwack-o-ray": 1335,
                             "RYNO III": 1343},
                    "rac4": {"Arbiter": 3172, "Fusion Rifle": 3240, "Hunter Mine Launcher": 3308, "B6-Obliterator": 3376, "Holoshield Launcher": 3444,
                             "Mini Turret Launcher": 3512, "Harbinger": 3580, "Scorpion Flail": 3920}
                   }

    def __init__(self, path, game):
        self.path = path
        self.game = game
        with open(path, "rb") as file: self.bytes = bytearray(file.read())
        self.readChunks()

    def readChunks(self):
        self.chunks = []
        chunkOffset = 8
        while(chunkOffset < len(self.bytes)):
            chunkCrc16Offset = chunkOffset + 4
            chunkDataOffset = chunkOffset + 8
            chunkLen = int.from_bytes(self.bytes[chunkOffset:(chunkOffset + 4)], byteorder = "little")
            self.chunks.append((chunkOffset, chunkCrc16Offset, chunkDataOffset, chunkLen))
            chunkOffset = chunkDataOffset + chunkLen

    def getItems(self):
        items = []
        if self.game != "rac4":
            for name, offset in self.ITEMS_OFFSET[self.game].items(): items.append((name, self.bytes[offset]))
        else:
            for name, offset in self.ITEMS_OFFSET[self.game].items():
                valBytes = self.bytes[offset:(offset + 2)]
                val = int.from_bytes(valBytes, byteorder = "little")
                items.append((name, int(val != 65535)))
        return items

    def updateItem(self, name, val):
        if self.game != "rac4": self.bytes[self.ITEMS_OFFSET[self.game][name]] = 1 if val else 0
        else:
            if val:
                for i in range(2):
                    if self.bytes[self.ITEMS_OFFSET[self.game][name] + i] == 255: self.bytes[self.ITEMS_OFFSET[self.game][name] + i] = 0
            else:
                for i in range(2): self.bytes[self.ITEMS_OFFSET[self.game][name] + i] = 255

    def getValues(self):
        values = []
        for name, data in self.VALUE_OFFSET[self.game].items():
            offset, size = data[0], data[1]
            valBytes = self.bytes[offset:(offset + size)]
            val = int.from_bytes(valBytes, byteorder = "little")
            if name == "Bolts Multiplier" and self.game != "rac2": val += 1
            elif name == "Language":
                for lang, byte in self.LANGUAGES.items():
                    if byte == val:
                        val = lang
                        break
            values.append((name, str(val)))
        return values

    def updateValue(self, name, val):
        offset, size, max = self.VALUE_OFFSET[self.game][name][0], self.VALUE_OFFSET[self.game][name][1], self.VALUE_OFFSET[self.game][name][2]
        if name == "Language": val = self.LANGUAGES[val]
        val = min(int(val), max)
        if name == "Bolts Multiplier" and self.game != "rac2": val -= 1
        if val < 0: val = 0
        valBytes = val.to_bytes(size, byteorder = "little")
        for i in range(size): self.bytes[offset + i] = valBytes[i]

    def updateCrc16(self):
        for chunk in self.chunks:
            crc16Offset, dataOffset, dataLen = chunk[1], chunk[2], chunk[3]
            data = self.bytes[dataOffset:(dataOffset + dataLen)]
            crc16 = 0x8320
            for byte in data:
                crc16 ^= byte << 8
                for _ in range(8): crc16 = (crc16 << 1) ^ 0x1F45 if crc16 & 0x8000 else crc16 << 1
            crc16 &= 0xFFFF
            crc16Bytes = crc16.to_bytes(2, byteorder = "little")
            for i in range(2): self.bytes[crc16Offset + i] = crc16Bytes[i]

    def update(self):
        self.updateCrc16()
        with open(self.path, "wb") as file: file.write(self.bytes)