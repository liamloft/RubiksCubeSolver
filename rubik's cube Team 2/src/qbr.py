
import anvil.server
import socket
import array as arr
from rubik_solver import utils
import combiner
from combiner import combine
state = 0

anvil.server.connect("UQWJL2TCOXKCXG3FUX3MJB74-2TGLLKQ2WUWJIOZN")
@anvil.server.callable

def start():
    from sys import exit as Die
    try:
        import sys
        import kociemba
        import argparse

        from combiner import combine
        from video import webcam
        from normalizer import normalize
    except ImportError as err:
        Die(err)


    class Qbr:

        def __init__(self, normalize, language):
            self.humanize = normalize
            self.language = (language[0]) if isinstance(language, list) else language

        def run(self):
            global state
            state         = webcam.scan()
            if not state:
                print('\033[0;33m[QBR SCAN ERROR] Ops, you did not scan in all 6 sides.')
                print('Please try again.\033[0m')
                Die(1)

            unsolvedState = combine.sides(state)
            try:
                algorithm     = kociemba.solve(unsolvedState)
                length        = len(algorithm.split(' '))
            except Exception as err:
                #print('\033[0;33m[QBR SOLVE ERROR] Ops, you did not scan in all 6 sides correctly.')
                #print('Please try again.\033[0m')
                Die(1)

            #print('-- SOLUTION --')
            #print('Starting position:\n    front: green\n    top: white\n')
            #print(algorithm, '({0} moves)'.format(length), '\n')

            if self.humanize:
                manual = normalize.algorithm(algorithm, self.language)
                for index, text in enumerate(manual):
                    print('{}. {}'.format(index+1, text))
            Die(0)

    if __name__ == '__main__':
        # define argument parser.
        parser = argparse.ArgumentParser()
        parser.add_argument('-n', '--normalize', default=False, action='store_true',
                help='Shows the solution normalized. For example "R2" would be: \
                        "Turn the right side 180 degrees".')
        parser.add_argument('-l', '--language', nargs=1, default='en',
                help='You can pass in a single \
                        argument which will be the language for the normalization output. \
                        Default is "en".')
        args = parser.parse_args()

        # run Qbr with its arguments.
        Qbr(
            args.normalize,
            args.language
        ).run()

        
@anvil.server.callable        
def setCubeState():

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(("localhost", 2500))

	# Open and read text file with cube state information
	# NOTE: This is just an example to show the interaction with the cube simulator,
	#		user must assemble the packets with the output of the vision algorithm

	#creates a handle from the text file given by the vision system of the current
	#	state of the cube:
	file = open("simulador.txt", "r")
	str = file.read()
	lines = str.split("\n")

	# Assemble Set Cube State Command packet (see manual)
	command = 0xFA
	payloadLen = 48
	packet = arr.array('B', [0] * (payloadLen + 2))
	packet[0] = command
	packet[1] = payloadLen
	for idx in range(1, len(lines)):
		packet[idx + 1] = int(lines[idx][-1])

	# Write packet to cube simulator
	client.send(packet)
	client.close()

@anvil.server.callable
def solve_for_Moves():
        #Takes current state of the cube in the form of string:
	cube = combine.sides(state)
	#Gets the needed moves for solving the cube:
	solution = utils.solve(cube, 'Kociemba')
	solution_list = list()
	solution_converted = list()
	#converts the items of the solution list of movements into strings
	for line in solution:
	  movement = str(line)
	  solution_list.append(movement)
	#prepares the strings of the solution list to be entered into simulator:
	for line in solution_list:
	  if line == 'U': x = 'D'
	  elif line == 'U2': x = 'D2'
	  elif line == "U'": x = "D'"

	  elif line == 'F': x = 'R'
	  elif line == 'F2': x = 'R2'
	  elif line == "F'": x = "R'"

	  elif line == 'R': x = 'F'
	  elif line == 'R2': x = 'F2'
	  elif line == "R'": x = "F'"

	  elif line == 'B': x = 'L'
	  elif line == 'B2': x = 'L2'
	  elif line == "B'": x = "L'"

	  elif line == 'L': x = 'B'
	  elif line == 'L2': x = 'B2'
	  elif line == "L'": x = "B'"

	  elif line == 'D': x = 'U'
	  elif line == 'D2': x = 'U2'
	  elif line == "D'": x = "U'"
	  else: x = 'error'
	  solution_converted.append(x)
#From the prepared solution, it converts it into a text file for simulator:
	with open('your_file.txt', 'w') as f:
		for item in solution_converted[:-1]:
			f.write("%s\n" % item)
		f.write("%s" % solution_converted[-1])

@anvil.server.callable
def setCubeMoves():

	# Dictionary of cube moves
	movesDict = {
		"U":	0,
		"U2": 	1,
		"U'": 	2,
		"B": 	3,
		"B2": 	4,
		"B'": 	5,
		"R": 	6,
		"R2": 	7,
		"R'": 	8,
		"F": 	9,
		"F2": 	10,
		"F'": 	11,
		"L": 	12,
		"L2":	13,
		"L'":	14,
		"D": 	15,
		"D2":	16,
		"D'":	17
	}

	# Connect TCP/IP client to localhost in port 2500
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(("localhost", 2500))

	# Open and read text file with cube moves information
	# NOTE: This is just an example to show the interaction with the cube simulator,
	#		user must assemble the packets with the output of the cube solution algorithm
	#file = open("movesSolution.txt", "r")
	file = open("your_file.txt", "r")
	str = file.read()
	lines = str.split("\n")
	nMoves = len(lines) # number of moves detected in text file

	# Assemble Set Cube Moves Command packet (see manual)
	command = 0xFB
	payloadLen = nMoves
	packet = arr.array('B', [0] * (payloadLen + 2))
	packet[0] = command
	packet[1] = payloadLen
	for idx in range(0, nMoves):
		cubeMove = lines[idx]
		packet[idx + 2] = movesDict[cubeMove]

	# Write packet to cube simulator
	client.send(packet)
	client.close()

anvil.server.wait_forever()
