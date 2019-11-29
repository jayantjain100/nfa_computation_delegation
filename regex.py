""" Uses functions from AutomataTheory.py to convert a regex into an epsilon-NFA    """
from AutomataTheory import *
from nfa import NFA
import sys

def regex_to_nfa(inp):
    # Takes an regex as input (inp) and returns an epsilon-NFA corresponding to the same regex
    # Used logic and parsers from AutomataTheory.py 
    nfaObj = NFAfromRegex(inp)
    nfa = nfaObj.getNFA()
    transitions = {}
    for fromstate, tostates in nfa.transitions.items():
        for state in tostates:
            for char in tostates[state]:
                ch = char
                if (char == ":e:"):
                    ch = 'eps'
                if ch in transitions:
                    if (fromstate-1) in transitions[ch]:
                        transitions[ch][fromstate-1] = (transitions[ch][fromstate-1]+[state-1]) 
                    else:
                        transitions[ch][fromstate-1] = [state-1]
                else:
                    transitions[ch] = {(fromstate-1) : [state-1]}
    sigma = [x for x in nfa.language]
    startstate = nfa.startstate - 1
    finalstates = [x-1 for x in nfa.finalstates]
    return NFA(len(nfa.states), sigma, transitions, finalstates, startstate)