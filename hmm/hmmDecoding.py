class hmmDecoding:
    def __init__(self):
        self.PI=(0.8,0.2)
        self.A=(
            (0.6,0.3),
            (0.4,0.5)
        )
        self.B=(
            (0.2,0.5),
            (0.4,0.4),
            (0.4,0.1)
        )
    
    def decoding(self,observation):
        o=[observation[i]-1 for i in range(3)]
        v=[
            [0,0],
            [0,0],
            [0,0],
        ]
        bt=[
            [0,0],
            [0,0],
            [0,0]
        ]
        #initialization
        v[0][0]=self.B[o[0]][0]*self.PI[0]
        v[0][1]=self.B[o[0]][1]*self.PI[1]
        bt[0][0]=0
        bt[0][1]=0
        #recursion
        for t in range(1,3):
            for j in range(2):
                for i in range(2):
                    tt=v[t-1][i]*self.A[i][j]*self.B[o[t]][j]
                    if tt>v[t][j] :
                        v[t][j]=tt
                        bt[t][j]=i
        #termination
        p=max(v[2][0],v[2][1])
        def _fqt():
            if v[2][0]>v[2][1]:
                return 0
            return 1
        qt=_fqt()
        path=[]
        path.insert(0,qt)
        for t in range(1,-1,-1):
            path.insert(0,bt[t][path[0]])
        return path

if __name__=="__main__":
    hmm=hmmDecoding()
    path=hmm.decoding((3,1,3))
    print(path)