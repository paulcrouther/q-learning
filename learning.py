import random

class QLearning:
    def __init__(self, actions, epsilon, alpha, gamma, iterations):
        self.q = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        self.iterations = iterations

    def deacreasing_parameter(self):
        if(self.alpha > 0):
            self.alpha = self.alpha - self.alpha/self.iterations
        else:
            self.alpha = 0
        if(self.epsilon > 0):        
            self.epsilon = self.epsilon - self.epsilon/self.iterations
        else:
            self.epsilon = 0

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)
        #return self.q.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

    def learnQ(self, state, action, reward, value):    
        oldv = self.q.get((state, action), None) 
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)
            print self.q[(state, action)]
    
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

