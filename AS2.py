import os
import time
import shutil
import threading
from multiprocessing import Pool
import queue

file_queue = queue.Queue()
thread_list = []
process_list = []
root_dir = os.getcwd()
dataset_dir = root_dir + "/processes_threads/"
new_dir = root_dir + "/copy_results/"

filenames = os.listdir(dataset_dir)
filepaths = []
for filename in filenames:
    filepaths.append(dataset_dir + filename)


def copy_simple():
    for filename in os.listdir(dataset_dir):
        if filename.endswith(".txt"):
            shutil.copy(dataset_dir + filename, new_dir + filename)

def copy_t():
    while True:
        file_name = file_queue.get()
        if file_name is None:
            break
        shutil.copy(file_name, new_dir)
        file_queue.task_done()

def copy_p(file_name):
    shutil.copy(file_name, new_dir)
    print(file_name)

def thread_test(workers):
    for i in range(workers):
        t = threading.Thread(target=copy_t)
        t.start()
        thread_list.append(t)
    for file_name in filenames:
        file_queue.put(dataset_dir + file_name)
        
    file_queue.join()

    for i in range(workers):
        file_queue.put(None)
    for t in thread_list:
        t.join()

def process_test(workers):
    p = Pool(workers)
    p.map(copy_p, filepaths)
    p.close()
    p.join()

start = time.time()
#copy_simple()
#6.3741278648376465
#real	0m6.437s
#user	0m0.702s
#sys	0m3.200s

#thread_test(4)
#5.597242593765259
#real	0m5.668s
#user	0m2.267s
#sys	0m6.486s

process_test(4)
#5.328332185745239
#real	0m5.407s
#user	0m1.241s
#sys	0m6.055s

end = time.time()
print(end - start)
