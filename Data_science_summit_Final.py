#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/datasigntist/deeplearning/blob/master/Introduction_to_Genetic_Computing_2.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# 
# # **Python Challenge**
# 
# Description
# 
# The eight queens puzzle is the problem of placing eight chess queens on an 8×8 chessboard so that no two queens threaten each other; thus, a solution requires that no two queens share the same row, column, or diagonal. The eight queens puzzle is an example of the more general n queens problem of placing n non-attacking queens on an n×n chessboard. (Source : https://en.wikipedia.org/wiki/Eight_queens_puzzle )
# 
# Challenge
# 
# The challenge is to generate one right sequence through Genetic Programming. The sequence has to be 8 numbers between 0 to 7. Each number represents the positions the Queens can be placed. Each number refers to the row number in the specific column
# 
# 0 3 4 5 6 1 2 4
# 
# · 0 is the row number in the column 0 where the Queen can be placed
# 
# · 3 is the row number in the column 1 where the Queen can be placed
# 
# 
# This challenge can have 92 correct sequences. Our challenege is to generate any of those correct sequence.
# 
# 

# In[1]:


import _thread
import time
import random
import numpy as np
from numpy.random import choice
import pandas as pd
import threading 
import sys


global return_code,right_sequence
return_code="0"

def main():
    return_list1=[]
    global return_code
    global right_sequence
    global loop_no
    
    ##### Below variables can be tuned #####
    size_of_chess=8
    mutationRate = 0.01
    totalPopulation = 150
    crossOver = 0.5
    generationCount = 1000
    ########################################
    
    
    return_list1=NQueens(size_of_chess).solve() 

    for index in range(len(return_list1)):
            thread_name=''.join(return_list1[index])
            thread_instance = threading.Thread(target=preprocessing, args=(size_of_chess,thread_name,mutationRate,totalPopulation,crossOver,generationCount,)) 
            thread_instance.start()
    print_str="\n"+" ***** "+ right_sequence +" is the correct sequence which is generated first in generation no :"+loop_no +" ***** "
    print(print_str)
    
def inital_population(totalPopulation,size_of_chess,target,secure_random,alpha_list):     
      populationData1 = []
      fitnessData1 = []
      for outloop in range(totalPopulation):
            randomData = []
            fitnessScore = 0
            for inloop in range(size_of_chess):
                     selectedData = secure_random.choice(alpha_list)
                     if (selectedData == target[inloop]):
                           fitnessScore = fitnessScore + 1
                     randomData.append(selectedData)
            populationData1.append(randomData)
            fitnessData1.append(fitnessScore)
      return (populationData1,fitnessData1)
      


def preprocessing(size_of_chess,thread_name,mutationRate,totalPopulation,crossOver,generationCount): 
      global return_code,loop_no
      
     
      
      secure_random = random.SystemRandom()
      target = thread_name
      alpha_list = [chr(x) for x in range(ord('0'), ord('7')+1 )]
      populationData = []
      fitnessData = []
      populationData,fitnessData=inital_population(totalPopulation,size_of_chess,target,secure_random,alpha_list)
      probabilityDist = []
      for outloop in range(totalPopulation):
            probabilityDist.append(fitnessData[outloop]/len(target))
      probDataFrame = pd.DataFrame({'String':populationData,'FitnessScore':fitnessData,'Probability':probabilityDist})
      probDataFrame = probDataFrame.sort_values(['Probability'],ascending=False)
      probDataFrame = probDataFrame.reset_index(drop=True)
      probDataFrame.head()
      crossover_n_mutation(alpha_list,crossOver,target,generationCount,probDataFrame,thread_name,secure_random,populationData,probabilityDist,fitnessData)


        
        
def crossover_n_mutation(alpha_list,crossOver,target,generationCount,probDataFrame,thread_name,secure_random,populationData,probabilityDist,fitnessData):
      global return_code,right_sequence,loop_no

      crossOverPoint = int(crossOver*len(target))
      #print("\n")
      for loop in range(generationCount):
        if return_code=="1":
              sys.exit(0)
        else:
              draw=[]
              draw.append(probDataFrame[0:1]["String"].values[0])
              draw.append(probDataFrame[1:2]["String"].values[0])
              if (getFitnessScore(draw[0],target)==len(target) | getFitnessScore(draw[1],target)==len(target)):
                    print_str=""
                    print_str0=''.join([elem for elem in draw[0]])
                    print_str1=''.join([elem for elem in draw[1]])
                    #print_str="Final score|draw[0]:"+print_str0+"|FS:"+str(getFitnessScore(draw[0],target))+"|draw[1]:"+print_str1+"|FS:"+str(getFitnessScore(draw[1],target))
                    #print_str="Final score|draw[0]:"+print_str0+"|FS:"+getFitnessScore(draw[0],target)
                    print(print_str)
                    
                    return_code="1"
                    right_sequence=thread_name
                    
                    loop_no=str(loop)
                    #print(probDataFrame.head(30))
                    sys.exit(0)
                    break
              child1 = draw[0][0:crossOverPoint]+draw[1][crossOverPoint:]
              child2 = draw[1][0:crossOverPoint]+draw[0][crossOverPoint:]
              child1[random.randint(0,len(target)-1)] = secure_random.choice(alpha_list)
              child2[random.randint(0,len(target)-1)] = secure_random.choice(alpha_list)
              populationData.append(child1)
              populationData.append(child2)
              fitnessData = []
              totalPopulation = len(populationData)
              for outloop in range(totalPopulation):
                    fitnessScore = getFitnessScore(populationData[outloop],target)
                    fitnessData.append(fitnessScore)
              probabilityDist = []
              for outloop in range(totalPopulation):
                    probabilityDist.append(fitnessData[outloop]/sum(fitnessData))
              probDataFrame = pd.DataFrame({'String':populationData,'FitnessScore':fitnessData,'Probability':probabilityDist})
              probDataFrame = probDataFrame.sort_values(['Probability'],ascending=False)
              probDataFrame = probDataFrame.reset_index(drop=True)
              if return_code=="1":
                    sys.exit(0)
              else:
                    
                    a=""
                    #op_string="\n"+'Thread '+str(thread_name)+' Generation '+str(loop)+' '+' Average Fitness Score '+str(probDataFrame["FitnessScore"].mean())+' '+ ''.join(elem for elem in child1)+' '+str(getFitnessScore(child1,target))+' '+''.join(elem for elem in child2)+' '+str(getFitnessScore(child2,target))
                    op_string="\n"+'Thread '+str(thread_name)+' Generation '+str(loop)+' '+'|Child1 :'+ ''.join(elem for elem in child1)+'|FS of Child1: '+str(getFitnessScore(child1,target))+'|Child2 :'+''.join(elem for elem in child2)+'|FS of Child2 :'+str(getFitnessScore(child2,target))
                    print(op_string)
                    
            
        


    

def getFitnessScore(data,target):

          data = ''.join([elem for elem in data])
          fitnessScore = 0
          for inloop in range(len(target)):
                if (data[inloop] == target[inloop]):
                        fitnessScore = fitnessScore + 1
          #print ("data :",data)
          #print ("target :", target)
          #print ("fitness score :", fitnessScore)
          return fitnessScore


    

def maxProb(probabilityDist):
        probabilityList = [f for f in set(probabilityDist)]
        return (probabilityList[len(probabilityList)-2])


def viewElement(data):
          data = ''.join([elem for elem in data])
          return data

        
        
class NQueens:
    """Generate all valid solutions for the n queens puzzle"""
    def __init__(self,size):
        # Store the puzzle (problem) size and the number of valid solutions
        self.size = size
        self.solutions = 0


    def solve(self):
        """Solve the n queens puzzle and print the number of solutions"""

        final_list=[]
        positions = [-1] * self.size
        self.put_queen(positions, 0,final_list)
        #print("Found", self.solutions, "solutions.")
        return final_list


    def put_queen(self, positions, target_row,final_list):
        """
        Try to place a queen on target_row by checking all N possible cases.
        If a valid place is found the function calls itself trying to place a queen
        on the next row until all N queens are placed on the NxN board.
        """
        # Base (stop) case - all N rows are occupied
        
        if target_row == self.size:
            
            self.show_full_board(positions,final_list)
            # self.show_short_board(positions)
            self.solutions += 1
        else:
            # For all N columns positions try to place a queen
            for column in range(self.size):
                # Reject all invalid positions
                if self.check_place(positions, target_row, column):
                    positions[target_row] = column
                    self.put_queen(positions, target_row + 1,final_list)
        


    def check_place(self, positions, ocuppied_rows, column):
        """
        Check if a given position is under attack from any of
        the previously placed queens (check column and diagonal positions)
        """
        for i in range(ocuppied_rows):
            if positions[i] == column or                 positions[i] - i == column - ocuppied_rows or                 positions[i] + i == column + ocuppied_rows:

                return False
        return True

    def show_full_board(self, positions,final_list):
        """Show the full NxN board"""
        
        small_list=[]
        for row in range(self.size):
            line = ""
            for column in range(self.size):
                if positions[row] == column:
                    #line += "Q "
                    small_list.append(str(column))
                    #print("Pervez :{},{}".format(row,column))
                #else:
                    #line += ". "
                    
            #print(line)
        final_list.append(small_list)
        #print("\n")
        

    def show_short_board(self, positions):
        """
        Show the queens positions on the board in compressed form,
        each number represent the occupied column position in the corresponding row.
        """
        line = ""
        for i in range(self.size):
            line += str(positions[i]) + " "
        #print(line)

if __name__ == "__main__":
    # execute only if run as a script

    main()


# In[ ]:




