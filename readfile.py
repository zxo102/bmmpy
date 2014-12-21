#这是什么文件
def readfile():
    file=open(r'C:\Users\Administrator\Desktop\12345.txt','rt')
    info_list=[]
    vert_info=file.readlines()
    for i in range(len(vert_info)):
        if len(vert_info[i].strip())!=0:
            ni =vert_info[i].split()
            info_list.append(ni)
    return info_list
if __name__ == "__main__":
    out=readfile()
    print(out)
            
