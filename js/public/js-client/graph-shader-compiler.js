function reDrawGraph(graph, offsetx, offsety, scale){
    let canvas = document.getElementById('canvas');

    let gl = canvas.getContext('webgl');
    if (!gl)
        alert("Webgl failure!");

    function createShader(gl, type, source){
        let shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);

        let success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
        if (success)
            return shader;

        console.log(gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
    }

    let vertexShaderSource = document.getElementById('2d-vertex-shader').text;
    let fragmentShaderSource = document.getElementById('2d-fragment-shader').text;

    let vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
    let fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

    function createProgram(gl, vertexShader, fragmentShader){
        let program = gl.createProgram();
        gl.attachShader(program, vertexShader);
        gl.attachShader(program, fragmentShader);
        gl.linkProgram(program);

        let success = gl.getProgramParameter(program, gl.LINK_STATUS);
        if (success) {
            return program;
        }

        console.log(gl.getProgramInfoLog(program));
        gl.deleteProgram(program);
        return program; //HERE COULD BE ERROR
    }

    let program = createProgram(gl, vertexShader, fragmentShader);

    //VERTEX SHADER VARIABLES
    let positionAttributeLocation = gl.getAttribLocation(program, 'a_position');
    let resolutionUniformLocation = gl.getUniformLocation(program, 'u_resolution');
    let minCoordsUniformLocation = gl.getUniformLocation(program, 'u_minLonLat');
    let maxCoordsUniformLocation = gl.getUniformLocation(program, 'u_maxLonLat');
    let offsetUniformLocation = gl.getUniformLocation(program, 'u_offset');
    let scaleUniformLocation = gl.getUniformLocation(program, 'u_scale');

    //FRAGMENT SHADER VARIABLES
    let colorsUniformLocation = gl.getUniformLocation(program, 'u_colors');

    //BUFFER
    let positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

    //COORDINATES ARRAY
    let linesCoords = [];
    for (let i = 0; i < graph.edgesAmount; i++){
        linesCoords.push(graph[i].from.lon);
        linesCoords.push(graph[i].from.lat);
        linesCoords.push(graph[i].to.lon);
        linesCoords.push(graph[i].to.lat);
    }
    //console.log(linesCoords);

    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(linesCoords), gl.STATIC_DRAW);

    //RENDERER DEFAULTS
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
    gl.clearColor(0,0,0,1);
    gl.clear(gl.COLOR_BUFFER_BIT);

    gl.useProgram(program);

    gl.enableVertexAttribArray(positionAttributeLocation);

    let size = 2;
    let type = gl.FLOAT;
    let normalize = false;
    let stride = 0;
    let offset = 0;

    if (offsetx === undefined)
        offsetx = 0;
    if (offsety === undefined)
        offsety = 0;
    if (scale === undefined)
        scale = 1;

    //INIT VERTEX SHADER VARIABLES
    gl.vertexAttribPointer(positionAttributeLocation, size, type, normalize, stride, offset);
    gl.uniform2f(resolutionUniformLocation, gl.canvas.width, gl.canvas.height);
    gl.uniform2f(minCoordsUniformLocation, graph.minLon, graph.minLat);
    gl.uniform2f(maxCoordsUniformLocation, graph.maxLon, graph.maxLat);
    gl.uniform2f(offsetUniformLocation, offsetx, offsety);
    gl.uniform2f(scaleUniformLocation, scale, scale);

    //INIT FRAGMENT SHADER VARIABLES
    gl.uniform4f(colorsUniformLocation, 0.5, 0.5, 0.5, 0.5);

    //DRAW
    gl.drawArrays(gl.LINES, 0, graph.edgesAmount * 2);
    //console.log('DRAWN');
}