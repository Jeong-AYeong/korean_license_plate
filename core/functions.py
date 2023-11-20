import os
import cv2
import random
import numpy as np
import tensorflow as tf

from core.utils import read_class_names
from core.config import cfg
from time import time

from ocr.model import LPRNet
from ocr.loader import resize_and_normailze



# function for cropping each detection and saving as new image
def crop_objects(img, data, path, allowed_classes):
    boxes, scores, classes, num_objects = data
    num_objects = int(num_objects)
    class_names = read_class_names(cfg.YOLO.CLASSES)
    #create dictionary to hold count of objects for image name
    jdict = [{"location": f"A{i+1}", "inOut": "out"} for i in range(3)]
    counts = dict()
    idx = 0
    num_objects = min(num_objects, len(classes))
    for i in range(num_objects):
        if isinstance(classes[i], np.ndarray) and len(classes[i]) > 0:
            class_index = int(classes[i][0])
        else:
            class_index = int(classes[i])

            # 클래스 인덱스를 사용하여 클래스 이름 추출
        if class_index in class_names:
            class_name = class_names[class_index]
        else:
            print(f"Unrecognized class index: {class_index}")
            continue

        if class_name in allowed_classes:
            counts[class_name] = counts.get(class_name, 0) + 1
            if len(boxes[i]) == 4:  # boxes[i]가 4개의 요소를 가질 경우
                xmin, ymin, xmax, ymax = boxes[i]
            else:  # 다른 형태의 경우, 적절한 인덱싱 사용
                box = boxes[i][0]
                # print(boxes)
                xmin, ymin, xmax, ymax = box[0], box[1], box[2], box[3]

            if xmin == 0 or xmax == 0:
                print("No valid bounding box found for object", i)
                continue  # 다음 객체로 넘어감

            # 유효한 경우, loc 함수 호출
            location = loc(img, xmin, xmax)
            ymin, ymax, xmin, xmax = int(ymin), int(ymax), int(xmin), int(xmax)
            # cropped_img = img[ymin:ymax, xmin:xmax]
            cropped_img = img[xmin:xmax, ymin:ymax]
            # construct image name and join it to path for saving crop properly
            img_name = class_name + '_' + str(location[-1]) + '.jpg'
            img_path = os.path.join(path, img_name)
            # save image
            if cropped_img.size == 0:
                print("Cropped image is empty:", img_name)
                continue
            cv2.imwrite(img_path, cropped_img)
            carNum, prob = OCR(img_path)
            count = {"location": location, "inOut": "in", "carNum" : carNum[0], "disabled" : 0, "credit": prob}
            jdict[int(location[-1])-1] = count
        else:
            continue
        
        
        
    return jdict
        
classnames = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "가", "나", "다", "라", "마", "거", "너", "더", "러",
              "머", "버", "서", "어", "저", "고", "노", "도", "로",
              "모", "보", "소", "오", "조", "구", "누", "두", "루",
              "무", "부", "수", "우", "주", "허", "하", "호"
              ]

def OCR(img):
    # t = time()
    args = {'image' : img, 'weights' : './ocr/weights_best.pb'}

    #tf.compat.v1.enable_eager_execution()
    net = LPRNet(len(classnames) + 1)
    net.load_weights(args["weights"])

    img = cv2.imread(args["image"])
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    x = np.expand_dims(resize_and_normailze(img), axis=0)
    
    carNum, score = net.predict(x, classnames)

    cv2.destroyAllWindows()

    file_path = "./CarNum_list.txt"

    # 파일에서 현재 데이터 읽기
    with open(file_path, 'r') as file:
        existing_data = file.read().splitlines()

    # 새로운 데이터 중 중복되지 않은 것만 찾기
    new_data = [num for num in carNum if num not in existing_data]

    with open(file_path, 'a') as file:
        file.write('\n'.join(new_data))
        file.write("\n")
    return carNum, float(score)

def loc(image, xmin, xmax):
    image_h, image_w, _ = image.shape
    xmin = xmin/image_w
    xmax = xmax/image_w

    center = (xmin + xmax) / 2.0

    if center > 0 and center < 0.33:
        loc = "A1"
    elif center>=0.33 and center< 0.66:
        loc = "A2"
    else:
        loc = "A3"
    return loc

