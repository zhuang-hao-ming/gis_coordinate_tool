# -*- coding: utf-8 -*-
import fiona



from transform import Transform
from gooey import Gooey
from gooey import GooeyParser


def recur_map(f, data):
    """递归处理所有坐标
    
    Arguments:
        f {function} -- [apply function]
        data {collection} -- [fiona collection]
    """

    return[ not type(x) is list and f(x) or recur_map(f, x) for x in data ]


@Gooey()
def convertor():
    """convert input china coordinate to another. 
\b
    Arguments:  
        convert_type {string} -- [coordinate convert type, e.g. wgs2bd]   
\b
            wgs2gcj : convert WGS-84 to GCJ-02
            wgs2bd  : convert WGS-84 to DB-09  
            gcj2wgs : convert GCJ-02 to WGS-84  
            gcj2bd  : convert GCJ-02 to BD-09  
            bd2wgs  : convert BD-09 to WGS-84  
            bd2gcj  : convert BD-09 to GCJ-02 
        src_path {string} -- [source file path]  
        dst_path {string} -- [destination file path]  
    Example:
\b 
        coord_covert wgs2gcj ./test/data/line/multi-polygon.shp ~/temp/qqqq.shp 
    """ 

    parser = GooeyParser(description='火星坐标系转换')
    file_group = parser.add_argument_group('文件设定',gooey_options={'show_border': False})
    file_group.add_argument('src_path', help='输入文件', widget='FileChooser')
    file_group.add_argument('dst_path', help='输出路径', widget='DirChooser')

    coord_group = parser.add_argument_group('坐标系设定： gcj(高德，天地图), bd(百度), wgs(wgs84)',gooey_options={'show_border': False})
    coord_group.add_argument('input_crs_type', help='输入坐标系', choices=['wgs', 'gcj', 'bd'])
    coord_group.add_argument('output_crs_type', help='输出坐标系', choices=['wgs', 'gcj', 'bd'])
    
    args = parser.parse_args()

    src_path = args.src_path
    dst_path = args.dst_path
    input_crs_type = args.input_crs_type
    output_crs_type = args.output_crs_type

    if input_crs_type == output_crs_type:
        print('输入和输出坐标系一致')
        return

    convert_type = '{}2{}'.format(input_crs_type, output_crs_type)

    print(convert_type)

    with fiona.open(src_path, 'r', encoding='utf-8') as source:
        source_schema = source.schema.copy()
        with fiona.open(dst_path, 'w', encoding='utf-8', **source.meta) as out:
            transform = Transform()
            f = lambda x: getattr(transform, convert_type)(x[0], x[1])  #dynamic call convert func

            for fea in source:
                collections = fea['geometry']['coordinates']
                if type(collections) is tuple:
                    fea['geometry']['coordinates'] = f(collections)
                elif type(collections) is list:
                    fea['geometry']['coordinates'] = recur_map(f, collections)
                else:
                    raise TypeError("collection must be list or tuple")
                out.write(fea)

if __name__ == '__main__':
    convertor()