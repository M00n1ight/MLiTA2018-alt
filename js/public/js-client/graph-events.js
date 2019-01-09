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

let path = undefined;

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

        //to make it at the next tick of eventloop
        //to not set the point after mouseup->click
        setTimeout(function(){
            isAbleToPoint = true;
        }, 0);

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

        if (isPath){
            for (let i = 0; i < path.length; i++){
                path[i] = shiftSvg(path[i])
            }
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

canvas.addEventListener('mouseleave', function (event) {
    //console.log(event.relatedTarget.tagName);
    if (isMouseMoved &&
            event.relatedTarget !== null &&
            event.relatedTarget.tagName !== 'BUTTON' &&
            event.relatedTarget.tagName !== 'DIV' &&
            event.relatedTarget.tagName !== 'SELECT') {
        canvas.dispatchEvent(new Event('mouseup'));
    }
});

// document.body.addEventListener('mousemove', function(event){
//     //console.log(event.target.tagName);
//     if (isMouseMoved && (
//         event.target.tagName === 'SELECT' ||
//         event.target.tagName === 'BUTTON' ||
//         event.target.tagName === 'DIV'))
//     {
//         canvas.dispatchEvent(new Event('mousemove'));
//     }
// });

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

    if (isPath){
        for (let i = 0; i < path.length; i++){
            path[i].x *= scaleSpeed;
            path[i].y *= scaleSpeed;
        }
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
    if (isPath){
        for (let i = 0; i < path.length; i++){
            path[i].x /= scaleSpeed;
            path[i].y /= scaleSpeed;
        }
    }
    console.log('Current scale: ' + scale);
    reDrawGraph(graph, currentOffsetx, currentOffsety, scale);
    reDrawSvg();
});

let buttonSwapPoints = document.getElementById('swap_points');
buttonSwapPoints.addEventListener('click', function(event){
    if (pointFrom && pointTo){
        let copy = pointFrom;
        pointFrom = pointTo;
        pointTo = copy;
        reDrawSvg()
    }
});

let buttonClearPoints = document.getElementById('clear_points');
// buttonClearPoints.addEventListener('mousemove', function(event){
//     event.preventDefault();
//     event.stopPropagation();
//     return false;
// });
buttonClearPoints.addEventListener('click', function(event){
    isPath = false;

    for (let i = 0; i < oldLines.length; i++){
        oldLines[i].remove();
    }
    oldLines = [];

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
        let cLonLat = fromDegToShaderXY(graph[i].from.lon, graph[i].from.lat);

        //CALCULATE DISTANCE FROM 'FROM' AND 'TO'
        let distanceFrom =
            Math.pow(cLonLat.x - pointFrom.x, 2) + Math.pow(cLonLat.y - pointFrom.y, 2);
        let distanceTo =
            Math.pow(cLonLat.x - pointTo.x, 2) + Math.pow(cLonLat.y - pointTo.y, 2);

        //COMPARE DISTANCES
        if (distanceFrom < minSqFrom){
            minSqFrom = distanceFrom;
            from = graph[i].from;
        }

        if (distanceTo < minSqTo){
            minSqTo = distanceTo;
            to = graph[i].from;
        }

        //THEN DO FOR NODE TO OF EDGE
        //TRANSLATE DEFAULT COORDS TO CURRENT MAP STATE
        cLonLat = fromDegToShaderXY(graph[i].to.lon, graph[i].to.lat);

        //CALCULATE DISTANCE FROM 'FROM' AND 'TO'
        distanceFrom =
            Math.pow(cLonLat.x - pointFrom.x, 2) + Math.pow(cLonLat.y - pointFrom.y, 2);
        distanceTo =
            Math.pow(cLonLat.x - pointTo.x, 2) + Math.pow(cLonLat.y - pointTo.y, 2);

        //COMPARE DISTANCES
        if (distanceFrom < minSqFrom){
            minSqFrom = distanceFrom;
            from = graph[i].to;
        }

        if (distanceTo < minSqTo){
            minSqTo = distanceTo;
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
    testCircle.setAttribute('r', 10);
    testCircle.setAttribute('fill', 'yellow');
    testCircle.setAttribute('cx', clickC.x);
    testCircle.setAttribute('cy', clickC.y);
    svg.appendChild(testCircle);

    shaderC = fromDegToShaderXY(to.lon, to.lat);
    clickC = fromShaderXYToClickTY(shaderC.x, shaderC.y);
    testCircle = document.createElementNS("http://www.w3.org/2000/svg", 'circle');
    testCircle.setAttribute('r', 10);
    testCircle.setAttribute('fill', 'green');
    testCircle.setAttribute('cx', clickC.x);
    testCircle.setAttribute('cy', clickC.y);
    svg.appendChild(testCircle);*/
});

let buttonFindPath = document.getElementById('find_path');
buttonFindPath.addEventListener('click', function(event){

    //CODE FROM FIND NODES EVENT
    // ITS COPIED INSTEAD OF CLICK SIMULATION
    // BC FIND NODES BUTTON IS ONLY DEV BUTTON
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
        let cLonLat = fromDegToShaderXY(graph[i].from.lon, graph[i].from.lat);

        //CALCULATE DISTANCE FROM 'FROM' AND 'TO'
        let distanceFrom =
            Math.pow(cLonLat.x - pointFrom.x, 2) + Math.pow(cLonLat.y - pointFrom.y, 2);
        let distanceTo =
            Math.pow(cLonLat.x - pointTo.x, 2) + Math.pow(cLonLat.y - pointTo.y, 2);

        //COMPARE DISTANCES
        if (distanceFrom < minSqFrom){
            minSqFrom = distanceFrom;
            from = graph[i].from;
        }

        if (distanceTo < minSqTo){
            minSqTo = distanceTo;
            to = graph[i].from;
        }

        //THEN DO FOR NODE TO OF EDGE
        //TRANSLATE DEFAULT COORDS TO CURRENT MAP STATE
        cLonLat = fromDegToShaderXY(graph[i].to.lon, graph[i].to.lat);

        //CALCULATE DISTANCE FROM 'FROM' AND 'TO'
        distanceFrom =
            Math.pow(cLonLat.x - pointFrom.x, 2) + Math.pow(cLonLat.y - pointFrom.y, 2);
        distanceTo =
            Math.pow(cLonLat.x - pointTo.x, 2) + Math.pow(cLonLat.y - pointTo.y, 2);

        //COMPARE DISTANCES
        if (distanceFrom < minSqFrom){
            minSqFrom = distanceFrom;
            from = graph[i].to;
        }

        if (distanceTo < minSqTo){
            minSqTo = distanceTo;
            to = graph[i].to;
        }
    }
    console.log('SEARCH END');
    console.log(`FROM:\n lon ${from.lon}\n lat ${from.lat}`);
    console.log(`TO:\n lon ${to.lon}\n lat ${to.lat}`);
    //END

    let select = document.getElementById('select_alg');
    let algorithmId = select.options[select.selectedIndex].value;
    console.log(`Selected: ${algorithmId}`);

    //FINDING PATH
    if (from && to) {
        console.log(from, to);
        $.ajax({
            url: `/ajax/calculatePath?alg=${algorithmId}&fromLon=${from.lon}&fromLat=${from.lat}&toLon=${to.lon}&toLat=${to.lat}`,
            success: function (data) {
                console.log("DATA FETCH");
                console.log(data);
                console.log("END DATA FETCH");

                if (data.path.length < 2){
                    alert('No way found');
                }

                path = data.path.map(function(val, index, data){
                    let xy = fromDegToShaderXY(val.x, val.y);
                    return {
                        x: xy.x,
                        y: xy.y
                    }
                });

                if (data.time > 0)
                    alert(`${data.time} sec`);

                isPath = true;
                reDrawSvg();
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
            svgRemovePath();
            pointTo = fromClickXYToShaderXY(event.offsetX, event.offsetY);
            console.log(`pointTo set to ${pointTo.x}:${pointTo.y}`);
        }
    }
    reDrawSvg();
    //isAbleToPoint = true;
});