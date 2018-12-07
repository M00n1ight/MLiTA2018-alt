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

});

let buttonFindPath = document.getElementById('find_path');
buttonFindPath.addEventListener('click', function(event){

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