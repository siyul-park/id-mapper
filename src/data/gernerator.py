import os
from pathlib import Path

from tqdm import tqdm

from src.data.dataset import COCODataset
from src.data.utils import get_data_size


class BoundingBoxImageGenerator:
    def __init__(
            self,
            coco_dataset: COCODataset,
            path: str or Path,
            format: str
    ):
        path = Path(path)

        self.__coco_dataset = coco_dataset
        self.__path = path.joinpath(coco_dataset.dataset)
        self.__format = format

    def generate(self, force: bool = False):
        if os.path.exists(self.__path) and force:
            os.remove(self.__path)

        self.__path.mkdir(parents=True, exist_ok=True)

        existed_data_size = get_data_size(self.__path)
        current_data_index = 0

        print(f'Generate bounding box images from {self.__coco_dataset.data_path} to {self.__path}')
        for image, annotations in tqdm(self.__coco_dataset):
            boxes = annotations[:, :4]
            for box in boxes:
                current_data_index += 1

                if current_data_index <= existed_data_size:
                    continue

                image_dir = self.__path.joinpath(str(current_data_index - 1))
                image_dir.mkdir(parents=True)

                instance_image = image.crop(box)
                instance_image.save(image_dir.joinpath(f'0.{self.__format}'))



