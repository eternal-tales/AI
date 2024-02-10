# AI Modelling ( Multi-modal Chatbot )

## 1. Task
Real-time Text and Image generation corresponding to user's message

## 2. Model
### 2.1. Text Generation: OpenAI GPT (Chat) API
- Making a chatting agent with user's pet information (user giving when joining the app).
  
### 2.2. Image Generation: [Dreambooth Fast Stable Diffusion](https://github.com/TheLastBen/fast-stable-diffusion)
- Using pre-training checkpoint: [runwayml/stable-diffusion-v1-5](https://huggingface.co/runwayml/stable-diffusion-v1-5)
- Finetuning a model with user's 5 pet photos (user giving when joining the app).

## 3. Dataset
**Dreambooth**(*kind of sd finetuning method*) makes it possible to finetune the model with only a few images. Therefore, we do not use a large dataset. We only use data of 5 images for finetuning. Finetuning takes about 30 minutes. The finetuning outputs(ckpts) are as follows.

<details>
<summary>강아지 양파*</summary>
<div markdown="1">
- (hf) ckpt: dhdbsrlw/pet-onion
</div>
</details>

<details>
<summary>강아지 제로</summary>
<div markdown="1">
  
<a href="https://huggingface.co/dhdbsrlw/pet-onion">
<h3>ckpt: dhdbsrlw/pet-onion</h3>
</a>

</div>
</details>

<details>
<summary>강아지 몽자</summary>
<div markdown="1">
- (hf) ckpt: dhdbsrlw/pet-onion
</div>
</details>


## 4. Generation Output

