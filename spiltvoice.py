
import demucs.separate
import torch
from demucs import pretrained,apply
import demucs.api as demucsApi

def separate_audio(audio_path, output_dir,model,stem):
    print(model)
    print(stem)
    demucs.separate.main(["--mp3","--two-stems",stem,"-n",model,"/Users/flea/personal/earn2shopify/aitools/demucs/output.wav"])


def cc(result):
    #print(result)
    pass
def test(mName:str):
    separator=demucsApi.Separator(model=mName,device='mps',callback=cc,callback_arg={'abc':0})
    origin, separated=separator.separate_audio_file("/Users/flea/personal/earn2shopify/aitools/demucs/output.wav")
    print(separated)
    # Remember to create the destination folder before calling `save_audio`
    # Or you are likely to recieve `FileNotFoundError`
    # Remember to create the destination folder before calling `save_audio`
    # Or you are likely to recieve `FileNotFoundError`

    # 遍历 separated 字典并保存每个音频源
    for stem, tensor in separated.items():
        print(f"Stem: {stem}")
        print(f"Tensor: {tensor}")

        # 构建输出文件名
        output_file = f"/Users/flea/personal/earn2shopify/aitools/demucs/{stem}_output.wav"

        # 保存音频文件
        demucsApi.save_audio(tensor, output_file, samplerate=separator.samplerate)


test("htdemucs")