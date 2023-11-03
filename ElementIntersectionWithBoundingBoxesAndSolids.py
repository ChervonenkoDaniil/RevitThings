# Загрузить стандартную библиотеку Python и библиотеку DesignScript
import sys
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitNodes')
import Revit
from Revit.Elements import *

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager as DM

from System.Collections.Generic import *

# Введенные в этом узле данные сохраняется в виде списка в переменных IN.

lines_to_find_coords = IN[0]  # Линии контура здания
roof_lvl_ind = IN[1]  # Индексы кровли
roof_lvl_number = len(roof_lvl_ind)

doc = DM.Instance.CurrentDBDocument

start_points = [[] for i in range(len(lines_to_find_coords))]
end_points = [[] for i in range(len(lines_to_find_coords))]

# Разместите код под этой строкой

for roof_number in range(len(lines_to_find_coords)):
    for lines_set in lines_to_find_coords[roof_number]:
        for lines_contour in lines_set:
            start_points[roof_number].append(line.StartPoint for line in lines_contour)
            end_points[roof_number].append(line.EndPoint for line in lines_contour)
    continue

max_x = []
min_x = []
max_y = []
min_y = []
min_z = []
max_x_coord = []
min_x_coord = []
max_y_coord = []
min_y_coord = []
min_z_coord = []

x_coord_start = [[] for i in range(roof_lvl_number)]
x_coord_end = [[] for i in range(roof_lvl_number)]
y_coord_start = [[] for i in range(roof_lvl_number)]
y_coord_end = [[] for i in range(roof_lvl_number)]
z_coord_start = [[] for i in range(roof_lvl_number)]
z_coord_end = [[] for i in range(roof_lvl_number)]

# Получение начальных и конечных точек линий контуров перекрытий
for roof_number in range(len(start_points)):

    for points_set in range(len(start_points[roof_number])):

        for start_point in start_points[roof_number][points_set]:
            x_coord_start[roof_number].append(start_point.X)
            y_coord_start[roof_number].append(start_point.Y)
            z_coord_start[roof_number].append(start_point.Z)

        for end_point in end_points[roof_number][points_set]:
            x_coord_end[roof_number].append(end_point.X)
            y_coord_end[roof_number].append(end_point.Y)
            z_coord_end[roof_number].append(end_point.Z)

# Получение максимальных значений координат
for roof_number in range(len(x_coord_start)):
    max_x.append(max(x_coord_start[roof_number] + x_coord_end[roof_number]))
    max_y.append(max(y_coord_start[roof_number] + y_coord_end[roof_number]))
    min_x.append(min(x_coord_start[roof_number] + x_coord_end[roof_number]))
    min_y.append(min(y_coord_start[roof_number] + y_coord_end[roof_number]))
    min_z.append(min(z_coord_start[roof_number] + z_coord_end[roof_number]))

"""max_points = [Point.Create(XYZ(max_x[i],max_y[i],min_z[i]+5000)) for i in range(roof_lvl_number)]
min_points = [Point.Create(XYZ(min_x[i],min_y[i],min_z[i])) for i in range(roof_lvl_number)]
max_points_coord = [[max_x[j], max_y[j], min_z[j]+5000] for j in range(roof_lvl_number)]
min_points_coord = [[min_x[j], min_y[j], min_z[j]]for j in range(roof_lvl_number)]"""

# Получение координат точек углов ограждающих рамок по перекрытиям
min_points_coord = [XYZ(min_x[j], min_y[j], min_z[j]) for j in range(roof_lvl_number)]
max_min_points_coord = [XYZ(max_x[j], min_y[j], min_z[j]) for j in range(roof_lvl_number)]
max_points_coord = [XYZ(max_x[j], max_y[j], min_z[j]) for j in range(roof_lvl_number)]
min_max_points_coord = [XYZ(min_x[j], max_y[j], min_z[j]) for j in range(roof_lvl_number)]

# Получение граней контура ограждающей рамки по перекрытиям
edge_min_to_maxmin = [Line.CreateBound(min_points_coord[j], max_min_points_coord[j]) for j in range(roof_lvl_number)]
edge_maxmin_to_max = [Line.CreateBound(max_min_points_coord[j], max_points_coord[j]) for j in range(roof_lvl_number)]
edge_max_to_minmax = [Line.CreateBound(max_points_coord[j], min_max_points_coord[j]) for j in range(roof_lvl_number)]
edge_minmax_to_min = [Line.CreateBound(min_max_points_coord[j], min_points_coord[j]) for j in range(roof_lvl_number)]

# Формирование солидов
# Получение списка наборов кривых
curve_loop_list = [List[Curve]() for i in range(roof_lvl_number)]
for i in range(roof_lvl_number):
    curve_loop_list[i].Add(edge_min_to_maxmin[i])
    curve_loop_list[i].Add(edge_maxmin_to_max[i])
    curve_loop_list[i].Add(edge_max_to_minmax[i])
    curve_loop_list[i].Add(edge_minmax_to_min[i])

# Получение списка контуров
loop = [List[CurveLoop]() for i in range(roof_lvl_number)]
for i in range(roof_lvl_number):
    loop[i].Add(CurveLoop.Create(curve_loop_list[i]))

# Получение направления выдавливания - вверх
basis_z = XYZ.BasisZ
# Получение высоты будущих солида
height = 5000

# Построение солидов
solid_boxes = [GeometryCreationUtilities.CreateExtrusionGeometry(loop[i], basis_z, height) for i in range(roof_lvl_number)]

# Формирование боксов
# Формирование контура для фильтра
# outlines = [Outline(min_points[i].Coord, max_points[i].Coord) for i in range(roof_lvl_number)]

# Формирование контура по боксам
"""boxes = [BoundingBoxXYZ() for i in range(roof_lvl_number)]
for j in range(len(boxes)):
    boxes[j].Min = min_points[j].Coord
    boxes[j].Max = max_points[j].Coord
b = [boxes[j].Max for j in range(len(boxes))]

outlines = [Outline(boxes[j].Min, boxes[j].Max) for j in range(len(boxes))]"""

# Фильтр вхождения по солиду
filter_in = [ElementIntersectsSolidFilter(solid_boxes[i], False) for i in range(len(solid_boxes))]
# Фильтр вхождения по боксу
# filter_in = [BoundingBoxIsInsideFilter(outlines[i], False) for i in range(len(outlines))]

collector_in = [FilteredElementCollector(doc).WhereElementIsNotElementType().WherePasses(filter_in[i]).ToElements() for i in range(len(solid_boxes))]
# collector_in = FilteredElementCollector(doc).WherePasses(filter_in).ToElements()
# collector_out = FilteredElementCollector(doc, view_id).WherePasses(filter_out).WhereElementsIsNotElementType().ToElements()"""

# Назначьте вывод переменной OUT.
# OUT = solid_boxes
#OUT = max_points_coord, min_points_coord, collector_in
OUT = collector_in