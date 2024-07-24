import oss2,os,sys
from datetime import datetime
import dashscope
import json
from urllib import request
from http import HTTPStatus
from environs import Env
import ssl
from dashscope.audio.asr import (Recognition,RecognitionResult)
ssl._create_default_https_context = ssl._create_unverified_context
env = Env()
def load_config():
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        return  os.path.join(sys._MEIPASS, '.env.local')
    else:
        # 如果是开发环境
        return  '.env.local'


def upload_file(object_name):
    ak=''
    ask=''
    dashscope.api_key=''
    env.read_env(load_config(), recurse = False)
    if len(env.str('DASHSCOPE_AK', '')) > 0:
        dashscope.api_key = env.str('DASHSCOPE_AK')
    if env.str('OSS_AK', ''):
        print("------")
        ak = env.str('OSS_AK')
        ask = env.str('OSS_SK')
    auth = oss2.Auth(ak, ask)
    bucket=oss2.Bucket(auth, "oss-cn-hangzhou.aliyuncs.com", "dawanapp")
    fname=datetime.now().strftime("%Y%m%d%H%M%S")
    ossKey=fname+".wav"
    result=bucket.put_object_from_file(key=ossKey,filename=object_name)
    os.remove(object_name)
    url=bucket.sign_url('GET',ossKey,36000,slash_safe=True)
    return url
def voice_to_text(voiceOss):
    task_response = dashscope.audio.asr.Transcription.async_call(
        model='paraformer-mtl-v1',
        file_urls=[
            voiceOss
        ])

    transcription_response = dashscope.audio.asr.Transcription.wait(
        task=task_response.output.task_id)

    if transcription_response.status_code == HTTPStatus.OK:
        print(transcription_response.output)
        transcription=transcription_response.output['results'][0]
        url = transcription['transcription_url']
        result = json.loads(request.urlopen(url).read().decode('utf8'))
        sentences=result['transcripts'][0]['sentences']
        outTxt=""
        for s in sentences:
            outTxt+=s['text']+"\n"

        return outTxt
            # print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        return transcription_response.output.message
