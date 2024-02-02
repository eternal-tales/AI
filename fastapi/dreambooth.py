import os
from IPython.display import clear_output
from IPython.utils import capture
from os import listdir
from os.path import isfile
from subprocess import check_output
import wget
import time

#@markdown #Create/Load a Session

try:
  MODEL_NAME
  pass
except:
  MODEL_NAME=""

PT=""

Session_Name = "try01" #@param{type: 'string'}
while Session_Name=="":
  print('[1;31mInput the Session Name:')
  Session_Name=input('')
Session_Name=Session_Name.replace(" ","_")

#@markdown - Enter the session name, it if it exists, it will load it, otherwise it'll create an new session.

Session_Link_optional = "" #@param{type: 'string'}

#@markdown - Import a session from another gdrive, the shared gdrive link must point to the specific session's folder that contains the trained CKPT, remove any intermediary CKPT if any.

WORKSPACE='/content/gdrive/MyDrive/Fast-Dreambooth'

if Session_Link_optional !="":
  print('[1;32mDownloading session...')
  with capture.capture_output() as cap:
    %cd /content
    if not os.path.exists(str(WORKSPACE+'/Sessions')):
      %mkdir -p $WORKSPACE'/Sessions'
      time.sleep(1)
    %cd $WORKSPACE'/Sessions'
    !gdown --folder --remaining-ok -O $Session_Name  $Session_Link_optional
    %cd $Session_Name
    !rm -r instance_images
    !unzip instance_images.zip
    !rm -r captions
    !unzip captions.zip
    %cd /content


INSTANCE_NAME=Session_Name
OUTPUT_DIR="/content/models/"+Session_Name
SESSION_DIR=WORKSPACE+'/Sessions/'+Session_Name
INSTANCE_DIR=SESSION_DIR+'/instance_images'
CAPTIONS_DIR=SESSION_DIR+'/captions'
MDLPTH=str(SESSION_DIR+"/"+Session_Name+'.ckpt')

if os.path.exists(str(SESSION_DIR)):
  mdls=[ckpt for ckpt in listdir(SESSION_DIR) if ckpt.split(".")[-1]=="ckpt"]
  if not os.path.exists(MDLPTH) and '.ckpt' in str(mdls):

    def f(n):
      k=0
      for i in mdls:
        if k==n:
          !mv "$SESSION_DIR/$i" $MDLPTH
        k=k+1

    k=0
    print('[1;33mNo final checkpoint model found, select which intermediary checkpoint to use, enter only the number, (000 to skip):\n[1;34m')

    for i in mdls:
      print(str(k)+'- '+i)
      k=k+1
    n=input()
    while int(n)>k-1:
      n=input()
    if n!="000":
      f(int(n))
      print('[1;32mUsing the model '+ mdls[int(n)]+" ...")
      time.sleep(2)
    else:
      print('[1;32mSkipping the intermediary checkpoints.')
    del n

with capture.capture_output() as cap:
  %cd /content
  resume=False

if os.path.exists(str(SESSION_DIR)) and not os.path.exists(MDLPTH):
  print('[1;32mLoading session with no previous model, using the original model or the custom downloaded model')
  if MODEL_NAME=="":
    print('[1;31mNo model found, use the "Model Download" cell to download a model.')
  else:
    print('[1;32mSession Loaded, proceed to uploading instance images')

elif os.path.exists(MDLPTH):
  print('[1;32mSession found, loading the trained model ...')
  wget.download('https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/det.py')
  print('[1;33mDetecting model version...')
  Model_Version=check_output('python det.py --MODEL_PATH '+MDLPTH, shell=True).decode('utf-8').replace('\n', '')
  clear_output()
  print('[1;32m'+Model_Version+' Detected')
  !rm det.py
  if Model_Version=='1.5':
    !wget -q -O config.yaml https://github.com/CompVis/stable-diffusion/raw/main/configs/stable-diffusion/v1-inference.yaml
    print('[1;32mSession found, loading the trained model ...')
    !python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path $MDLPTH --dump_path "$OUTPUT_DIR" --original_config_file config.yaml
    !rm /content/config.yaml

  elif Model_Version=='V2.1-512px':
    !wget -q -O convertodiff.py https://raw.githubusercontent.com/TheLastBen/fast-stable-diffusion/main/Dreambooth/convertodiffv2.py
    print('[1;32mSession found, loading the trained model ...')
    !python /content/convertodiff.py "$MDLPTH" "$OUTPUT_DIR" --v2 --reference_model stabilityai/stable-diffusion-2-1-base
    !rm /content/convertodiff.py

  elif Model_Version=='V2.1-768px':
    !wget -q -O convertodiff.py https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/convertodiffv2-768.py
    print('[1;32mSession found, loading the trained model ...')
    !python /content/convertodiff.py "$MDLPTH" "$OUTPUT_DIR" --v2 --reference_model stabilityai/stable-diffusion-2-1
    !rm /content/convertodiff.py


  if os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
    resume=True
    clear_output()
    print('[1;32mSession loaded.')
  else:
    if not os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
      print('[1;31mConversion error, if the error persists, remove the CKPT file from the current session folder')

elif not os.path.exists(str(SESSION_DIR)):
    %mkdir -p "$INSTANCE_DIR"
    print('[1;32mCreating session...')
    if MODEL_NAME=="":
      print('[1;31mNo model found, use the "Model Download" cell to download a model.')
    else:
      print('[1;32mSession created, proceed to uploading instance images')

    #@markdown

    #@markdown # The most important step is to rename the instance pictures of each subject to a unique unknown identifier, example :
    #@markdown - If you have 10 pictures of yourself, simply select them all and rename only one to the chosen identifier for example : phtmejhn, the files would be : phtmejhn (1).jpg, phtmejhn (2).png ....etc then upload them, do the same for other people or objects with a different identifier, and that's it.
    #@markdown - Checkout this example : https://i.imgur.com/d2lD3rz.jpeg