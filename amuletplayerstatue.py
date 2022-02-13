# Amulet Player Statue operation based on SethBling's MCEdit Player Statue filter

# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

# Extended by pau101 to handle more layers in MCEdit

# Modified by Marcono1234 on 13.05.2015 to support UUIDs of players in MCEdit

# Adapted for Amulet plus slim arm texture support by Addgame

# Needs Amulet 0.8.5b0 or later
import base64
import io
import json
import pathlib
import urllib.request

from PIL import Image
from amulet.api.block import Block
from amulet.api.data_types import Dimension
from amulet.api.level import BaseLevel
from amulet.api.selection import SelectionGroup

operation_options = {
    "Amulet PlayerStatue v1.3": ["label"],
    "Enter either Name/UUID or select file with skin type": ["label"],
    "-------------------------------": ["label"],
    "Name/UUID": ["str"],
    "--------------------------------": ["label"],
    "Provided file will be preferred over Name/UUID": ["label"],
    "Skin File": ["file_open"],
    "Skin Type": ["str_choice", "Steve (Classic)", "Alex (Slim)", "Legacy"],
    "Cape File": ["file_open"],
    "---------------------------------": ["label"],
    "Layers To Show": ["label"],
    "Cape": ["bool", True],
    "Left Sleeve": ["bool", True],
    "Left Pants Leg": ["bool", True],
    "Hat": ["bool", True],
    "Jacket": ["bool", True],
    "Right Sleeve": ["bool", True],
    "Right Pants Leg": ["bool", True]
}

game_version = ("java", (1, 18, 1))

blocks = (("acacia_wood", (103, 96, 86)), ("acacia_planks", (168, 90, 50)), ("birch_wood", (216, 215, 210)),
          ("birch_planks", (192, 175, 121)), ("black_glazed_terracotta", (67, 30, 32)),
          ("black_terracotta", (37, 22, 16)), ("blue_concrete", (44, 46, 143)),
          ("blue_glazed_terracotta", (47, 64, 139)), ("blue_terracotta", (74, 59, 91)), ("blue_wool", (53, 57, 157)),
          ("bricks", (150, 97, 83)), ("brown_concrete", (96, 59, 31)), ("brown_glazed_terracotta", (119, 106, 85)),
          ("brown_terracotta", (77, 51, 35)), ("brown_wool", (114, 71, 40)), ("coarse_dirt", (119, 85, 59)),
          ("cyan_concrete", (21, 119, 136)), ("cyan_glazed_terracotta", (52, 118, 125)), ("cyan_wool", (21, 137, 145)),
          ("dark_oak_wood", (60, 46, 26)), ("dark_oak_planks", (66, 43, 20)), ("dark_prismarine", (51, 91, 75)),
          ("diamond_block", (98, 237, 228)), ("diamond_ore", (121, 141, 140)), ("dirt", (134, 96, 67)),
          ("emerald_block", (42, 203, 87)), ("emerald_ore", (108, 136, 115)), ("end_stone", (219, 222, 158)),
          ("end_stone_bricks", (218, 224, 162)), ("gold_block", (246, 208, 61)), ("gold_ore", (145, 133, 106)),
          ("gray_terracotta", (57, 42, 35)), ("green_concrete", (73, 91, 36)),
          ("green_glazed_terracotta", (117, 142, 67)), ("green_terracotta", (76, 83, 42)),
          ("green_wool", (84, 109, 27)), ("iron_ore", (136, 129, 122)), ("packed_ice", (141, 180, 250)),
          ("blue_ice", (116, 167, 253)), ("jungle_wood", (85, 67, 25)), ("jungle_planks", (160, 115, 80)),
          ("lapis_block", (30, 67, 140)), ("lapis_ore", (107, 117, 141)), ("light_blue_concrete", (35, 137, 198)),
          ("light_blue_glazed_terracotta", (94, 164, 208)), ("light_blue_terracotta", (113, 108, 137)),
          ("light_blue_wool", (58, 175, 217)), ("light_gray_glazed_terracotta", (144, 166, 167)),
          ("light_gray_terracotta", (135, 106, 97)), ("lime_concrete", (94, 168, 24)),
          ("lime_glazed_terracotta", (162, 197, 55)), ("lime_terracotta", (103, 117, 52)),
          ("lime_wool", (112, 185, 25)), ("magenta_concrete", (169, 48, 159)),
          ("magenta_glazed_terracotta", (208, 100, 191)), ("magenta_terracotta", (149, 88, 108)),
          ("magenta_wool", (189, 68, 179)), ("mossy_cobblestone", (110, 118, 94)),
          ("mossy_stone_bricks", (115, 121, 105)), ("red_mushroom_block", (200, 46, 45)),
          ("brown_mushroom_block", (149, 111, 81)), ("netherrack", (97, 38, 38)), ("nether_bricks", (44, 21, 26)),
          ("nether_wart_block", (114, 2, 2)), ("note_block", (88, 58, 40)), ("oak_wood", (109, 85, 50)),
          ("oak_planks", (162, 130, 78)), ("obsidian", (15, 10, 24)), ("orange_concrete", (224, 97, 0)),
          ("orange_glazed_terracotta", (154, 147, 91)), ("orange_terracotta", (161, 83, 37)),
          ("orange_wool", (240, 118, 19)), ("pink_concrete", (213, 101, 142)),
          ("pink_glazed_terracotta", (235, 154, 181)), ("pink_terracotta", (161, 78, 78)),
          ("pink_wool", (237, 141, 172)), ("polished_granite", (154, 106, 89)), ("prismarine_bricks", (99, 171, 158)),
          ("purple_concrete", (100, 31, 156)), ("purple_glazed_terracotta", (109, 48, 152)),
          ("purple_terracotta", (118, 70, 86)), ("purple_wool", (121, 42, 172)), ("purpur_block", (169, 125, 169)),
          ("nether_quartz_ore", (117, 65, 62)), ("redstone_block", (175, 24, 5)), ("redstone_ore", (140, 109, 109)),
          ("red_concrete", (142, 32, 32)), ("red_glazed_terracotta", (181, 59, 53)), ("red_nether_bricks", (69, 7, 9)),
          ("red_terracotta", (143, 61, 46)), ("red_wool", (160, 39, 34)), ("snow_block", (249, 254, 254)),
          ("soul_sand", (81, 62, 50)), ("sponge", (195, 192, 74)), ("spruce_wood", (58, 37, 16)),
          ("spruce_planks", (114, 84, 48)), ("granite", (149, 103, 85)), ("terracotta", (152, 94, 67)),
          ("wet_sponge", (171, 181, 70)), ("white_glazed_terracotta", (188, 212, 202)),
          ("white_terracotta", (209, 178, 161)), ("yellow_concrete", (240, 175, 21)),
          ("yellow_glazed_terracotta", (234, 192, 88)), ("yellow_terracotta", (186, 133, 35)),
          ("yellow_wool", (248, 197, 39)), ("smooth_stone", (158, 158, 158)), ("honeycomb_block", (229, 148, 29)),
          ("warped_wart_block", (22, 119, 121)), ("soul_soil", (75, 57, 46)), ("warped_planks", (43, 104, 99)),
          ("crimson_planks", (101, 48, 70)), ("crying_obsidian", (32, 10, 60)),
          ("stripped_warped_hyphae", (57, 150, 147)), ("stripped_crimson_hyphae", (137, 57, 90)),
          ("warped_hyphae", (58, 58, 77)), ("crimson_hyphae", (92, 25, 29)), ("nether_gold_ore", (115, 54, 42)),
          ("gilded_blackstone", (55, 42, 38)), ("chiseled_nether_bricks", (47, 23, 28)),
          ("cracked_nether_bricks", (40, 20, 23)), ("amethyst_block", (133, 97, 191)),
          ("raw_gold_block", (221, 169, 46)), ("raw_iron_block", (166, 135, 107)), ("raw_copper_block", (154, 105, 79)),
          ("copper_ore", (124, 125, 120)), ("waxed_copper_block", (192, 107, 79)), ("waxed_cut_copper", (191, 106, 80)),
          ("waxed_exposed_copper", (161, 125, 103)), ("waxed_exposed_cut_copper", (154, 121, 101)),
          ("waxed_oxidized_copper", (82, 162, 132)), ("waxed_oxidized_cut_copper", (79, 153, 126)),
          ("waxed_weathered_copper", (108, 153, 110)), ("waxed_weathered_cut_copper", (109, 145, 107)),
          ("moss_block", (89, 109, 45)), ("rooted_dirt", (144, 103, 76)), ("deepslate_iron_ore", (106, 99, 94)),
          ("deepslate_gold_ore", (115, 102, 78)), ("deepslate_copper_ore", (92, 93, 89)),
          ("deepslate_redstone_ore", (104, 73, 74)), ("deepslate_emerald_ore", (78, 104, 87)),
          ("deepslate_lapis_ore", (79, 90, 115)), ("deepslate_diamond_ore", (83, 106, 106)))

XDIM = 1
YDIM = 2
ZDIM = 3

# Regions are pixel x low, pixel x high, pixel y low, pixel y high, dim for pixel x, dim for pixel y,
# starting world x, starting world y, starting world z
# (starting coords are relative to some calculated starting point such that the X and Y dimensions here are opposite
# from world X and Y dimensions but Z dimension matches world Z dimension)
base_regions = [
    (8, 16, 0, 8, XDIM, ZDIM, 4, 31, 1),  # Head Top
    (16, 24, 0, 8, XDIM, ZDIM, 4, 24, 1),  # Head Bottom
    (24, 32, 8, 16, -XDIM, YDIM, 4, 24, 8),  # Head Back
    (0, 8, 8, 16, -ZDIM, YDIM, 4, 24, 1),  # Head Right
    (16, 24, 8, 16, ZDIM, YDIM, 11, 24, 1),  # Head Left
    (8, 16, 8, 16, XDIM, YDIM, 4, 24, 1),  # Head Front

    (20, 28, 16, 20, XDIM, ZDIM, 4, 23, 3),  # Body Top
    (28, 36, 16, 20, XDIM, -ZDIM, 4, 12, 3),  # Body Bottom
    (32, 40, 20, 32, -XDIM, YDIM, 4, 12, 6),  # Body Back
    # (16, 20, 20, 32, -ZDIM, YDIM, 4, 12, 3),  # Body Right
    # (28, 32, 20, 32, ZDIM, YDIM, 11, 12, 3),  # Body Left
    (20, 28, 20, 32, XDIM, YDIM, 4, 12, 3),  # Body Front

    (4, 8, 16, 20, XDIM, ZDIM, 4, 11, 3),  # Right Leg Top
    (8, 12, 16, 20, XDIM, ZDIM, 4, 0, 3),  # Right Leg Bottom
    (12, 16, 20, 32, -XDIM, YDIM, 4, 0, 6),  # Right Leg Back
    (0, 4, 20, 32, -ZDIM, YDIM, 4, 0, 3),  # Right Leg Outside
    (4, 8, 20, 32, XDIM, YDIM, 4, 0, 3),  # Right Leg Front
]

thick_right_arm_regions = [
    (44, 48, 16, 20, XDIM, ZDIM, 0, 23, 3),  # Right Arm Top
    (48, 52, 16, 20, XDIM, ZDIM, 0, 12, 3),  # Right Arm Bottom
    (52, 56, 20, 32, -XDIM, YDIM, 0, 12, 6),  # Right Arm Back
    (40, 44, 20, 32, -ZDIM, YDIM, 0, 12, 3),  # Right Arm Outside
    (44, 48, 20, 32, XDIM, YDIM, 0, 12, 3)  # Right Arm Front
]

legacy_regions = [
    *base_regions,

    *thick_right_arm_regions,

    (4, 8, 16, 20, XDIM, ZDIM, 8, 11, 3),  # Left Leg Top
    (8, 12, 16, 20, -XDIM, ZDIM, 8, 0, 3),  # Left Leg Bottom
    (12, 16, 20, 32, XDIM, YDIM, 8, 0, 6),  # Left Leg Back
    (0, 4, 20, 32, -ZDIM, YDIM, 11, 0, 3),  # Left Leg Outside
    (4, 8, 20, 32, -XDIM, YDIM, 8, 0, 3),  # Left Leg Front

    (44, 48, 16, 20, XDIM, ZDIM, 12, 23, 3),  # Left Arm Top
    (48, 52, 16, 20, -XDIM, ZDIM, 12, 12, 3),  # Left Arm Bottom
    (52, 56, 20, 32, XDIM, YDIM, 12, 12, 6),  # Left Arm Back
    (40, 44, 20, 32, -ZDIM, YDIM, 15, 12, 3),  # Left Arm Outside
    (44, 48, 20, 32, -XDIM, YDIM, 12, 12, 3)  # Left Arm Front

]

unique_left_leg_regions = [
    (20, 24, 48, 52, XDIM, ZDIM, 8, 11, 3),  # Left Leg Top
    (24, 28, 48, 52, XDIM, ZDIM, 8, 0, 3),  # Left Leg Bottom
    (28, 32, 52, 64, -XDIM, YDIM, 8, 0, 6),  # Left Leg Back
    (24, 28, 52, 64, ZDIM, YDIM, 11, 0, 3),  # Left Leg Outside
    (20, 24, 52, 64, XDIM, YDIM, 8, 0, 3),  # Left Leg Front
]

steve_regions = [
    *base_regions,

    *thick_right_arm_regions,

    *unique_left_leg_regions,

    (36, 40, 48, 52, XDIM, ZDIM, 12, 23, 3),  # Left Arm Top
    (40, 44, 48, 52, XDIM, ZDIM, 12, 12, 3),  # Left Arm Bottom
    (44, 48, 52, 64, -XDIM, YDIM, 12, 12, 6),  # Left Arm Back
    (40, 44, 52, 64, ZDIM, YDIM, 15, 12, 3),  # Left Arm Outside
    (36, 40, 52, 64, XDIM, YDIM, 12, 12, 3)  # Left Arm Front
]

alex_regions = [
    *base_regions,

    *unique_left_leg_regions,

    (44, 47, 16, 20, XDIM, ZDIM, 1, 23, 3),  # Right Arm Top
    (47, 50, 16, 20, XDIM, ZDIM, 1, 12, 3),  # Right Arm Bottom
    (51, 54, 20, 32, -XDIM, YDIM, 1, 12, 6),  # Right Arm Back
    (40, 44, 20, 32, -ZDIM, YDIM, 1, 12, 3),  # Right Arm Outside
    (44, 47, 20, 32, XDIM, YDIM, 1, 12, 3),  # Right Arm Front

    (36, 39, 48, 52, XDIM, ZDIM, 12, 23, 3),  # Left Arm Top
    (39, 42, 48, 52, XDIM, ZDIM, 12, 12, 3),  # Left Arm Bottom
    (43, 46, 52, 64, -XDIM, YDIM, 12, 12, 6),  # Left Arm Back
    (39, 43, 52, 64, ZDIM, YDIM, 14, 12, 3),  # Left Arm Outside
    (36, 39, 52, 64, XDIM, YDIM, 12, 12, 3)  # Left Arm Front
]

hat_regions = [
    (40, 48, 0, 8, XDIM, ZDIM, 4, 32, 1),  # Hat Top
    (56, 64, 8, 16, -XDIM, YDIM, 4, 24, 9),  # Hat Back
    (32, 40, 8, 16, -ZDIM, YDIM, 3, 24, 1),  # Hat Right
    (48, 56, 8, 16, ZDIM, YDIM, 12, 24, 1),  # Hat Left
    (40, 48, 8, 16, XDIM, YDIM, 4, 24, 0)  # Hat Front
]

cape_region = (1, 11, 1, 17, -XDIM, YDIM, 3, 8, 8)  # Cape

jacket_regions = [
    (20, 28, 36, 48, XDIM, YDIM, 4, 12, 2),  # Jacket Front
    (32, 40, 36, 48, -XDIM, YDIM, 4, 12, 7)  # Body Back
]

right_pants_regions = [
    (8, 12, 32, 36, XDIM, ZDIM, 4, -1, 3),  # Right Pants Bottom
    (0, 4, 36, 48, -ZDIM, YDIM, 3, 0, 3),  # Right Pants Outside
    (12, 16, 36, 48, -XDIM, YDIM, 4, 0, 7),  # Right Pants Back
    (4, 8, 36, 48, XDIM, YDIM, 4, 0, 2)  # Right Pants Front
]

left_pants_regions = [
    (8, 12, 48, 52, XDIM, ZDIM, 8, -1, 3),  # Left Pants Bottom
    (8, 12, 52, 64, ZDIM, YDIM, 12, 0, 3),  # Left Pants Outside
    (12, 16, 52, 64, -XDIM, YDIM, 8, 0, 7),  # Left Pants Back
    (4, 8, 52, 64, XDIM, YDIM, 8, 0, 2)  # Left Pants Front
]

slim_left_sleeve_regions = [
    (52, 55, 48, 52, XDIM, ZDIM, 12, 24, 3),  # Left Sleeve Top
    (55, 58, 48, 52, XDIM, ZDIM, 12, 11, 3),  # Left Sleeve Bottom
    (59, 62, 52, 64, -XDIM, YDIM, 12, 12, 7),  # Left Sleeve Back
    (55, 59, 52, 64, ZDIM, YDIM, 15, 12, 3),  # Left Sleeve Outside
    (52, 55, 52, 64, XDIM, YDIM, 12, 12, 2)  # Left Sleeve Front
]

slim_right_sleeve_regions = [
    (44, 47, 32, 36, XDIM, ZDIM, 1, 24, 3),  # Right Sleeve Top
    (47, 50, 32, 36, XDIM, ZDIM, 1, 11, 3),  # Right Sleeve Bottom
    (51, 54, 36, 48, -XDIM, YDIM, 1, 12, 7),  # Right Sleeve Back
    (40, 44, 36, 48, -ZDIM, YDIM, 0, 12, 3),  # Right Sleeve Outside
    (44, 47, 36, 48, XDIM, YDIM, 1, 12, 2)  # Right Sleeve Front
]

thick_left_sleeve_regions = [
    (52, 56, 48, 52, XDIM, ZDIM, 12, 24, 3),  # Left Sleeve Top
    (56, 60, 48, 52, XDIM, ZDIM, 12, 11, 3),  # Left Sleeve Bottom
    (60, 64, 52, 64, -XDIM, YDIM, 12, 12, 7),  # Left Sleeve Back
    (56, 60, 52, 64, ZDIM, YDIM, 16, 12, 3),  # Left Sleeve Outside
    (52, 56, 52, 64, XDIM, YDIM, 12, 12, 2)  # Left Sleeve Front
]

thick_right_sleeve_regions = [
    (44, 48, 32, 36, XDIM, ZDIM, 0, 24, 3),  # Right Sleeve Top
    (48, 52, 32, 36, XDIM, ZDIM, 0, 11, 3),  # Right Sleeve Bottom
    (52, 56, 36, 48, -XDIM, YDIM, 0, 12, 7),  # Right Sleeve Back
    (40, 44, 36, 48, -ZDIM, YDIM, -1, 12, 3),  # Right Sleeve Outside
    (44, 48, 36, 48, XDIM, YDIM, 0, 12, 2)  # Right Sleeve Front
]


def is_transparent(color):
    return color[3] < 128


def get_closest(color):
    # Calculate the closest block
    closest = blocks[0][0]
    best_dist = 255 * 255 * 3
    for (name, (r, g, b)) in blocks:
        (dr, dg, db) = (color[0] - r, color[1] - g, color[2] - b)
        dist = dr * dr + dg * dg + db * db
        if dist < best_dist:
            closest = name
            best_dist = dist
    return Block.from_string_blockstate("minecraft:" + closest)


def connect_to_server(url, set_timeout=120):
    connection = urllib.request.urlopen(url, timeout=set_timeout)
    data = connection.read()
    connection.close()

    if len(data) == 0:
        raise Exception("Received empty file. Might be caused by invalid player name")

    return data


def connect_json_return(url, set_timeout=120):
    data = json.loads(connect_to_server(url, set_timeout))
    if "error" in data:
        raise Exception(
            "Couldn't get information from Mojang servers:\n{}\n{}".format(data["error"], data["errorMessage"]))
    return data


def get_uuid_from_name(player_name):
    received_json = connect_json_return("https://api.mojang.com/users/profiles/minecraft/" + player_name)
    return received_json["id"]


def get_skin_from_uuid(player_uuid, get_cape):
    received_json = connect_json_return("https://sessionserver.mojang.com/session/minecraft/profile/" + player_uuid)
    # Get first element by using tuple unpacking with trailing values assigned to throwaway variable
    texture_element, *_ = [property_element for property_element in received_json["properties"] if
                           property_element.get("name", "") == "textures"]
    if not texture_element:
        raise Exception("Unable to get texture property for player")
    texture_object = texture_element["value"]
    decoded_texture_object = json.loads(base64.b64decode(texture_object))
    skin_object = decoded_texture_object["textures"]["SKIN"]
    is_slim = "metadata" in skin_object and skin_object["metadata"]["model"] == "slim"
    skin_bytes = connect_to_server(skin_object["url"])
    cape_bytes = None
    if get_cape and "CAPE" in decoded_texture_object["textures"]:
        cape_bytes = connect_to_server(decoded_texture_object["textures"]["CAPE"]["url"])
    return skin_bytes, is_slim, cape_bytes


def operation(world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict):
    # Get the image
    cape_image = None
    has_extra_layers = True
    is_slim = False
    if options["Skin File"]:
        # Use skin file
        skin_path = pathlib.Path(options["Skin File"])
        skin_image = Image.open(skin_path).convert("RGBA")
        if options["Cape"] and options["Cape File"]:
            cape_path = pathlib.Path(options["Cape File"])
            if cape_path.exists():
                cape_image = Image.open(cape_path).convert("RGBA")
            else:
                print("amuletplayerstatue: Could not find cape file - ignoring")
        # Select region
        if options["Skin Type"] == "Legacy":
            regions = legacy_regions
            has_extra_layers = False
        elif options["Skin Type"] == "Steve (Classic)":
            regions = steve_regions
        else:  # options["Skin Type"] == "Alex (Slim)"
            regions = alex_regions
            is_slim = True
    elif options["Name/UUID"]:
        # No skin file provided
        name_input = options["Name/UUID"]
        if len(name_input) < 3:
            raise Exception("Name/UUID input is too short to be valid")
        # If there is a dash or the name is larger than 16 then assume UUID
        if not (len(name_input) > 16 or "-" in name_input):
            # Get the UUID from player name
            player_uuid = get_uuid_from_name(name_input)
        else:
            # Ensure we don't have any dashes from user input
            player_uuid = name_input.replace("-", "")
        skin_bytes, is_slim, cape_bytes = get_skin_from_uuid(player_uuid, options["Cape"])
        skin_image = Image.open(io.BytesIO(skin_bytes))
        if cape_bytes:
            cape_image = Image.open(io.BytesIO(cape_bytes))
        if is_slim:
            regions = alex_regions
        elif skin_image.size[1] > 32:
            regions = steve_regions
        else:
            regions = legacy_regions
            has_extra_layers = False
    else:
        raise Exception("No skin was provided by either name/UUID or file")

    regions = regions.copy()
    if has_extra_layers:
        if options["Left Sleeve"]:
            if is_slim:
                regions.extend(slim_left_sleeve_regions)
            else:
                regions.extend(thick_left_sleeve_regions)
        if options["Right Sleeve"]:
            if is_slim:
                regions.extend(slim_right_sleeve_regions)
            else:
                regions.extend(thick_right_sleeve_regions)
        if options["Right Pants Leg"]:
            regions.extend(right_pants_regions)
        if options["Left Pants Leg"]:
            regions.extend(left_pants_regions)
        if options["Jacket"]:
            regions.extend(jacket_regions)
        if options["Cape"] and cape_image:
            regions.append(cape_region)

    if options["Hat"]:
        regions.extend(hat_regions)

    # Perform the block placing
    current_image = None
    for region in regions:
        if region == cape_region:
            current_image = cape_image
        else:
            current_image = skin_image

        (xl, xh, yl, yh, dim1, dim2, sx, sy, sz) = region

        lx = sx
        ly = sy
        lz = sz
        if dim1 == -ZDIM:
            lz = sz + xh - xl - 1
        if dim2 == -ZDIM:
            lz = sz + yh - yl - 1
        if dim1 == -XDIM:
            lx = sx + xh - xl - 1

        for px in range(xl, xh):
            for py in reversed(range(yl, yh)):
                color = current_image.getpixel((px, py))
                if not is_transparent(color):
                    block = get_closest(color)
                    base_loc = selection.min
                    block_loc = (base_loc[0] + 15 - lx, base_loc[1] + ly, base_loc[2] + lz)
                    world.set_version_block(*block_loc, dimension, game_version, block)

                if dim2 == YDIM:
                    ly = ly + 1
                if dim2 == ZDIM:
                    lz = lz + 1
                if dim2 == -ZDIM:
                    lz = lz - 1

            if dim2 == YDIM:
                ly = sy
            if dim2 == ZDIM:
                lz = sz
            if dim2 == -ZDIM:
                lz = sz + yh - yl - 1

            if dim1 == XDIM:
                lx = lx + 1
            if dim1 == -XDIM:
                lx = lx - 1
            if dim1 == ZDIM:
                lz = lz + 1
            if dim1 == -ZDIM:
                lz = lz - 1

    current_image.close()


export = {
    "name": "PlayerStatue",
    "operation": operation,
    "options": operation_options
}
