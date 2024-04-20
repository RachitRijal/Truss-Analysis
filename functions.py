import numpy as np
import math

def assign_BCs(NL, ENL):
    PD = np.size(NL,1)
    NoN = np.size(NL,0)

    DOFs = 0  #Degree of Freedom
    DOCs = 0  #Degree of Constraints

    for i in range(0, NoN):
        for j in range(0, PD):
            if ENL[i,PD+j] == -1:
                DOCs -= 1
                ENL[i, 2*PD+j] = DOCs
            else:
                DOFs += 1
                ENL[i, 2*PD+j] = DOFs

    for i in range(0, NoN):
        for j in range(0, PD):
            if ENL[i, 2*PD+j] < 0:
                ENL[i, 3*PD+j] = abs(ENL[i,2*PD+j]) + DOFs
            else:
                ENL[i, 3*PD+j] = abs(ENL[i, 2*PD+j])

    DOCs = abs(DOCs)

    return (ENL, DOFs, DOCs)


def assemble_stiffness(ENL, EL, NL, E, A):
    NoE = np.size(EL,0)
    NPE = np.size(EL,1)
    PD = np.size(NL,1)
    NoN = np.size(NL,0)

    K = np.zeros([NoN*PD, NoN*PD])

    for i in range(0, NoE):
        nl = EL[i,0:NPE]    #extracts nodes of an element
        k = element_stiffness(nl, ENL, E, A)
        for r in range(NPE):
            for p in range(PD):
                for q in range(NPE):
                    for s in range(PD):
                        row = ENL[nl[r]-1, p+3*PD]
                        column = ENL[nl[q]-1, s+3*PD]
                        value = k[r*PD+p,q*PD+s]
                        
                        K[int(row)-1, int(column)-1] += value
    return K

def element_stiffness(nl, ENL, E, A):
    X1 = ENL[nl[0]-1,0]
    Y1 = ENL[nl[0]-1,1]
    X2 = ENL[nl[1]-1,0]
    Y2 = ENL[nl[1]-1,1]

    L = math.sqrt((X1-X2)**2+(Y1-Y2)**2)

    C = (X2-X1)/L
    S = (Y2-Y1)/L

    k = (E*A/L)* np.array([[C*C, C*S, -C*C, -C*S],
                           [C*S, S*S, -C*S, -S*S],
                           [-C*C, -C*S, C*C, C*S],
                           [-C*S, -S*S, C*S, S*S]])
    
    return k