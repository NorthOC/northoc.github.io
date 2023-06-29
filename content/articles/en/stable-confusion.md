# My experience with stable diffusion + tutorial

## Context

I've been experimenting with Stable Diffusion. In short, it is a model used to generate images. Similar ones are Midjourney and DALLE 2. It is wild, unpredictable, a black box. And, sometimes, it makes you go "woaaaah". The fact that you can take a prompt and transform it into a picture is crazy, however the most underrated feature of Stable Diffusion is the img2img. You basically take an image, and combine it with a prompt, and then the model can spit out some cool stuff:

[like this](/static/images/stable-diffusion/waifu.png)

## CUDA CUDA CU..

I like that Machine Learning is steering towards open-source but, in its current situation, no matter what model [Facebook](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/) or [Google](https://ai.google/) releases, there is one big problem. To run any AI efficiently, you need a [CUDA](https://en.wikipedia.org/wiki/CUDA)-compatible Graphics Processing Unit (aka. GPU).

CUDA is cool because it allows for GPUs to make matrices calculations simultaneously, reducing the amount of time one has to wait for the output. But, as of now, CUDA works only with NVIDIAs GPUs. You can run an AI instance locally without an NVIDIA GPU, but it will take an absurd amount of time to generate even one picture (about an hour). This means that if you have a powerful AMD GPU, you're a pleb who can't do anything in AI.

## Nvidia vs The World (a funny story)

At work, I have solid Windows PC which can handle heavy loads of processing. But guess what, there's no NVIDIA GPU in it. When I ran Stable Diffusion, it took about 40 minutes to even generate one picture.

So I went back home, pulled out my ASUS X555L beater laptop, which I bought in 2016: 

4 Gigs of RAM, 2,5 GHz CPU, still uses an HDD (don't worry I upgraded after this post) barely even loads one tab of Firefox at this point lol. But guess what? It has an NVIDIA GeForce 930M (with CUDA compatibility) GPU! It took less than 2 minutes to generate one image... Yep.

## Tutorial

You may want to try out Stable-Diffusion for yourself, so here's how to do it (for Windows):

### Requirements

An Nvidia graphics card with CUDA compatibility.

### Instructions

1. Install Nvidia drivers [from here](https://www.nvidia.com/en-gb/geforce/geforce-experience/)
2. Install Python 3.10.6 [from here](https://www.python.org/downloads/release/python-3106/)
3. Install Visual Studio [from here](https://visualstudio.microsoft.com/downloads/)
4. Install CUDA Toolkit [from here](https://developer.nvidia.com/cuda-downloads)
5. Install Git [from here](https://git-scm.com/downloads)
6. Download the Stable Diffusion 1.4 checkpoint [from here](https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt)
7. Clone the Stable Diffusion repository. open your command line interface (cmd) and type this: `git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui`
8. Move the checkpoint file you downloaded to `stable-diffusion-webui/models/Stable-Diffusion` folder
9. Run the program with `webui-user.bat`
10. Open your browser and type [http://127.0.0.1:7860](http://127.0.0.1:786)

### What to do if I have low RAM?

If your computer, like mine, is older than [ancient Rome](https://en.wikipedia.org/wiki/Antikythera_mechanism), modify `webui-user.bat` (open with notepad) with these parameters:

`COMMANDLINE_ARGS=--xformers --lowvram`

Now you can say you have experience in Machine Learning.