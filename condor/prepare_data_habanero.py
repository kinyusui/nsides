import numpy as np
from scipy import stats, sparse, io


import argparse
parser = argparse.ArgumentParser(description='Keras MLP model for DDI PSM.')
parser.add_argument('--model-number',
                    help='Numerical ID of the drug against which to fit the model',
                    action='store',
                    dest='model_num',
                    default=2451)
args = parser.parse_args()

args.model_num = int(args.model_num)

#runIndices = [30, 87, 88, 95, 144, 153, 158, 168, 169, 170, 179, 189, 202, 214, 226, 235, 288, 289, 295, 299, 317, 323, 374, 383, 401, 402, 457, 478, 531, 628, 674, 676, 677, 690, 698, 702, 712, 792, 810, 849, 902, 951, 974, 977, 1036, 1041, 1042, 1057, 1084, 1119, 1225, 1242, 1271, 1281, 1285, 1289, 1290, 1300, 1360, 1384, 1400, 1410, 1428, 1441, 1508, 1517, 1525, 1528, 1533, 1538, 1551, 1562, 1574, 1585, 1640, 1668, 1678, 1711, 1738, 1741, 1769, 1807, 1816, 1820, 1851, 1853, 1891, 1896, 1904, 1910, 1942, 1950, 1990, 1995, 1996, 2039, 2040, 2054, 2058, 2068, 2127, 2149, 2168, 2221, 2236, 2265, 2270, 2303, 2309, 2313, 2315, 2316, 2317, 2333, 2341, 2369, 2383, 2385, 2412, 2426, 2430, 2437, 2439, 2442, 2447, 2449, 2470, 2477, 2506, 2513, 2527, 2534, 2537, 2569, 2590, 2609, 2611, 2616, 2657, 2679, 2746, 2749, 2764, 2765, 2785, 2793, 2811, 2826, 2875, 2881, 2981, 2987, 2992, 3033, 3039, 3148, 3164, 3168, 3192, 3198, 3210, 3372, 3391, 3401, 3429, 3430, 3502, 3519, 3522, 3543, 3560, 3562, 3584, 3591, 3609, 3693, 3712, 3750, 3790, 3803, 3830, 3853, 3856, 3884, 3895, 3899, 3908, 3909, 3917, 3931, 3968, 3981, 4016, 4022, 4050, 4082, 4121, 4138, 4153, 4190, 2451, 1617, 2863]

runIndices = [2451,2465,2571,2512,2200,2431,2596,2875,2889,2912,2882,1931,2973,2975,2977,2983,2984,2996,3015,2960,2231,2922,2934,1955,2985,3014,2928,2916,2865,2859,2094,1960,2897,2904,2932,2071,3020,3023,2926,1864,2858,2860,2237,2950,1898,1966,2048,1876,2001,1971,2066,1793,1845,1724,1804,1745,1738,1770,1692,1782,2854,2955,3017,2890,2850,2780,2793,2731,2773,1714,1844,1697,1709,1775,1760,1786,1809,1815,1831,1799,1816,1766,1947,1801,3266,1995,2219,2114,2156,1896,2154,2296,2259,2373,2374,2324,2359,2291,2305,2283,2400,2357,2372,2311,2270,2278,2286,2304,2011,2266,2361,2391,2405,2276,1825,2207,1848,3910,1740,1837,1853,1703,1783,2524,2518,2492,2548,2552,2437,2527,1962,2031,2753,2342,2157,2723,2789,2790,1871,2804,2803,2811,2788,2835,2717,2238,2236,3180,3669,4215]


for reportblock in range(0,50):
    #if args.verbose:
        #print("Report Block: {0} out of 49.".format(reportblock))
    thisReportBlock = np.load("../data/AEOLUS_all_reports_"+str(reportblock)+".npy").item()
    if reportblock == 0:
        allReports = thisReportBlock
    else:
        allReports = sparse.vstack((allReports,thisReportBlock))
    print "Processed ",reportblock

allReportsCSR = allReports.tocsr()
del (allReports)
allReportsCSR = allReportsCSR[0:4855498]  # discard empty rows at end of dataset
#thisReportBlock_array = allReportsCSR.toarray()
thisReportBlock_array = allReportsCSR
del(allReportsCSR)
maxidx = runIndices[args.model_num]
colmax = thisReportBlock_array[:,maxidx]
colmax = colmax.astype(bool)
to_keep_col = list(set(range(thisReportBlock_array.shape[1])))
#to_keep_col.remove(maxidx)
colmax = thisReportBlock_array[:,maxidx]
colmax = colmax.astype(bool)
colmax = colmax.toarray()
posReports = thisReportBlock_array[np.where(colmax == True)[0]].toarray()
fractions = np.divide(np.sum(posReports.astype(float),axis=0),np.sum(colmax))
print len(to_keep_col), "columns."
to_keep_col = np.where(fractions > 0.00)[0]
print len(to_keep_col), "columns."
to_keep_col = np.delete(to_keep_col,np.where(to_keep_col==maxidx))
print len(to_keep_col), "columns."
thisReportBlock_array = thisReportBlock_array[:,to_keep_col]
colmax = colmax.astype(int)


#np.save("model_"+str(runIndices[args.model_num])+"_reports.npy",thisReportBlock_array)
io.mmwrite("model_"+str(runIndices[args.model_num])+"_reports.mtx",thisReportBlock_array,field='integer')
np.save("model_"+str(runIndices[args.model_num])+"_reports.npy",thisReportBlock_array.toarray())
np.save("model_"+str(runIndices[args.model_num])+"_outcomes.npy",colmax)

del colmax
del thisReportBlock_array




