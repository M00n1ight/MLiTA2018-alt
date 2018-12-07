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
let zoom = document.getElementsByClassName('zoom_button');
for (let i = 0; i < zoom.length; i++){
    zoom[i].addEventListener('click', function(event){
        let inner = zoom[i].innerHTML;
        if (inner === '+') {
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
        }
        else if (inner === '-') {
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
        }
        else if (inner === 'Clear points'){
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
        }
        console.log('Current scale: ' + scale);
        reDrawGraph(graph, currentOffsetx, currentOffsety, scale);
        reDrawSvg();
    })
}

canvas.addEventListener('click', function(event){
    //TEST
    // let result = fromClickXYToShaderXY(event.offsetX, event.offsetY);
    // console.log(`TEST 1 RESULT\n${event.offsetX} : ${event.offsetY} -> ${result.x} : ${result.y}`);
    // let result1 = fromShaderXYToClickTY(result.x, result.y);
    // console.log(`TEST 2 RESULT\n${result.x} : ${result.y} -> ${result1.x} : ${result1.y}`);
    //END TEST
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