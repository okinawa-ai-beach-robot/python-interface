import os
import yaml
import random

from beachbot.config import config, logger


class Dataset:
    def __init__(self, datasetpath=None, subtype="train") -> None:
        self.classes = []
        self.images = []
        self.rects = []
        if datasetpath is not None:
            # load files
            with open(datasetpath + os.path.sep + "data.yaml", "r") as stream:
                data_cfg = yaml.safe_load(stream)
                num_classes = str(data_cfg["nc"])
                self.classes = data_cfg["names"]
                logger.info(
                    "Dataset defines "
                    + str(num_classes)
                    + " classes -> "
                    + str(self.classes)
                )
                assert (
                    len(self.classes) != num_classes
                ), "Error: Dataset inconsistent, number of classes does not match number of labels"
                self.images, self.rects = Dataset._load_img_list(
                    datasetpath + os.path.sep + subtype
                )

    def random_prune(self, num_samples):
        sel = list(range(len(self.images)))
        random.shuffle(sel)
        sel = sel[:num_samples]
        ndata = Dataset()
        ndata.classes = self.classes
        ndata.images = [self.images[i] for i in sel]
        ndata.rects = [self.rects[i] for i in sel]
        return ndata

    def list_dataset_paths():
        base_path = get_dataset_path()
        datasetfolders = [f.path for f in os.scandir(base_path) if f.is_dir()]
        return datasetfolders

    def _load_img_list(path):
        # Expect subfolder labels and images
        imgs = [
            f.path for f in os.scandir(path + os.path.sep + "images") if f.is_file()
        ]
        label_files = [
            (os.path.sep + "labels" + os.path.sep)
            .join(imgp.rsplit((os.path.sep + "images" + os.path.sep), 1))
            .replace(".jpg", ".txt")
            for imgp in imgs
        ]

        annotations = []
        for lf, imgf in zip(label_files, imgs):
            with open(lf) as fc:
                lines = [line.rstrip() for line in fc]
                meta = []
                for line in lines:
                    content = [float(value) for value in line.split(" ")]
                    if len(content) == 5:
                        # Convert from YOLO format to our format:
                        # [classid, rect_x_top_left, rect_y_top_left, rect_width, rect_height]
                        content[0] = int(content[0])
                        x = content[1] - content[3] / 2
                        y = content[2] - content[4] / 2
                        meta.append(
                            {
                                "classid": content[0],
                                "rect": [x, y, content[3], content[4]],
                            }
                        )
                annotations.append(meta)
        return imgs, annotations
