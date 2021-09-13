import math
import numpy as np
import random
import matplotlib.pyplot as plt
from numpy.core.numeric import outer
from scipy.interpolate import interp1d
from PIL import Image

N = 640 
variation = int(N*0.1)
# FROM LOWER TO HIGHER
sky_colors = [[132,218,243], [95,208,243], [58,193,242]]
mountain_colors = [[94,45,12], [140,68,18], [205,101,28]]
sun_color = [255, 247, 176]
outer_sun = [249,255,176]
transition_height = int(N * 0.1)
sky_height = int(N*0.15)
# TODO PONER LA CREUETA

def getPoints(lower, upper, pixels=N):
    array = []
    for i in range(int(pixels*0.15)):
        if(i % 5 == 0):
            if len(array) > 0:
                min_range = max(array[-1] - variation, pixels*lower)
                max_range = min(array[-1] + variation, pixels*upper)
                pass
            else: 
                min_range = pixels*lower
                max_range = pixels*upper
            
            array.append(random.randrange(min_range, max_range))
    return array

def plotHorizon(data, interpolation='slinear', length=N):
    plt.axis([0, length, 0, length])
    xnew = np.linspace(0,length, num=length+1, endpoint=True)
    datasets = []
    for plots in data:
        x = np.linspace(0, length, num=len(plots), endpoint=True)
        y = np.array(plots)    
        f2 = interp1d(x, y, kind=interpolation)
        datasets.append(f2(xnew))
#        plt.plot(x, y, 'o', xnew, f2(xnew), '--')

    return np.array(datasets)

def drawSun(array, horizon):
    print("Drawing sun...")
    radius = 50
    outer_radius = radius + 10
    xpos = random.randint(0, N)
    ypos = random.randint(0, int(horizon[xpos]))
    # ALGO falla, no sé el qué, la verdad
    # Pero solo falla de vez en cuando 
    for row in range(ypos - outer_radius, ypos + outer_radius):
        for column in range(xpos - outer_radius, xpos + outer_radius):
            if (row > 0 and column < N and column > 0):
                euclidean = math.sqrt((row - ypos)**2 + (column - xpos)**2) 
                if euclidean <= radius:
                    array[row][column] = sun_color
                elif euclidean >= radius + 5 and euclidean <= outer_radius:
                    array[row][column] = outer_sun
                    
    array[xpos][ypos] = [0,0,0]

    return array

def drawSky(array, horizon):
    print("Drawing sky...")
    ## Generar el cielo, el bluesky
    for column in range(N): 
        #array[horizon][column] = [0, 0, 0]
        
        transition21 = column % 2
        transition10 = column % 2
        
        for row in range(N):   
            # Se pinta el cielo
            if row < horizon[column]:
                if(row < N*0.2):
                    colorincho = sky_colors[2]
                elif(row < N*0.3):
                    # Transicion 2 - 1
                    colorincho = sky_colors[transition21+1]
                    transition21 = abs(transition21 -1)
                elif(row < N*0.5):
                    colorincho = sky_colors[1]
                elif(row < N*0.6):
                    colorincho = sky_colors[transition10]
                    transition10 = abs(transition10 - 1)
                else:
                    colorincho = sky_colors[0]
                array[row][column] = colorincho
            # El horizonte no tiene por qué ser de una sola montaña, 
            # así que no tiene sentido pintarla ahora.
            else:
                break
    return array

def drawCloud(array, horizon): 
    print("Drawing one single cloud")
    cloud_data = getPoints(0.1, 0.7, 600)
    
    cloud_dataset = plotHorizon([cloud_data], 'next', length=400)
    ypos = random.randint(0, N/4)
    xpos = random.randint(0, N)
    for row in range(80):
        if row < N and row < horizon[row]:
            for column in range(len(cloud_dataset[0])):
                if column < N:
                    xpos = int(cloud_dataset[0][column])
                    array[row][xpos] = [255, 255,255]
    return array
                    
def drawMountains(data, array):
    index_mountain = 0
    for mountain in data:
        print("Drawing mountain ", index_mountain , " of 3")
        for column in range(N):
            rowStart = mountain[column]
            for row in range(int(rowStart), N):
                array[row][column] = mountain_colors[index_mountain]
        index_mountain += 1
    return array

def generate(data):
    print("Generating image...")
    horizon = data.min(axis=0)
    array = np.zeros([N, N, 3], dtype=np.uint8)
    array[:,:] = [255, 255, 255]
    
    array = drawSky(array, horizon)
    array = drawSun(array, horizon)
    drawCloud(array, horizon)
    array = drawMountains(data, array)

    image = Image.fromarray(array, "RGB")
    image.show()
    return image

def main():
    data = []
    print("Generating plots for mountains:")
    for i in range(random.randint(1, 3)):
        print(i, " of 3")
        data.append(getPoints( 0.3 + 0.15* i, 0.9, N))

    horizons = plotHorizon(data)
    
    
    image = generate(horizons)

if __name__ == '__main__': 
    main()