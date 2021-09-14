import math
import numpy as np
import random
import matplotlib.pyplot as plt
from numpy.core.numeric import outer
from scipy.interpolate import interp1d
from PIL import Image
import sys 

N = 640 
variation = int(N*0.1)
# FROM LOWER TO HIGHER
sky_colors = {"day": [[132,218,243], [95,208,243], [58,193,242]], 
              "night": [[138, 74, 216], [88, 74, 216], [60, 70, 190]]}
mountain_colors = {"desert": [[94,45,12], [140,68,18], [205,101,28]], 
                    "green": [[17,31,36],[24,45,51], [48,90,102]]}
sun_color = [255, 247, 176]
ground_color = [79, 164, 71]
earth_color = [[168, 87, 49], [146, 82, 46]]
outer_sun = [249,255,176]
transition_height = int(N * 0.1)
sky_height = int(N*0.15)
cloud_circles = 10
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
            
            array.append(random.randrange(int(min_range), int(max_range)))
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

    return array

def drawSky(array, horizon, time):
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
                    colorincho = sky_colors[time][2]
                elif(row < N*0.3):
                    # Transicion 2 - 1
                    colorincho = sky_colors[time][transition21+1]
                    transition21 = abs(transition21 -1)
                elif(row < N*0.5):
                    colorincho = sky_colors[time][1]
                elif(row < N*0.6):
                    colorincho = sky_colors[time][transition10]
                    transition10 = abs(transition10 - 1)
                else:
                    colorincho = sky_colors[time][0]
                array[row][column] = colorincho
            # El horizonte no tiene por qué ser de una sola montaña, 
            # así que no tiene sentido pintarla ahora.
            else:
                break
    return array

def drawStars(array, horizon):
    for i in range(20):
        ystar = random.randint(40, int(horizon.min()))
        xstar = random.randint(20, N - 20)
        for x in range(4):
            for y in range(4):
                array[ystar + y][xstar + x] = [255, 255, 255]
    return array

def drawCloud(array, horizon): 
#   TODO, PERO EXTREMO TODO
    print("Drawing one single cloud")
    width = 100
    height = 30
    radius = 20
    ycloud = random.randint(0, int(horizon.min()))
    xcloud = random.randint(20, N - 20)
    for i in range(cloud_circles):
        ypos = random.randint(ycloud, ycloud + height)
        xpos = random.randint(xcloud, xcloud + width)
        for row in range(ypos - radius, ypos + radius):
            for column in range(xpos - radius, xpos + radius):
                if row > ycloud + 10: 
                    continue
                if (row > 0 and column < N and column > 0):
                    euclidean = math.sqrt((row - ypos)**2 + (column - xpos)**2) 
                    if euclidean <= radius:
                        array[row][column] = [255, 255, 255]

    return array
                    
def drawMountains(data, array, biome):
    index_mountain = 2
    for mountain in data:
        print("Drawing mountain ", index_mountain  + 1 , " of 3")
        for column in range(N):
            rowStart = mountain[column]
            for row in range(int(rowStart), N):
                array[row][column] = mountain_colors[biome][index_mountain]
        index_mountain -= 1
    return array

def drawGround(array):
    print("Drawing the soil")
    ground = getPoints(0.05, 0.1, N)
    ground_dataset = plotHorizon([ground], interpolation="nearest", length=N)[0]
    
    max_point = N - int(ground_dataset.max()) - 20
    for column in range(N):
        point = N - int(ground_dataset[column])          

        while point > max_point:
            array[point][column] = ground_color
            point-=1
        point = N - int(ground_dataset[column])
        while point < N:
            if point >N - ground_dataset[column] + 25:
                colorincho = earth_color[0]
            else:
                colorincho = earth_color[1]
            array[point][column] = colorincho
            point+=1
    return array

def generate(data, biome, time):
    print("Generating image...")
    print("Biome: ", biome)
    print("Time: ", time)
    horizon = data.min(axis=0)
    array = np.zeros([N, N, 3], dtype=np.uint8)
    array[:,:] = [255, 255, 255]
    
    array = drawSky(array, horizon, time)
    array = drawSun(array, horizon) if time == "day" else drawStars(array, horizon)
    if time == "day":
        for i in range(random.randint(1, 5)):
            array = drawCloud(array, horizon)
    array = drawMountains(data, array, biome)
    if biome == "green":
        array = drawGround(array)
    


    image = Image.fromarray(array, "RGB")
    # image.show()
    return image

def main():
    data = []
    biome = ["desert", "green"]
    time = ["night", "day"]
    print("Generating plots for mountains:")
    for i in range(3):
        data.append(getPoints( 0.3 + 0.15* i, 0.9, N))

    horizons = plotHorizon(data)
    
    
    image = generate(horizons, biome[random.randint(0,1)], time[random.randint(0,1)])
    # image = generate(horizons, "green", "day")
    image.show()
        

if __name__ == '__main__': 
    main()