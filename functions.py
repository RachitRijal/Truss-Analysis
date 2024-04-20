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


def assemble_forces(ENL, NL):
    PD = np.size(NL, 1)
    NoN = np.size(NL, 0)
    FP = []
    #Checking for known Force i.e. applied force
    for i in range(NoN):
        for j in range(PD):
            if ENL[i,PD+j] == 1:
                FP.append(ENL[i,5*PD+j])
    FP = np.vstack([FP]).reshape(-1,1)

    return FP

def assemble_displacement(ENL, NL):
    PD = np.size(NL, 1)
    NoN = np.size(NL, 0)
    UP = []
    #Checking for known Displacement i.e. fixed nodes
    for i in range(NoN):
        for j in range(PD):
            if ENL[i,PD+j] == -1:
                UP.append(ENL[i,5*PD+j])
    UP = np.vstack([UP]).reshape(-1,1)

    return UP

def update_nodes(ENL, U_u, NL, Fu):
    PD = np.size(NL,1)
    NoN = np.size(NL,0)
    DOFs = 0
    DOCs = 0
    for i in range(NoN):
        for j in range(PD):
            #Check for whether displacement or force to be updated
            if ENL[i, PD+j] == 1:
                ENL[i,4*PD+j] = U_u[DOFs]
                DOFs += 1
            else:
                ENL[i,5*PD+j] = Fu[DOCs]
                DOCs += 1

    return ENL
