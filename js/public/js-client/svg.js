let isSvgPointReady = false;
let circleFrom = undefined;
let textA = undefined;
let circleTo = undefined;
let textB = undefined;

let readyA = false;
let readyB = false;

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
        console.log(xy);
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