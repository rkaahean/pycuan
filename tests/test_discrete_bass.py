from pycuan.adopt.discrete_bass import *

N, A = get_bass_model(0.01, 0.02, 100, period=30)
print(N, A)
