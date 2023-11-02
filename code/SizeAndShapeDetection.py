from scipy.spatial.distance import euclidean
from imutils import perspective
from imutils import contours
from remove_bg_api import RemoveBg
import numpy as np
import imutils
import cv2
import datetime
import os
import numpy as np

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct
def show_images(images):
        # Function to show array of images (intermediate results)
        for i, img in enumerate(images):
                cv2.imshow("image_" + str(i), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # Initialize api wrapper
def save_images(images):
        image_dict = Convert(images)
        for key in image_dict:
                filename = key+'.jpg'
                cv2.imwrite(filename, image_dict[key])
                
def mainfunction(fileDict):
        ct = datetime.datetime.now
        output_path_folder = os.path.join(fileDict['outputPath'], datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.mkdir(output_path_folder)
        output_path = output_path_folder + '/background.png'
        removebg = RemoveBg('EPDWBX9XqQjYAV24cNx3ZnSV')  
        # Send and save the finished image
        image = removebg.remove_bg_file(input_path= fileDict['inputPath'], out_path= output_path, size="preview", raw=False)  
        # Print path
        print("Image was saved along the path: {}".format(image))
        os.chdir(output_path_folder) 
        img_path = output_path
        
        # Read image and preprocess
        originalImage = cv2.imread(fileDict['inputPath'])
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        edged1 = cv2.Canny(blur, 50, 100)
        edged2 = cv2.dilate(edged1, None, iterations=1)
        edged3 = cv2.erode(edged2, None, iterations=1)
        
        # Find contours
        cnts = cv2.findContours(edged3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        #cv2.imshow("Contours",cnts)
        # Sort contours from left to right as leftmost contour is reference object
        (cnts, _) = contours.sort_contours(cnts)

        # Remove contours which are not large enough
        cnts = [x for x in cnts if cv2.contourArea(x) > 100]

        #cv2.drawContours(image, cnts, -1, (0,255,0), 3)

        #show_images([image, edged])
        #print(len(cnts))

        # Reference object dimensions
        # Here for reference I have used a 2cm x 2cm square
        '''ref_object = cnts[0]
        box = cv2.minAreaRect(ref_object)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        dist_in_pixel = euclidean(tl, tr)
        dist_in_cm = 2'''
        pixel_per_cm = fileDict['pixelPerCM']
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Draw remaining contours
        for cnt in cnts:
                box = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                box = perspective.order_points(box)
                (tl, tr, br, bl) = box
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
                mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0])/2), tl[1] + int(abs(tr[1] - tl[1])/2))
                mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0])/2), tr[1] + int(abs(tr[1] - br[1])/2))
                wid = euclidean(tl, tr)/pixel_per_cm
                ht = euclidean(tr, br)/pixel_per_cm
                approx = cv2.approxPolyDP(cnt,  0.009 * cv2.arcLength(cnt, True), True)
                if(len(approx) == 4):               
                        if w == h:   
                                cv2.putText(image, "{:.1f}cm".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                                cv2.putText(image, "Square", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                        else:
                                cv2.putText(image, "{:.1f}cm".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                                cv2.putText(image, "{:.1f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                                cv2.putText(image, "Rectangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)    
                if(len(approx) >= 10):  
                        cv2.putText(image, "{:.1f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                        cv2.putText(image, "Circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                    
                if(len(approx) == 3):
                        cv2.putText(image, "{:.1f}cm".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                        cv2.putText(image, "{:.1f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                        cv2.putText(image, "Triangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                if(len(approx) == 5):
                        cv2.putText(image, "{:.1f}cm".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                        cv2.putText(image, "{:.1f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                        cv2.putText(image, "Pentagon", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        show_images([image, gray, blur, edged1, edged2, edged3])
        save_images(['originalImage',originalImage, 'image', image, 'gray', gray, 'blur', blur, 'edged1', edged1, 'edged2', edged2, 'edged3', edged3])
