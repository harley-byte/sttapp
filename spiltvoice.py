import os.path
import torch

import demucs.api as demucsApi
def get_available_device():
    if torch.cuda.is_available():
        return 'cuda'
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return 'mps'
    else:
        return 'cpu'
def separate_audio(audio_path, output_dir,model,stem):
    print(model)
    print(stem)
    separator = demucsApi.Separator(model=model, device=get_available_device(), callback=cc)
    origin, separated = separator.separate_audio_file(audio_path)
    # 遍历 separated 字典并保存每个音频源
    for stem, tensor in separated.items():
        print(f"Stem: {stem}")
        print(f"Tensor: {tensor}")

        # 构建输出文件名
        output_file =  os.path.join(output_dir,"{stem}_output.wav")

        # 保存音频文件
        demucsApi.save_audio(tensor, output_file, samplerate=separator.samplerate)



def cc(result):
    #print(result)
    pass



