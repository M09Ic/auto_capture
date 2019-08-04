import os,subprocess,sys,getopt,time,ctypes



def main(filename):

    f = open(filename,'r',encoding='UTF-8')
    for i in f:
        ip,port = i.split(':')
        print(ip,port)
        subprocess.Popen("start python poc.py -t %s -p %s" % (ip, port), shell=True)
        # subprocess.Popen("start python poc.py -t %s -p %s"%(ip,port),shell=True)

if __name__ == '__main__':

    opts, args = getopt.getopt(sys.argv[1:], '-h-f:', ['help','file'])

    for opt_name, opt_value in opts:
        if opt_name in ('-h', '--help'):
            print('-f 文件路径')


        if opt_name in ('-f', '--file'):
            filename = opt_value
            main(filename)

        # subprocess.Popen("start python p.py", shell=True)






