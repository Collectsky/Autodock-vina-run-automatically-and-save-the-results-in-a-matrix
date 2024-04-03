
import re
import os
import numpy as np
import pandas as pd
import time
start_time = time.time()  # 记录开始时间

pro_name = ["-1-","-2-","-3-"]  # protein name，这里放蛋白pdbqt的名字
lig_ID= [1,2,3,5]                   # ligand lig_ID，这里放配体pdbqt的名字
pro = len(pro_name)
lig = len(lig_ID)
matrix = np.zeros((lig, pro))
df = pd.DataFrame(matrix, columns=pro_name, index=lig_ID)
# 下面是每个蛋白的坐标，可以按照此格式更改
XYZ = {"-1-":"""center_x = 21.925        
center_y = -9.3
center_z = -1.013
size_x = 38.0
size_y = 44.0
size_z = 36.0
""","-2-":"""center_x = 31.739
center_y = 21.58
center_z = 25.04
size_x = 54.0
size_y = 40.0
size_z = 40.0
""","-3-":"""center_x = -5.959
center_y = 0.103
center_z = 2.339
size_x = 76.0
size_y = 92.0
size_z = 52.0
"""}


for indexx, x in enumerate(pro_name):
    xyz = XYZ[x]
    # 生成config模块
    for indexY, i in enumerate(lig_ID):
        config = '''receptor = {}.pdbqt
ligand = {}.pdbqt
{}out = {}{}.pdbqt
num_modes = 5
exhaustiveness = 15
    '''.format(x, i, xyz, x, i)
        wd = ".\\{}{}.txt".format(x, i)
        with open(wd, mode="w", encoding='utf-8') as ff:
            ff.write(''.join(config))
            ff.close()
    # 模拟cmd命令进行对接
    for indexY, i in enumerate(lig_ID):
        print("正在运行{}{}".format(x, i))
        a = '{}{}.txt'.format(x, i)
        b = '.\\vina.exe --config .\\' + a
        root_pattern = 'rmsd(.*?)0.000'
        result = os.popen(b)
        context = result.read()
        out = context.encode('utf-8')
        o = str(out)
        oo = re.findall(root_pattern, o)
        for ii in oo:
            ooo = ii
            ooo = ooo[-15:]
            pattern = r"\S+"
            ooo = re.findall(pattern, ooo)
            # 将结果保存在矩阵中
            print(str(x) + str(i) + "\t" + str(ooo[0]) + "\n")
            df.at[i, x] = str(ooo[0])
            df.to_csv(".\\结果{}-{}.csv".format(lig, pro))
            pass
        pass
    pass


end_time = time.time()  # 记录结束时间
elapsed_time = end_time - start_time  # 计算耗时
print(f"本次计算耗时{elapsed_time:.6f}秒")

