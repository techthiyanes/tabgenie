#!/usr/bin/env python3
import logging

from ..processing import Processor


logger = logging.getLogger(__name__)


class ExportProcessor(Processor):
    def __init__(self):
        super().__init__()

    def process(self, content):
        dataset = content["dataset_obj"]
        table = dataset.get_table(
            split=content["split"], table_idx=content["table_idx"], edited_cells=content.get("edited_cells")
        )
        export_html_format = "simple_html_with_props" if content["include_props"] else "simple_html"

        exported = dataset.export_table(
            table, export_format=content["export_format"], export_html_format=export_html_format
        )

        return exported
