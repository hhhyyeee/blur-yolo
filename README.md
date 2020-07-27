## Image Blurring API with Darkflow

* Darkflow https://github.com/thtrieu/darkflow
* Opencv for Python

### How to setup
1. Make /api/images directory
2. pip install .
3. Run `uvicorn main:app --reload`

### Outline
* FastAPI based Web API which outfocuses the given picture.
* Yolo detects the objects from the picture and determines the prominent one.
* Blur out the rest of the picture using OpenCV.

### Getting better...
#### 26/07/20
* Using `yolo.cfg`, `yolo.weights`. Takes 40 seconds from sending HTTP request to getting response. Both initialising and predicting consume huge amount of time. Light-weighted model or none-initialised server would probably help.

#### 27/07/20
* Using `yolov2-tiny-voc.cfg`, `yolov2-tiny-voc.weights`. Takes 9.21seconds.