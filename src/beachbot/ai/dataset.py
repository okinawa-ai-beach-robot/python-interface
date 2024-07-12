import os
import yaml

from .. import get_dataset_path, logger


class Dataset():
    def __init__(self, datasetpath=None, subtype="train") -> None:
        self.classes=[]
        self.images=[]
        self.rects=[]
        if datasetpath is not None:
            # load files
            with open(datasetpath + os.path.sep + "data.yaml", 'r') as stream:
                data_cfg = yaml.safe_load(stream)
                num_classes = str(data_cfg['nc'])
                self.classes = data_cfg['names']
                logger.info("Dataset defines " + str(num_classes) + " classes -> " +  str(self.classes))
                assert len(self.classes)!=num_classes, "Error: Dataset inconsistent, number of classes does not match number of labels"
                self.images, self.rects = Dataset._load_img_list(datasetpath + os.path.sep + subtype)

    def list_dataset_paths():
        base_path=get_dataset_path()
        datasetfolders = [ f.path for f in os.scandir(base_path) if f.is_dir() ]
        return datasetfolders
  

    def _load_img_list(path):
        # Expect subfolder labels and images
        imgs = [ f.path for f in os.scandir(path + os.path.sep + "images") if f.is_file() ]
        label_files = [(os.path.sep+"labels"+os.path.sep).join(imgp.rsplit((os.path.sep+"images"+os.path.sep), 1)).replace(".jpg",".txt") for imgp in imgs]

        annotations=[]
        for lf, imgf in zip(label_files, imgs):
            with open(lf) as fc:
                lines = [line.rstrip() for line in fc]
                meta=[]
                for line in lines:
                    content = [float(value) for value in line.split(' ')]
                    if len(content)==5:
                    # classid, rect_x, rect_y rect_x2, rect_y2
                        content[0] = int(content[0])
                        meta.append({"classid": content[0], "rect:":[content[1],content[2],content[3],content[4]]})
                annotations.append(meta)
        return imgs, annotations


                









