let canvas = document.getElementById('canvas');

//TRANSLATION
let isMouseDown = false;
let mouseStartX = undefined;
let mouseStartY = undefined;

let isMouseMoved = false;
let isAbleToPoint = true;
let currentOffsetx = 0;
let currentOffsety = 0;
let moveOffsetx = 0;
let moveOffsety = 0;

let pointFrom = undefined;
let pointTo = undefined;

let svgPrevOffsetx = 0;
let svgPrevOffsety = 0;

let from, to;

canvas.addEventListener('mousedown', function(event){
    if (!isMouseDown && isGraphDrawn){
        isMouseDown = true;
        mouseStartX = event.offsetX;
        mouseStartY = event.offsetY;
    }
    console.log(`X: ${mouseStartX}\nY: ${mouseStartY}`);
});

canvas.addEventListener('mouseup', function(event){
    isMouseDown = false;
    if (isMouseMoved){
        isMouseMoved = false;
        currentOffsetx = (currentOffsetx + 2 * moveOffsetx);
        currentOffsety = (currentOffsety + 2 * moveOffsety);
        svgPrevOffsetx = 0;
        svgPrevOffsety = 0;
    }
});

canvas.addEventListener('mousemove', function(event){
    if (isMouseDown && isGraphDrawn){
        isMouseMoved = true;
        isAbleToPoint = false;
        moveOffsetx = (event.offsetX - mouseStartX);
        moveOffsety = (event.offsetY - mouseStartY);

        if (pointFrom){
            pointFrom = shiftSvg(pointFrom);
        }

        if (pointTo){
            pointTo = shiftSvg(pointTo);
        }


        svgPrevOffsetx = moveOffsetx;
        svgPrevOffsety = moveOffsety;

        reDrawGraph(graph,
            (currentOffsetx + 2 * moveOffsetx), (currentOffsety + 2 * moveOffsety), scale);

        reDrawSvg();
    }


    function shiftSvg(point){
        let result = {};
        let clickPoint = fromShaderXYToClickTY(point.x, point.y);
        result.x = clickPoint.x + (- svgPrevOffsetx + moveOffsetx);
        result.y = clickPoint.y + (- svgPrevOffsety + moveOffsety);
        return fromClickXYToShaderXY(result.x, result.y);
    }
});

//SCALING
let scale = 1;
let scaleSpeed = 1.5;


let buttonScale = document.getElementById('scale');
buttonScale.addEventListener('click', function(event){
    scale *= scaleSpeed;
    currentOffsetx *= scaleSpeed;
    currentOffsety *= scaleSpeed;
    if (pointFrom){
        pointFrom.x *= scaleSpeed;
        pointFrom.y *= scaleSpeed;
    }
    if (pointTo){
        pointTo.x *= scaleSpeed;
        pointTo.y *= scaleSpeed
    }
    console.log('Current scale: ' + scale);
    reDrawGraph(graph, currentOffsetx, currentOffsety, scale);
    reDrawSvg();
});

let buttonUnscale = document.getElementById('unscale');
buttonUnscale.addEventListener('click', function(event){
    scale /= scaleSpeed;
    currentOffsetx /= scaleSpeed;
    currentOffsety /= scaleSpeed;
    if (pointFrom){
        pointFrom.x /= scaleSpeed;
        pointFrom.y /= scaleSpeed;
    }
    if (pointTo){
        pointTo.x /= scaleSpeed;
        pointTo.y /= scaleSpeed;
    }
    console.log('Current scale: ' + scale);
    reDrawGraph(graph, currentOffsetx, currentOffsety, scale);
    reDrawSvg();
});

let buttonClearPoints = document.getElementById('clear_points');
buttonClearPoints.addEventListener('click', function(event){
    pointFrom = undefined;
    pointTo = undefined;
    if (circleFrom){
        circleFrom.setAttribute('cx', -10000);
        circleFrom.setAttribute('cy', -10000);
        textA.setAttribute('x', -10000);
        textA.setAttribute('y', -10000);
    }
    if (circleTo){
        circleTo.setAttribute('cx', -10000);
        circleTo.setAttribute('cy', -10000);
        textB.setAttribute('x', -10000);
        textB.setAttribute('y', -10000)
    }
    reDrawGraph(graph, currentOffsetx, currentOffsety, scale);
    reDrawSvg();
});

let buttonFindNodes = document.getElementById('find_nodes');
buttonFindNodes.addEventListener('click', function(event){
    console.log('START SEARCH');
    //SEARCH VARIABLES
    let minSqFrom = 1000000;
    let minSqTo = 1000000;
    let deltaLon = graph.maxLon - graph.minLon;
    let deltaLat = graph.maxLat - graph.minLat;

    //CALCULATION VARIABLES
    let scaledOffsetx = currentOffsetx / canvas.width;
    let scaledOffsety = currentOffsety / canvas.height;
    let scaledelta2lon = scale / deltaLon * 2;
    let scaledelta2lat = scale / deltaLat * 2;

    //SEARCH
    for (let i = 0; i < graph.edgesAmount; i++){
        if ((i+1) % 1000 === 0)
            console.log('1000 iteration');
        //FIRSTLY DO FOR NODE FROM OF EDGE
        //TRANSLATE DEFAULT COORDS TO CURRENT MAP STATE
        let cLonLat = {
            lon: scaledelta2lon *
                (graph[i].from.lon - graph.minLon) - scale + scaledOffsetx,
            lat: scaledelta2lat *
                (graph[i].from.lat - graph.minLat) - scale - scaledOffsety,
        };

        //CALCULATE DISTANCE FROM 'FROM' AND 'TO'
        let distanceFrom =
            Math.pow(cLonLat.lon - pointFrom.x, 2) + Math.pow(cLonLat.lat - pointFrom.y, 2);
        let distanceTo =
            Math.pow(cLonLat.lon - pointTo.x, 2) + Math.pow(cLonLat.lat - pointTo.y, 2);

        //COMPARE DISTANCES
        if (distanceFrom < minSqFrom){
            minSqFrom = distanceFrom;
            from = graph[i].from;
        }

        if (distanceTo < minSqTo){
            minSqTo = distanceFrom;
            to = graph[i].from;
        }

        //THEN DO FOR NODE TO OF EDGE
        //TRANSLATE DEFAULT COORDS TO CURRENT MAP STATE
        cLonLat = {
            lon: scaledelta2lon *
                (graph[i].to.lon - graph.minLon) - 1 + scaledOffsetx,
            lat: scaledelta2lat *
                (graph[i].to.lat - graph.minLat) - 1 - scaledOffsety,
        };

        //CALCULATE DISTANCE FROM 'FROM' AND 'TO'
        distanceFrom =
            Math.pow(cLonLat.lon - pointFrom.x, 2) + Math.pow(cLonLat.lat - pointFrom.y, 2);
        distanceTo =
            Math.pow(cLonLat.lon - pointTo.x, 2) + Math.pow(cLonLat.lat - pointTo.y, 2);

        //COMPARE DISTANCES
        if (distanceFrom < minSqFrom){
            minSqFrom = distanceFrom;
            from = graph[i].to;
        }

        if (distanceTo < minSqTo){
            minSqTo = distanceFrom;
            to = graph[i].to;
        }
    }
    console.log('SEARCH END');
    console.log(`FROM:\n lon ${from.lon}\n lat ${from.lat}`);
    console.log(`TO:\n lon ${to.lon}\n lat ${to.lat}`);

    //TEST VISUALIZATION
    /*let shaderC = fromDegToShaderXY(from.lon, from.lat);
    let clickC = fromShaderXYToClickTY(shaderC.x, shaderC.y);
    let testCircle = document.createElementNS("http://www.w3.org/2000/svg", 'circle');
    testCircle.setAttribute('r', 4);
    testCircle.setAttribute('fill', 'green');
    testCircle.setAttribute('cx', clickC.x);
    testCircle.setAttribute('cy', clickC.y);
    svg.appendChild(testCircle);*/
});

let buttonFindPath = document.getElementById('find_path');
buttonFindPath.addEventListener('click', function(event){
    if (from && to) {
        console.log(from, to);
        $.ajax({
            url: `/ajax/calculatePath?fromLon=${from.lon}&fromLat=${from.lat}&toLon=${to.lon}&toLat=${to.lat}`,
            success: function (data) {
                console.log("DATA FETCH");
                console.log(data);
                console.log("END DATA FETCH");
            }
        })
    }
});

canvas.addEventListener('click', function(event){
    if (isGraphDrawn && isAbleToPoint){
        if (pointFrom === undefined){
            pointFrom = fromClickXYToShaderXY(event.offsetX, event.offsetY);
            console.log(`pointFrom set to ${pointFrom.x}:${pointFrom.y}`);
        }
        else {
            pointTo = fromClickXYToShaderXY(event.offsetX, event.offsetY);
            console.log(`pointTo set to ${pointTo.x}:${pointTo.y}`);
        }
    }
    reDrawSvg();
    isAbleToPoint = true;
});