canvas = document.getElementById('canvas');

let gl = canvas.getContext('webgl');
if (!gl){
    alert("Webgl failure");
}

function createShader(gl, type, source){
    let shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    let success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);

    if (success){
        return shader;
    }

    console.log(gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
}

let vertexShaderSource = document.getElementById('2d-vertex-shader').text;
let fragmentShaderSource = document.getElementById('2d-fragment-shader').text;
//shader creation
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
}

let program = createProgram(gl, vertexShader, fragmentShader);

let positionAttributeLocation = gl.getAttribLocation(program, 'a_position');
let resolutionUniformLocation = gl.getUniformLocation(program, 'u_resolution');
let colorsUniformLocation = gl.getUniformLocation(program, 'u_colors');
let positionBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

let poses = [
    0,0,
    0,500,
    500,0,
];

gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(poses), gl.STATIC_DRAW);

//RENDERING
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
gl.vertexAttribPointer(
    positionAttributeLocation, size, type, normalize, stride, offset);
gl.uniform2f(resolutionUniformLocation, gl.canvas.width, gl.canvas.height);
gl.uniform4f(colorsUniformLocation, Math.random(), Math.random(), Math.random(), 1);

let primitiveType = gl.TRIANGLES;
offset = 0;
let count = 3;
gl.drawArrays(primitiveType, offset, count);

poses = [
    500, 0,
    500, 500,
];
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(poses), gl.STATIC_DRAW);
gl.vertexAttribPointer(positionAttributeLocation, 2, gl.FLOAT, false, 0, 0);
gl.drawArrays(gl.LINES, 0, 2);