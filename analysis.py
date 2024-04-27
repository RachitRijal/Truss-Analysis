import numpy as np
import pandas as pd
from functions import*

#NodeList = NumberOfNodes*ProblemDimension
NL = np.array([[0,0],
               [1,0],
               [0.5,1]])

#ElementList = NumberOfElements*NodesPerElements         
EL = np.array([[1,2],
               [2,3],
               [3,1]])

#BoundaryConditions:Dirichlet or Neumann (x-axis,y-axis) => -1:fixed, 1:movable
DorN = np.array([[-1,-1],
                 [1,-1],
                 [1,1]])

#Force
Fu = np.array([[0,0],
               [0,0],
               [0,-20]])

#Displacement
U_u = np.array([[0,0],
                [0,0],
                [0,0]])

#Young's Modulus
E = 10**6

#Crosssection Area
A = 0.01

#ProblemDimension
PD = np.size(NL, 1) #1 to extract the column
#Number of Nodes
NoN = np.size(NL, 0)

#Extended Node List
ENL = np.zeros([NoN, 6*PD])

ENL[:,0:PD] = NL[:,:]
ENL[:,PD:2*PD] = DorN[:,:]

(ENL, DOFs, DOCs) = assign_BCs(NL,ENL)

K = assemble_stiffness(ENL, EL, NL, E, A)


ENL[:,4*PD:5*PD] = U_u[:]
ENL[:,5*PD:6*PD] = Fu[:]

U_u = U_u.flatten()
Fu = Fu.flatten()

Fp = assemble_forces(ENL, NL)
Up = assemble_displacement(ENL, NL)


#Fragmentation of Global Stiffness Matrix
K_UU = K[:DOFs,:DOFs]
K_UP = K[:DOFs,DOFs:]
K_PU = K[DOFs: ,:DOFs]
K_PP = K[DOFs:,DOFs:]

F = Fp - np.matmul(K_UP, Up)
U_u = np.matmul(np.linalg.inv(K_UU),F)
Fu = np.matmul(K_PU,U_u) + np.matmul(K_PP,Up)

ENL = update_nodes(ENL, U_u, NL, Fu)


df = pd.DataFrame(ENL)
df = df.to_string()