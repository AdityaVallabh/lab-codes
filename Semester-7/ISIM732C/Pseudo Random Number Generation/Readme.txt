Pseudo-Random Number Generator - IIT2016517

Additive Congruence Method:
lambda = 1
mu     = 1000000007
mod    = 2147483649
seed   = 10007
chi = 0.1

Multiplicative Congruence Method:
lambda = 259
mu     = 0
mod    = 2147483649
seed   = 10007
chi = 5.0

Mixed Congruence Method:
lambda = 259
mu     = 1000000007
mod    = 2147483649
seed   = 10007
chi = 3.14

In-built Generator (Python) == Mersenne Twister
seed = 10007
chi = 11.34

Usage: prng.py [-h] [-a LAMBDAA] [-b MU] [-m MODULO] [-s SEED] [-t NUMBERS]
Custom Random Number Generator
optional arguments:
  -h, --help      Show this help message and exit
  -a, --lambdaa   Lambda
  -b, --mu        Mu
  -m, --modulo    Modulo
  -s, --seed      Seed
  -t, --numbers   Numbers

Command to run: "$ python prng.py"