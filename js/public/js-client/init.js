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