class hmmLikelihood:
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
    def likelihood(self,observation):
        o=observation
        alpha=[
            [0,0],
            [0,0],
            [0,0]
        ]
        for j in range(2):
            alpha[0][j]=self.PI[j]*self.B[o[0]-1][j]
        for t in range(1,3):
            for j in range(2):
                alpha[t][j]=( alpha[t-1][0]*self.A[0][j] + alpha[t-1][1]*self.A[1][j] )*self.B[o[t]-1][j]
        likelihood=alpha[2][0]+alpha[2][1]
        return likelihood
        
if __name__=="__main__":
    observation=(3,1,3)
    h=hmmLikelihood()
    likelihood=h.likelihood(observation)
    print(likelihood)