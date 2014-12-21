#文本说明：极其特殊情况下---如果交点在与主巷端点相同或者靠的太近，且角度比较大，导致支巷宽的边缘线超过此段主巷，则把交点稍微往另外一边移动一点。
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
def line_line(h,w,llv01,lrv01,llv02,lrv02,N='fuck'):#前面的为主巷，后为支巷。并且按照点的先后顺序，先左后右，支巷是先交点。
    m=w/2;faces=[];verts=[]
    xl01=llv01[0];yl01=llv01[1];zl01=llv01[2]
    xr01=lrv01[0];yr01=lrv01[1];zr01=lrv01[2]
    xl02=llv02[0];yl02=llv02[1];zl02=llv02[2]
    xr02=lrv02[0];yr02=lrv02[1];zr02=lrv02[2]
    if xl01-xr01==0:k1=10000000
    else:
        k1=(yl01-yr01)/(xl01-xr01)
    if k1==0:k1=0.0000001
    if xl02-xr02==0:k2=10000000
    else:
        k2=(yl02-yr02)/(xl02-xr02)
    if k2==0:k2=0.0000001
    #下面计算每条直线两段的两个bottom点
    bvl01,bvr01=line_two_bottom(m,llv01,lrv01)
    bvl02,bvr02=line_two_bottom(m,llv02,lrv02)
    #下面计算拱形分点
    a1=distance(bvr01[0],lrv02);a2=distance(bvr01[1],lrv02)
    if a1>a2:
        loopr01,archr01=create3CenteredArch(h,bvr01[1],bvr01[0])
    else:
        loopr01,archr01=create3CenteredArch(h,bvr01[0],bvr01[1])
    a3=distance(lrv01,bvr02[0]);a4=distance(lrv01,bvr02[1])
    if a3>a4:
        loopr02,archr02=create3CenteredArch(h,bvr02[1],bvr02[0])
    else:
        loopr02,archr02=create3CenteredArch(h,bvr02[0],bvr02[1])
    #下面计算交点
    jv01=[];jv02=[];g01=int((len(archr01)+1)/2)
    for i in range(g01):
        x1=archr01[i][0];y1=archr01[i][1];z1=archr01[i][2]
        x2=archr02[i][0];y2=archr02[i][1];z2=archr02[i][2]
        jv01.append([(k1*x1 - k2*x2 - y1 + y2)/(k1 - k2), k1*(-k2*x2 + y2 + k2*(k1*x1 - y1)/k1)/(k1 - k2),z1])
    ls1=archr02[:]
    ls1.reverse()
    for i in range(g01):
        x1=archr01[i][0];y1=archr01[i][1];z1=archr01[i][2]
        x2=ls1[i][0];    y2=ls1[i][1];    z2=ls1[i][2]
        jv02.append([(k1*x1 - k2*x2 - y1 + y2)/(k1 - k2), k1*(-k2*x2 + y2 + k2*(k1*x1 - y1)/k1)/(k1 - k2),z1])
    bvr1=[];bvl1=[];bvl2=[]#三方的bottom点
    bvr1.append(jv01[0])
    bvl1.append(jv02[0])
    a5=distance(jv01[0],lrv02);a6=distance(jv02[0],lrv02)
    if a5>=a6:
       bvl2.append(jv02[0])
    else:
        bvl2.append(jv01[0])
    bvr1.append(line_additional_bottom(w,llv01,jv01[0],lrv01))
    bvl1.append(line_additional_bottom(w,llv01,jv02[0],lrv01))
    bvl2.append(line_additional_bottom(w,llv02,bvl2[0],lrv02))
    #下面计算三方的拱形点
    loopr1,archr1=create3CenteredArch(h,bvr1[0],bvr1[1])
    loopl1,archl1=create3CenteredArch(h,bvl1[0],bvl1[1])
    #loopl2,archl2=create3CenteredArch(h,bvl2[0],bvl2[1])
    #下面分四部分形成模型
    loop1=[];arch1=[];loop2=[];arch2=[];loop3=[];arch3=[];loop4=[];arch4=[]
    loop5=[];arch5=[];loop6=[];arch6=[];loop7=[];arch7=[];loop8=[];arch8=[]
    #section 1
    arch1=archr1[32:]
    arch1.append(bvr1[0])
    
    for i in range(len(arch1)):
        loop1.append(i+len(verts))
    verts.extend(arch1)
    arch2=archl1[32:]
    arch2.append(bvl1[0])
    for i in range(len(arch2)):
        loop2.append(i+len(verts))
    verts.extend(arch2)
    faces.extend(createFaces(loop1,loop2))
    #section 2
    arch3=archr1[:33]
    for i in range(len(arch3)):
        loop3.append(i+len(verts))
    verts.extend(arch3)    
    arch4=jv01[:]
    for i in range(len(arch4)):
        loop4.append(i+len(verts))
    verts.extend(arch4)
    faces.extend(createFaces(loop3,loop4))
    #section 3
    arch5=jv02[:]
    for i in range(len(arch5)):
        loop5.append(i+len(verts))
    verts.extend(arch5)
    arch6=archl1[:33]
    for i in range(len(arch6)):
        loop6.append(i+len(verts))
    verts.extend(arch6)
    faces.extend(createFaces(loop5,loop6))
    #section 4
    jv02re=jv02[:]
    jv02re.reverse()#翻转jv02re
    jv02re.pop(0)
    arch7=jv01[:]
    arch7.extend(jv02re)
    for i in range(len(arch7)):
        loop7.append(i+len(verts))
    verts.extend(arch7)
    a8=(bvl2[0][1]-arch7[0][1])*(bvl2[1][0]-arch7[len(arch7)-1][0])
    a9=(bvl2[1][1]-arch7[len(arch7)-1][1])*(bvl2[0][0]-arch7[0][0])
    if '%.6f'%a8=='%.6f'%a9:
      loopl2,archl2=create3CenteredArch(h,bvl2[0],bvl2[1])
    else:
        loopl2,archl2=create3CenteredArch(h,bvl2[1],bvl2[0])
    arch8=archl2[:]
    for i in range(len(arch8)):
        loop8.append(i+len(verts))
    verts.extend(arch8)
    faces.extend(createFaces(loop7,loop8,closed=True))
    me = bpy.data.meshes.new("joint_%s"%N)
    ob = bpy.data.objects.new("joint_%s"%N, me)
    bpy.context.scene.objects.link(ob)
    me.from_pydata(verts,[],faces)
    me.update(calc_edges=True)
    return bvl1,bvr1,bvl2
    
    
        
        
        
    
    
    
    
