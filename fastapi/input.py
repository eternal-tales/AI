import shutil
from google.colab import files
import time
from PIL import Image
from tqdm import tqdm
import ipywidgets as widgets
from io import BytesIO
import wget

with capture.capture_output() as cap:
  %cd /content
  if not os.path.exists("/content/smart_crop.py"):
    wget.download('https://raw.githubusercontent.com/TheLastBen/fast-stable-diffusion/main/Dreambooth/smart_crop.py')
  from smart_crop import *

#@markdown #Instance Images
#@markdown ----

#@markdown
#@markdown - Run the cell to upload the instance pictures.
#@markdown - You can add `external captions` in txt files by simply giving each txt file the same name as the instance image, for example dikgur (1).jpg and dikgur (1).txt, and upload them here, to use the external captions, check the box "external_captions" in the training cell. `All the images must have one same extension` jpg or png or....etc

Remove_existing_instance_images= True #@param{type: 'boolean'}
#@markdown - Uncheck the box to keep the existing instance images.

if Remove_existing_instance_images:
  if os.path.exists(str(INSTANCE_DIR)):
    !rm -r "$INSTANCE_DIR"
  if os.path.exists(str(CAPTIONS_DIR)):
    !rm -r "$CAPTIONS_DIR"

if not os.path.exists(str(INSTANCE_DIR)):
  %mkdir -p "$INSTANCE_DIR"
if not os.path.exists(str(CAPTIONS_DIR)):
  %mkdir -p "$CAPTIONS_DIR"

if os.path.exists(INSTANCE_DIR+"/.ipynb_checkpoints"):
  %rm -r $INSTANCE_DIR"/.ipynb_checkpoints"


IMAGES_FOLDER_OPTIONAL="" #@param{type: 'string'}

#@markdown - If you prefer to specify directly the folder of the pictures instead of uploading, this will add the pictures to the existing (if any) instance images. Leave EMPTY to upload.

Smart_Crop_images= True #@param{type: 'boolean'}
Crop_size = 512 #@param ["512", "576", "640", "704", "768", "832", "896", "960", "1024"] {type:"raw"}

#@markdown - Smart crop the images without manual intervention.

while IMAGES_FOLDER_OPTIONAL !="" and not os.path.exists(str(IMAGES_FOLDER_OPTIONAL)):
  print('[1;31mThe image folder specified does not exist, use the colab file explorer to copy the path :')
  IMAGES_FOLDER_OPTIONAL=input('')

if IMAGES_FOLDER_OPTIONAL!="":
  if os.path.exists(IMAGES_FOLDER_OPTIONAL+"/.ipynb_checkpoints"):
    %rm -r "$IMAGES_FOLDER_OPTIONAL""/.ipynb_checkpoints"

  with capture.capture_output() as cap:
    !mv $IMAGES_FOLDER_OPTIONAL/*.txt $CAPTIONS_DIR
  if Smart_Crop_images:
    for filename in tqdm(os.listdir(IMAGES_FOLDER_OPTIONAL), bar_format='  |{bar:15}| {n_fmt}/{total_fmt} Uploaded'):
      extension = filename.split(".")[-1]
      identifier=filename.split(".")[0]
      new_path_with_file = os.path.join(INSTANCE_DIR, filename)
      file = Image.open(IMAGES_FOLDER_OPTIONAL+"/"+filename)
      width, height = file.size
      if file.size !=(Crop_size, Crop_size):
        image=crop_image(file, Crop_size)
        if extension.upper()=="JPG" or extension.upper()=="jpg":
            image[0] = image[0].convert("RGB")
            image[0].save(new_path_with_file, format="JPEG", quality = 100)
        else:
            image[0].save(new_path_with_file, format=extension.upper())
      else:
        !cp "$IMAGES_FOLDER_OPTIONAL/$filename" "$INSTANCE_DIR"

  else:
    for filename in tqdm(os.listdir(IMAGES_FOLDER_OPTIONAL), bar_format='  |{bar:15}| {n_fmt}/{total_fmt} Uploaded'):
      %cp -r "$IMAGES_FOLDER_OPTIONAL/$filename" "$INSTANCE_DIR"

  print('\n[1;32mDone, proceed to the next cell')


elif IMAGES_FOLDER_OPTIONAL =="":
  up=""
  uploaded = files.upload()
  for filename in uploaded.keys():
    if filename.split(".")[-1]=="txt":
      shutil.move(filename, CAPTIONS_DIR)
    up=[filename for filename in uploaded.keys() if filename.split(".")[-1]!="txt"]
  if Smart_Crop_images:
    for filename in tqdm(up, bar_format='  |{bar:15}| {n_fmt}/{total_fmt} Uploaded'):
      shutil.move(filename, INSTANCE_DIR)
      extension = filename.split(".")[-1]
      identifier=filename.split(".")[0]
      new_path_with_file = os.path.join(INSTANCE_DIR, filename)
      file = Image.open(new_path_with_file)
      width, height = file.size
      if file.size !=(Crop_size, Crop_size):
        image=crop_image(file, Crop_size)
        if extension.upper()=="JPG" or extension.upper()=="jpg":
            image[0] = image[0].convert("RGB")
            image[0].save(new_path_with_file, format="JPEG", quality = 100)
        else:
            image[0].save(new_path_with_file, format=extension.upper())
      clear_output()
  else:
    for filename in tqdm(uploaded.keys(), bar_format='  |{bar:15}| {n_fmt}/{total_fmt} Uploaded'):
      shutil.move(filename, INSTANCE_DIR)
      clear_output()
  print('\n[1;32mDone, proceed to the next cell')

with capture.capture_output() as cap:
  %cd "$INSTANCE_DIR"
  !find . -name "* *" -type f | rename 's/ /-/g'
  %cd "$CAPTIONS_DIR"
  !find . -name "* *" -type f | rename 's/ /-/g'

  %cd $SESSION_DIR
  !rm instance_images.zip captions.zip
  !zip -r instance_images instance_images
  !zip -r captions captions
  %cd /content