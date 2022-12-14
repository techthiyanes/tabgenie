#!/usr/bin/env python3
import logging
import os
import json

from .processing import Processor, Pipeline
from .linearize import LinearizeProcessor

from tinyhtml import h
import requests

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

class ModelAPIPipeline(Pipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processors = [LinearizeProcessor(), ModelAPIProcessor(model_url=self.cfg["model_url"])]

    def to_key(self, content):
        cells = content.get("cells", None)

        if cells:
            cells = str(set(cells))

        key = (content["dataset"], content["split"], content["table_idx"], cells)
        return key


class ModelAPIProcessor(Processor):
    
    def __init__(self, model_url):
        super().__init__()
        self.model_url = model_url

    def process(self, content):
        data = {
            "input_text" : content,
            "beam_size" : 3
        }
        res = requests.post(self.model_url.rstrip("/") + "/generate/", json=data)

        if res.ok:
            out = json.loads(res.text)["out"]

            lis = [h("li")(o) for o in out]
            ul = h("ul")(lis)

            return self.html_render(ul)

        return ""
