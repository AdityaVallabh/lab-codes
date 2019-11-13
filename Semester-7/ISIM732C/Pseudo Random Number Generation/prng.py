import argparse
import random

# Parser for command-line arguments ;)
parser = argparse.ArgumentParser(description='Custom Random Number Generator')
parser.add_argument('-a', '--lambdaa', type=int, default=259, help='Lambda')
parser.add_argument('-b', '--mu', type=int, default=10**9 + 7, help='Mu')
parser.add_argument('-m', '--modulo', type=int, default=2**31 + 1, help='Modulo')
parser.add_argument('-s', '--seed', type=int, default=10**4 + 7, help='Seed')
parser.add_argument('-t', '--numbers', type=int, default=1000, help='Numbers')
args = parser.parse_args()

class RandomGenerator:
    '''Random Number Generator for Additive, Multiplicative and Mixed Congruence methods'''

    # Assigning default parameters
    default_l = args.lambdaa
    default_u = args.mu
    default_m = args.modulo
    default_seed = args.seed

    # Initialize paramters
    def __init__(self, l=default_l, u=default_u, m=default_m, seed=default_seed):
        self.seed = seed
        self.l = l
        self.u = u
        self.m = m

    # Multiplicative Congruence Parameters
    def multiplicative(self, l=default_l, seed=default_seed):
        self.seed = seed
        self.l = l
        self.u = 0

    # Additive Congruence Parameters
    def additive(self, u=default_u, seed=default_seed):
        self.seed = seed
        self.l = 1
        self.u = u

    # Mixed Congruence Parameters
    def mixed(self, l=default_l, u=default_u, seed=default_seed):
        self.seed = seed
        self.l = l
        self.u = u

    # Returns a random number each time
    def getNum(self):
        num = self.seed
        self.seed = (self.l * self.seed + self.u)%self.m
        return num/(self.m-1)

# Chi-Square test with 10 classes
def chiSquare(nums, classes=10):
    classCounts = [0] * classes
    for num in nums:
        c = int(num * classes)
        classCounts[c] += 1
    exp = len(nums)//classes
    sqe = 0.0
    for count in classCounts:
        sqe += ((count - exp)**2)/exp
    return sqe

# Writes a list of numbers to a file
def writeFile(nums, name):
    with open(name, 'w') as f:
        f.write(str(nums))

# Generates random numbers and performs chi-square test
def do(getRandomNumber, name):
    nums = [getRandomNumber() for _ in range(args.numbers)]
    res = chiSquare(nums)
    writeFile(nums, name + '.txt')
    print(name + ':', res)

# Main method
def main():
    randomGen = RandomGenerator()
    randomGen.additive()
    do(randomGen.getNum, 'Additive')
    randomGen.multiplicative()
    do(randomGen.getNum, 'Multiplicative')
    randomGen.mixed()
    do(randomGen.getNum, 'Mixed')
    random.seed(randomGen.default_seed)
    do(random.random, 'MersenneTwister')

if __name__ == '__main__':
    main()
