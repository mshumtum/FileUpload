import os
import cv2
import numpy as np
from PIL import Image
import shortuuid



def generate_edges(path, _filename,rgb_code=(254,1,154),threshold1=120, threshold2=450):
    def overlap_and_shift_edges(background_image, foreground_image,shift=(-250,0)):
        background = Image.open(background_image)
        foreground = Image.open(foreground_image)
        background.paste(foreground, shift, foreground)
        output_file = output_filename
        output_file = os.path.join(path, output_file)
        background.save(output_file)
        return output_filename

    filename = os.path.join(path, _filename)
    filename = str(filename)
    image = cv2.imread(filename)
    output_filename = shortuuid.uuid()+'.png'
    # convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # perform the canny edge detector to detect image edges
    edges = cv2.Canny(gray, threshold1=threshold1, threshold2=threshold2)
    gray = cv2.cvtColor(edges,cv2.COLOR_BGR2RGB)
    # plt.imshow(edges, cmap="gray")
    cv2.imwrite(output_filename, edges)
    
    #changing color of edges
    im = cv2.imread(output_filename, 0)
    im2 = cv2.imread(output_filename)
    edges2 = cv2.Canny(im,120,250)
    rgb = cv2.cvtColor(edges2, cv2.COLOR_GRAY2RGB)
    rgb *= np.array(rgb_code,np.uint8)

    out = np.bitwise_or(im2, rgb)
    # implot = plt.imshow(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    cv2.imwrite(output_filename, out)

    #removing black background
    src = cv2.imread(output_filename, 1)
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
    b, g, r = cv2.split(src)
    rgba = [b,g,r, alpha]
    dst = cv2.merge(rgba,4)
    cv2.imwrite(output_filename, dst)
    processed_file = overlap_and_shift_edges(filename, output_filename,shift=(-200,0))
    os.remove(output_filename)
    return processed_file
    