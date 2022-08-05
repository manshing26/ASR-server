from ASR.file_function.file_func import path_checker, slash, select_bg, output_auto
from ASR.file_function.logic_func import GetLogfbank, GetMfcc_slim, GetMfcc

path_checker = path_checker
slash = slash

#################################### model parameter ####################################
GPU = True
VERSION = 'verR1.1c'
DOUBLE_INPUT = False
FEATURE_EXTRACTION = GetLogfbank
FEATURE_LENGTH = FEATURE_EXTRACTION.FEATURE_LENGTH
FEATURE_EXTRACTION_2= GetMfcc
FEATURE_LENGTH_2 = FEATURE_EXTRACTION_2.FEATURE_LENGTH
FEATURE_BG, FEATURE_BG_2 = select_bg(FEATURE_LENGTH,FEATURE_LENGTH_2)
LABEL_MAX_STRING_LENGTH = 64
AUDIO_LENGTH = 1600
OUTPUT_MODE = "C" ## 1424:"A", 409:"B", 4788:"C"
OUTPUT_LENGTH = 200
OUTPUT_SIZE, DICT = output_auto(OUTPUT_MODE) ## Number of pinyins --> 1424/409/4788(word)
VAD_PADDING = 5

## For training ##
AUDIO_SPEED = 1
SPEED_CHANGE = "constant" # stage 1: constant | stage 2: range (!ft_PINYIN need to set constant)
ADD_NOISE = False
SAVE_STEP = 500
BATCH_SIZE = 5
DATASETS = ['st-cmds','aishell','aidatatang','magicdata','primewords']

#################################### path parameter ####################################
data_path = "/audio/"

abs_path_prefix = "/wd/"
speech_model_folder = "/saved_model/"
DL_language_model_folder = "/saved_model/"

cnn_trained_folder = ''
test_audio = data_path + 'CoLdStArT.wav'
dict_folder = abs_path_prefix + 'ASR/dict/'
bg_folder = abs_path_prefix + 'ASR/bg/'
pinyin_dict = dict_folder + 'dict.txt'
word_dict = dict_folder + 'word2.txt'

#################################### TFX parameter ####################################

USE_TFX = True
TFX_ASR_PATH = "http://sv:8501/v1/models/asr:predict"
TFX_LM_PATH = "http://sv:8501/v1/models/lm:predict"