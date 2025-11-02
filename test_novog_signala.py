from parse import parse_1signal

if __name__ == '__main__':
    novi_signali = parse_1signal("b9/b9.route",{1,10,11})
    for signal_id in novi_signali:
        print(f"{signal_id},{novi_signali[{10}]}")

"""
python3 test_novog_signala.py

1,[403, 412, 1100, 1564, 1572, 1580, 453, 450, 1572, 438, 432, 1564, 1152, 1616, 582, 576]
10,[817, 826, 1404, 1699, 1691, 1316, 1731, 1271, 887, 882, 1691, 1683, 1263, 747, 738]
11,[1009, 1018, 1720, 892, 882, 1720, 1267, 1259, 750, 738]
"""

