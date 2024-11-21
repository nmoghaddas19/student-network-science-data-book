import networkx as nx
import numpy as np
import pickle
import sys
print(sys.executable)
from mpi4py import MPI

def zombie_model_agent_based(G, alpha=0.2, beta=0.1, delta = 0.2, gamma = 0.2, n_seeds=5, n_iter=500):
    """
    Does an agent-based rumor model simulation on a given network.
    
    Inputs:
    --------------
    G: networkx graph object
    alpha: parameter that governs conversion from ignorant to spreader; float in range (0, 1.0]
    beta: parameter that governs conversion from spreader to stifler; float in range (0, 1.0]
    n_seeds: number of initial infected nodes; int.
    n_iter: number of iterations to run the model for; int.

    Returns: 
    -------------
    States of each node at each time step
    """    
    state_dict = {n: 'susceptibles' for n in G.nodes}
    seed_nodes = np.random.choice(list(G.nodes), n_seeds, replace=False)
    for seed in seed_nodes:
        state_dict[seed] = 'zombie'
    
    state_dict_list = []
    for i in range(n_iter):
        state_dict_list.append(state_dict)
        state_dict_new = state_dict.copy()
        susceptibles = [n for n, state in state_dict.items() if state == 'susceptible']
        zombies = [n for n, state in state_dict.items() if state == 'zombies']
        bittens = [n for n, state in state_dict.items() if state == 'bittens']
        deads = [n for n, state in state_dict.items() if state == 'deads']
        perma_deads = [n for n, state in state_dict.items() if state == 'perma_deads']


        for susceptible in susceptibles:
            for neighbor in G.neighbors(susceptible):
                if state_dict[neighbor] == 'zombies' and np.random.uniform() <= beta*alpha:
                    state_dict_new[neighbor] = 'perma-deads'
                else:
                    state_dict_new[susceptible] = 'bittens'
        for bitten in bittens:
            if np.random.uniform() <= delta:
                state_dict_new[bitten] = 'deads'
        for dead in deads:
            if np.random.uniform() <= gamma:
                state_dict_new[dead] = 'zombies'
            
        state_dict = state_dict_new
    
    return state_dict_list

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
G = nx.watts_strogatz_graph(2500, 6, 0.05)

pickle.dump(zombie_model_agent_based(G), open('zombie_model_agent_based_process_{}.pkl'.format(str(rank)), 'wb'))
