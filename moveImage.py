import os
import subprocess

root_path = '/Users/wyw/Documents/9月无人机拍牛/3cattle2/train/labels'
sourceDir = '/Users/wyw/Documents/9月无人机拍牛/extract_images2'
targetDir = '/Users/wyw/Documents/9月无人机拍牛/3cattle2/train/images'
def seize(name):
    print(name, targetDir)
    label = name.replace('.txt', '.jpeg')
    str = "mv " +sourceDir + "/" + label + "  " + targetDir 
    print(str)
    subprocess.call(str, shell = True)

for root, dirs, files in os.walk(root_path):
    for file_name in files:
        seize(file_name)

    