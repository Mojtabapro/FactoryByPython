from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET

class FileHandler(ABC):
    @abstractmethod
    def read(self, file_path):
        pass

    @abstractmethod
    def write(self, file_path, data):
        pass

class JSONFileHandler(FileHandler):
    def read(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def write(self, file_path, data):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print(f"JSON file saved: {file_path}")

class XMLFileHandler(FileHandler):
    def read(self, file_path):
        tree = ET.parse(file_path)
        data =''
        root = tree.getroot()
        for child in root:
            data +=f"{child.tag} : {child.text} \n"
            for subchild in child:
                data +=f"{subchild.tag} : {subchild.text} \n"

        return data

    def write(self, file_path, data):
        tree = ET.ElementTree(data)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
        print(f"XML file saved: {file_path}")


class FileHandlerFactory:
    @staticmethod
    def get_handler(file_type):
        if file_type.lower() == 'json':
            return JSONFileHandler()
        elif file_type.lower() == 'xml':
            return XMLFileHandler()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")


if __name__ == "__main__":
    file_name = input("Plase, inter file name(whitout type): ").strip().lower()
    file_type = input("Enter file type (json/xml): ").strip().lower()
    handler = FileHandlerFactory.get_handler(file_type)

    file_path = f"./files/{file_name}.{file_type}"

    if file_type == "json":
        data = {"name": "Mojtaba", "age": 25}
        handler.write(file_path, data)
    else:
        data = ET.Element("Person")
        ET.SubElement(data, "Name").text = "Mojtaba"
        ET.SubElement(data, "Age").text = "25"
        handler.write(file_path, data)

    read_data = handler.read(file_path)
    print(f"Data read from {file_path}: \n", read_data)
