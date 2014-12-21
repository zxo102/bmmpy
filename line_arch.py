def distance(a,b):
    l=sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
    return l
def line_two_bottom(m,a,b):
    x1=a[0];y1=a[1];z1=a[2]
    x2=b[0];y2=b[1];z2=b[2]
    if x1-x2==0:k=10000000
    else:
        k=(y1-y2)/(x1-x2)
    if k==0:k=0.0000001    
    bva=[((k**2*x1 - k*sqrt(m**2*(k**2 + 1)) + x1)/(k**2 + 1), y1 + sqrt(m**2*(k**2 + 1))/(k**2 + 1)), ((k**2*x1 + k*sqrt(m**2*(k**2 + 1)) + x1)/(k**2 + 1), y1 - sqrt(m**2*(k**2 + 1))/(k**2 + 1))]
    bvb=[((k**2*x2 - k*sqrt(m**2*(k**2 + 1)) + x2)/(k**2 + 1), y2 + sqrt(m**2*(k**2 + 1))/(k**2 + 1)), ((k**2*x2 + k*sqrt(m**2*(k**2 + 1)) + x2)/(k**2 + 1), y2 - sqrt(m**2*(k**2 + 1))/(k**2 + 1))]
     
    return [[bva[0][0],bva[0][1],z1],[bva[1][0],bva[1][1],z1]],[[bvb[0][0],bvb[0][1],z2],[bvb[1][0],bvb[1][1],z2]]

def line_additional_bottom(w,a,btv,b):
    x1=a[0];y1=a[1];z1=a[2]
    x2=b[0];y2=b[1];z2=b[2]
    x3=btv[0];y3=btv[1];z3=btv[2]
    if x1-x2==0:k=10000000
    else:
        k=(y1-y2)/(x1-x2)
    if k==0:k=0.0000001
    jv=[((k**2*x3 - k*sqrt(w**2*(k**2 + 1)) + x3)/(k**2 + 1), y3 + sqrt(w**2*(k**2 + 1))/(k**2 + 1)), ((k**2*x3 + k*sqrt(w**2*(k**2 + 1)) + x3)/(k**2 + 1), y3 - sqrt(w**2*(k**2 + 1))/(k**2 + 1))]
    a01=[jv[0][0],jv[0][1],z3];a02=[jv[1][0],jv[1][1],z3]
    l01=distance(a01,a);l02=distance(a01,b)
    l03=distance(a02,a);l04=distance(a02,b)
    l1=l01+l02;l2=l03+l04
    if l1>l2:
        return a02
    else:
        return a01

def arch_two_bottom(w,lv,cv,rv):
    m=w/2
    xl=lv[0];yl=lv[1];zl=lv[2]
    xc=cv[0];yc=cv[1];zc=cv[2]
    xr=rv[0];yr=rv[1];zr=rv[2]
    if xl-xc==0:k1=10000000
    else:
        k1=(yl-yc)/(xl-xc)
    if k1==0:k1=0.0000001
    if xr-xc==0:k2=10000000
    else:
        k2=(yr-yc)/(xr-xc)
    if k2==0:k2=0.0000001
    al=[((k1*xl - sqrt(k1**2*m**2*(k1**2 + 1))/(k1**2 + 1))/k1, yl - sqrt(k1**2*m**2*(k1**2 + 1))/(k1**2 + 1)), ((k1*xl + sqrt(k1**2*m**2*(k1**2 + 1))/(k1**2 + 1))/k1, yl + sqrt(k1**2*m**2*(k1**2 + 1))/(k1**2 + 1))]
    ar=[((k2*xr - sqrt(k2**2*m**2*(k2**2 + 1))/(k2**2 + 1))/k2, yr - sqrt(k2**2*m**2*(k2**2 + 1))/(k2**2 + 1)), ((k2*xr + sqrt(k2**2*m**2*(k2**2 + 1))/(k2**2 + 1))/k2, yr + sqrt(k2**2*m**2*(k2**2 + 1))/(k2**2 + 1))]
    bvl=[];bvr=[]
    bvl.append([al[0][0],al[0][1],zl])
    bvl.append([al[1][0],al[1][1],zl])
    bvr.append([ar[0][0],ar[0][1],zr])
    bvr.append([ar[1][0],ar[1][1],zr])
    return bvl,bvr

def arch_additional_bottom(w,lv,cv,btv,rv=[]):
    x1=lv[0];y1=lv[1];z1=lv[2]
    x2=cv[0];y2=cv[1];z2=cv[2]
    x3=btv[0];y3=btv[1];z3=btv[2]
    if x3-x2==0:k=10000000
    else:
        k=(y3-y2)/(x3-x2)
    if k==0:k=0.0000001
    jv=[((k*x3 - sqrt(k**2*w**2*(k**2 + 1))/(k**2 + 1))/k, y3 - sqrt(k**2*w**2*(k**2 + 1))/(k**2 + 1)), ((k*x3 + sqrt(k**2*w**2*(k**2 + 1))/(k**2 + 1))/k, y3 + sqrt(k**2*w**2*(k**2 + 1))/(k**2 + 1))]
    a1=[jv[0][0],jv[0][1],z3];a2=[jv[1][0],jv[1][1],z3]
    l1=distance(a1,lv);l2=distance(a2,lv)
    if l1>l2:
        return a2
    else:
        return a1
def line_arch(h,w,llv01,lrv01,alv02,acv02,arv02):
    #alv02 交点
    m=w/2;faces=[];verts=[]
    xl01=llv01[0];yl01=llv01[1];zl01=llv01[2]
    xr01=lrv01[0];yr01=lrv01[1];zr01=lrv01[2]
    xal=alv02[0];yal=alv02[1];zal=alv02[2]
    xac=acv02[0];yac=acv02[1];zac=acv02[2]
    xar=arv02[0];yar=arv02[1];zar=arv02[2]
    if xl01-xr01==0:k1=10000000
    else:
        k1=(yl01-yr01)/(xl01-xr01)
    if k1==0:k1=0.0000001
    #下面计算直线和弧线两端bottom点：
    bvl01,bvr01=line_two_bottom(m,llv01,lrv01)
    bvl02,bvr02=arch_two_bottom(w,alv02,acv02,arv02)
    #下面计算直线左边，弧线右边拱形分点：
    a01=distance(bvl01[0],acv02);a02=distance(bvl01[1],acv02)
    if a01>a02:
        loopl01,archl01=create3CenteredArch(h,bvr01[1],bvr01[0])
    else:
        loopl01,archl01=create3CenteredArch(h,bvr01[0],bvr01[1])
    a03=distance(bvr02[0],llv01);a04=distance    
    
