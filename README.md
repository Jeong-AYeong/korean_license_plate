# korean_license_plate
차량 번호판(한글)을 텍스트로 변환

## 💻 프로젝트 소개
영상에서 차량 번호판을 detect하고 ocr을 이용해 텍스트로 변환하는 프로젝트입니다.
<br>

### 🔗 개발 환경
- 'tensorflow-gpu == 2.5.0'
- 'opencv-python'
- lxml
- tqdm
- absl-py
- matplotlib
- easydict
- pillow

### 실행방법
'''
python detectvideo.py --framework tflite --weights ./checkpoints/yolov4-416.tflite --video [VIDEO_PATH] --lpr
'''
[VIDEO_PATH]에는 차량 번호판을 식별하려는 영상의 위치와 영상의 이름을 작성하시면 됩니다.
