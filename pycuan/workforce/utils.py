def compute_ratio_revenue(sf, adb_min, adb_max, c, d):
    return adb_min + (adb_max - adb_min) * (sf ** c) / (d + sf ** c)