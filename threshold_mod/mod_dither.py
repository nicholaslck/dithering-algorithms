# Implementation of paper 
# - Improving mid-tone quality of variable-coefficient error diffusion using threshold modulation
# https://dl.acm.org/doi/abs/10.1145/1201775.882289
import numpy as np
import cv2
from tqdm import tqdm
from numba import jit, njit

@njit
def thresold_func(d, rand_d, modulation_strength):
    if d < 0:
        d = 0
    if d > 255:
        d = 255
    d = int(np.floor(d))
    m = (rand_d % 128) * modulation_strength[d]
    threshold = 128 + m
    if d >= threshold:
        return 255
    return 0

@njit
def distribute_error(error_map, diff, i, j, input_level, coefficients):
    H,W = error_map.shape
    coefs = coefficients[input_level]
    term_r = diff * coefs[0] / coefs[3]
    term_dl = diff * coefs[1] / coefs[3]
    term_d = diff * coefs[2] / coefs[3]

    if j+1 < W:
        error_map[i][j+1] += term_r
    if i+1 < H:
        if j-1 >= 0:
            error_map[i+1][j-1] += term_dl
        error_map[i+1][j] += term_d
    return error_map

@njit
def main(img):

    modulation_strength = {
        0: 0.0,
        1: 0.0,
        2: 0.0,
        3: 0.0,
        4: 0.0,
        5: 0.0,
        6: 0.0,
        7: 0.0,
        8: 0.0,
        9: 0.0,
        10: 0.0,
        11: 0.0,
        12: 0.0,
        13: 0.0,
        14: 0.0,
        15: 0.0,
        16: 0.0,
        17: 0.0,
        18: 0.0,
        19: 0.0,
        20: 0.0,
        21: 0.0,
        22: 0.0,
        23: 0.0,
        24: 0.0,
        25: 0.0,
        26: 0.0,
        27: 0.0,
        28: 0.0,
        29: 0.0,
        30: 0.0,
        31: 0.0,
        32: 0.0,
        33: 0.0,
        34: 0.0,
        35: 0.0,
        36: 0.0,
        37: 0.0,
        38: 0.0,
        39: 0.0,
        40: 0.0,
        41: 0.0,
        42: 0.0,
        43: 0.0,
        44: 0.34,
        45: 0.34,
        46: 0.34,
        47: 0.34,
        48: 0.34,
        49: 0.34,
        50: 0.34,
        51: 0.34,
        52: 0.34,
        53: 0.34,
        54: 0.34,
        55: 0.34,
        56: 0.34,
        57: 0.34,
        58: 0.34,
        59: 0.34,
        60: 0.34,
        61: 0.34,
        62: 0.34,
        63: 0.34,
        64: 0.5,
        65: 0.5,
        66: 0.5,
        67: 0.5,
        68: 0.5,
        69: 0.5,
        70: 0.5,
        71: 0.5,
        72: 0.5,
        73: 0.5,
        74: 0.5,
        75: 0.5,
        76: 0.5,
        77: 0.5,
        78: 0.5,
        79: 0.5,
        80: 0.5,
        81: 0.5,
        82: 0.5,
        83: 0.5,
        84: 0.5,
        85: 1.0,
        86: 1.0,
        87: 1.0,
        88: 1.0,
        89: 1.0,
        90: 1.0,
        91: 1.0,
        92: 1.0,
        93: 1.0,
        94: 1.0,
        95: 0.17,
        96: 0.17,
        97: 0.17,
        98: 0.17,
        99: 0.17,
        100: 0.17,
        101: 0.17,
        102: 0.5,
        103: 0.5,
        104: 0.5,
        105: 0.5,
        106: 0.5,
        107: 0.7,
        108: 0.7,
        109: 0.7,
        110: 0.7,
        111: 0.7,
        112: 0.79,
        113: 0.79,
        114: 0.79,
        115: 0.79,
        116: 0.79,
        117: 0.79,
        118: 0.79,
        119: 0.79,
        120: 0.79,
        121: 0.79,
        122: 0.79,
        123: 0.79,
        124: 0.79,
        125: 0.79,
        126: 0.79,
        127: 1.0,
        128: 1.0,
        129: 0.79,
        130: 0.79,
        131: 0.79,
        132: 0.79,
        133: 0.79,
        134: 0.79,
        135: 0.79,
        136: 0.79,
        137: 0.79,
        138: 0.79,
        139: 0.79,
        140: 0.79,
        141: 0.79,
        142: 0.79,
        143: 0.79,
        144: 0.7,
        145: 0.7,
        146: 0.7,
        147: 0.7,
        148: 0.7,
        149: 0.5,
        150: 0.5,
        151: 0.5,
        152: 0.5,
        153: 0.5,
        154: 0.17,
        155: 0.17,
        156: 0.17,
        157: 0.17,
        158: 0.17,
        159: 0.17,
        160: 0.17,
        161: 1.0,
        162: 1.0,
        163: 1.0,
        164: 1.0,
        165: 1.0,
        166: 1.0,
        167: 1.0,
        168: 1.0,
        169: 1.0,
        170: 1.0,
        171: 0.5,
        172: 0.5,
        173: 0.5,
        174: 0.5,
        175: 0.5,
        176: 0.5,
        177: 0.5,
        178: 0.5,
        179: 0.5,
        180: 0.5,
        181: 0.5,
        182: 0.5,
        183: 0.5,
        184: 0.5,
        185: 0.5,
        186: 0.5,
        187: 0.5,
        188: 0.5,
        189: 0.5,
        190: 0.5,
        191: 0.5,
        192: 0.34,
        193: 0.34,
        194: 0.34,
        195: 0.34,
        196: 0.34,
        197: 0.34,
        198: 0.34,
        199: 0.34,
        200: 0.34,
        201: 0.34,
        202: 0.34,
        203: 0.34,
        204: 0.34,
        205: 0.34,
        206: 0.34,
        207: 0.34,
        208: 0.34,
        209: 0.34,
        210: 0.34,
        211: 0.34,
        212: 0.0,
        213: 0.0,
        214: 0.0,
        215: 0.0,
        216: 0.0,
        217: 0.0,
        218: 0.0,
        219: 0.0,
        220: 0.0,
        221: 0.0,
        222: 0.0,
        223: 0.0,
        224: 0.0,
        225: 0.0,
        226: 0.0,
        227: 0.0,
        228: 0.0,
        229: 0.0,
        230: 0.0,
        231: 0.0,
        232: 0.0,
        233: 0.0,
        234: 0.0,
        235: 0.0,
        236: 0.0,
        237: 0.0,
        238: 0.0,
        239: 0.0,
        240: 0.0,
        241: 0.0,
        242: 0.0,
        243: 0.0,
        244: 0.0,
        245: 0.0,
        246: 0.0,
        247: 0.0,
        248: 0.0,
        249: 0.0,
        250: 0.0,
        251: 0.0,
        252: 0.0,
        253: 0.0,
        254: 0.0,
        255: 0.0}

    coefficients = {
        0: (13, 0, 5, 18),
        1: (1300249, 0, 499250, 1799499),
        2: (214114, 287, 99357, 313758),
        3: (351854, 0, 199965, 551819),
        4: (801100, 0, 490999, 1292099),
        5: (801100, 0, 490999, 1292099),
        6: (801100, 0, 490999, 1292099),
        7: (801100, 0, 490999, 1292099),
        8: (801100, 0, 490999, 1292099),
        9: (801100, 0, 490999, 1292099),
        10: (704075, 297466, 303694, 1305235),
        11: (704075, 297466, 303694, 1305235),
        12: (704075, 297466, 303694, 1305235),
        13: (704075, 297466, 303694, 1305235),
        14: (704075, 297466, 303694, 1305235),
        15: (704075, 297466, 303694, 1305235),
        16: (704075, 297466, 303694, 1305235),
        17: (704075, 297466, 303694, 1305235),
        18: (704075, 297466, 303694, 1305235),
        19: (704075, 297466, 303694, 1305235),
        20: (704075, 297466, 303694, 1305235),
        21: (704075, 297466, 303694, 1305235),
        22: (46613, 31917, 21469, 99999),
        23: (46613, 31917, 21469, 99999),
        24: (46613, 31917, 21469, 99999),
        25: (46613, 31917, 21469, 99999),
        26: (46613, 31917, 21469, 99999),
        27: (46613, 31917, 21469, 99999),
        28: (46613, 31917, 21469, 99999),
        29: (46613, 31917, 21469, 99999),
        30: (46613, 31917, 21469, 99999),
        31: (46613, 31917, 21469, 99999),
        32: (47482, 30617, 21900, 99999),
        33: (47482, 30617, 21900, 99999),
        34: (47482, 30617, 21900, 99999),
        35: (47482, 30617, 21900, 99999),
        36: (47482, 30617, 21900, 99999),
        37: (47482, 30617, 21900, 99999),
        38: (47482, 30617, 21900, 99999),
        39: (47482, 30617, 21900, 99999),
        40: (47482, 30617, 21900, 99999),
        41: (47482, 30617, 21900, 99999),
        42: (47482, 30617, 21900, 99999),
        43: (47482, 30617, 21900, 99999),
        44: (43024, 42131, 14826, 99981),
        45: (43024, 42131, 14826, 99981),
        46: (43024, 42131, 14826, 99981),
        47: (43024, 42131, 14826, 99981),
        48: (43024, 42131, 14826, 99981),
        49: (43024, 42131, 14826, 99981),
        50: (43024, 42131, 14826, 99981),
        51: (43024, 42131, 14826, 99981),
        52: (43024, 42131, 14826, 99981),
        53: (43024, 42131, 14826, 99981),
        54: (43024, 42131, 14826, 99981),
        55: (43024, 42131, 14826, 99981),
        56: (43024, 42131, 14826, 99981),
        57: (43024, 42131, 14826, 99981),
        58: (43024, 42131, 14826, 99981),
        59: (43024, 42131, 14826, 99981),
        60: (43024, 42131, 14826, 99981),
        61: (43024, 42131, 14826, 99981),
        62: (43024, 42131, 14826, 99981),
        63: (43024, 42131, 14826, 99981),
        64: (36411, 43219, 20369, 99999),
        65: (36411, 43219, 20369, 99999),
        66: (36411, 43219, 20369, 99999),
        67: (36411, 43219, 20369, 99999),
        68: (36411, 43219, 20369, 99999),
        69: (36411, 43219, 20369, 99999),
        70: (36411, 43219, 20369, 99999),
        71: (36411, 43219, 20369, 99999),
        72: (38477, 53843, 7678, 99998),
        73: (38477, 53843, 7678, 99998),
        74: (38477, 53843, 7678, 99998),
        75: (38477, 53843, 7678, 99998),
        76: (38477, 53843, 7678, 99998),
        77: (40503, 51547, 7948, 99998),
        78: (40503, 51547, 7948, 99998),
        79: (40503, 51547, 7948, 99998),
        80: (40503, 51547, 7948, 99998),
        81: (40503, 51547, 7948, 99998),
        82: (40503, 51547, 7948, 99998),
        83: (40503, 51547, 7948, 99998),
        84: (40503, 51547, 7948, 99998),
        85: (35865, 34108, 30026, 99999),
        86: (35865, 34108, 30026, 99999),
        87: (35865, 34108, 30026, 99999),
        88: (35865, 34108, 30026, 99999),
        89: (35865, 34108, 30026, 99999),
        90: (35865, 34108, 30026, 99999),
        91: (35865, 34108, 30026, 99999),
        92: (35865, 34108, 30026, 99999),
        93: (35865, 34108, 30026, 99999),
        94: (35865, 34108, 30026, 99999),
        95: (34117, 36899, 28983, 99999),
        96: (34117, 36899, 28983, 99999),
        97: (34117, 36899, 28983, 99999),
        98: (34117, 36899, 28983, 99999),
        99: (34117, 36899, 28983, 99999),
        100: (34117, 36899, 28983, 99999),
        101: (34117, 36899, 28983, 99999),
        102: (35464, 35049, 29485, 99998),
        103: (35464, 35049, 29485, 99998),
        104: (35464, 35049, 29485, 99998),
        105: (35464, 35049, 29485, 99998),
        106: (35464, 35049, 29485, 99998),
        107: (16477, 18810, 14712, 49999),
        108: (16477, 18810, 14712, 49999),
        109: (16477, 18810, 14712, 49999),
        110: (16477, 18810, 14712, 49999),
        111: (16477, 18810, 14712, 49999),
        112: (33360, 37954, 28685, 99999),
        113: (33360, 37954, 28685, 99999),
        114: (33360, 37954, 28685, 99999),
        115: (33360, 37954, 28685, 99999),
        116: (33360, 37954, 28685, 99999),
        117: (33360, 37954, 28685, 99999),
        118: (33360, 37954, 28685, 99999),
        119: (33360, 37954, 28685, 99999),
        120: (33360, 37954, 28685, 99999),
        121: (33360, 37954, 28685, 99999),
        122: (33360, 37954, 28685, 99999),
        123: (33360, 37954, 28685, 99999),
        124: (33360, 37954, 28685, 99999),
        125: (33360, 37954, 28685, 99999),
        126: (33360, 37954, 28685, 99999),
        127: (35269, 36066, 28664, 99999),
        128: (35269, 36066, 28664, 99999),
        129: (33360, 37954, 28685, 99999),
        130: (33360, 37954, 28685, 99999),
        131: (33360, 37954, 28685, 99999),
        132: (33360, 37954, 28685, 99999),
        133: (33360, 37954, 28685, 99999),
        134: (33360, 37954, 28685, 99999),
        135: (33360, 37954, 28685, 99999),
        136: (33360, 37954, 28685, 99999),
        137: (33360, 37954, 28685, 99999),
        138: (33360, 37954, 28685, 99999),
        139: (33360, 37954, 28685, 99999),
        140: (33360, 37954, 28685, 99999),
        141: (33360, 37954, 28685, 99999),
        142: (33360, 37954, 28685, 99999),
        143: (33360, 37954, 28685, 99999),
        144: (16477, 18810, 14712, 49999),
        145: (16477, 18810, 14712, 49999),
        146: (16477, 18810, 14712, 49999),
        147: (16477, 18810, 14712, 49999),
        148: (16477, 18810, 14712, 49999),
        149: (35464, 35049, 29485, 99998),
        150: (35464, 35049, 29485, 99998),
        151: (35464, 35049, 29485, 99998),
        152: (35464, 35049, 29485, 99998),
        153: (35464, 35049, 29485, 99998),
        154: (34117, 36899, 28983, 99999),
        155: (34117, 36899, 28983, 99999),
        156: (34117, 36899, 28983, 99999),
        157: (34117, 36899, 28983, 99999),
        158: (34117, 36899, 28983, 99999),
        159: (34117, 36899, 28983, 99999),
        160: (34117, 36899, 28983, 99999),
        161: (35865, 34108, 30026, 99999),
        162: (35865, 34108, 30026, 99999),
        163: (35865, 34108, 30026, 99999),
        164: (35865, 34108, 30026, 99999),
        165: (35865, 34108, 30026, 99999),
        166: (35865, 34108, 30026, 99999),
        167: (35865, 34108, 30026, 99999),
        168: (35865, 34108, 30026, 99999),
        169: (35865, 34108, 30026, 99999),
        170: (35865, 34108, 30026, 99999),
        171: (40503, 51547, 7948, 99998),
        172: (40503, 51547, 7948, 99998),
        173: (40503, 51547, 7948, 99998),
        174: (40503, 51547, 7948, 99998),
        175: (40503, 51547, 7948, 99998),
        176: (40503, 51547, 7948, 99998),
        177: (40503, 51547, 7948, 99998),
        178: (40503, 51547, 7948, 99998),
        179: (38477, 53843, 7678, 99998),
        180: (38477, 53843, 7678, 99998),
        181: (38477, 53843, 7678, 99998),
        182: (38477, 53843, 7678, 99998),
        183: (38477, 53843, 7678, 99998),
        184: (36411, 43219, 20369, 99999),
        185: (36411, 43219, 20369, 99999),
        186: (36411, 43219, 20369, 99999),
        187: (36411, 43219, 20369, 99999),
        188: (36411, 43219, 20369, 99999),
        189: (36411, 43219, 20369, 99999),
        190: (36411, 43219, 20369, 99999),
        191: (36411, 43219, 20369, 99999),
        192: (43024, 42131, 14826, 99981),
        193: (43024, 42131, 14826, 99981),
        194: (43024, 42131, 14826, 99981),
        195: (43024, 42131, 14826, 99981),
        196: (43024, 42131, 14826, 99981),
        197: (43024, 42131, 14826, 99981),
        198: (43024, 42131, 14826, 99981),
        199: (43024, 42131, 14826, 99981),
        200: (43024, 42131, 14826, 99981),
        201: (43024, 42131, 14826, 99981),
        202: (43024, 42131, 14826, 99981),
        203: (43024, 42131, 14826, 99981),
        204: (43024, 42131, 14826, 99981),
        205: (43024, 42131, 14826, 99981),
        206: (43024, 42131, 14826, 99981),
        207: (43024, 42131, 14826, 99981),
        208: (43024, 42131, 14826, 99981),
        209: (43024, 42131, 14826, 99981),
        210: (43024, 42131, 14826, 99981),
        211: (43024, 42131, 14826, 99981),
        212: (47482, 30617, 21900, 99999),
        213: (47482, 30617, 21900, 99999),
        214: (47482, 30617, 21900, 99999),
        215: (47482, 30617, 21900, 99999),
        216: (47482, 30617, 21900, 99999),
        217: (47482, 30617, 21900, 99999),
        218: (47482, 30617, 21900, 99999),
        219: (47482, 30617, 21900, 99999),
        220: (47482, 30617, 21900, 99999),
        221: (47482, 30617, 21900, 99999),
        222: (47482, 30617, 21900, 99999),
        223: (47482, 30617, 21900, 99999),
        224: (46613, 31917, 21469, 99999),
        225: (46613, 31917, 21469, 99999),
        226: (46613, 31917, 21469, 99999),
        227: (46613, 31917, 21469, 99999),
        228: (46613, 31917, 21469, 99999),
        229: (46613, 31917, 21469, 99999),
        230: (46613, 31917, 21469, 99999),
        231: (46613, 31917, 21469, 99999),
        232: (46613, 31917, 21469, 99999),
        233: (46613, 31917, 21469, 99999),
        234: (704075, 297466, 303694, 1305235),
        235: (704075, 297466, 303694, 1305235),
        236: (704075, 297466, 303694, 1305235),
        237: (704075, 297466, 303694, 1305235),
        238: (704075, 297466, 303694, 1305235),
        239: (704075, 297466, 303694, 1305235),
        240: (704075, 297466, 303694, 1305235),
        241: (704075, 297466, 303694, 1305235),
        242: (704075, 297466, 303694, 1305235),
        243: (704075, 297466, 303694, 1305235),
        244: (704075, 297466, 303694, 1305235),
        245: (704075, 297466, 303694, 1305235),
        246: (801100, 0, 490999, 1292099),
        247: (801100, 0, 490999, 1292099),
        248: (801100, 0, 490999, 1292099),
        249: (801100, 0, 490999, 1292099),
        250: (801100, 0, 490999, 1292099),
        251: (801100, 0, 490999, 1292099),
        252: (351854, 0, 199965, 551819),
        253: (214114, 287, 99357, 313758),
        254: (1300249, 0, 499250, 1799499),
        255: (13, 0, 5, 18)
    }

    H, W = img.shape
    rand = np.random.randint(0, 255, (H,W))
    new_img = np.zeros((H,W), dtype=np.float32)
    error_map = np.zeros((H+1, W+1), dtype=np.float32)

    for i in range(H):
        for j in range(W):
            corrected_level = img[i,j] + error_map[i,j]
            intensity = thresold_func(corrected_level, rand[i,j], modulation_strength)
            diff = corrected_level - intensity
            error_map = distribute_error(error_map, diff, i, j, img[i,j], coefficients)
            new_img[i,j] = intensity

    return new_img

main(np.zeros((10,10), dtype=np.uint8)) # trigger compilation, takes ~30s for the first time.

if __name__ == '__main__':
    from argparse import ArgumentParser
    from time import time
    parser = ArgumentParser()
    parser.add_argument('input', type=str)
    parser.add_argument('output', type=str)
    args = parser.parse_args()

    # DO NOT REPORT THIS... COMPILATION TIME IS INCLUDED IN THE EXECUTION TIME!
    img = cv2.imread(args.input, cv2.IMREAD_GRAYSCALE)
    start = time()
    # new_img = dither(img)
    new_img = main(img)
    end = time()
    print("Elapsed (with compilation) = %s" % (end - start))


    # NOW THE FUNCTION IS COMPILED, RE-TIME IT EXECUTING FROM CACHE
    start = time()
    # new_img = dither(img)
    new_img = main(img)
    end = time()
    print("Elapsed (after compilation) = %s" % (end - start))

    cv2.imwrite(args.output, new_img)
