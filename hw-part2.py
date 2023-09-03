import concurrent.futures
from multiprocessing import cpu_count
from time import time, sleep


FACTORIZE_LIST = [
    128,
    255,
    99999,
    10651060,
    112272535095,
    1125827059421,
    1122725350952,
    115280095190774,
    115797848077000,
    1099726899285419]


def factorize(number):
    for num in number:
        m = []
        i = 1
        while i**2 <= num:
            if num % i == 0:
                m.append(i)
                if i != num//i:
                    m.append(num // i)
            i += 1
        m.sort()
        print(f"number: {num} == dividers : {m}")
    
def factorize_process(number):
    m = []
    i = 1
    while i**2 <= number:
        if number % i == 0:
            m.append(i)
            if i != number//i:
                m.append(number // i)
        i += 1
    m.sort()
    return m

    



if __name__ == '__main__':
    #Через процессы
    with concurrent.futures.ProcessPoolExecutor(cpu_count()) as executor:
        timer = time()
        for number, dividers in zip(FACTORIZE_LIST, executor.map(factorize_process, FACTORIZE_LIST)):
            print(f"number: {number} == dividers : {dividers}")
        print(f"Done {cpu_count()}-core proccesses in time: {timer - time()}")
        print("\n\n\n")

     
     
    #Через функцию
    timer = time()
    factorize(FACTORIZE_LIST)
    print(f"1 proccess done in time: {timer - time()}")
    

    
    
    
    


#a, b, c, d  = factorize(128, 255, 99999, 10651060)
'''
assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
'''

