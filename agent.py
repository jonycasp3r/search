#!/usr/bin/python3
'''
Very simple example how to use gym_wrapper and BaseAgent class for state space search 
@author: Zdeněk Rozsypálek, and the KUI-2019 team
@contact: svobodat@fel.cvut.cz
@copyright: (c) 2017, 2018, 2019
'''

import time
import kuimaze
import os
import random
from queue import *
import kuimaze.maze

def heuristiccost(cost,a,b): #heuristic function of the currently searched vertex supplemented with the path cost
        x=abs(a[1][0]-b[1][0])
        y=abs(a[1][1]-b[1][1])
        return x+y+cost


class Agent(kuimaze.BaseAgent):
    '''
    Simple example of agent class that inherits kuimaze.BaseAgent class 
    '''


    def __init__(self, environment):
        self.environment = environment
    def find_path(self):
        observation = self.environment.reset() 
        goal = [0,observation[1][0:2]]
        start = [0,observation[0][0:2]]
        frontier=PriorityQueue()
        cost={}
        queue={}
        queue[start[1]]=0
        cost[start[1]]=0 #cost of the start is 0
        queue[goal[1]]=0
        frontier.put(start) #first position to the frontier
        print(start,"start")
        
        while frontier.not_empty:
            node=frontier.get()
            if node[1]==goal[1]: #if its goal position, searching is done
                break
            
            neighbours=self.environment.expand(node[1]) #initialization of all the neighbors
            for neighbour in neighbours:
                neighbour=neighbour[::-1] #neighbour.reverse()
                cost_now=neighbour[0]+cost[node[1]]
                
                
                if neighbour[1] not in cost or cost[neighbour[1]]>cost_now: #if the cost of the route to the peak is less than the currently best one, or the peak has not yet been explored
                    cost[neighbour[1]]=cost_now
                    neighbour[0]=heuristiccost(cost_now, goal, neighbour)
                    frontier.put(neighbour)
                    queue[neighbour[1]]=node[1]
                    
        if queue[goal[1]]!=0:

                q=[]
                node2=goal[1]
                while True:
                        if start[1]==node2: #if the searched position is the current position, it ends
                            q.append(start[1])
                            q=q[::-1] #q.reverse()
                            return q
                        q.append(node2)
                        node2=queue[node2]

        else:
                return None
                
if __name__ == '__main__':

    MAP = 'maps/normal/normal3.bmp'
    MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), MAP)
    GRAD = (0, 0)
    SAVE_PATH = False
    SAVE_EPS = False

    env = kuimaze.InfEasyMaze(map_image=MAP, grad=GRAD)       # For using random map set: map_image=None
    agent = Agent(env) 

    path = agent.find_path()
    print(path)
    env.set_path(path)          # set path it should go from the init state to the goal state
    if SAVE_PATH:
        env.save_path()         # save path of agent to current directory
    if SAVE_EPS:
        env.save_eps()          # save rendered image to eps
    env.render(mode='human')
    time.sleep(3)
