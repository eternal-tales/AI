# Train

 #Start DreamBooth

import os
from IPython.display import clear_output
from google.colab import runtime
from subprocess import getoutput
import time
import random

if os.path.exists(INSTANCE_DIR+"/.ipynb_checkpoints"):
  %rm -r $INSTANCE_DIR"/.ipynb_checkpoints"

if os.path.exists(CAPTIONS_DIR+"/.ipynb_checkpoints"):
  %rm -r $CAPTIONS_DIR"/.ipynb_checkpoints"

Resume_Training = False #@param {type:"boolean"}

if resume and not Resume_Training:
  print('[1;31mOverwrite your previously trained model ? answering "yes" will train a new model, answering "no" will resume the training of the previous model?  yes or no ?[0m')
  while True:
    ansres=input('')
    if ansres=='no':
      Resume_Training = True
      break
    elif ansres=='yes':
      Resume_Training = False
      resume= False
      break

while not Resume_Training and MODEL_NAME=="":
  print('[1;31mNo model found, use the "Model Download" cell to download a model.')
  time.sleep(5)

#@markdown  - If you're not satisfied with the result, check this box, run again the cell and it will continue training the current model.

MODELT_NAME=MODEL_NAME

UNet_Training_Steps=1500 #@param{type: 'number'}
UNet_Learning_Rate = 2e-6 #@param ["2e-5","1e-5","9e-6","8e-6","7e-6","6e-6","5e-6", "4e-6", "3e-6", "2e-6"] {type:"raw"}
untlr=UNet_Learning_Rate

#@markdown - These default settings are for a dataset of 10 pictures which is enough for training a face, start with 1500 or lower, test the model, if not enough, resume training for 200 steps, keep testing until you get the desired output, `set it to 0 to train only the text_encoder`.

Text_Encoder_Training_Steps=350 #@param{type: 'number'}

#@markdown - 200-450 steps is enough for a small dataset, keep this number small to avoid overfitting, set to 0 to disable, `set it to 0 before resuming training if it is already trained`.

Text_Encoder_Learning_Rate = 1e-6 #@param ["2e-6", "1e-6","8e-7","6e-7","5e-7","4e-7"] {type:"raw"}
txlr=Text_Encoder_Learning_Rate

#@markdown - Learning rate for the text_encoder, keep it low to avoid overfitting (1e-6 is higher than 4e-7)


trnonltxt=""
if UNet_Training_Steps==0:
   trnonltxt="--train_only_text_encoder"

Seed=''

ofstnse=""
Offset_Noise = False #@param {type:"boolean"}
#@markdown - Always use it for style training.

if Offset_Noise:
  ofstnse="--offset_noise"

External_Captions = False #@param {type:"boolean"}
#@markdown - Get the captions from a text file for each instance image.
extrnlcptn=""
if External_Captions:
  extrnlcptn="--external_captions"

Resolution = "512" #@param ["512", "576", "640", "704", "768", "832", "896", "960", "1024"]
Res=int(Resolution)

#@markdown - Higher resolution = Higher quality, make sure the instance images are cropped to this selected size (or larger).

fp16 = True

if Seed =='' or Seed=='0':
  Seed=random.randint(1, 999999)
else:
  Seed=int(Seed)

if fp16:
  prec="fp16"
else:
  prec="no"

precision=prec

resuming=""
if Resume_Training and os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
  MODELT_NAME=OUTPUT_DIR
  print('[1;32mResuming Training...[0m')
  resuming="Yes"
elif Resume_Training and not os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
  print('[1;31mPrevious model not found, training a new model...[0m')
  MODELT_NAME=MODEL_NAME
  while MODEL_NAME=="":
    print('[1;31mNo model found, use the "Model Download" cell to download a model.')
    time.sleep(5)

V2=False
if os.path.getsize(MODELT_NAME+"/text_encoder/pytorch_model.bin") > 670901463:
  V2=True

s = getoutput('nvidia-smi')
GCUNET="--gradient_checkpointing"
TexRes=Res
if Res<=768:
  GCUNET=""

if V2:
  if Res>704:
    GCUNET="--gradient_checkpointing"
  if Res>576:
    TexRes=576

if 'A100' in s :
   GCUNET=""
   TexRes=Res


Enable_text_encoder_training= True

if Text_Encoder_Training_Steps==0 :
   Enable_text_encoder_training= False
else:
  stptxt=Text_Encoder_Training_Steps


#@markdown ---------------------------
Save_Checkpoint_Every_n_Steps = False #@param {type:"boolean"}
Save_Checkpoint_Every=500 #@param{type: 'number'}
if Save_Checkpoint_Every==None:
  Save_Checkpoint_Every=1
#@markdown - Minimum 200 steps between each save.
stp=0
Start_saving_from_the_step=500 #@param{type: 'number'}
if Start_saving_from_the_step==None:
  Start_saving_from_the_step=0
if (Start_saving_from_the_step < 200):
  Start_saving_from_the_step=Save_Checkpoint_Every
stpsv=Start_saving_from_the_step
if Save_Checkpoint_Every_n_Steps:
  stp=Save_Checkpoint_Every
#@markdown - Start saving intermediary checkpoints from this step.

Disconnect_after_training=False #@param {type:"boolean"}

#@markdown - Auto-disconnect from google colab after the training to avoid wasting compute units.

def dump_only_textenc(trnonltxt, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps):

    !accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
    $trnonltxt \
    $extrnlcptn \
    $ofstnse \
    --image_captions_filename \
    --train_text_encoder \
    --dump_only_text_encoder \
    --pretrained_model_name_or_path="$MODELT_NAME" \
    --instance_data_dir="$INSTANCE_DIR" \
    --output_dir="$OUTPUT_DIR" \
    --captions_dir="$CAPTIONS_DIR" \
    --instance_prompt="$PT" \
    --seed=$Seed \
    --resolution=$TexRes \
    --mixed_precision=$precision \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 --gradient_checkpointing \
    --use_8bit_adam \
    --learning_rate=$txlr \
    --lr_scheduler="linear" \
    --lr_warmup_steps=0 \
    --max_train_steps=$Training_Steps

def train_only_unet(stpsv, stp, SESSION_DIR, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, Res, precision, Training_Steps):
    clear_output()
    if resuming=="Yes":
      print('[1;32mResuming Training...[0m')
    print('[1;33mTraining the UNet...[0m')
    !accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
    $extrnlcptn \
    $ofstnse \
    --image_captions_filename \
    --train_only_unet \
    --save_starting_step=$stpsv \
    --save_n_steps=$stp \
    --Session_dir=$SESSION_DIR \
    --pretrained_model_name_or_path="$MODELT_NAME" \
    --instance_data_dir="$INSTANCE_DIR" \
    --output_dir="$OUTPUT_DIR" \
    --captions_dir="$CAPTIONS_DIR" \
    --instance_prompt="$PT" \
    --seed=$Seed \
    --resolution=$Res \
    --mixed_precision=$precision \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 $GCUNET \
    --use_8bit_adam \
    --learning_rate=$untlr \
    --lr_scheduler="linear" \
    --lr_warmup_steps=0 \
    --max_train_steps=$Training_Steps


if Enable_text_encoder_training :
  print('[1;33mTraining the text encoder...[0m')
  if os.path.exists(OUTPUT_DIR+'/'+'text_encoder_trained'):
    %rm -r $OUTPUT_DIR"/text_encoder_trained"
  dump_only_textenc(trnonltxt, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps=stptxt)


if UNet_Training_Steps!=0:
  train_only_unet(stpsv, stp, SESSION_DIR, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, Res, precision, Training_Steps=UNet_Training_Steps)

if UNet_Training_Steps==0 and Text_Encoder_Training_Steps==0 :
  print('[1;32mNothing to do')
else:
  if os.path.exists('/content/models/'+INSTANCE_NAME+'/unet/diffusion_pytorch_model.bin'):
    prc="--fp16" if precision=="fp16" else ""
    !python /content/diffusers/scripts/convertosdv2.py $prc $OUTPUT_DIR $SESSION_DIR/$Session_Name".ckpt"
    clear_output()
    if os.path.exists(SESSION_DIR+"/"+INSTANCE_NAME+'.ckpt'):
      clear_output()
      print("[1;32mDONE, the CKPT model is in your Gdrive in the sessions folder")
      if Disconnect_after_training :
        time.sleep(20)
        runtime.unassign()
    else:
      print("[1;31mSomething went wrong")
  else:
    print("[1;31mSomething went wrong")