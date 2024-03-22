from typing import Union, List, Tuple

import torch

from batchgenerators_torch.transforms.base.basic_transform import SegOnlyTransform


class ConvertSegmentationToRegionsTransform(SegOnlyTransform):
    def __init__(self, regions: Union[List, Tuple], channel_in_seg: int = 0):
        super().__init__()
        self.regions = regions
        self.channel_in_seg = channel_in_seg

    def get_parameters(self, **data_dict) -> dict:
        return {}

    def _apply_to_segmentation(self, segmentation: torch.Tensor, **params) -> torch.Tensor:
        num_regions = len(self.regions)
        region_output = torch.zeros((num_regions, *segmentation.shape[1:]), dtype=segmentation.dtype, device=segmentation.device)
        for region_id, region_source_labels in enumerate(self.regions):
            if not isinstance(region_source_labels, (list, tuple)):
                region_source_labels = (region_source_labels, )
            for label_value in region_source_labels:
                region_output[region_id][segmentation[self.channel_in_seg] == label_value] = 1
        return region_output