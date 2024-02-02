import os
import time
from IPython.utils import capture
from IPython.display import clear_output
import wget
from subprocess import check_output
import urllib.request
import requests
import base64
from gdown.download import get_url_from_gdrive_confirmation
from urllib.parse import urlparse, parse_qs, unquote
from urllib.request import urlopen, Request


def getsrc(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'civitai.com':
        src='civitai'
    elif parsed_url.netloc == 'drive.google.com':
        src='gdrive'
    elif parsed_url.netloc == 'huggingface.co':
        src='huggingface'
    else:
        src='others'
    return src



def get_name(url, gdrive):
    if not gdrive:
        response = requests.get(url, allow_redirects=False)
        if "Location" in response.headers:
            redirected_url = response.headers["Location"]
            quer = parse_qs(urlparse(redirected_url).query)
            if "response-content-disposition" in quer:
                disp_val = quer["response-content-disposition"][0].split(";")
                for vals in disp_val:
                    if vals.strip().startswith("filename="):
                        filenm=unquote(vals.split("=", 1)[1].strip())
                        return filenm.replace("\"","")
    else:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
        lnk="https://drive.google.com/uc?id={id}&export=download".format(id=url[url.find("/d/")+3:url.find("/view")])
        res = requests.session().get(lnk, headers=headers, stream=True, verify=True)
        res = requests.session().get(get_url_from_gdrive_confirmation(res.text), headers=headers, stream=True, verify=True)
        content_disposition = six.moves.urllib_parse.unquote(res.headers["Content-Disposition"])
        filenm = re.search(r"filename\*=UTF-8''(.*)", content_disposition).groups()[0].replace(os.path.sep, "_")
        return filenm

#@markdown - Skip this cell if you are loading a previous session that contains a trained model.

#@markdown ---

Model_Version = "1.5" #@param [ "1.5", "V2.1-512px", "V2.1-768px"]

#@markdown - Choose which version to finetune.

with capture.capture_output() as cap:
  os.chdir('/content')

#@markdown ---

Path_to_HuggingFace= "runwayml/stable-diffusion-v1-5" #@param {type:"string"}

#@markdown - Load and finetune a model from Hugging Face, use the format "profile/model" like : runwayml/stable-diffusion-v1-5
#@markdown - If the custom model is private or requires a token, create token.txt containing the token in "Fast-Dreambooth" folder in your gdrive.

MODEL_PATH = "" #@param {type:"string"}

MODEL_LINK = "" #@param {type:"string"}


if os.path.exists('/content/gdrive/MyDrive/Fast-Dreambooth/token.txt'):
  with open("/content/gdrive/MyDrive/Fast-Dreambooth/token.txt") as f:
     token = f.read()
  authe=f'https://USER:{token}@'
else:
  authe="https://"

def downloadmodel():

  if os.path.exists('/content/stable-diffusion-v1-5'):
    !rm -r /content/stable-diffusion-v1-5
  clear_output()

  os.chdir('/content')
  clear_output()
  !mkdir /content/stable-diffusion-v1-5
  os.chdir('/content/stable-diffusion-v1-5')
  !git config --global init.defaultBranch main
  !git init
  !git lfs install --system --skip-repo
  !git remote add -f origin  "https://huggingface.co/runwayml/stable-diffusion-v1-5"
  !git config core.sparsecheckout true
  !echo -e "scheduler\ntext_encoder\ntokenizer\nunet\nvae\nmodel_index.json\n!vae/diffusion_pytorch_model.bin\n!*.safetensors\n!*.fp16.bin\n!*.non_ema.bin" > .git/info/sparse-checkout
  !git pull origin main
  if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
    !wget -q -O vae/diffusion_pytorch_model.bin https://huggingface.co/stabilityai/sd-vae-ft-mse/resolve/main/diffusion_pytorch_model.bin
    !rm -r .git
    !rm model_index.json
    time.sleep(1)
    wget.download('https://raw.githubusercontent.com/TheLastBen/fast-stable-diffusion/main/Dreambooth/model_index.json')
    os.chdir('/content')
    clear_output()
    print('[1;32mDONE !')
  else:
    while not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
         print('[1;31mSomething went wrong')
         time.sleep(5)

def newdownloadmodel():

  os.chdir('/content')
  clear_output()
  !mkdir /content/stable-diffusion-v2-768
  os.chdir('/content/stable-diffusion-v2-768')
  !git config --global init.defaultBranch main
  !git init
  !git lfs install --system --skip-repo
  !git remote add -f origin  "https://huggingface.co/stabilityai/stable-diffusion-2-1"
  !git config core.sparsecheckout true
  !echo -e "scheduler\ntext_encoder\ntokenizer\nunet\nvae\nfeature_extractor\nmodel_index.json\n!*.safetensors\n!*.fp16.bin" > .git/info/sparse-checkout
  !git pull origin main
  !rm -r /content/stable-diffusion-v2-768/.git
  os.chdir('/content')
  clear_output()
  print('[1;32mDONE !')


def newdownloadmodelb():

  os.chdir('/content')
  clear_output()
  !mkdir /content/stable-diffusion-v2-512
  os.chdir('/content/stable-diffusion-v2-512')
  !git config --global init.defaultBranch main
  !git init
  !git lfs install --system --skip-repo
  !git remote add -f origin  "https://huggingface.co/stabilityai/stable-diffusion-2-1-base"
  !git config core.sparsecheckout true
  !echo -e "scheduler\ntext_encoder\ntokenizer\nunet\nvae\nfeature_extractor\nmodel_index.json\n!*.safetensors\n!*.fp16.bin" > .git/info/sparse-checkout
  !git pull origin main
  !rm -r /content/stable-diffusion-v2-512/.git
  os.chdir('/content')
  clear_output()
  print('[1;32mDONE !')


if Path_to_HuggingFace != "":
  if authe=="https://":
    textenc= f"{authe}huggingface.co/{Path_to_HuggingFace}/resolve/main/text_encoder/pytorch_model.bin"
    txtenc_size=urllib.request.urlopen(textenc).info().get('Content-Length', None)
  else:
    textenc= f"https://huggingface.co/{Path_to_HuggingFace}/resolve/main/text_encoder/pytorch_model.bin"
    req=urllib.request.Request(textenc)
    req.add_header('Authorization', f'Bearer {token}')
    txtenc_size=urllib.request.urlopen(req).info().get('Content-Length', None)
  if int(txtenc_size)> 670000000 :
    if os.path.exists('/content/stable-diffusion-custom'):
      !rm -r /content/stable-diffusion-custom
    clear_output()
    os.chdir('/content')
    clear_output()
    print("[1;32mV2")
    !mkdir /content/stable-diffusion-custom
    os.chdir('/content/stable-diffusion-custom')
    !git config --global init.defaultBranch main
    !git init
    !git lfs install --system --skip-repo
    !git remote add -f origin  "{authe}huggingface.co/{Path_to_HuggingFace}"
    !git config core.sparsecheckout true
    !echo -e "scheduler\ntext_encoder\ntokenizer\nunet\nvae\nfeature_extractor\nmodel_index.json\n!*.safetensors" > .git/info/sparse-checkout
    !git pull origin main
    if os.path.exists('/content/stable-diffusion-custom/unet/diffusion_pytorch_model.bin'):
      !rm -r /content/stable-diffusion-custom/.git
      os.chdir('/content')
      MODEL_NAME="/content/stable-diffusion-custom"
      clear_output()
      print('[1;32mDONE !')
    else:
      while not os.path.exists('/content/stable-diffusion-custom/unet/diffusion_pytorch_model.bin'):
            print('[1;31mCheck the link you provided')
            time.sleep(5)
  else:
    if os.path.exists('/content/stable-diffusion-custom'):
      !rm -r /content/stable-diffusion-custom
    clear_output()
    os.chdir('/content')
    clear_output()
    print("[1;32mV1")
    !mkdir /content/stable-diffusion-custom
    os.chdir('/content/stable-diffusion-custom')
    !git init
    !git lfs install --system --skip-repo
    !git remote add -f origin  "{authe}huggingface.co/{Path_to_HuggingFace}"
    !git config core.sparsecheckout true
    !echo -e "scheduler\ntext_encoder\ntokenizer\nunet\nvae\nmodel_index.json\n!*.safetensors" > .git/info/sparse-checkout
    !git pull origin main
    if os.path.exists('/content/stable-diffusion-custom/unet/diffusion_pytorch_model.bin'):
      !rm -r /content/stable-diffusion-custom/.git
      !rm model_index.json
      time.sleep(1)
      wget.download('https://raw.githubusercontent.com/TheLastBen/fast-stable-diffusion/main/Dreambooth/model_index.json')
      os.chdir('/content')
      MODEL_NAME="/content/stable-diffusion-custom"
      clear_output()
      print('[1;32mDONE !')
    else:
      while not os.path.exists('/content/stable-diffusion-custom/unet/diffusion_pytorch_model.bin'):
            print('[1;31mCheck the link you provided')
            time.sleep(5)

elif MODEL_PATH !="":

  modelname=os.path.basename(MODEL_PATH)
  sftnsr=""
  if modelname.split('.')[-1]=='safetensors':
    sftnsr="--from_safetensors"

  %cd /content
  clear_output()
  if os.path.exists(str(MODEL_PATH)):
    wget.download('https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/det.py')
    print('[1;33mDetecting model version...')
    Custom_Model_Version=check_output('python det.py '+sftnsr+' --MODEL_PATH '+str(MODEL_PATH), shell=True).decode('utf-8').replace('\n', '')
    clear_output()
    print('[1;32m'+Custom_Model_Version+' Detected')
    !rm det.py
    if Custom_Model_Version=='1.5':
      !wget -q -O config.yaml https://github.com/CompVis/stable-diffusion/raw/main/configs/stable-diffusion/v1-inference.yaml
      !python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path "$MODEL_PATH" --dump_path stable-diffusion-custom --original_config_file config.yaml $sftnsr
      !rm /content/config.yaml

    elif Custom_Model_Version=='V2.1-512px':
      !wget -q -O convertodiff.py https://raw.githubusercontent.com/TheLastBen/fast-stable-diffusion/main/Dreambooth/convertodiffv2.py
      !python /content/convertodiff.py "$MODEL_PATH" /content/stable-diffusion-custom --v2 --reference_model stabilityai/stable-diffusion-2-1-base $sftnsr
      !rm /content/convertodiff.py

    elif Custom_Model_Version=='V2.1-768px':
      !wget -q -O convertodiff.py https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/convertodiffv2-768.py
      !python /content/convertodiff.py "$MODEL_PATH" /content/stable-diffusion-custom --v2 --reference_model stabilityai/stable-diffusion-2-1 $sftnsr
      !rm /content/convertodiff.py


    if os.path.exists('/content/stable-diffusion-custom/unet/diffusion_pytorch_model.bin'):
      clear_output()
      MODEL_NAME="/content/stable-diffusion-custom"
      print('[1;32mDONE !')
    else:
      !rm -r /content/stable-diffusion-custom
      while not os.path.exists('/content/stable-diffusion-custom/unet/diffusion_pytorch_model.bin'):
        print('[1;31mConversion error')
        time.sleep(5)
  else:
    while not os.path.exists(str(MODEL_PATH)):
       print('[1;31mWrong path, use the colab file explorer to copy the path')
       time.sleep(5)

elif MODEL_LINK !="":
    os.chdir('/content')

    src=getsrc(MODEL_LINK)

    if src=='civitai':
       modelname=get_name(str(MODEL_LINK), False)
    elif src=='gdrive':
       modelname=get_name(str(MODEL_LINK), True)
    else:
       modelname=os.path.basename(str(MODEL_LINK))

    sftnsr=""
    if modelname.split('.')[-1]!='safetensors':
      modelnm="model.ckpt"
    else:
      modelnm="model.safetensors"
      sftnsr="--from_safetensors"

    !gdown --fuzzy "$MODEL_LINK" -O $modelnm

    if os.path.exists(modelnm):
      if os.path.getsize(modelnm) > 1810671599:
        wget.download('https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/det.py')
        print('[1;33mDetecting model version...')
        Custom_Model_Version=check_output('python det.py '+sftnsr+' --MODEL_PATH '+modelnm, shell=True).decode('utf-8').replace('\n', '')
        clear_output()
        print('[1;32m'+Custom_Model_Version+' Detected')
        !rm det.py
        if Custom_Model_Version=='1.5':
          !wget -q -O config.yaml https://github.com/CompVis/stable-diffusion/raw/main/configs/stable-diffusion/v1-inference.yaml
          !python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path $modelnm --dump_path stable-diffusion-custom --original_config_file config.yaml $sftnsr
          !rm config.yaml

        elif Custom_Model_Version=='V2.1-512px':
          !wget -q -O convertodiff.py https://raw.githubusercontent.com/TheLastBen/fast-stable-diffusion/main/Dreambooth/convertodiffv2.py
          !python /content/convertodiff.py $modelnm /content/stable-diffusion-custom --v2 --reference_model stabilityai/stable-diffusion-2-1-base $sftnsr
          !rm convertodiff.py

        elif Custom_Model_Version=='V2.1-768px':
          !wget -q -O convertodiff.py https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/convertodiffv2-768.py
          !python /content/convertodiff.py $modelnm /content/stable-diffusion-custom --v2 --reference_model stabilityai/stable-diffusion-2-1 $sftnsr
          !rm convertodiff.py


        if os.path.exists('/content/stable-diffusion-custom/unet/diffusion_pytorch_model.bin'):
          clear_output()
          MODEL_NAME="/content/stable-diffusion-custom"
          print('[1;32mDONE !')
        else:
          !rm -r stable-diffusion-custom
          !rm $modelnm
          while not os.path.exists('/content/stable-diffusion-custom/unet/diffusion_pytorch_model.bin'):
            print('[1;31mConversion error')
            time.sleep(5)
      else:
        while os.path.getsize(modelnm) < 1810671599:
           print('[1;31mWrong link, check that the link is valid')
           time.sleep(5)

else:
  if Model_Version=="1.5":
    if not os.path.exists('/content/stable-diffusion-v1-5'):
      downloadmodel()
      MODEL_NAME="/content/stable-diffusion-v1-5"
    else:
      MODEL_NAME="/content/stable-diffusion-v1-5"
      print("[1;32mThe v1.5 model already exists, using this model.")
  elif Model_Version=="V2.1-512px":
    if not os.path.exists('/content/stable-diffusion-v2-512'):
      newdownloadmodelb()
      MODEL_NAME="/content/stable-diffusion-v2-512"
    else:
      MODEL_NAME="/content/stable-diffusion-v2-512"
      print("[1;32mThe v2-512px model already exists, using this model.")
  elif Model_Version=="V2.1-768px":
    if not os.path.exists('/content/stable-diffusion-v2-768'):
      newdownloadmodel()
      MODEL_NAME="/content/stable-diffusion-v2-768"
    else:
      MODEL_NAME="/content/stable-diffusion-v2-768"
      print("[1;32mThe v2-768px model already exists, using this model.")