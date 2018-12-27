let isSvgPointReady = false;
let circleFrom = undefined;
let textA = undefined;
let circleTo = undefined;
let textB = undefined;

let readyA = false;
let readyB = false;

let isPath = false;
let oldLines = [];

function reDrawSvg(){

    svg.setAttribute('width', canvas.width);
    svg.setAttribute('height', canvas.height);


    if (!isSvgPointReady) {
        if (pointFrom && !circleFrom) {
            circleFrom = createSvgCircle(20, 'red', 'lightgray', 2);
            textA = createSvgText('A');
        }
        if (pointTo && !circleTo) {
            circleTo = createSvgCircle(20, 'red', 'lightgray', 2);
            textB = createSvgText('B');
            isSvgPointReady = true;
        }

        if (!readyA && circleFrom) {
            svg.appendChild(circleFrom);
            svg.appendChild(textA);
            readyA = true;
        }
        if (!readyB && circleTo) {
            svg.appendChild(circleTo);
            svg.appendChild(textB);
            readyB = true;
        }
    }

    if (readyA && pointFrom){
        let xy = fromShaderXYToClickTY(pointFrom.x, pointFrom.y);
        //console.log(xy);
        circleFrom.setAttribute('cx', xy.x);
        circleFrom.setAttribute('cy', xy.y);
        textA.setAttribute('x', (xy.x - 9).toString());
        textA.setAttribute('y', (xy.y + 10).toString());
    }

    if (readyB && pointTo){
        let xy = fromShaderXYToClickTY(pointTo.x, pointTo.y);
        circleTo.setAttribute('cx', xy.x);
        circleTo.setAttribute('cy', xy.y);
        textB.setAttribute('x', (xy.x - 9).toString());
        textB.setAttribute('y', (xy.y + 10).toString());
    }

    if (isPath){
        drawPath()
    }


    function drawPath(){
        //console.log('PATH REDRAWN');

        //deleting old lines if exist
        if (oldLines.length !== 0) {
            for (let i = 0; i < oldLines.length; i++) {
                oldLines[i].remove();
            }
            oldLines = [];

        }
        //console.log(path);

        let clickXY = [];

        for (let i = 0; i < path.length; i++){
            let xy = fromShaderXYToClickTY(path[i].x, path[i].y);
            clickXY.push({
                x: xy.x,
                y: xy.y
            })
        }

        //console.log(clickXY);

        for (let i = 0; i < clickXY.length - 1 ; i++) {
            let line = createLine(clickXY[i].x, clickXY[i].y, clickXY[i + 1].x, clickXY[i + 1].y);
            svg.appendChild(line);
            oldLines.push(line);
        }

        function createLine(x1, y1, x2, y2){
            let l = document.createElementNS("http://www.w3.org/2000/svg", 'line');
            l.setAttribute('x1', x1);
            l.setAttribute('y1', y1);
            l.setAttribute('x2', x2);
            l.setAttribute('y2', y2);
            l.setAttribute('stroke', 'red');
            l.setAttribute('stroke-width', '6');
            return l;
        }

        circleFrom.remove();
        svg.appendChild(circleFrom);
        textA.remove();
        svg.appendChild(textA);

        circleTo.remove();
        svg.appendChild(circleTo);
        textB.remove();
        svg.appendChild(textB);

    }

    function createSvgCircle(r, fill, s, sw){
        let c = document.createElementNS("http://www.w3.org/2000/svg", 'circle');
        c.setAttribute('r', r.toString());
        c.setAttribute('fill', fill);
        c.setAttribute('stroke', s);
        c.setAttribute('stroke-width', sw.toString());
        return c;
    }

    function createSvgText(text, fill){
        let t = document.createElementNS("http://www.w3.org/2000/svg", 'text');
        t.setAttribute('fill', 'black');
        t.setAttribute('font-size', '30px');
        t.innerHTML = text;
        return t;
    }

    //write a convert from click xy to view xy
}

function svgRemovePath(){
    path = [];
    if (oldLines.length !== 0) {
        for (let i = 0; i < oldLines.length; i++) {
            oldLines[i].remove();
        }
        oldLines = [];

    }
}
