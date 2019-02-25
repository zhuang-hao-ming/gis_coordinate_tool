

'''
投影shp文件
'''

import geopandas as gpd
# import time
import argparse
from gooey import Gooey
from gooey import GooeyParser

@Gooey(program_name='投影小程序')
def proj_shp_file():
    '''
    将输入的带有空间坐标系的文件转换到另外一个空间坐标系下


    Parameters:
    ------------------
    in_shp_path: str
        输入的带有空间坐标系的文件（原始空间坐标系由输入文件中获取）
    out_shp_path: str
        输出路径
    out_epsg: int
        目标空间坐标系的epsg标记


    '''
    parser = GooeyParser(description='将带有空间坐标系的文件（shp）投影到任意其它坐标系')
    group = parser.add_argument_group('必须参数',gooey_options={'show_border': False})
    group.add_argument('in_shp_path', help='输入的带有空间坐标系的文件', widget='FileChooser')
    group.add_argument('out_shp_path', help='输出路径', widget='DirChooser')
    group.add_argument('out_epsg', help='目标空间坐标系的epsg标记')
    args = parser.parse_args()
    # print(args.out_epsg)



    # begin_tick = time.time()

    tmp = gpd.GeoDataFrame.from_file(args.in_shp_path)
    # print(tmp.crs)
    tmp_proj = tmp.to_crs({'init': 'epsg:4326'})
    tmp_proj.to_file(args.out_shp_path, encoding='utf-8')
    
    # print('elapse {} '.format(time.time() - begin_tick))



if __name__ == '__main__':
    proj_shp_file()
