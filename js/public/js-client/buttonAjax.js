let buttonStart = document.getElementById('startButton');
let svg = document.createElementNS("http://www.w3.org/2000/svg", 'svg');
let isGraphDrawn = false;
let isSvgDrawn = false;
let graph = undefined;
let current_city_id = undefined;

buttonStart.onclick = function(){
    console.log('BUTTON CLICKED');
    let cnv = document.getElementById('canvas');
    let menu = document.getElementById('menu');
    let start_menu = document.getElementById('start_menu');
    let city_pre_chooser = document.getElementById('city_chooser');
    menu.style.display = 'flex';
    // for(let i = 0; i < zoomButtons.length; i++){
    //     zoomButtons[i].hidden = false;
    // }

    cnv.hidden = false;
    resizeCanvasFS();
    start_menu.hidden = true;
    current_city_id = city_pre_chooser.options[city_pre_chooser.selectedIndex].value;
    menu.appendChild(city_pre_chooser);
    city_chooser.disabled = true;

    $.ajax({
        url: `/ajax/getGraph?city=${current_city_id}`,
        success: function(g){
            console.log('AJAX SUCCEED');

            // for(let i = 0; i < zoomButtons.length; i++){
            //     zoomButtons[i].hidden = false;
            // }

            reDrawGraph(g, 0, 0, 1);

            document.body.insertBefore(svg, cnv);

            reDrawSvg();

            enableButtons();

            isSvgDrawn = true;
            isGraphDrawn = true;
            graph = g;
        }
    })
};