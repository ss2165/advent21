from typing import Callable
import numpy as np
from math import floor, ceil
def cost(posar: np.ndarray, pos: int) -> int:
    return sum(np.abs(posar - pos))

def quad_cost(posar: np.ndarray, pos: int) -> int:
    dif = np.abs(posar - pos)
    return 0.5*np.sum(dif*(dif+1))
def min_pos(pos:list[int]) -> tuple[int, int]:
    # WARNING I think this only works if the minimum happens to be one of the
    # positions

    posar = np.array(pos)
    posar.sort()
    minpos = posar[int(len(pos)/2) - 1]


    return minpos, cost(posar, minpos)


def deriv(posar: np.ndarray, pos: int) -> float:
    posar.sort()
    # k = int(np.where(posar ==pos)[0][0])
    k = np.searchsorted(posar, pos)
    print(k)
    N = len(posar)
    sumar = np.sum(posar)

    return N*(pos - 0.5) + k - sumar

def gen_opt(posar: np.ndarray) -> Callable[[np.ndarray], float]:
    def opt(midpos: np.ndarray) -> float:
        return abs(deriv(posar, int(midpos[0])))
    
    return opt

poses = np.array([1101,1,29,67,1102,0,1,65,1008,65,35,66,1005,66,28,1,67,65,20,4,0,1001,65,1,65,1106,0,8,99,35,67,101,99,105,32,110,39,101,115,116,32,112,97,115,32,117,110,101,32,105,110,116,99,111,100,101,32,112,114,111,103,114,97,109,10,281,282,677,25,264,2,413,1654,100,68,1111,667,281,128,172,188,4,432,250,232,1282,773,24,1182,33,200,989,148,179,108,208,330,152,227,597,517,1205,489,342,98,287,375,413,385,419,115,42,1363,425,1104,1869,362,111,985,1028,192,504,381,58,634,391,174,125,23,39,255,1437,198,259,154,1644,1275,250,444,122,71,697,184,594,307,694,177,131,269,1780,592,678,128,33,41,541,132,241,883,82,498,1008,153,985,127,801,78,137,128,68,69,180,833,250,1476,127,439,1856,276,58,1785,520,1214,749,429,126,576,9,184,578,1173,83,896,475,23,183,108,532,1114,775,748,422,577,758,1365,97,726,118,206,283,485,798,338,459,954,361,205,30,736,65,94,857,986,452,273,210,1551,354,91,26,60,1691,391,163,132,833,52,629,309,261,148,328,17,604,309,907,441,361,104,190,434,246,295,223,141,239,662,682,494,467,185,1,236,367,125,139,1289,657,279,238,482,512,1498,3,1297,148,548,1053,277,400,713,33,140,227,408,1,1592,219,805,538,535,567,703,939,662,546,993,552,341,144,396,922,324,662,82,142,320,859,369,28,106,741,254,389,483,680,1317,3,177,46,1461,53,1516,858,993,968,1325,4,4,175,303,126,847,754,1129,993,79,67,1381,766,470,1324,726,48,26,703,5,1002,102,1839,236,370,1005,855,262,1018,325,3,681,397,1420,1163,155,961,452,512,112,222,39,435,64,746,185,151,397,1648,315,381,25,1053,151,280,230,602,130,173,784,664,129,625,114,405,773,191,116,1017,1401,16,47,72,192,88,68,802,446,479,7,347,167,35,713,74,404,628,283,920,402,1173,273,436,671,1544,149,278,331,766,888,10,567,53,138,10,132,1273,266,270,305,93,1649,86,3,224,79,1188,609,1107,308,1525,159,895,911,824,1135,560,43,436,1225,1332,57,245,90,1057,814,54,68,168,9,190,572,916,42,330,500,310,1269,583,27,482,399,361,706,1109,252,433,851,137,1081,118,107,254,1062,640,1284,297,379,177,268,230,1148,727,829,129,51,808,223,559,14,155,189,1050,931,1069,927,73,594,44,1049,32,253,1621,134,263,5,926,339,141,220,1330,319,408,722,611,0,303,680,323,502,373,46,61,3,121,263,346,88,39,1084,297,822,468,764,138,161,449,35,1162,1308,312,694,207,921,330,1621,302,707,378,612,7,3,1595,1075,915,171,370,516,115,157,340,603,984,239,2,266,1501,129,110,1272,1105,221,431,1002,455,1204,595,914,1396,59,1576,260,446,1898,584,18,204,66,920,526,0,1199,290,1275,12,14,187,818,448,1015,442,292,1019,383,1217,17,228,214,778,53,148,68,388,15,496,310,428,186,18,206,104,760,790,408,1652,95,1351,325,144,73,1301,1085,29,967,342,656,428,533,67,1252,365,130,49,457,34,808,88,47,803,125,291,558,457,160,1157,1410,90,215,638,1009,446,698,1102,171,1736,878,115,1195,1453,261,121,1,59,56,295,368,646,1220,73,370,555,27,94,186,1536,1527,641,8,626,44,86,266,0,110,329,278,777,1839,20,651,435,172,4,144,617,48,201,751,440,231,0,686,1550,605,208,0,10,613,552,788,183,18,71,119,705,223,17,645,77,83,1342,1671,561,499,836,247,678,923,205,69,69,353,242,114,97,132,234,245,364,40,1061,117,665,183,192,448,283,593,71,208,1537,386,35,434,840,462,27,458,347,293,93,288,250,753,536,1317,124,968,937,503,305,19,24,638,560,488,254,1556,748,86,551,972,1675,28,175,1008,607,263,19,446,566,316,236,1577,0,802,340,526,778,763,41,489,1225,145,116,1,1556,221,703,624,33,74,1404,869,574,190,326,646,33,582,1212,703,76,97,54,41,127,48,309,556,10,356,1028,306,712,193,325,81,100,1414,107,81,1150,339,70,346,523,250,265,104,1302,797,499,829,455,591,170,1339,60,1312,631,665,530,95,348,36,1122,1334,775,54,819,604,759,708,139,1394,481,683,26,66,177,54,318,33,1714,43,801,121,384,560,658,50,159,1835,333,232,203,449,221,659,160,83,93,1176,1170,279,265,907,617,45,342,104,723,1027,697,494,952,494,820,90,462,208,1596,513,24,192,438,138,132,2,566,324,826,444,866,1038,851,629,646,48,334,258,14,571,963,458,62,208,233,31,368,884,207,88,682,118,634,1277,51,352,90,194,323,99,24,138,82,501,1084,403,270,638,401
])
poses.sort()

# minimum is always in vicinity of the mean
# x = mean + 0.5 - k/N
# where k is the index of the largest position in the sorted array that is
# smaller than x; x_k <= x < x_k+1
mean = poses.mean()
minpos2 = min( ((i, quad_cost(poses, i)) for i in range(floor(mean-1), ceil(mean + 2))), key=lambda x: x[1])
print(poses.mean())
print(minpos2)
