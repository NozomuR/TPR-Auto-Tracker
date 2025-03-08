items_config = {
    # -------------------------
    # Regular Items (read individually)
    # -------------------------
    "gale_boomerang": {
         "name": "Gale Boomerang",
         "address": 0x8040625C,
         "acquired_value": 64,
         "image_file": "Gale_Boomerang.png",
         "progressive": False,
         "get_state": lambda val: "acquired" if val == 64 else "empty"
    },
    "lantern": {
         "name": "Lantern",
         "address": 0x8040625D,
         "acquired_value": 72,
         "image_file": "Lantern.png",
         "progressive": False,
         "get_state": lambda val: "acquired" if val == 72 else "empty"
    },
    "spinner": {
         "name": "Spinner",
         "address": 0x8040625E,
         "acquired_value": 65,
         "image_file": "Spinner.png",
         "progressive": False,
         "get_state": lambda val: "acquired" if val == 65 else "empty"
    },
    "iron_boots": {
         "name": "Iron Boots",
         "address": 0x8040625F,
         "acquired_value": 69,
         "image_file": "Iron_Boots.png",
         "progressive": False,
         "get_state": lambda val: "acquired" if val == 69 else "empty"
    },
    "heros_bow": {
         "name": "Hero's Bow",
         "address": 0x80406260,
         "acquired_value": 67,
         "image_file": "Hero_Bow.png",
         "progressive": False,
         "get_state": lambda val: "acquired" if val == 67 else "empty"
    },
    "hawkeye": {
         "name": "Hawkeye",
         "address": 0x80406261,
         "acquired_value": 62,
         "image_file": "Hawkeye.png",
         "progressive": False,
         "get_state": lambda val: "acquired" if val == 62 else "empty"
    },
    "ball_and_chain": {
         "name": "Ball and Chain",
         "address": 0x80406262,
         "acquired_value": 66,
         "image_file": "Ball_and_Chain.png",
         "progressive": False,
         "get_state": lambda val: "acquired" if val == 66 else "empty"
    },
    "dominion_rod": {
        "name": "Dominion Rod",
        "address": 0x80406264,  # Base address: rod obtained when not 255.
        "powered_address": 0x804069D5,  # Address for the powered flag.
        "progressive": True,
        "image_files": {
            "empty": "Dominion_Rod_empty.png",  # When rod not obtained (base value == 255)
            "powerless": "Dominion_Rod_depowered.png",  # When rod is obtained but not powered
            "powered": "Dominion_Rod_powered.png"  # When powered (cutscene played)
        },
        # Changed the check so that it returns "powered" if the top bit (0x80) is set.
        "get_state": lambda base_val, powered_val: "empty" if base_val == 255
        else ("powered" if (powered_val & 0x80) == 0x80 else "powerless")
    },
    "clawshot": {
         "name": "Clawshot",
         "address": 0x80406265,
         "secondary_address": 0x80406266,
         "progressive": True,
         "states": {
              "double": 71,
              "clawshot": 68,
              "empty": 255
         },
         "image_files": {
              "double": "Double_Clawshots.png",
              "clawshot": "Clawshot.png",
              "empty": "Clawshot.png"
         },
         "get_state": lambda primary, secondary: "double" if secondary == 71 else ("clawshot" if primary == 68 else "empty")
    },
    "bottles": {
        "name": "Bottles",
        # The four addresses for each bottle flag.
        "addresses": [0x80406267, 0x80406268, 0x80406269, 0x8040626A],
        "progressive": False,
        "image_file": "Empty_Bottle.png",  # Base image for bottles (should be in your items folder)
        # Here we assume that if a bottle is NOT acquired its value is 255.
        "get_state": lambda values: sum(1 for v in values if v != 255)
    },
    "bomb_bag1": {
         "name": "Bomb Bag 1",
         "address": 0x8040626B,
         "progressive": True,
         "states": {
             "none": 255,
             "empty": 80,
             "bombs": 112,
             "water": 113,
             "bomblings": 114
         },
         "image_files": {
             "none": "Bomb_bag.png",
             "empty": "Bomb_bag.png",
             "bombs": "Bombs.png",
             "water": "Water_Bombs.png",
             "bomblings": "Bomblings.png"
         },
         "get_state": lambda val: (
              "bombs" if val == 112 else
              "water" if val == 113 else
              "bomblings" if val == 114 else
              "empty" if val == 80 else
              "none"
         )
    },
    "bomb_bag2": {
         "name": "Bomb Bag 2",
         "address": 0x8040626C,
         "progressive": True,
         "states": {
             "none": 255,
             "empty": 80,
             "bombs": 112,
             "water": 113,
             "bomblings": 114
         },
         "image_files": {
             "none": "Bomb_bag.png",
             "empty": "Bomb_bag.png",
             "bombs": "Bombs.png",
             "water": "Water_Bombs.png",
             "bomblings": "Bomblings.png"
         },
         "get_state": lambda val: (
              "bombs" if val == 112 else
              "water" if val == 113 else
              "bomblings" if val == 114 else
              "empty" if val == 80 else
              "none"
         )
    },
    "bomb_bag3": {
         "name": "Bomb Bag 3",
         "address": 0x8040626D,
         "progressive": True,
         "states": {
             "none": 255,
             "empty": 80,
             "bombs": 112,
             "water": 113,
             "bomblings": 114
         },
         "image_files": {
             "none": "Bomb_bag.png",
             "empty": "Bomb_bag.png",
             "bombs": "Bombs.png",
             "water": "Water_Bombs.png",
             "bomblings": "Bomblings.png"
         },
         "get_state": lambda val: (
              "bombs" if val == 112 else
              "water" if val == 113 else
              "bomblings" if val == 114 else
              "empty" if val == 80 else
              "none"
         )
    },
    "ooccoo": {
         "name": "Ooccoo",
         "address": 0x8040626E,
         "progressive": False,
         "acquired_condition": lambda val: val in (37, 39, 45, 51),
         "image_file": None,
         "get_state": lambda val: "acquired" if val in (37, 39, 45, 51) else "empty"
    },
    "quest_item": {
         "name": "Quest Item",
         "address": 0x8040626F,
         "progressive": False,
         "acquired_condition": lambda val: val in (128, 129, 130, 144, 145),
         "image_file": None,
         "get_state": lambda val: "acquired" if val in (128, 129, 130, 144, 145) else "empty"
    },
    "fishing_rod": {
         "name": "Fishing Rod",
         "address": 0x80406270,
         "progressive": True,
         "states": {
             "rod2": 92,
             "rod1": 74,
             "empty": 255
         },
         "image_files": {
             "rod2": "Fishing_Rod_2.png",
             "rod1": "Fishing_Rod_1.png",
             "empty": "Fishing_Rod_1.png"
         },
         "get_state": lambda val: "rod2" if val == 92 else ("rod1" if val == 74 else "empty")
    },
    "horse_call": {
         "name": "Horse Call",
         "address": 0x80406271,
         "progressive": True,
         "states": {
             "variant2": 132,
             "variant1": 131,
             "empty": 255
         },
         "image_files": {
             "variant2": "Horse_Call.png",
             "variant1": "Horse_Call.png",
             "empty": "Horse_Call.png"
         },
         "get_state": lambda val: "variant2" if val == 132 else ("variant1" if val == 131 else "empty")
    },
    "ancient_sky_book": {
        "name": "Ancient Sky Book",
        "bitwise": True,
        "progressive": False,
        "image_file": "Ancient_Sky_Book.png",
        "get_state": lambda data: "acquired" if (data[30] & (1 << 1)) != 0 else "empty"
    },
    "slingshot": {
         "name": "Slingshot",
         "address": 0x80406273,
         "acquired_value": 75,
         "image_file": "Slingshot.png",
         "progressive": False,
         "get_state": lambda val: "acquired" if val == 75 else "empty"
    },
    # -------------------------
    # Equipment Items (bitwise items)
    # These items now use a single image file, and the tracker creates a colored version
    # (for "acquired") and an automatic greyed-out version (for "empty").
    # -------------------------
    "sword": {
         "name": "Sword",
         "bitwise": True,
         "progressive": True,
         "image_files": {
             # For the "none" state, use the Wooden Sword image (it will be loaded greyed out)
             "none": "Wooden_Sword.png",
             # When acquired, the progression is as follows:
             "wooden": "Wooden_Sword.png",
             "ordon": "Ordon_Sword.png",
             "master": "Master_Sword.png",
             "light": "Light_Sword.png"
         },
         "get_state": lambda data: (
             "light" if (data[10] & (1 << 1)) != 0 else
             "master" if (data[6] & (1 << 1)) != 0 else
             "ordon" if (data[6] & (1 << 0)) != 0 else
             "wooden" if (data[4] & (1 << 7)) != 0 else
             "none"
         )
    },
    "combined_magic_armor": {
        "name": "Magic & Zora Armor",
        "bitwise": True,
        "progressive": False,
        # This lambda checks data[5] for both bits: bit 0 for Magic Armor and bit 1 for Zora Armor.
        "get_state": lambda data: (
             "acquired" if (data[5] & (1 << 0)) != 0 else "empty",
             "acquired" if (data[5] & (1 << 1)) != 0 else "empty"
        ),
        "image_files": {
             "magic": "zora_magic_1.png",
             "zora": "zora_magic_2.png"
        }
    },
    "combined_shields": {
        "name": "Shields",
        "bitwise": True,
        "progressive": False,
        # This lambda reads the bitwise data (assuming data[6] holds the shield flags):
        "get_state": lambda data: (
            "acquired" if (data[6] & (1 << 4)) != 0 else "empty",  # Hylian Shield status
            "acquired" if (data[6] & (1 << 2)) != 0 else "empty"  # Ordon Shield status
        ),
        # Use your two image files for each half.
        "image_files": {
            "hylian": "Hylian_Shield.png",
            "ordon": "Ordon_Shield.png"
        }
    },
    "shadow_crystal": {
         "name": "Shadow Crystal",
         "bitwise": True,
         "progressive": False,
         "image_file": "Shadow_Crystal.png",
         "get_state": lambda data: "acquired" if (data[5] & (1 << 2)) != 0 else "empty"
    },
    "aurus_memo": {
         "name": "Auru's Memo",
         "bitwise": True,
         "progressive": False,
         "image_file": "Aurus_Memo.png",
         "get_state": lambda data: "acquired" if (data[17] & (1 << 0)) != 0 else "empty"
    },
    "ashei_sketch": {
         "name": "Ashei's Sketch",
         "bitwise": True,
         "progressive": False,
         "image_file": "Asheis_Sketch.png",
         "get_state": lambda data: "acquired" if (data[17] & (1 << 1)) != 0 else "empty"
    },
    "scent": {
        "name": "Equipped Scent",
        "address": 0x804061D6,
        "progressive": False,
        "image_file": "Scent.png",
        # Map the possible values (pumpkin removed) to a state name.
        "get_state": lambda val: {
             176: "ilia",
             178: "poe",
             179: "reekfish",
             180: "youth",
             181: "medicine",
             255: "none"
        }.get(val, "none")
    },
    "mirror_shards": {
        "name": "Mirror Shards",
        "address": 0x804062CA,
        "progressive": True,
        # Convert the bitmask to a count of acquired shards:
        #   0x00 (00000000) -> 0 shards -> "empty"
        #   0x01 (00000001) -> 1 shard  -> "shard_1"
        #   0x03 (00000011) -> 2 shards -> "shard_2"
        #   0x07 (00000111) -> 3 shards -> "shard_3"
        #   0x0F (00001111) or more -> "completed"
        "get_state": lambda val: (lambda count: "completed" if count >= 4
        else ("empty" if count == 0
              else f"shard_{count}"))(bin(val).count("1")),
        "image_files": {
            "empty": "mirror/shard_empty.png",
            "shard_1": "mirror/shard_1.png",
            "shard_2": "mirror/shard_2.png",
            "shard_3": "mirror/shard_3.png",
            "completed": "mirror/completed_mirror.png"
        }
    },
    # Add three separate entries for each fused shadow:
    "fused_shadow1": {
        "name": "Fused Shadow 1",
        "address": 0x804062C9,
        "progressive": False,
        # If the overall “completed” flag (bit 3) is set, show the completed image;
        # otherwise, check bit 0 for this slot.
        "get_state": lambda val: ("shadow" if (val & (1 << 0)) != 0 else "empty"),
        "image_files": {
            "shadow": "fused/fused_1.png",
            "empty": "fused/fused_empty1.png"
        }
    },
    "fused_shadow2": {
        "name": "Fused Shadow 2",
        "address": 0x804062C9,
        "progressive": False,
        "get_state": lambda val: ("shadow" if (val & (1 << 1)) != 0 else "empty"),
        "image_files": {
            "shadow": "fused/fused_2.png",
            "empty": "fused/fused_empty2.png"
        }
    },
    "fused_shadow3": {
        "name": "Fused Shadow 3",
        "address": 0x804062C9,
        "progressive": False,
        "get_state": lambda val: ("shadow" if (val & (1 << 2)) != 0 else "empty"),
        "image_files": {
            "shadow": "fused/fused_3.png",
            "empty": "fused/fused_empty3.png"
        }
    },
    "poe_souls": {
        "name": "Poe Souls",
        "address": 0x804062CC,  # the counter address
        "progressive": False,
        "image_file": "Poe_Souls.png",
        # In this case, the get_state simply returns the counter value.
        "get_state": lambda val: val
    },
    "Bugs": {
        "name": "Bugs",
        "addresses": [0x804062A5, 0x804062A6, 0x804062A7],
        "progressive": False,
        "image_file": "bug.png",  # This should be a base icon for the insects
        # This lambda takes a list of bytes and returns the total count of set bits.
        "get_state": lambda values: sum(bin(v).count("1") for v in values)
    },
    "hidden_skill": {
        "name": "Hidden Skill",
        # These three addresses come from the table you provided.
        "addresses": [0x804063F0, 0x804069EC, 0x804069ED],
        "progressive": False,
        "image_file": "hidden_skill.png",  # Make sure this file exists in your items folder.
        # This lambda reads the three bytes and counts how many of the golden wolf flags are set.
        # From 0x804063F0: check bit 0x80.
        # From 0x804069EC: check bits 0x1, 0x2, 0x4, 0x8.
        # From 0x804069ED: check bits 0x40 and 0x80.
        "get_state": lambda values: (
                (1 if (values[0] & 0x40) != 0 else 0) +
                sum(1 for bit in [0x1, 0x2, 0x4, 0x8] if values[1] & bit) +
                sum(1 for bit in [0x40, 0x80] if values[2] & bit)
        )
    },
    "trade_item": {
        "name": "Trade Item",
        "address": 0x8040629F,
        "progressive": False,
        "image_files": {
            "empty": "empty_trade.png",  # When no trade item is obtained.
            "wooden_statue": "wooden_statue.png",
            "invoice": "invoice.png",
            "renado_letter": "renado_letter.png",
            "horse_call": "horse_call.png"
        },
        "get_state": lambda val: (
            "horse_call" if (val & 0x08) != 0 else
            "renado_letter" if (val & 0x04) != 0 else
            "invoice" if (val & 0x02) != 0 else
            "wooden_statue" if (val & 0x01) != 0 else
            "empty"
        )
    },
    "wallet": {
        "name": "Wallet",
        "address": 0x80406291,
        "progressive": True,
        "image_files": {
            "empty": "empty_wallet.png",  # When not obtained.
            "standard": "standard_wallet.png",
            "big": "big_wallet.png",
            "giant": "giant_wallet.png"
        },
        # For a bit field wallet, we assume:
        # If bit 2 is set, it's the giant wallet;
        # else if bit 1 is set, it's the big wallet;
        # else if bit 0 is set, it's the standard wallet;
        # else empty.
        "get_state": lambda val: "giant" if (val & 0x04) != 0
        else ("big" if (val & 0x02) != 0
              else ("standard" if (val & 0x01) != 0 else "empty"))
    },
    "forest_small_keys": {
        "name": "Forest Temple Small Keys",
        "address": 0x804065CC,  # the counter address
        "progressive": False,
        "image_file": "small_key.png",
        # In this case, the get_state simply returns the counter value.
        "get_state": lambda val: val
    },
}

