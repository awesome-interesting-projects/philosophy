from collections import deque

"""
Check for satisfiability.


We define SAT class and the following function solve as a method of determining if there is an interpretation that
satisfies a given Boolean formula. If the variables of a given Boolean formula can be consistently replaced by the 
values True or False in such a way that the formula evluates to True, then is is satisfiable.
"""

class SAT(object):
    """
    Basic and somewhat efficient way of solving satisfiability using Python. 
    """
    def __init__(self):
        self.variables = []
        self.var_table = [] # table of variables
        self.clauses = []

    def addClause(self, line):
        """
        Add a clause to our list of clauses for each literal in the line of the file.
        """
        clause = []
        for i in line.split(): # for each literal in the line
            n = 1 if i.startswith("~") else 0 # n means negated 
            a = i[n:] # a is the variable
            if a not in self.var_table: # if the variable is not in our variable table
                self.var_table[a] = len(self.variables)
                self.variables.append(a)
            enc = self.var_table[a] << 1 | n # bitwise shift to create enc encoded literal
            clause.append(enc)
       self.clauses.append(tuple(set(clause)))
    
    @classmethod
    def file(cls, file):
        """
        Open the file and add our clauses from each line one by one.
        """
        i = cls() # instance of first argument to class method file
        for line in file: # for each line in the file
            line = line.strip() # remove unnecessary trailing charactres 
            if len(line) > 0 and not line.startswith("#"):
                i.addClause(line)
        return i

    def litToString(self, l):
        """
        Convert a literal l to a string.
        """ 
        if l & 1: # literal has the value of 1 boolean
             s = "~" # negate
        else:
             s = ""
        return s + self.variables[l >> 1] # convert literal to a bitwise operator 1 and add to our string s
    
    def cToString(self, c):
        """
        Convert clause c to string
        """
        return "".join(self.litToString(i) for i in c)
    
    def aToSTring(self, a, brief=False, s=""):
        """
        Convert an assignment a to a string. Can use in brief form or with starting string s.
        """ 
        lit = [] # list of literals
        for i, j in ((i,j) for i, j in zip(a, self.variables) if j.startswith(s): # for the variable values of our starting with string s
            if i == 0 and not brief:
                lit.append("~" + j)
            elif i:
                lit.append(j)
        return " ".join(lit)
       

def watchlist(i):
    """
    For an instance i, set up a watchlist. This lets each clause watch one of its literals so that all
    watched literals are either not yet assigned or they have been assigned true.
    """
    w = [deque() for _ in range(2 * len(i.variables))] # w is our watchlist 
    for c in i.clauses:
         w[c[0]].append(c) # keep track of which literal the clause is watching
    return w

def updateW(i, w, f, a):
    """
    Update the watchlist w after literal f was just assigned False by making any clause
    watching f something else. Return False if it's impossible (a clause contradicted the
    current assignment). i is our instance, w is the watchlist, f is the "flase_literal",
    and a is the assignment.
    """
    while w[f]:
        c = w[f][0] # get the clause c
        fa = False # found alternative
        for al in c: # for each alternative in clause
            b = al >> 1 # bitwise operator
            c = alternative & 1 # if alternative is True
            if a[b] is None or a[b] == a ^ 1: # if there is no assignment in bitwise form
                fa = True # we have found an alternative
                del w[f][0] # delete the false literal
                break
        if not fa:  
            return False
    return True


def solve(i, w, a, d):
    """
    Solve for satisfiability with number of variables d up to n-1. Assume variables 0,...,d-1 are 
    already assigned. Generate satisfying assignments and return them. i is an instance, w is the   
    watchlist, and a is the assignment. 
    """
    n = len(i.variables)
    s = [0] * n # state
    while True: # iterate until we find all solutions
        if d == n:
            yield a 
            d -= 1
            continue
    tr = False # we haven't tried an assignment
    if d == len(i.variables):
        yield a # when our instance's variables are accounted for by the variable array d
        return 
    for b in [0, 1]: # for each bitwise operator
        if (s[d] >> b) & 1 == 0: # if the state of h
            tr = True
            s[d] != 1 << b 
            a[d] = b
            if not updateW(i, w, (d<<1) | b, a): # if we can't update our watchlist with the corresponding false literal
                a[d] = None
        else:
            d += 1 
            break 
   if not tr:
        if d == 0:
            return # no solutions
        else:
            s[d] = 0 
            a[d] = None
            d -= 1

"""
Often difficult problems can be reduced to SAT.
"""
