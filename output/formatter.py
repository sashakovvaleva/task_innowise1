import json
import xml.etree.ElementTree as ET
from decimal import Decimal

class Formatter:
    def __init__(self, output_format):
        self.output_format = output_format

    def export(self, data):
        if self.output_format == 'json':
            self._export_json(data)
        elif self.output_format == 'xml':
            self._export_xml(data)

    def _export_json(self, data):
        def custom_serializer(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            
        with open('output/output.json', 'w') as json_file:
            json.dump(data, json_file, indent=4, default=custom_serializer)

    def _export_xml(self, data):
        root = ET.Element("Results")
        
        for key, value in data.items():
            group = ET.SubElement(root, key)
            
            for item in value:
                grou = ET.SubElement(root, key )
                
                if isinstance(item, (tuple, list)):
                    for idx, v in enumerate(item):
                        child = ET.SubElement(group, f"Field{idx + 1}") 
                        child.text = str(v) if v is not None else ""

        tree = ET.ElementTree(root)
        tree.write("output/output.xml", encoding="utf-8", xml_declaration=True)

       
    