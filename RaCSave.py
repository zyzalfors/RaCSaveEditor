import re

class RaCSave:
    GAMES = ("rac1", "rac2", "rac3", "rac4")

    LANGUAGES = {"EN": 0, "FR": 2, "DE": 3, "ES": 4 ,"IT": 5}

    VALUE_DATA = {"rac1": {"Bolts": (36, 4, True), "Completed": (48, 1, True), "Bomb Glove": (324, 4, True), "Devastator": (328, 4, True), "Visibomb Gun": (336, 4, True),
                           "Blaster": (344, 4, True), "Pyrocitor": (348, 4, True), "Mine Glove": (352, 4, True), "Tesla Claw": (360, 4, True), "Glove of Doom": (364, 4, True),
                           "RYNO": (376, 4, True), "Drone Device": (380, 4, True), "Decoy Glove": (384, 4, True)},
                  "rac2": {"Bolts": (36, 4, True), "Raritanium": (40, 4, True), "Completed": (54, 1, True), "Nanotech": (56, 4, True), "Crystals": (70, 2, True),
                           "Moonstones": (72, 2, False), "Bolts Multiplier": (94, 1, False), "Clank Zapper": (460, 4, True), "Bomb Glove": (472, 4, True), "Visibomb Gun": (480, 4, True),
                           "Decoy Glove": (492, 4, True), "Tesla Claw": (496, 4, True), "Chopper": (512, 4, True), "Pulse Rifle": (516, 4, True), "Seeker Gun": (520, 4, True),
                           "Hoverbomb Gun": (524, 4, True), "Blitz Gun": (528, 4, True), "Minirocket Tube": (532, 4, True), "Plasma Coil": (536, 4, True), "Lava Gun": (540, 4, True),
                           "Lancer": (544, 4, True), "Synthenoid": (548, 4, True), "Spiderbot Glove": (552, 4, True), "Bouncer": (572, 4, True), "Miniturret Glove": (588, 4, True),
                           "Gravity Bomb": (592, 4, True), "Zodiac": (596, 4, True), "RYNO II": (600, 4, True), "Shield Charger": (604, 4, True), "Language": (6264, 1, True)},
                  "rac3": {"Bolts": (36, 4, True), "Completed": (86, 1, True), "Nanotech": (88, 4, True), "Crystals": (102, 2, True), "Bolts Multiplier": (126, 1, False),
                           "Plasma Coil": (624, 4, True), "Lava Gun": (628, 4, True), "Bouncer": (636, 4, True), "Miniturret Glove": (644, 4, True), "Shield Charger": (648, 4, True),
                           "Shock Blaster": (716, 4, True), "N60 Storm": (748, 4, True), "Infector": (780, 4, True), "Annihilator": (812, 4, True), "Spitting Hydra": (844, 4, True),
                           "Disc Blade Gun": (876, 4, True), "Glove of Doom": (908, 4, True), "Rift Inducer": (940, 4, True), "Holoshield Glove": (972, 4, True), "Flux Rifle": (1004, 4, True),
                           "Nitro Launcher": (1036, 4, True), "Plasma Whip": (1068, 4, True), "RYNO III": (1164, 4, True), "Language": (11279, 1, True)},
                  "rac4": {"Bolts": (36, 4, True), "Nanotech": (44, 4, True), "Dread Points": (48, 4, True), "Bolts Multiplier": (66, 1, False), "Speed Mod": (325, 1, True),
                           "Ammo Mod": (326, 1, True), "Aiming Mod": (327, 1, True), "Impact Mod": (328, 1, True), "Area Mod": (329, 1, True), "XP Mod": (330, 1, True),
                           "Jackpot Mod": (331, 1, True), "Nanoleech Mod": (332, 1, True), "Dual Vipers": (3038, 2, True), "Magma Cannon": (3106, 2, True), "Arbiter": (3174, 2, True),
                           "Fusion Rifle": (3242, 2, True), "Hunter Mine Launcher": (3310, 2, True), "B6-Obliterator": (3378, 2, True), "Holoshield Launcher": (3446, 2, True), "Miniturret Launcher": (3514, 2, True),
                           "Harbinger": (3582, 2, True), "Scorpion Flail": (3922, 2, True), "Language": (30785, 1, True)}}

    ITEM_OFFSETS = {"rac1": {"Zoomerator": 88, "Raritanium": 89, "CodeBot": 90, "Heli-Pack": 442, "Thruster-Pack": 443,
                             "Hydro-Pack": 444, "Sonic Summoner": 445, "O2 Mask": 446, "Pilot Helmet": 447, "Suck Cannon": 449,
                             "Devastator": 451, "Swingshot": 452, "Visibomb Gun": 453, "Taunter": 454, "Blaster": 455,
                             "Pyrocitor": 456, "Mine Glove": 457, "Walloper": 458, "Tesla Claw": 459, "Glove of Doom": 460,
                             "Morph-o-ray": 461, "Hydrodisplacer": 462, "RYNO": 463, "Drone Device": 464, "Decoy Glove": 465,
                             "Trespasser": 466, "Metal Detector": 467, "Magneboots": 468, "Grind Boots": 469, "Hoverboard": 470,
                             "Hologuise": 471, "PDA": 472, "Map-o-matic": 473, "Bolt Grabber": 474, "Persuader": 475},
                    "rac2": {"Nanotech Boost 1": 84, "Nanotech Boost 2": 85, "Nanotech Boost 3": 86, "Nanotech Boost 4": 87, "Nanotech Boost 5": 88,
                             "Nanotech Boost 6": 89, "Nanotech Boost 7": 90, "Nanotech Boost 8": 91, "Nanotech Boost 9": 92, "Nanotech Boost 10": 93,
                             "Mapper": 661, "Armor Magnetizer": 663, "Levitator": 664, "Clank Zapper": 665, "Bomb Glove": 668,
                             "Swingshot": 669, "Visibomb Gun": 670, "Sheepinator": 672, "Decoy Glove": 673, "Tesla Claw": 674,
                             "Gravity Boots": 675, "Grind Boots": 676, "Glider": 677, "Chopper": 678, "Pulse Rifle": 679,
                             "Seeker Gun": 680, "Hoverbomb Gun": 681 , "Blitz Gun": 682, "Minirocket Tube": 683, "Plasma Coil": 684,
                             "Lava Gun": 685, "Synthenoid": 687, "Spiderbot Glove": 688, "Dynamo": 692, "Bouncer": 693,
                             "Electrolyzer": 694, "Thermanator": 695, "Miniturret Glove": 697, "Zodiac": 699, "RYNO II": 700,
                             "Shield Charger": 701, "Tractor Beam": 702, "Biker Helmet": 704, "Quark Statuette": 705, "Box Breaker": 706,
                             "Infiltrator": 707, "Walloper": 709, "Charge Boots": 710, "Hypnomatic": 711},
                    "rac3": {"Map-o-matic": 1197, "Bolt Grabber": 1199, "Hypershot": 1203, "Gravity Boots": 1205, "Plasma Coil": 1208,
                             "Lava Gun": 1209, "Refractor": 1210, "Bouncer": 1211, "Hacker": 1212, "Miniturret Glove": 1213,
                             "Shield Charger": 1214, "Charge Boots": 1221, "Thyrraguise": 1222, "Warp Pad": 1223, "Nano Pak": 1224,
                             "PDA": 1227, "Shock Blaster": 1231, "N60 Storm": 1239, "Infector": 1247, "Annihilator": 1255,
                             "Spitting Hydra": 1263, "Disc Blade Gun": 1271, "Glove of Doom": 1279, "Rift Inducer": 1287, "Holoshield Glove": 1295,
                             "Flux Rifle": 1303, "Nitro Launcher": 1311, "Plasma Whip": 1319, "Suck Cannon": 1327, "Qwack-o-ray": 1335,
                             "RYNO III": 1343},
                    "rac4": {"Arbiter": 3172, "Fusion Rifle": 3240, "Hunter Mine Launcher": 3308, "B6-Obliterator": 3376, "Holoshield Launcher": 3444,
                             "Miniturret Launcher": 3512, "Harbinger": 3580, "Scorpion Flail": 3920}}


    def __init__(self, path, game):
        self.path = path
        self.game = game.lower()

        with open(path, "rb") as f:
            self.bytes = bytearray(f.read())

        self.readChunks()


    def readChunks(self):
        self.chunks = []
        offset = 8

        while(offset < len(self.bytes)):
            size = int.from_bytes(self.bytes[offset:(offset + 4)], byteorder = "little")
            crc16Offset = offset + 4
            dataOffset = offset + 8
            self.chunks.append((offset, crc16Offset, dataOffset, size))
            offset = dataOffset + size


    def updateCrc16(self):
        for chunk in self.chunks:
            dataOffset = chunk[2]
            size = chunk[3]

            crc16 = 0x8320
            for byte in self.bytes[dataOffset:(dataOffset + size)]:
                crc16 ^= byte << 8

                for _ in range(8):
                    crc16 = (crc16 << 1) ^ 0x1F45 if crc16 & 0x8000 else crc16 << 1

            crc16 &= 0xFFFF
            crc16Bytes = crc16.to_bytes(2, byteorder = "little")
            crc16Offset = chunk[1]

            for i in range(2):
                self.bytes[crc16Offset + i] = crc16Bytes[i]


    def checkCrc16(self):
        for chunk in self.chunks:
            dataOffset = chunk[2]
            size = chunk[3]

            crc16 = 0x8320
            for byte in self.bytes[dataOffset:(dataOffset + size)]:
                crc16 ^= byte << 8

                for _ in range(8):
                    crc16 = (crc16 << 1) ^ 0x1F45 if crc16 & 0x8000 else crc16 << 1

            crc16 &= 0xFFFF
            crc16Offset = chunk[1]
            readCrc16 = int.from_bytes(self.bytes[crc16Offset:(crc16Offset + 2)], byteorder = "little")

            if crc16 != readCrc16:
                return chunk, False

        return None, True


    def getItems(self):
        items = []

        if not self.game in self.GAMES:
            return items

        if self.game != "rac4":
            for name, offset in self.ITEM_OFFSETS[self.game].items():
                items.append((name, self.bytes[offset]))

        else:
            for name, offset in self.ITEM_OFFSETS[self.game].items():
                val = int.from_bytes(self.bytes[offset:(offset + 2)], byteorder = "little")
                items.append((name, int(val != 65535)))

        return items


    def updateItem(self, name, val):
        if not self.game in self.GAMES:
            return

        offsets = self.ITEM_OFFSETS[self.game]
        if not name in offsets:
            return

        offset = offsets[name]

        if self.game != "rac4":
            self.bytes[offset] = 1 if val else 0

        else:
            if val:
                for i in range(2):
                    if self.bytes[offset + i] == 255:
                        self.bytes[offset + i] = 0

            else:
                for i in range(2):
                    self.bytes[offset + i] = 255


    def getValues(self):
        values = []

        if not self.game in self.GAMES:
            return values

        for name, data in self.VALUE_DATA[self.game].items():
            offset = data[0]
            size = data[1]
            val = int.from_bytes(self.bytes[offset:(offset + size)], byteorder = "little")

            if name == "Bolts Multiplier" and self.game != "rac2":
                val += 1

            elif name == "Language":
                val = next((lang for lang, byte in self.LANGUAGES.items() if byte == val), "")

            values.append((name, str(val)))

        return values


    def updateValue(self, name, val):
        if not self.game in self.GAMES:
            return

        data = self.VALUE_DATA[self.game]
        if not name in data:
            return

        size = data[name][1]
        if name == "Language":
            if not val in self.LANGUAGES:
                return

            val = self.LANGUAGES[val]

        else:
            signed = data[name][2]
            val = re.sub(r"[^0-9]", "", val)
            val = min(int(val), 2 ** (size * 8 - 1) - 1 if signed else 2 ** (size * 8) - 1)

            if name == "Bolts Multiplier" and self.game != "rac2":
                val -= 1

            if val < 0:
                val = 0

        offset = data[name][0]
        bytes = val.to_bytes(size, byteorder = "little")

        for i in range(size):
            self.bytes[offset + i] = bytes[i]


    def update(self):
        self.updateCrc16()

        with open(self.path, "wb") as f:
            f.write(self.bytes)