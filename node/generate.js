const { createCanvas } = require('canvas')

const N = 640
const variation = parseInt(N * 0.1)
const width = N
const height = N
const heightSky = parseInt(N*0.25)
const heightTransition = parseInt(N*0.1)
const sky_colors = {"day": ['#3AC1F2', '#5FD0F3','#84DAF3'],
                    "night": ['#3C46BE','#584AD8','#8A4AD8']}
const mountain_colors = {"desert": ['#CD651C','#8C4412','#5E2D0C'],
                         "green": ['#305A66', '#182D33', '#111F24']}
const canvas = createCanvas(width, height)
const ctx = canvas.getContext('2d')

// [[{x, y}, {x, y}]]
const getPoints = (lower, upper, pixels) => {
    var array = []
    for(var i = 0; i <= 100; i++) {
        if(i % 5 == 0) {
            let min_range, max_range;
            if(array.length > 0) {
                min_range = Math.max(array.at(-1).y - variation, pixels * lower)
                max_range = Math.min(array.at(-1).y + variation, pixels * upper)
            } else {
                min_range = pixels * lower
                max_range = pixels * upper
            }
            let ypos = Math.floor(Math.random() * (max_range - min_range) + min_range);
            array.push({x: i, y: ypos})
        }
    }
    return array
}

const saveFile = () => {
    const fs = require('fs')
    const out = fs.createWriteStream(__dirname +"/test.png")
    const stream = canvas.createPNGStream()
    stream.pipe(out)
    out.on('finish', () => console.log('PNG file created'))
}

const drawGround = (grass, dirt, dirt2) => {
    var ypos = parseInt(N*0.9)
    var xpos = 0;
    var width = N/100;
    for(var rect = 0; rect <= 100; rect++) {
        ctx.fillStyle = grass;
        var height = Math.floor(Math.random() * (30 - 25) + 25)
        ctx.fillRect(xpos, ypos, width +1, height)
        ctx.fillStyle = dirt;
        ctx.fillRect(xpos, ypos + height, width +1, 20)
        ctx.fillStyle = dirt2;
        ctx.fillRect(xpos, ypos + height + 20, width +1, N - ypos - height - 20)
        

        xpos += width
    }

}

const drawMountain = (array, color) =>  {

    ctx.fillStyle = color

    for(var i = 0; i < array.length -1; i++) {
        var xpos = array[i].x / 100 * N
        var ypos = array[i].y
        var xnext = array[i+1].x / 100 * N;
        var ynext = array[i+1].y
        ctx.beginPath()
        ctx.moveTo(xpos, ypos)
        ctx.lineTo(xnext, ynext)
        ctx.lineTo(xnext, N)
        ctx.lineTo(xpos, N)
        ctx.closePath()
        ctx.fill();
    }

}
const drawTransition = (heightSky, heightTransition, color1, color2) => {
    const widthPixel = 2;
    var res = 0;
    for(var i = 0; i <= heightTransition/2; i++) {
        for(var j = 0; j <= N/widthPixel; j++){
            if((j+i)%2 == 0) {
                ctx.fillStyle = color1
            } else {
                ctx.fillStyle = color2
            }
            ctx.fillRect(j*widthPixel, (heightSky +i*widthPixel) , widthPixel, widthPixel)
        }
        res += widthPixel;
    }
    return res;
}

const drawSky = (colors) => {
    var offSetY = 0;

    
    ctx.fillStyle = colors[0]
    ctx.fillRect(0, 0, N, heightSky)
    
    offSetY = drawTransition(heightSky, heightTransition, colors[0], colors[1])
    
    ctx.fillStyle = colors[1]
    ctx.fillRect(0, heightSky + offSetY, N, heightSky)

    offSetY = offSetY + drawTransition(heightSky*2 + offSetY, heightTransition, colors[1], colors[2])

    ctx.fillStyle = colors[2]
    ctx.fillRect(0, heightSky*2 + offSetY, N, heightSky)
}
const drawSun = () => {
    const radius = 50
    const outer_radius = 55
    const xpos = Math.floor(Math.random() * N)
    const ypos = Math.floor(Math.random() * N/2.5)

    ctx.fillStyle = '#FFF7B0'
    ctx.beginPath();
    ctx.arc(xpos, ypos, radius, 0, 2*Math.PI)
    ctx.fill();

    ctx.strokeStyle = "#FFF7B0"
    ctx.beginPath();
    ctx.arc(xpos, ypos, outer_radius, 0, 2*Math.PI)
    ctx.lineWidth = 3;
    ctx.stroke();   
}
const drawCloud = (thicc) => {
    
    const box = {width: 100, height: 15}
    const radius = Math.floor(Math.random() * (30 - 20) + 20)
    const ycloud = Math.floor(Math.random() * N/2)
    const xcloud = Math.floor(Math.random() * (N - 80) + 40)

    ctx.fillStyle = "#fff"
    for (var arc = 0; arc < thicc; arc++) {
        var ypos = Math.floor(Math.random() * box.height) + ycloud
        var xpos = Math.floor(Math.random() * box.width) + xcloud
        ctx.moveTo(xpos, ypos);
        var startAngle = 0;
        var endAngle = 2*Math.PI
        if(ypos + radius > ycloud + box.height) {
            var overflow = ypos + radius - ycloud - box.height
            var a = radius - overflow
            startAngle = Math.asin(a/radius)
            endAngle = Math.PI -startAngle
        }
        ctx.beginPath();
        ctx.arc(xpos, ypos, radius, startAngle, endAngle, true)
        ctx.fill()

    }
}

const drawStars = () => {
    for(var i = 0; i <= Math.floor(Math.random() * (80 - 20) + 10); i++) {
        const ystar = Math.floor(Math.random() * N/2)
        const xstar = Math.floor(Math.random() * (N - 80) + 40)
        ctx.fillStyle = "#fff"
        ctx.fillRect(xstar, ystar, 4, 4);
    }
}

const draw = (biome, time) => {

    ctx.fillStyle = '#fff'
    ctx.fillRect(0, 0, width, height)
    drawSky(sky_colors[time])
    drawSun() 

    if(time=="day"){ 
        ctx.globalAlpha = 0.8
        for (var i = 0; i < Math.floor(Math.random() * (7)); i++) {
            drawCloud(20)
        }
        ctx.globalAlpha = 1
    } else {
        drawStars()
    }

    var bound = 0
    for(var color of mountain_colors[biome]) {
        var lower_bound = 0.4 + bound
        var upper_bound = 0.6 + bound
        var array = getPoints(lower_bound, upper_bound, N)
        drawMountain(array, color)
        bound += 0.15
    }

    drawGround('#4FA447', '#92522E', '#A85731')
    

    
    saveFile()
}
const time =['night', 'day']
const biome = ['green', 'desert']

draw(
    biome[Math.round(Math.random())],
    time[Math.round(Math.random())]
    )