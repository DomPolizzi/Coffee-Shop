import os


def find_recur(f):
    if "node_modules" not in f: 
        #print(f)
        if os.path.isdir(f):
            for n in os.listdir(f):
                abspath = os.path.join(f, n)
                find_recur(abspath)
        else:
            try:
                with open(f, encoding='utf-8') as o:
                    if "Create Drink" in o.read():
                        print(f)
            except:
                pass

find_recur(os.getcwd())