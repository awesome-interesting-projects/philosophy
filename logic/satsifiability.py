"""
Check for satisfiability.
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
        i = cls() # instance of first argument to class method file
        for line in file: # for each line in the file
            line = line.strip() # remove unnecessary trailing charactres 
            if len(line) > 0 and not line.startswith("#"):
                i.addClause(line)
        return i 
