function makeCanvasFS() {
    let canvas = document.getElementById('canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.onresize = function(event){
    makeCanvasFS();
    reDrawGraph(graph, currentOffsetx, currentOffsety, scale);
};