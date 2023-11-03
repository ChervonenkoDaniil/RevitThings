# Загрузить стандартную библиотеку Python и библиотеку DesignScript
import sys
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Введенные в этом узле данные сохраняется в виде списка в переменных IN.
start_points = IN[0]
end_points = IN[1]
roof_indices = IN[2]
floor_indices = IN[3]
roof_zcoord = IN[4]
lvl_names = IN[5]

# 1.0 - Уровни кровли идут последовательно
## 1.1 - Перекрытие этажа ниже имеет одинаковую отметку на всем протяжении
## 1.2 - Перекрытие этажа ниже имеет разные отметки (Песочный)
# 2.0 - Уровни кровли идут непоследовательно (уровень одного из этажей выше отметки одной из кровель)
## 2.1 - Уровни ниже - одинаковые
## 2.2 - Уровень под нижней кровлей != уровню под уровнем выше нижней кровли
counter = 0.0
# Разместите код под этой строкой
for i in range(0, len(roof_indices) - 1):
    if roof_indices[i + 1] == roof_indices[i] + 1:
        counter = 1.0
    else:
        counter = 2.0

points_unificator_iter1 = [[[] for floors in indices] for indices in start_points]
points_unificator_iter2 = [[[] for floors in indices] for indices in start_points]
points_unificator_X = [[[] for floors in indices] for indices in start_points]
points_unificator_Y = [[[] for floors in indices] for indices in start_points]
points_unificator_Z = [[[] for floors in indices] for indices in start_points]

if counter == 1.0:
    for i in range(len(start_points)):
        for floor_quantity in range(len(start_points[i])):
            for points_set in start_points[i][floor_quantity]:
                points_unificator_iter1[i][floor_quantity].extend([points for points in points_set])

    for i in range(len(start_points)):
        for floor_quantity in range(len(points_unificator_iter1[i])):
            points_unificator_iter2[i][floor_quantity].append(points_unificator_iter1[i][floor_quantity])
    """for i in range(len(floor_indices)):
		for floor_quantity in range(len(floor_indices[i])):

			points_unificator_X[i][floor_quantity] = set(points_unificator[i][floor_quantity])"""

if counter == 2.0:

    level_list = [[] for i in range(len(roof_indices))]
    elev_index_list = [[] for i in range(len(roof_indices))]

    for key in range(len(roof_indices)):

        for lvl_index, lvl_name in lvl_names:

            if "К" in adsk_etazh[index_] and adsk_etazh[index_] not in key:
                continue

            else:
                level_list[key_list.index(key)].append(etazh)
                elev_index_list[key_list.index(key)].append(index_)

# Назначьте вывод переменной OUT.
OUT = points_unificator_iter1