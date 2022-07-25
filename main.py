import functions as f

fotka = 'pc_fotka.las'
lidar = 'pc_lidar.las'

f.split2clouds(fotka)
f.split2clouds(lidar)

fotka2 = fotka[:-4] + '_class_2.las'
fotka6 = fotka[:-4] + '_class_6.las'

lidar2 = lidar[:-4] + '_class_2.las'
lidar6 = lidar[:-4] + '_class_6.las'

name_mesh_fotka = 'model_' + fotka[3:-4] + '.obj'
name_mesh_lidar = 'model_' + lidar[3:-4] + '.obj'

f.mesh_generator_agi(fotka2, name_mesh_fotka)
f.mesh_generator_agi(lidar2, name_mesh_lidar)

