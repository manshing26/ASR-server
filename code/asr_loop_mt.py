import os
import io
import threading
import requests
import logging
from time import sleep

from db import Session
from model import record_table,record_table_temp
import config
from ASR.asr import asr_e2e,asr_double
from ASR.lm import LM
from ASR.file_function.file_func import AudioDecodeError

# os.environ['OPENBLAS_NUM_THREADS']='300'

log_format = '%(asctime)s %(levelname)-9s %(message)s'
logging.basicConfig(level=logging.WARNING,format=log_format)

class NoTask(Exception):
    pass

class ThreadPool():
    def __init__(self):
        if config.OUTPUT_MODE == "A":
            if config.DOUBLE_INPUT:
                self.asr = asr_double(config.VERSION)
            else:
                pass

            self.lm = LM(config.VERSION) # only for mode A model
        
        elif config.OUTPUT_MODE == "C":
            if config.DOUBLE_INPUT:
                pass
            else:
                self.asr = asr_e2e(config.VERSION)

        self.lock = threading.Lock()

    def run(self,temp_row,return_dic):
        
        try:
            # Download audio
            r = requests.get(url=temp_row.file_address, allow_redirects=True, timeout=15)

            s = io.BytesIO(r.content) # doesn't store audio

            # ASR
            with self.lock:
                result = self.asr.RecognizeSpeech_FromFile(s)
                if config.OUTPUT_MODE == "A":
                    result = self.lm.Predict_from_ASR(asr_result = result)
            
            if len(str(result)) >= 4000:
                result == "['ResultTooLong']"
            else:
                result = str(result)
        
        except requests.ReadTimeout:
            result = "['requests.ReadTimeoutError']"
            logging.error(f'requests.ReadTimeout Error for {temp_row.file_address}')

        except requests.ConnectionError as e:
            result = "['requests.ConnectionError']"
            logging.error(f'requests.Connection Error for {temp_row.file_address}\n{e}')

        except FileNotFoundError:
            result = "['FileNotFoundError']"
            logging.error(f'File Not Found Error for {temp_row.file_address}')

        except AudioDecodeError:
            result = "['AudioDecodeError']"
            logging.error(f'Audio Decode Error for {temp_row.file_address}')
        
        except Exception as e:
            result = "['unknownError']"
            logging.error(f'Unknown Error for {temp_row.file_address}\n{e}')

        finally:
            return_dic[temp_row.ticket] = result

def threading_function(sema,pool,temp_row,return_dic):
    with sema:
        pool.run(temp_row,return_dic)

if __name__=="__main__":

    pool = ThreadPool()
    sema = threading.Semaphore(5)

    while True:
        try:
            session = Session()
            return_dic = {}

            # query temp table
            results = session.query(record_table_temp).all()
            len_result = len(results)

            if len_result == 0: # early return
                raise NoTask
            elif len_result >= 200:
                results = results[:200]

            threading_ls = [None]*len_result
            
            for idx,temp_row in enumerate(results):
                threading_ls[idx] = threading.Thread(target=threading_function,args=(sema,pool,temp_row,return_dic))
                threading_ls[idx].start()

            for idx in range(len_result):
                threading_ls[idx].join()

            for r in results: # delete temp row
                session.delete(r)

            logging.debug(f'{return_dic}')

            update = session.query(record_table).filter(record_table.ticket.in_(return_dic.keys())).all()

            for u in update:
                logging.debug(f'{u.ticket}')
                u.finished = True
                u.result = return_dic[u.ticket]

            session.commit()

        except NoTask:
            logging.info('No new record')

        except Exception as e:
            logging.error(f'Exception: {e}')

        finally:
            session.close()
            sleep(int(os.environ['SLEEP_TIME']))
