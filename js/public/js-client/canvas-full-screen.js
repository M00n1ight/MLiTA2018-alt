function makeCanvasFS() {
    let canvas = document.getElementById('canvas');
    let svg = document.getElementById('svg');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    if (isSvgDrawn) {
        svg.width = window.innerWidth;
        svg.height = window.height;
    }
}

window.onresize = function(event){
    makeCanvasFS();
    reDrawGraph(graph, currentOffsetx, currentOffsety, scale);
};