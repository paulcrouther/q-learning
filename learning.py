import random

class QLearning:
    def __init__(self, actions, epsilon, alpha, gamma):
        self.q = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def chooseAction(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            q = [self.getQ(state, a) for a in self.actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = self.actions[i]
        return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)

    def printQ(self):
        keys = self.q.keys()
        states = list(set([a for a,b in keys]))
        actions = list(set([b for a,b in keys]))
        
        dstates = ["".join([str(int(t)) for t in list(tup)]) for tup in states]
        print (" "*4) + " ".join(["%8s" % ("("+s+")") for s in dstates])
        for a in actions:
            print ("%3d " % (a)) + \
                " ".join(["%8.2f" % (self.getQ(s,a)) for s in states])

    def printV(self):
        keys = self.q.keys()
        states = [a for a,b in keys]
        statesX = list(set([x for x,y in states]))
        statesY = list(set([y for x,y in states]))

        print (" "*4) + " ".join(["%4d" % (s) for s in statesX])
        for y in statesY:
            maxQ = [max([self.getQ((x,y),a) for a in self.actions])
                    for x in statesX]
            print ("%3d " % (y)) + " ".join([ff(q,4) for q in maxQ])
        
import math
def ff(f,n):
    fs = "{:f}".format(f)
    if len(fs) < n:
        return ("{:"+n+"s}").format(fs)
    else:
        return fs[:n]