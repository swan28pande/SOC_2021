import numpy as np
import random

global numPlayers,numQuestions
numPlayers = 100
numQuestions = 10000

def sigmoid(x):
	return 1.0/(1.0+np.exp(-x))

def verdict(x):
	p=sigmoid(x)
	sample=random.random()
	if(sample<p):
		return True
	else:
		return False

def generate_testcase():
	p_skills = np.random.uniform(-3.0,3.0,numPlayers)
	q_difficulty = np.random.uniform(-3.0,3.0,numQuestions)
	cheater_id = random.randint(0,numPlayers-1)
	testcase = np.zeros((numPlayers,numQuestions))
	for player_id in range(numPlayers):
		for question_id in range(numQuestions):
			if(player_id!=cheater_id):
				diff = (p_skills[player_id]-q_difficulty[question_id])
				if(verdict(diff)):
					testcase[player_id][question_id]=1
			else:
				cheat = (random.random()<0.5)
				if(cheat):
					testcase[player_id][cheater_id]=1
				else:
					diff = (p_skills[player_id]-q_difficulty[question_id])
					if(verdict(diff)):
						testcase[player_id][question_id]=1
	return testcase,cheater_id
