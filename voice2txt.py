import oss2,os
from datetime import datetime
import dashscope
import json
from urllib import request
from http import HTTPStatus
from dashscope.audio.asr import (Recognition,RecognitionResult)
ak = os.environ.get('OSS_ACCESS_KEY')
ask = os.environ.get('OSS_SECRET_KEY')
dashscope.api_key = os.environ.get('DASHSCOPE_AK')
auth=oss2.Auth(ak,ask)

def upload_file(object_name):
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
