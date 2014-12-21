from math import *
def handle_arch(leftv,circlecenter,rightv):
    cv=[]
    xl=leftv[0]; yl=leftv[1]; zl=leftv[2]
    x0=circlecenter[0]; y0=circlecenter[1]; z0=circlecenter[2]
    xr=rightv[0]; yr=rightv[1]; zr=rightv[2]
    r=sqrt(pow((xl-x0),2)+pow((yl-y0),2))#计算半径
    div01=12#将弧形等分成12份
    radian=acos((2*r**2-(xl-xr)**2-(yl-yr)**2)/(2*r**2))
    if radian > pi/2:
        div01=18
    alpha=radian/div01
    if xl-x0==0: k=100000000#return {'error'},{'error'}
    else:
        k=(yl-y0)/(xl-x0)#左端点与圆心连线的斜率
    #fd=[((k**2*x0 - k*y0 + k*y4 - k*sqrt(k**2*r**2 - k**2*y0**2 + 2*k**2*y0*y4 - k**2*y4**2 - 2*k*x0*y0 + 2*k*x0*y4 + 2*k*x4*y0 - 2*k*x4*y4 + r**2 - x0**2 + 2*x0*x4 - x4**2) + x4)/(k**2 + 1), (k**2*y4 - k*x0 + k*x4 + y0 + sqrt(k**2*r**2 - k**2*y0**2 + 2*k**2*y0*y4 - k**2*y4**2 - 2*k*x0*y0 + 2*k*x0*y4 + 2*k*x4*y0 - 2*k*x4*y4 + r**2 - x0**2 + 2*x0*x4 - x4**2))/(k**2 + 1)), ((k**2*x0 - k*y0 + k*y4 + k*sqrt(k**2*r**2 - k**2*y0**2 + 2*k**2*y0*y4 - k**2*y4**2 - 2*k*x0*y0 + 2*k*x0*y4 + 2*k*x4*y0 - 2*k*x4*y4 + r**2 - x0**2 + 2*x0*x4 - x4**2) + x4)/(k**2 + 1), (k**2*y4 - k*x0 + k*x4 + y0 - sqrt(k**2*r**2 - k**2*y0**2 + 2*k**2*y0*y4 - k**2*y4**2 - 2*k*x0*y0 + 2*k*x0*y4 + 2*k*x4*y0 - 2*k*x4*y4 + r**2 - x0**2 + 2*x0*x4 - x4**2))/(k**2 + 1))]
    for i in range(div01):
          if i==0: continue
          else:
            m=r*cos(i*alpha)
            jv=[((k*x0 - sqrt(k**2*m**2*(k**2 + 1))/(k**2 + 1))/k, y0 - sqrt(k**2*m**2*(k**2 + 1))/(k**2 + 1)), ((k*x0 + sqrt(k**2*m**2*(k**2 + 1))/(k**2 + 1))/k, y0 + sqrt(k**2*m**2*(k**2 + 1))/(k**2 + 1))]
            #jv=[[sqrt(m**2/(k**2+1))+x0, y0+k*sqrt(m**2/(k**2+1))], [-sqrt(m**2/(k**2+1))+x0, y0-k*sqrt(m**2/(k**2+1))]]
            a=(jv[0][0]-xl)**2+(jv[0][1]-yl)**2-(jv[1][0]-xl)**2-(jv[1][1]-yl)**2
            if a>0:
                x4=jv[1][0]
                y4=jv[1][1]
            else:
                x4=jv[0][0]
                y4=jv[0][1]
            print(x4,y4)    
            fd=[((k**2*x0 - k*y0 + k*y4 - k*sqrt(k**2*r**2 - k**2*y0**2 + 2*k**2*y0*y4 - k**2*y4**2 - 2*k*x0*y0 + 2*k*x0*y4 + 2*k*x4*y0 - 2*k*x4*y4 + r**2 - x0**2 + 2*x0*x4 - x4**2) + x4)/(k**2 + 1), (k**2*y4 - k*x0 + k*x4 + y0 + sqrt(k**2*r**2 - k**2*y0**2 + 2*k**2*y0*y4 - k**2*y4**2 - 2*k*x0*y0 + 2*k*x0*y4 + 2*k*x4*y0 - 2*k*x4*y4 + r**2 - x0**2 + 2*x0*x4 - x4**2))/(k**2 + 1)), ((k**2*x0 - k*y0 + k*y4 + k*sqrt(k**2*r**2 - k**2*y0**2 + 2*k**2*y0*y4 - k**2*y4**2 - 2*k*x0*y0 + 2*k*x0*y4 + 2*k*x4*y0 - 2*k*x4*y4 + r**2 - x0**2 + 2*x0*x4 - x4**2) + x4)/(k**2 + 1), (k**2*y4 - k*x0 + k*x4 + y0 - sqrt(k**2*r**2 - k**2*y0**2 + 2*k**2*y0*y4 - k**2*y4**2 - 2*k*x0*y0 + 2*k*x0*y4 + 2*k*x4*y0 - 2*k*x4*y4 + r**2 - x0**2 + 2*x0*x4 - x4**2))/(k**2 + 1))]
            
            b=(fd[0][0]-xr)**2+(fd[0][1]-yr)**2-(fd[1][0]-xr)**2-(fd[1][1]-yr)**2
            if b>0:
                x3=fd[1][0]
                y3=fd[1][1]
                z3=zl
            else:
                x3=fd[0][0]
                y3=fd[0][1]
                z3=zl
            cv.append([x3,y3,z3])
    return cv#, radian      
a=[0,0,0]
b=[5,-4,0]
#radian=pi/2
c=[5,3,0]
if __name__ == "__main__":
    out=handle_arch(a,b,c)
    print(out) 

                
    
