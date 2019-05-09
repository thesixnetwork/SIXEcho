from __future__ import print_function
from datasketch import MinHash
import deepcut
import time

class Client(object):
    def __init__(self,api_key=None,host_url=None):
        print("init")
        self.api_key = api_key
        self.host_url = host_url
        self.array_words = []
        self.min_hash = MinHash(num_perm=128)
    
    def digest(self):
        print("digest")

    def generate(self,str=None,fpath=None):
        if fpath:
            self.load_file(fpath)  
        else:
            words = self.tokenize(str)
            for d in words:
                self.min_hash.update(d.encode('utf8'))

    def upload(self):
        print("upload")

    def tokenize(self,str):
        words = deepcut.tokenize(str)
        new_words = [word for word in words if word != ' ']
        return new_words

    def load_file(self,fpath):
        print()
        # for x in range(0,100):
        #     self.printProgressBar(x,100)
        #     time.sleep(0.1)
        # print("process")

    def printProgressBar (self,iteration, total, prefix = 'Progress', suffix = 'Complete', decimals = 1, length = 100, fill = '='):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = "\r")
        # Print New Line on Complete
        if iteration == total: 
            print()