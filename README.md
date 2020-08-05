## Image Blurring API with Darkflow

* Darkflow https://github.com/thtrieu/darkflow
* Opencv for Python
* Fastapi for Python https://fastapi.tiangolo.com/
* tiny-yolo https://pjreddie.com/darknet/yolo/

### How to setup
1. Run `pip3 install -r requirements.txt`
2. `python3 setup.py build_ext --inplace`
3. Make `/api` directory
4. Run `uvicorn main:app --reload`

### Outline
* FastAPI based Web API which outfocuses the given picture.
* Yolo detects the objects from the picture and determines the prominent one.
* Blur out the rest of the picture using OpenCV.

### Getting better...
#### 26/07/20
* Using `yolo.cfg`, `yolo.weights`. Takes 40 seconds from sending HTTP request to getting response. Both initialising and predicting consume huge amount of time. Light-weighted model or none-initialised server would probably help.

#### 27/07/20
* Using `yolov2-tiny-voc.cfg`, `yolov2-tiny-voc.weights`. Takes 9.21seconds.

#### 05/08/20
* Wrote Requirements.txt file