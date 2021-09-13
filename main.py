import math
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from PIL import Image

N = 640 
variation = int(N*0.1)
# FROM LOWER TO HIGHER
sky_colors = [[132,218,243], [95,208,243], [58,193,242]]
transition_height = int(N * 0.1)
sky_height = int(N*0.15)
def getPoints():

    array = []
    x = []
    for i in range(int(N*0.1)):
        if(i % 5 == 0):
            x.append(i)
            if len(array) > 0:
                min_range = max(array[-1] - variation, N * 0.1)
                max_range = min(array[-1] + variation, N * 0.9)
                pass
            else: 
                min_range = N*0.2
                max_range = N*0.8
            
            array.append(random.randrange(min_range, max_range))
    return array

def plotHorizon(data):
    plt.axis([0, N, 0, N])
    x = np.linspace(0, N, num=len(data), endpoint=True)
    y = np.array(data)
    
    f2 = interp1d(x, y, kind='cubic')
    xnew = np.linspace(0,N, num=N+1, endpoint=True)
    # plt.plot(x, y, 'o', xnew, f2(xnew), '--')

    return f2(xnew)

def generate(data):
    array = np.zeros([N, N, 3], dtype=np.uint8)
    array[:,:] = [255, 255, 255]
    
    ## Generar el cielo, el bluesky
    for row in range(len(data) -1):
        horizon = int(data[row])
        array[horizon][row] = [0, 0, 0]
        
        transition21 = 8 if row % 2 == 0 else 4
        # Vamos de abajo a arriba
        for column in range(N-1):   
            depth = 1
            if column < horizon:
                # Hay que comprobar donde está el puntero para saber qué color pintar
                if(column < N*0.2):
                    colorincho = sky_colors[2]
                elif(column < N*0.3):
                    # Transicion 2 - 1

                    colorincho = sky_colors[2 if transition21 > 4 else 1]
                    transition21 -= 1
                    if transition21 < 0:
                        transition21 = 8 if row % 2 == 0 else 4

                else:
                    colorincho = sky_colors[0]
                array[column][row] = colorincho
    image = Image.fromarray(array, "RGB")
    image.show()
    return image

def main():
    data = getPoints()
    horizon_arr = plotHorizon(data)
    print(horizon_arr)
    image = generate(horizon_arr)

if __name__ == '__main__': 
    main()