# TTS_GLaDOS
This repo contains code for creating a text-to-speech model emulating the voice of GLaDOS, the malevolent AI from the Portal video games. The text-to-speech model uses [Variational Inference with adversarial
learning for end-to-end Text-to-Speech](https://github.com/jaywalnut310/vits) implemented using [coqui-ai's TTS library](https://github.com/coqui-ai/TTS) and is with `.wav` files scraped from a [Portal wiki](https://theportalwiki.com/wiki/GLaDOS_voice_lines).

The model does a pretty good job synthesizing English language speach as I imagine GLaDOS might. For example, if we gibe the model:
> "Hello. You have found code for creating a text to speech model of my voice. Enjoy it. While you can."

We get: <br>

https://user-images.githubusercontent.com/10395840/235816423-7a6301dd-278f-43d5-95ef-d0a727657dee.mp4

# test audio
https://github.com/ianrose42/TTS_GLaDOS/blob/main/repo_audio/github_greeting.mp4

## now with brake...


# Code to train the model

## Step 1: d-vectors
```
python3 TTS/bin/compute_embeddings.py \
    --model_path model_se.pth.tar \ # Path to model checkpoint file. It defaults to the released speaker encoder.
    --config_path  config_se.json \ # Path to model config file. It defaults to the released speaker encoder config.
    --config_dataset_path  config.json \ # Path to dataset config file. You either need to provide this or `formatter_name`, `dataset_name` and `dataset_path` arguments.
    --output_path d_vector_file.json # Path for output `pth` or `json` file.
```

FIRST! re-sample the newly downloaded files such that they have 16000 sample rate
SECOND! arrange the files so that VCTK will be happy (done)
THIRD! Check if the test sentences are/should be in training data (they do not)
FOURTH! make d-vectors

For the d-vectors:
```
python3 TTS/bin/compute_embeddings.py     --model_path /text_to_speech/latest_yourtts_files/latest_model_dl/tts_models--multilingual--multi-dataset--your_tts/tts_models--multilingual--multi-dataset--your_tts/model_se.pth.tar     --config_path  /text_to_speech/latest_yourtts_files/latest_model_dl/tts_models--multilingual--multi-dataset--your_tts/tts_models--multilingual--multi-dataset--your_tts/config_se.json     --formatter_name vctk     --dataset_name glados     --dataset_path /TTS_GLaDOS/VCTK/     --output_path /TTS_GLaDOS/VCTK/speakers.pth
```
Train the model:
```
python3 TTS/bin/train_tts.py \
    --config_path /text_to_speech/latest_yourtts_files/latest_model_dl/tts_models--multilingual--multi-dataset--your_tts/tts_models--multilingual--multi-dataset--your_tts/config.json \
    --restore_path /text_to_speech/latest_yourtts_files/latest_model_dl/actually_checkpoint/model+SCL/checkpoint_70000.pth.tar
```


Also helpful, docker commands:
```
docker run -it --rm \
    -v /home/ian/Desktop/wisdom/projects/misc/TTS_GLaDOS:/TTS_GLaDOS \
    -v /home/ian/Desktop/wisdom/projects/text_to_speech:/text_to_speech \
    -p 5001:5002 \
    --shm-size 30G \
    --entrypoint '/bin/bash' \
    "ghcr.io/coqui-ai/tts"
```
Second container launch command:
```
docker run -it --rm \
    --user "$(id -u):$(id -g)" \
    -v /home/ian/Desktop/wisdom/projects/misc/TTS_GLaDOS:/TTS_GLaDOS \
    -v /home/ian/Desktop/wisdom/projects/text_to_speech:/text_to_speech \
    -p 5001:5002 \
    --shm-size 30G \
    --entrypoint '/bin/bash' \
    "ghcr.io/coqui-ai/tts"
```


Change sample rate:
```
python TTS/bin/resample.py \
    --input_dir /TTS_GLaDOS/glados_data/ \
    --output_sr 16000 \
    --output_dir /TTS_GLaDOS/glados16000_data/ \
    --n_jobs 8 \
    --file_ext wav
```
Actually training the model:
```
python3 /TTS_GLaDOS/train_glados.py
```