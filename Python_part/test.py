#用来测试Tensorflow
from MyCNN import plr

plr.init_tensorflow()
photo_path="D:/tmp/Plr_UploadPhoto/1527736074811_3b7b23df-b983-449c-88b1-9bf05ecdc41f.jpg"
plr.input_photo(photo_path)
photo_path="D:/tmp/mycifar10_data/Train/家电数码_大家电_电视/3a1dd8a5-cc80-496b-9c87-e1464fb67baa.jpg"
plr.input_photo(photo_path)