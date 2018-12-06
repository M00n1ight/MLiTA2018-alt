let buttonStart = document.getElementById('startButton');
let svg = document.createElementNS("http://www.w3.org/2000/svg", 'svg');
let isGraphDrawn = false;
let isSvgDrawn = false;
let graph = undefined;

buttonStart.onclick = function(){
    console.log('BUTTON CLICKED');
    let cnv = document.getElementById('canvas');
    let zoomButtons = document.getElementsByClassName('zoom_button');

    cnv.hidden = false;
    makeCanvasFS();
    buttonStart.hidden = true;

    for(let i = 0; i < zoomButtons.length; i++){
        zoomButtons[i].hidden = false;
    }

    $.ajax({
        url: '/ajax/getGraph',
        success: function(g){
            console.log('AJAX SUCCEED');

            reDrawGraph(g, 0, 0, 1);

            document.body.insertBefore(svg, cnv);

            reDrawSvg();

            isSvgDrawn = true;
            isGraphDrawn = true;
            graph = g;
        }
    })
};