import unicodecsv as csv
import multiprocessing as mp

def file_to_list(file):
    data = []
    print(file)
    f = open(file, 'rbU')
    contents = csv.reader(f.read().splitlines())
    count = 0
    try:
        for c in contents:
            count += 1
            data.append(c)
    except Exception as e:
        print("count",count)
        raise e

    return data
    
def important_lists(data):
    urls = []
    likes = []
    followers = []
    count = 0
    try:
        for d in data:
            count += 1
            urls.append(d[0])
            likes.append(int(d[1]))
            followers.append(int(d[7]))
    except Exception as e:
        print("count", count)
        raise e
    return urls, likes, followers

def divide_work(fx, first, last, n, args):
    print('Dividing {1} work amongst {0} workers'.format(n, fx.__name__))
    jobs = []
    chunksize = (last - first) // n
    for i in range(n):
        start = first + i * chunksize
        end = first + (i + 1) * chunksize
        p = mp.Process(target=fx, args=(start,end)+args)
        jobs.append(p)
        p.start()
    for p in jobs:
        p.join()
        