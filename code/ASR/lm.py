import config
from ASR.file_function.file_func import slash, GetSymbolList, GetWordList
from ASR.file_function.logic_func import *

import os
import json
import requests
import numpy as np
from typing import List
from tensorflow.keras.models import load_model

class LM():

    def __init__(self,ver=config.VERSION) -> None:

        self.slash = slash()
        self.list_symbol = GetSymbolList(config.pinyin_dict)
        self.list_word = GetWordList(config.word_dict)

        self.model_name = config.DL_language_model_folder + f'{ver}/language_model'

        if config.USE_TFX == False:
            assert os.path.isdir(self.model_name)
            self.base_model = load_model(self.model_name)

    def get_base_predict(self,input_):

        if config.USE_TFX:
            i = {"instances":input_.tolist()}
            r = requests.post(config.TFX_LM_PATH, data=json.dumps(i))
            base_pred = json.loads(r.text)['predictions']
            base_pred = np.array(base_pred)
        else:
            base_pred = self.base_model.predict(x=input_)

        return base_pred

    def Predict(self,pinyin_list:List) -> str:

        pinyin_list_num = [to_list_index(pinyin,self.list_symbol) for pinyin in pinyin_list]

        x = np.zeros((1,64,),dtype=np.int32)
        x[0,:] = self.list_symbol.index('_')
        x[0,0:(len(pinyin_list_num))] = pinyin_list_num

        result = self.get_base_predict(input_=x)[0]
        idx = np.argmax(result,axis=1)
        sentence = [self.list_word[i] for i in idx]
        sentence = [sen for sen in sentence if sen != '_']

        return (''.join(sentence))

    def Predict_from_ASR(self,asr_result):

        for slice in asr_result:
            slice['Text'] = self.Predict(slice['Text'])
        
        return asr_result