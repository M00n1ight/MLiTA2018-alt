function resizeCanvasFS() {
    let canvas = document.getElementById('canvas');
    //let svg = document.getElementById('svg');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    if (isSvgDrawn) {
        svg.setAttribute('width', canvas.width);
        svg.setAttribute('height', canvas.height);
    }
}

window.onresize = function(event){
    if (isGraphDrawn) {
        resizeCanvasFS();
        reDrawGraph(graph, currentOffsetx, currentOffsety, scale);
        reDrawSvg();
    }
};