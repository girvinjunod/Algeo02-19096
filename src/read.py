import re
import string
import requests
import numpy as np
import glob
import errno

def read_first(path_to_folder):
    kal = []
    nama = path_to_folder
    try:
        with open(nama, encoding='utf-8') as f:
            i = 0
            temp = f.read(1)
            while((temp!='.') and (i<=150)):
                i += 1
                temp = f.read(1)
        with open(nama, encoding='utf-8') as f:
            temp = f.read(i+1)
            kal.append(temp)
    except IOError as exc: #Not sure what error this is
        if exc.errno != errno.EISDIR:
            raise
    return kal[0]

path = "../test/apple.txt"
print(read_first(path))
