
"""
把pacal voc格式的xml文件转成coco格式的json文件
convert the format xml of pascal voc to json of coco

xml的使用可参考          
coco json的数据格式可参考 https://zhuanlan.zhihu.com/p/29393415
---------------------------------------------------
pacal voc xml
<annotation>
    <folder>VOC2007</folder>
    <filename>000C7C0E.jpg</filename>
    <size>
        <width>2666</width>
        <height>2000</height>
        <depth>3</depth>
    </size>
    <object>
        <name>bar</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>152</xmin>
            <ymin>876</ymin>
            <xmax>315</xmax>
            <ymax>1036</ymax>
        </bndbox>
    </object>
    <object>
        <name>bar</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>210</xmin>
            <ymin>1036</ymin>
            <xmax>375</xmax>
            <ymax>1182</ymax>
        </bndbox>
    </object>
<annotation>
---------------------------------------------------
coco json
{
    "info": info,
    "licenses": [license],
    "images": [image],
    "annotations": [annotation],
    "categories": [category]
}
image{
    "id": int,
    "width": int,
    "height": int,
    "file_name": str,
    "license": int,
    "flickr_url": str,
    "coco_url": str,
    "date_captured": datetime,
}
annotation{
    "id": int,    
    "image_id": int,
    "category_id": int,
    "segmentation": RLE or [polygon],
    "area": float,
    "bbox": [x,y,width,height],
    "iscrowd": 0 or 1,
}
categories{
    "id": int,
    "name": str,
    "supercategory": str,
}
---------------------------------------------------
"""

import xml.etree.ElementTree as ET
import os
import json


class Xml2Json():
    """
    把pacal voc格式的xml文件转成coco格式的json文件
    """
    def __init__(self):
        self.coco = dict()
        self.coco['images'] = []            #images数组元素的数量等同于划入训练集（或者测试集）的图片的数量
        self.coco['type'] = 'instances'
        self.coco['annotations'] = []       #数组元素的数量等同于训练集（或者测试集）中bounding box的数量
        self.coco['categories'] = []        #数组元素的数量等同于类别的数量

        self.category_set = dict()          #类别的集合（不重复）
        self.image_set = set()              # 图片的集合（不重复）
        self.category_item_id = 0           #每一类一个id
        self.image_id = 20180000000         #每张图片一个id
        self.annotation_id = 0              #每个标注框一个id

    def convert(self, xml_path, json_file):
        """
        xml 转 json
        Args:
            xml_path(str): 读取的xml路径
            json_file(str):保存的json路径
        """
        print("-----------converting-----------")
        for f in os.listdir(xml_path):
            if not f.endswith('.xml'):
                continue
            xml_file = os.path.join(xml_path, f)
            # 解析xml文件
            file_name, image_size, object_list = self._parse_xml(xml_file)
            # 添加图片
            image_id = self._add_image_item(file_name, image_size)
            # 添加类别、annotation
            for o_l in object_list:
                object_name = o_l["name"]
                if object_name not in self.category_set:
                    self._add_category_item(object_name)
                self._add_annotation_item(object_name, image_id, o_l["bndbox"])

        json.dump(self.coco, open(json_file, 'w',encoding='utf-8'))
        print("-----------convert successfully-----------")

    def _add_category_item(self, name):
        """
        添加一个类别
            categories{
                "id": int,
                "name": str,
                "supercategory": str,
            }
        Args:
            name(str): 类名
        return:
            category_item_id
        """
        category_item = dict()
        category_item['supercategory'] = 'none'
        self.category_item_id += 1
        category_item['id'] = self.category_item_id
        category_item['name'] = name
        self.coco['categories'].append(category_item)
        self.category_set[name] = self.category_item_id

    def _add_image_item(self, file_name, size):
        """
        添加一张图片
            image{
                "id": int,
                "width": int,
                "height": int,
                "file_name": str,
            }
        Args:
            file_name(str): 图片名
            size(dict):     图片尺寸
        return:
            image_id
        """
        if file_name is None:
            raise Exception('Could not find filename tag in xml file.')
        if size['width'] is None:
            raise Exception('Could not find width tag in xml file.')
        if size['height'] is None:
            raise Exception('Could not find height tag in xml file.')
        self.image_id += 1
        image_item = dict()
        image_item['id'] = self.image_id
        image_item['file_name'] = file_name
        image_item['width'] = size['width']
        image_item['height'] = size['height']
        self.coco['images'].append(image_item)
        self.image_set.add(file_name)
        return self.image_id

    def _add_annotation_item(self, object_name, image_id, bbox):
        """
        添加一个annotation
            annotation{
                "id": int,
                "image_id": int,
                "category_id": int,
                "segmentation": RLE or [polygon],
                "area": float,
                "bbox": [x,y,width,height],
                "iscrowd": 0 or 1,
            }
        Args:
            object_name(str):   类名
            image_id(int):      图片id
            bbox(dict):         标注框
        """
        bbox_xmin = bbox["xmin"]
        bbox_ymin = bbox["ymin"]
        bbox_xmax = bbox["xmax"]
        bbox_ymax = bbox["ymax"]

        annotation_item = dict()
        annotation_item['segmentation'] = []
        seg = []
        #left_top
        seg.extend([bbox_xmin, bbox_ymin])
        #left_bottom
        seg.extend([bbox_xmin, bbox_ymax])
        #right_bottom
        seg.extend([bbox_xmax, bbox_ymax])
        #right_top
        seg.extend([bbox_xmax, bbox_ymin])

        annotation_item['segmentation'].append(seg)
        annotation_item['area'] = (bbox_xmax - bbox_xmin) * (bbox_ymax - bbox_ymin)
        annotation_item['iscrowd'] = 0
        annotation_item['ignore'] = 0
        annotation_item['image_id'] = image_id
        annotation_item['bbox'] = [bbox_xmin, bbox_ymin, bbox_xmax - bbox_xmin, bbox_ymax - bbox_ymin]
        annotation_item['category_id'] = self.category_set[object_name]
        self.annotation_id += 1
        annotation_item['id'] = self.annotation_id
        self.coco['annotations'].append(annotation_item)

    def _parse_xml(self, xml_file):
        """
        解析xml文件
        Args:
            xml_path: xml 路径
        return:
            file_name image_size bnd_box
        """
        tree = ET.ElementTree(file=xml_file)
        root = tree.getroot()
        if root.tag != "annotation":
            raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))
        file_name = next(tree.iter(tag="filename")).text # 获取文件名
        image_size = dict()
        for size_elem in next(tree.iter(tag="size")): # 获取image size
            if size_elem.tag == "width":
                image_size["width"] = int(size_elem.text)
            elif size_elem.tag == "height":
                image_size["height"] = int(size_elem.text)
            else:
                image_size["depth"] = int(size_elem.text)
        object_list = []
        for elem in tree.iter(tag="object"): # 遍历所有的object
            elem_dict = dict()
            elem_dict["name"] = next(elem.iter(tag="name")).text
            elem_dict["bndbox"] = {}
            for b_b in next(elem.iter(tag="bndbox")): #获取标注框
                elem_dict["bndbox"][b_b.tag] = float(b_b.text)
            object_list.append(elem_dict)

        return file_name, image_size, object_list

x2j = Xml2Json()
x2j.convert("val_xml", "instances_val2017.json")
