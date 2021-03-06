class bunchTrainIndex(object):
  
    def __init__(self):
        self.bunchTrainStart = [
                [3,10],[46,8],[58,8],[70,8],[82,8],[121,8],[133,8],[145,8],[157,8],[172,8],[184,8],[196,8],[208,8],[223,8],[235,8],[247,8],[259,8],[274,8],[286,8],[298,8],[310,8],[349,8],[361,8],[373,8],[385,8],[400,8],[412,8],[424,8],[436,8],[451,8],[463,8],[475,8],[487,8],[502,8],[514,8],[526,8],[538,8],[577,8],[589,8],[601,8],[613,8],[628,8],[640,8],[652,8],[664,8],[679,8],[691,8],[703,8],[715,8],[730,8],[742,8],[754,8],[766,8],[826,8],[838,8],[850,8],[862,8],[877,8],[889,8],[901,8],[913,8],[928,8],[940,8],[952,8],[964,8],[1003,8],[1015,8],[1027,8],[1039,8],[1054,8],[1066,8],[1078,8],[1090,8],[1105,8],[1117,8],[1129,8],[1141,8],[1156,8],[1168,8],[1180,8],[1192,8],[1231,8],[1243,8],[1255,8],[1267,8],[1282,8],[1294,8],[1306,8],[1318,8],[1333,8],[1345,8],[1357,8],[1369,8],[1384,8],[1396,8],[1408,8],[1420,8],[1459,8],[1471,8],[1483,8],[1495,8],[1510,8],[1522,8],[1534,8],[1546,8],[1561,8],[1573,8],[1585,8],[1597,8],[1612,8],[1624,8],[1636,8],[1648,8],[1720,8],[1732,8],[1744,8],[1756,8],[1771,8],[1783,8],[1795,8],[1807,8],[1822,8],[1834,8],[1846,8],[1858,8],[1897,8],[1909,8],[1921,8],[1933,8],[1948,8],[1960,8],[1972,8],[1984,8],[1999,8],[2011,8],[2023,8],[2035,8],[2050,8],[2062,8],[2074,8],[2086,8],[2125,8],[2137,8],[2149,8],[2161,8],[2176,8],[2188,8],[2200,8],[2212,8],[2227,8],[2239,8],[2251,8],[2263,8],[2278,8],[2290,8],[2302,8],[2314,8],[2353,8],[2365,8],[2377,8],[2389,8],[2404,8],[2416,8],[2428,8],[2440,8],[2455,8],[2467,8],[2479,8],[2491,8],[2506,8],[2518,8],[2530,8],[2542,8],[2614,8],[2626,8],[2638,8],[2650,8],[2665,8],[2677,8],[2689,8],[2701,8],[2716,8],[2728,8],[2740,8],[2752,8],[2791,8],[2803,8],[2815,8],[2827,8],[2842,8],[2854,8],[2866,8],[2878,8],[2893,8],[2905,8],[2917,8],[2929,8],[2944,8],[2956,8],[2968,8],[2980,8],[3019,8],[3031,8],[3043,8],[3055,8],[3070,8],[3082,8],[3094,8],[3106,8],[3121,8],[3133,8],[3145,8],[3157,8],[3172,8],[3184,8],[3196,8],[3208,8],[3247,8],[3259,8],[3271,8],[3283,8],[3298,8],[3310,8],[3322,8],[3334,8],[3349,8],[3361,8],[3373,8],[3385,8],[3400,8],[3412,8],[3424,8],[3436,8]
                ]
        self.nBunches = 3564
        self.bunchTrainIndices = [0] * self.nBunches
        for b, l in self.bunchTrainStart:
            for k in range(l):
                self.bunchTrainIndices[b+k] = k + 1

    def get(self, bx):
        if bx >= self.nBunches:
            return -1
        return self.bunchTrainIndices[bx]

ti = bunchTrainIndex()

# how to get the index for a bx
#print(ti.get(bx=48))
