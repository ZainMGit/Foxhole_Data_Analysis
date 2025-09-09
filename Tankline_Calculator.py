##Very Basic python script to calculate DPS of Warden Tankline


import math


# ----------------------------------
# Base guns (global, unmodified)
# ----------------------------------
GUNS = {
    "40mm_AP": {"damage_per_shot": 220, "damage_type": "AP", "shots_per_volley": 1},
    "68mm_AP": {"damage_per_shot": 320, "damage_type": "AP", "shots_per_volley": 1},
    "75mm_HE": {"damage_per_shot": 250, "damage_type": "HE", "shots_per_volley": 1},
}

# ----------------------------------
# Vehicles with loadouts AND per-gun modifiers
# gun_mods entries are OPTIONAL and apply only for that vehicle
# ----------------------------------
VEHICLES = {
    "Devitt": {
        "loadout": ["40mm_AP"],
        # No modifiers
    },
    "Silverhand": {
        "loadout": ["68mm_AP", "40mm_AP"],
        "gun_mods": {
            # Example modifiers:
            # 68mm does +10% damage and double-taps per volley
            "68mm_AP": {"damage_mul": 1.10, "shots_per_volley": 1},
            # 40mm does -10% damage on this chassis
            "40mm_AP": {"damage_mul": 0.90},
        },
    },
    "Flood": {
        "loadout": ["75mm_HE"],
        # Example: convert HE to AP for a variant (uncomment to test)
        # "gun_mods": {"75mm_HE": {"damage_type": "AP"}}
    },
}

# ----------------------------------
# Target tank (only fields you asked for)
# ----------------------------------
ENEMY_TANK = {
    "name": "Enemy Medium",
    "hp": 1600,
    "disabled_hp": 400,
    "explosive_res": 0.20,  # 20% HE reduction
    "ap_res": 0.10,         # 10% AP reduction
    "armor": 0.33           # deflect chance (IGNORED for MIN volleys)
}

# Example lineup: counts of vehicles (not guns)
LINEUP = {
    "Silverhand": 1,
    "Devitt": 1,
    # "Flood": 1,
}

# ----------------------------------
# Helpers: apply per-vehicle gun modifiers
# ----------------------------------

def get_effective_gun_params(vehicle_key, gun_key):
    """Return a dict with the gun parameters after vehicle-specific modifiers."""
    base = GUNS[gun_key]
    vmods = VEHICLES.get(vehicle_key, {}).get("gun_mods", {})
    mod = vmods.get(gun_key, {})

    damage_type = mod.get("damage_type", base["damage_type"])
    # multiplicative + additive damage adjustments
    damage_mul = mod.get("damage_mul", 1.0)
    damage_add = mod.get("damage_add", 0.0)
    damage_per_shot = base["damage_per_shot"] * damage_mul + damage_add

    # allow overriding shots_per_volley (if omitted, use base)
    spv = mod.get("shots_per_volley", base.get("shots_per_volley", 1))

    return {
        "damage_per_shot": damage_per_shot,
        "damage_type": damage_type,
        "shots_per_volley": spv,
    }

# ----------------------------------
# Minimum-volley calculator (all hits land; armor randomness ignored)
# ----------------------------------

def per_shot_damage_if_all_hit(vehicle_key, gun_key, tank):
    g = get_effective_gun_params(vehicle_key, gun_key)
    res = tank["ap_res"] if g["damage_type"].upper() == "AP" else tank["explosive_res"]
    return g["damage_per_shot"] * (1 - res)

def vehicle_volley_damage_if_all_hit(vehicle_key, tank):
    v = VEHICLES[vehicle_key]
    total = 0.0
    for gun_key in v["loadout"]:
        params = get_effective_gun_params(vehicle_key, gun_key)
        shots = params["shots_per_volley"]
        total += shots * per_shot_damage_if_all_hit(vehicle_key, gun_key, tank)
    return total

def lineup_volley_damage_if_all_hit(lineup, tank):
    total = 0.0
    for vehicle_key, count in lineup.items():
        if count <= 0:
            continue
        total += count * vehicle_volley_damage_if_all_hit(vehicle_key, tank)
    return total

def min_volleys_to_destroy(lineup, tank):
    v = lineup_volley_damage_if_all_hit(lineup, tank)
    if v <= 0: return math.inf
    return math.ceil(tank["hp"] / v)

def min_volleys_to_disable(lineup, tank):
    v = lineup_volley_damage_if_all_hit(lineup, tank)
    if v <= 0: return math.inf
    needed = max(0.0, tank["hp"] - tank["disabled_hp"])
    return math.ceil(needed / v)

def print_min_volley_report(lineup, tank):
    volley = lineup_volley_damage_if_all_hit(lineup, tank)
    print("Friendly Tankline When shooting this enemy tank (MIN volleys, all hits):\n")
    print(f"Target: {tank['name']}")
    print(f"  HP: {tank['hp']}, Disabled at: {tank['disabled_hp']}")
    print(f"  Resistances -> HE: {tank['explosive_res']*100:.0f}%  |  AP: {tank['ap_res']*100:.0f}%")
    print(f"  Armor (deflect chance): {tank['armor']*100:.0f}%  (IGNORED for MIN calculation)\n")

    print("Friendly Lineup (vehicles -> guns fired per volley with modifiers applied):")
    for v_name, c in lineup.items():
        if c <= 0:
            continue
        details = []
        for gun_key in VEHICLES[v_name]["loadout"] if False else VEHICLES:  # placeholder guard to avoid typo during paste
            guns_list = []
        for gun_key in VEHICLES[v_name]["loadout"]:
            p = get_effective_gun_params(v_name, gun_key)
            guns_list.append(f"{gun_key}[{p['damage_type']}] x{p['shots_per_volley']} ({p['damage_per_shot']:.0f}/shot)")
        print(f"  - {c}× {v_name}: " + ", ".join(guns_list))

    print("\nPer-vehicle volley damage (all hits, after modifiers & resistances):")
    for v_name, c in lineup.items():
        if c <= 0:
            continue
        dmg = vehicle_volley_damage_if_all_hit(v_name, tank)
        print(f"  - {v_name}: {dmg:.0f} HP/volley  (×{c} = {dmg*c:.0f})")

    print("\nResults (minimum possible):")
    print(f"  • Total damage per full volley: {volley:.0f} HP")
    print(f"  • MIN volleys to DISABLE: {min_volleys_to_disable(lineup, tank)}")
    print(f"  • MIN volleys to DESTROY: {min_volleys_to_destroy(lineup, tank)}")

# ----------------------------------
# Example run
# ----------------------------------
if __name__ == "__main__":
    print_min_volley_report(LINEUP, ENEMY_TANK)
