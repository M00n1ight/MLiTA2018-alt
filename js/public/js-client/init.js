let detectedFrom, detectedTo;

function fromClickXYToShaderXY(x,y){
    let result = {};
    result.x = x / canvas.width * 2 - 1;
    result.y = - (y / canvas.height * 2 - 1);
    return result;
}

function fromShaderXYToClickTY(x, y){
    let result = {};
    result.x = (x + 1) / 2 * canvas.width;
    result.y = (-y + 1) / 2 * canvas.height;
    return result;
}

function fromDegToShaderXY(lon, lat){
    let deltaLon = graph.maxLon - graph.minLon;
    let deltaLat = graph.maxLat - graph.minLat;
    let scaledOffsetx = currentOffsetx / canvas.width;
    let scaledOffsety = currentOffsety / canvas.height;
    let scaledelta2lon = scale / deltaLon * 2;
    let scaledelta2lat = scale / deltaLat * 2;

    return {
        x: scaledelta2lon *
            (lon - graph.minLon) - scale + scaledOffsetx,
        y: scaledelta2lat *
            (lat - graph.minLat) - scale - scaledOffsety,
    };
}

function getGraphMaces(){
    console.log(`Lon: ${graph.minLon} - ${graph.maxLon}\n
    Lat: ${graph.minLat} - ${graph.maxLat}`);
}

