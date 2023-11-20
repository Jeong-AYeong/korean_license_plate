# korean_license_plate
차량 번호판(한글)을 텍스트로 변환

  
## 💻 프로젝트 소개
영상에서 차량 번호판을 detect하고 ocr을 이용해 텍스트로 변환하는 프로젝트입니다.
<br>

  
## 🔧개발 환경
- 'tensorflow-gpu == 2.5.0'
- 'opencv-python'
- lxml
- tqdm
- absl-py
- matplotlib
- easydict
- pillow

   
  
## 🔗실행방법
```
python detectvideo.py --framework tflite --weights ./checkpoints/yolov4-416.tflite --video [VIDEO_PATH] --lpr
```
[VIDEO_PATH]에는 차량 번호판을 식별하려는 영상의 위치와 영상의 이름을 작성하시면 됩니다.


      

## 실행결과
![image](https://github.com/Jeong-AYeong/korean_license_plate/assets/87751593/81d799c3-f367-49c5-87be-5318a0d2aa8d)   
korea_license_plate/detections/crop 디렉토리에 각 영상별 폴더가 생성됩니다.     

![image](https://github.com/Jeong-AYeong/korean_license_plate/assets/87751593/d5a32560-6b8d-4a26-9e0a-015f2ebd52a2)   
디렉토리 별로 crop된 번호판의 이미지를 확인할 수 있습니다.   
  
![image](https://github.com/Jeong-AYeong/korean_license_plate/assets/87751593/03d76d91-9da5-469c-bd19-778da7f6b344)    
CarNum_List.txt파일에 인식된 번호판이 저장됩니다.    

## Demo 영상
