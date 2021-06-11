from PIL import Image
from stegano import lsb
from stegano import lsb
from os.path import isfile,join
import time                                                                 #install time ,opencv,numpy modules
import cv2
import numpy as np
import math
import os
import shutil
from subprocess import call,STDOUT

def frame_extraction(video):
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
    temp_folder="./tmp"
    print("[INFO] tmp directory is created")

    vidcap = cv2.VideoCapture(video)
    count = 0

    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1

    return count

def split_image(input_image, frame_count):
    image = []
    new_image = Image.new(input_image.mode, input_image.size)
    #pixels_new = new_image.load()
    for i in range(0, frame_count):
        image.append(new_image)
    return image

def encode_video(input_image, frame_count,root="./tmp/"):
    split_image_list=split_image(Image.open(input_image), frame_count)
    for i in range(0,len(split_image_list)):
        f_name="{}{}.png".format(root,i)
        secret_enc=merge(Image.open(f_name),split_image_list[i])
        secret_enc.save(f_name)
        print("[INFO] frame {} holds {}".format(f_name,split_image_list[i]))

def int_to_bin(rgb):

    r, g, b = rgb
    return ('{0:08b}'.format(r),
            '{0:08b}'.format(g),
            '{0:08b}'.format(b))

def bin_to_int(rgb):

    r, g, b = rgb
    return (int(r, 2),
            int(g, 2),
            int(b, 2))

def merge_rgb(rgb1, rgb2):

    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    rgb = (r1[:4] + r2[:4],
           g1[:4] + g2[:4],
            b1[:4] + b2[:4])
    return rgb

def merge(img1, img2):

    # Check the images dimensions
    if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
        raise ValueError('Image 2 should not be larger than Image 1!')

    # Get the pixel map of the two images
    pixel_map1 = img1.load()
    pixel_map2 = img2.load()

    # Create a new image that will be outputted
    new_image = Image.new(img1.mode, img1.size)
    pixels_new = new_image.load()

    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            rgb1 = int_to_bin(pixel_map1[i, j])

            # Use a black pixel as default
            rgb2 = int_to_bin((0, 0, 0))

            # Check if the pixel map position is valid for the second image
            if i < img2.size[0] and j < img2.size[1]:
                rgb2 = int_to_bin(pixel_map2[i, j])

            # Merge the two pixels and convert it to a integer tuple
            rgb = merge_rgb(rgb1, rgb2)

            pixels_new[i, j] = bin_to_int(rgb)

    return new_image

    video = "video_input.mov"
    temp_folder = "./tmp/"
    image = "./5.jpg"
    frame_count = frame_extraction(video)
    call(["ffmpeg", "-i",video , "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    encode_video(image, frame_count)
    call(["ffmpeg", "-i", "tmp/%d.png" , "-vcodec", "png", "tmp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    #clean_tmp()

