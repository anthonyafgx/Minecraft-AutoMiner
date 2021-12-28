import json
from PIL import ImageGrab
import time

# Handles all the information from the screen.

class Screen:
    def __init__(self, json_path = "screen.json"):
        # bounding boxes [x1, y1, x2, y2]
        self.targeted_block_bbox = []
        self.position_bbox = []
        self.facing_bbox = []

        # json path
        self.json_path = json_path

        # load data from json
        self.ReadJSON()

    def ReadJSON(self):
        file = open(self.json_path)
        data = json.load(file)

        self.targeted_block_bbox = data["targeted-block"]
        self.position_bbox = data["position"]
        self.facing_bbox = data["facing"]
        
        file.close()
    
    def SetTargetedBlockBbox(self, x1, y1, x2, y2):
        # set bbox
        self.targeted_block_bbox = [x1, y1, x2, y2]

        # open json file and convert to dict
        file = open(self.json_path)
        data = json.load(file)
        file.close()

        data["targeted-block"] = self.targeted_block_bbox

        # write to json new modified dict
        with open(self.json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def SetPositionBbox(self, x1, y1, x2, y2):
        # set bbox
        self.position_bbox = [x1, y1, x2, y2]

        # open json file and convert to dict
        file = open(self.json_path)
        data = json.load(file)
        file.close()

        data["position"] = self.position_bbox

        # write to json new modified dict
        with open(self.json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def SetFacingBbox(self, x1, y1, x2, y2):
        # set bbox
        self.position_bbox = [x1, y1, x2, y2]

        # open json file and convert to dict
        file = open(self.json_path)
        data = json.load(file)
        file.close()

        data["facing"] = self.position_bbox

        # write to json new modified dict
        with open(self.json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    # Shows Targeted Block Screenshot
    def _ShowTargetedBlock(self):
        img = ImageGrab.grab(bbox = self.targeted_block_bbox)
        img.show()

    # Shows Position Screenshot
    def _ShowPosition(self):
        img = ImageGrab.grab(bbox = self.position_bbox)
        img.show()

    # Shows "Facing" Screenshot
    def _ShowFacing(self):
        img = ImageGrab.grab(bbox = self.facing_bbox)
        img.show()

if __name__ == "__main__":
    screen = Screen()
    time.sleep(2)
    screen._ShowTargetedBlock()