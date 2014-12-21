import pickle
F=open(r'C:\Users\Administrator\Desktop\roadway_auto_generation\auto_plane\datafile1.pkl','rb')
def test(e):
    for i in xrange(len(e[1][1.1][1])):
       print(e[1][1.1][1][i])
e=pickle.load(F)
#print(e[1][1.1])
test(e)
