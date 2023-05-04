# TTS_GLaDOS
This repo contains code for creating a text-to-speech model emulating the voice of GLaDOS, the malevolent AI from the Portal video games. The text-to-speech model uses [YourTTS](https://github.com/Edresson/YourTTS) (an extension of [Variational Inference with adversarial
learning for end-to-end Text-to-Speech](https://github.com/jaywalnut310/vits)) implemented using [coqui-ai's TTS library](https://github.com/coqui-ai/TTS) and is trained with `.wav` files scraped from a [Portal wiki](https://theportalwiki.com/wiki/GLaDOS_voice_lines).

The model does a pretty good job synthesizing English language speech as I imagine GLaDOS might. For example, if we give the model:
> "Hello. You have found code for creating a text to speech model of my voice. Enjoy it. While you can."

We get: <br>

https://user-images.githubusercontent.com/10395840/235816423-7a6301dd-278f-43d5-95ef-d0a727657dee.mp4

# Table of Contents
**[Intro](#TTS_GLaDOS)**<br>
**[Preparation](#preparation)**<br>
**[Acquiring Training Data](#acquiring-training-data)**<br>
**[Training the Model](#code-to-train-the-model)**<br>
**[Generating Speech](#generating-speech)**<br>


# Preparation
I used audio files from the Portal and DotA video games to train the text-to-speech model, but I also added one speaker (p255) from the [VCTK dataset](https://datashare.ed.ac.uk/handle/10283/2950). A helpful script for downloading the VCTK data set is provided by [TTS](https://github.com/coqui-ai/TTS/blob/dev/recipes/vctk/download_vctk.sh). Also, to speed up the training, I used a transfer learning from one of coqui's models. If you would like to that too, you can download the necessary files [here](https://drive.google.com/drive/folders/15G-QS5tYQPkqiXfAdialJjmuqZV0azQV?usp=sharing) (I used the checkpoint from step 70000). More context can be found at the [YourTTS](https://github.com/Edresson/YourTTS) repo.

# Acquiring Training Data
To train the GLaDOS test-to-speech model, you need `.wav` files containing short utterances spoken with GLaDOS' voice, and `.txt` files corresponding to the words spoken in the `.wav` files. The GLaDOS audio files (and any other speaker files) need to have their sampling rate changed to 16,000 (see [criteria for a good TTS dataset](https://tts.readthedocs.io/en/latest/what_makes_a_good_dataset.html)). Each audio file used in training also needs to to have its embeddings computed. Here is how I did those things.

## Downloading Training Data
For the downloading data step, I used the [Jupyter Data Science docker image](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html). If you are in a container using that image, you can enter the same directory this README file is in, and download the `.wav` files and their text using this command:
```
python3 ./code/download_data.py \
    -o ./glados_data
```
This will create a `glados_data` directory which will include the GLaDOS `.wav` files and metadata.csv which contains the text associated with each `.wav` file. <br>
For more information about `download_data.py` run:
```
python3 ./code/download_data.py --help
```
## Adjusting Sample Rate
The GLaDOS `.wav` files all of have a sample rate greater than 40,000 Hz. That is not bad, but higher sampling rates make the data load more slowly, and all samples in the data set must have the same sample rate. So I reduced the sampling rate for the GLaDOS files and VCTK sample to 16,000 Hz. To do this, I used the tool that [TTS provides](https://github.com/coqui-ai/TTS/tree/dev/recipes)

Note: For this step and all the other steps using TTS, I used a [TTS docker image](https://tts.readthedocs.io/en/latest/docker_images.html) 

## Choosing Which Samples to Use
To decide which audio samples would be the most informative, I selected audio samples according to their length, number of words, and (importantly) signal to noise ratio. More details can be found in the [jupyter notebook](./code/dataset_analysis.ipynb)

## Compute Embeddings
To compute the embeddings run the following command inside the TTS container you are using, from inside the TTS directory within the image. For example:
```
python3 TTS/bin/compute_embeddings.py \
    --config_path  /path/to/this/README/configs/config_se.json \
    --formatter_name vctk \
    --dataset_name glados \
    --dataset_path /path/to/this/README/glados_data/VCTK/ \
    --output_path /path/to/this/README/glados_data/VCTK/speakers.pth
```
I'm using this config file and not the defaults because I find that increasing `preemphasis` and `ref_level_db` _dramatically_ increase how "GLaDOS-ey" the text-to-speech model sounds.

# Code to Train the Model
To Train the model, use this command (from within a TTS container):
```
python3 /path/to/this/README/train_glados.py
```
If you stop the training and would like to resume from the last checkpoint, use:
```
python3 /path/to/this/README/train_glados.py \
    --continue_path /path/to/this/README/YourTTS-EN-VCTK-...
```
 
# Generating Speech
Here is how the greeting message earlier in this README was created:
```
tts \
    --text "Hello. You have found code for creating a text to speech model of my voice. Enjoy it. While you can." \
    --model_path /path/to/this/README/YourTTS-EN-VCTK-.../best_model.pth \
    --config_path /path/to/this/README/YourTTS-EN-VCTK-.../config.json \
    --speaker_idx "VCTK_glados" \
    --out_path /path/to/this/README/repo_audio/github_greeting.wav
```
Note: I had to convert the `.wav` file to a `.mp4` file so that the file could be added to a GitHub README file.
