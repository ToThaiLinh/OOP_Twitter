import math

class Graph:
    def __init__(self, numNode, dumpingFactor=0.85, convergence=1e-6, maxLoop=100):
        self.dumpingFactor = dumpingFactor
        self.convergence = convergence
        self.maxLoop = maxLoop
        self.numNode = numNode
        self.numOut = [0] * numNode
        self.nodeIn = [[] for _ in range(numNode)]
        self.pr = [1.0 / numNode] * numNode 
        #khởi tạo pr[i] = 1/numNode

    def add_arc(self, fromNode, toNode):
        if toNode not in self.nodeIn[fromNode]:
            self.nodeIn[toNode].append(fromNode)
            self.numOut[fromNode] += 1

    def computePagerank(self):
        diff = 1
        numIteration = 0

	#lặp đến khi diff hội tụ hoặc số lần lặp ít hơn maxLoop
        while diff > self.convergence and numIteration < self.maxLoop:
            old_pr = self.pr[:]
            diff = 0
            sumZeroNodePr = sum(old_pr[i] for i in range(self.numNode) if self.numOut[i] == 0) #sum pagerank những đỉnh không có cạnh ra

            for i in range(self.numNode):
                rank = (1 - self.dumpingFactor) / self.numNode
                rank += self.dumpingFactor * sumZeroNodePr / self.numNode
                rank += self.dumpingFactor * sum(old_pr[j] / self.numOut[j] for j in self.nodeIn[i] if self.numOut[j] > 0) #pr[a] = pr[b]/numOut[b] + pr[c]/numOut[c] + ... + pr[z]/numOut[z] 
                diff += abs(rank - old_pr[i])
                self.pr[i] = rank

            numIteration += 1
            #print(f"Iteration {numIteration}: {self.pr}") if diff > self.convergence else None

    def printPagerank(self):
        for i, rank in enumerate(self.pr):
            print(f"Node {i} = {rank}")


n = 4 
graph = Graph(n)


graph.add_arc(0, 1)
graph.add_arc(0, 2)
graph.add_arc(1, 2)
graph.add_arc(2, 0)
graph.add_arc(2, 3)
graph.add_arc(3, 0)

graph.computePagerank()
graph.printPagerank()