import laspy
import open3d as o3d
from open3d import geometry
import numpy as np
import Metashape


def extraction(name, class_no):
    las = laspy.read(name)

    new_file = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
    new_file.header = las.header
    new_file.vlrs = las.vlrs
    new_file.points = las.points[las.classification == int(class_no)]
    class_no = str(class_no)
    out_name = name[0:-4] + '_class_' + class_no + '.las'
    new_file.write(out_name)
    print('Created ' + out_name)


def split2clouds(name_input):
    print('Cloud splited.')
    extraction(name_input, 2)
    extraction(name_input, 6)


def mesh_generator_agi(ground_las, name):
    # if crs == 'pl2000':
    #     crs = "EPSG::2178"
    #     print('### Coordinate Reference System set as PL-2000. ###')
    # elif crs == 'pl1992':
    #     crs = "EPSG::2180"
    #     print('### Coordinate Reference System set as PL-1992. ###')
    # else:
    #     print('Zły układ współrzędnych!!!!!!!!!!!!!!!')

    doc = Metashape.Document()
    chunk = doc.addChunk()
    # chunk.crs = Metashape.CoordinateSystem(crs)
    chunk.updateTransform()
    print('Chunk created.')

    print('#############################################')
    print('###        Starting points import         ###')
    print('#############################################')
    chunk.importPoints(path=ground_las, format=Metashape.PointsFormatLAS, calculate_normals=True)
    print('#############################################')
    print('###        Points import done             ###')
    print('#############################################')

    doc.save('TEF_agi.psx')

    chunk.resetRegion()

    print("Region set.")

    print('#############################################')
    print('###        Starting building model        ###')
    print('#############################################')
    chunk.buildModel(surface_type=Metashape.HeightField, interpolation=Metashape.Extrapolated,
                     face_count=Metashape.HighFaceCount, face_count_custom=200000, source_data=Metashape.DenseCloudData,
                     vertex_colors=False, vertex_confidence=True, volumetric_masks=False, keep_depth=True,
                     trimming_radius=10)
    print('#############################################')
    print('###        Model done.                    ###')
    print('#############################################')

    doc.save()
    path = r'C:\Users\admin1\Desktop\MGR1\TEF' + '\\' + name
    chunk.exportModel(path=path, binary=True, precision=6, texture_format=Metashape.ImageFormatJPEG, save_texture=False,
                      save_uv=True, save_normals=True, save_colors=False, save_confidence=False,
                      save_cameras=False, save_markers=True, save_udim=False, save_alpha=False,
                      embed_texture=False, strip_extensions=False, raster_transform=Metashape.RasterTransformNone,
                      colors_rgb_8bit=True, comment='', save_comment=True, format=Metashape.ModelFormatOBJ)

    doc.save()
