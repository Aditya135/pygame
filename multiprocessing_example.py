import multiprocessing as mp
import random,string

output = mp.Queue()

def rand_string(output):
    r_string = ''.join(random.sample(string.ascii_letters+string.digits,5))
    output.put(r_string)

processes = [mp.Process(target = rand_string,args=(output)) for i in range(5)]

for p in processes:
    p.start()

for p in processes:
    p.join()

result = [output.get() for p in processes]
print(result)