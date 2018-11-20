'''
Database module

author: 10zinten
'''
from pathlib import Path
import sqlite3
import csv
from xml.dom import minidom


Labels = Path('Labels').resolve()

class LabelDB(object):

    def __init__(self):
        self.conn = sqlite3.connect('label.db')
        print("[ INFO ] database created successfully ... ")
        self.curs = self.conn.cursor()
        self.curs.execute('''CREATE TABLE IF NOT EXISTS Label
                     (image TEXT NOT NULL,
                     box_num INT NULL,
                     x1 INT NOT NULL,
                     y1 INT NOT NULL,
                     x2 INT NOT NULL,
                     y2 INT NOT NULL);''')
        print("[ INFO ] Table created successfully ... ")

    def close(self):
        self.conn.close()

    def insert(self, image_path, box_num, box):
        self.curs.execute("INSERT INTO Label (image, box_num, x1, y1, x2, y2) \
                          VALUES (?,?,?,?,?,?)", [image_path, box_num] + box)

    def gen_csv(self):
        self.curs.execute("SELECT * FROM Label")
        with open(str(Labels/'labels.csv'), 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            for image, box_num, x1, y1, x2, y2 in self.curs.fetchall():
                filewriter.writerow([image, box_num, x1, y1, x2, y2])

    def gen_xml(self):
        self.curs.execute("SELECT * FROM Label")
        root = minidom.Document()

        annotation = root.createElement('annotation')
        root.appendChild(annotation)

        count = 1
        for image_path, box_num, x1, y1, x2, y2 in self.curs.fetchall():
            dataPoint = root.createElement('datapoint')
            dataPoint.setAttribute('id', str(count))
            annotation.appendChild(dataPoint)

            child = root.createElement('path')
            child.appendChild(root.createTextNode(image_path))
            dataPoint.appendChild(child)

            child = root.createElement('x1')
            child.appendChild(root.createTextNode(str(x1)))
            dataPoint.appendChild(child)

            child = root.createElement('y1')
            child.appendChild(root.createTextNode(str(y1)))
            dataPoint.appendChild(child)

            child = root.createElement('x2')
            child.appendChild(root.createTextNode(str(x2)))
            dataPoint.appendChild(child)

            child = root.createElement('y2')
            child.appendChild(root.createTextNode(str(y2)))
            dataPoint.appendChild(child)

            count += 1

        xml_str = root.toprettyxml(indent="\t")

        with open(str(Labels/'labels.xml'), 'w') as f:
            f.write(xml_str)


if __name__ == "__main__":
    labeldb = LabelDB()
    labeldb.insert('image-01', 1, 200, 300, 400, 500)
    labeldb.gen_csv()
    labeldb.close()
