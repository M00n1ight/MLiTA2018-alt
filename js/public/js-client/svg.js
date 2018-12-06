let isSvgPointReady = false;
let circleFrom = undefined;
let textA = undefined;
let circleTo = undefined;
let textB = undefined;

function reDrawSvg(){

    svg.setAttribute('width', canvas.width);
    svg.setAttribute('height', canvas.height);

    if (!isSvgPointReady) {
        circleFrom = createSvgCircle(40, 'blue', 'lightblue', 10);
        textA = createSvgText('A');
        circleTo = createSvgCircle(40, 'blue', 'lightblue', 10);
        textB = createSvgText('B');

        isSvgPointReady = true;

        svg.appendChild(circleFrom);
        svg.appendChild(textA);
        svg.appendChild(circleTo);
        svg.appendChild(textB);
    }



    function createSvgCircle(r, fill, s, sw){
        let c = document.createElementNS("http://www.w3.org/2000/svg", 'circle');
        c.setAttribute('r', r.toString());
        c.setAttribute('fill', fill);
        c.setAttribute('stroke', s);
        c.setAttribute('sw', sw.toString());
        return c;
    }

    function createSvgText(text){
        let t = document.createElementNS("http://www.w3.org/2000/svg", 'text');
        t.innerHTML = text;
        return t;
    }

    //write a convert from click xy to view xy
}