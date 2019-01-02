let JSONStream = require('JSONStream');
let es = require('event-stream');
let fs = require('fs');
let EventEmitter = require('events').EventEmitter;
let Buffer = require('buffer').Buffer;
let graphLoad = new EventEmitter;

let Graph = require('./../classes/graph');
let Node = require('./../classes/node');
let Edge = require('./../classes/edge');

let graph = new Graph;
let testCounter = 0;

console.log('start')
readMap()

function readMap(){
    fs.createReadStream('export.json', {encoding: 'utf8'})
        .pipe(JSONStream.parse('elements.*'))
        .pipe(es.mapSync(callback))
        .on('end', done);
};

function callback(el) {
    testCounter++;
    if (!(testCounter % 1000)) console.log(testCounter);
    if (el.type === 'node') processOSMNode(el);
    else if (el.type === 'way') processOSMWay(el);
}

function done() {
    console.log('file read');
    const buffer = Buffer.from(JSON.stringify(graph.toViewJSON()));
    //console.log(buffer)
    fs.open('maps/SPb3_bin', 'w', function(err, fd){
    	if (err){
    		throw 'error opening file';
    	}

    	fs.write(fd, buffer, 0, buffer.length, null, function(err){
    		if (err) throw 'error writing file';
    		fs.close(fd, function(){
    			console.log('file written');
    			fs.open('maps/SPb3_bin', 'r', function(err, fd) {
				    fs.fstat(fd, function(err, stats) {
				        var bufferSize=stats.size,
				            chunkSize=1024,
				            buffer1=new Buffer(bufferSize),
				            bytesRead = 0;

				        while (bytesRead < bufferSize) {
				            if ((bytesRead + chunkSize) > bufferSize) {
				                chunkSize = (bufferSize - bytesRead);
				            }
				            fs.read(fd, buffer1, bytesRead, chunkSize, bytesRead);
				            bytesRead += chunkSize;
				        }
				        console.log(JSON.parse(buffer1));
				        fs.close(fd);
				    });
				});
    		})
    	})
    })
    //console.log(JSON.parse(buffer))

}




















function processOSMError() {
    console.log('error');
}

function processOSMNode(node) {
    let n = new Node();
    n.setParams(node.id, node.lon, node.lat);
    graph.addNode(n);
}

function processOSMWay(way) {
    let currentNodes = way.nodes;
    if (!currentNodes) {
        console.log('no nodes', way);
        return;
    }
    for (let i = 1; i < currentNodes.length; ++i) {
        let nodeFrom = graph.findNodeById(currentNodes[i]);
        let nodeTo = graph.findNodeById(currentNodes[i - 1]);
        let edge = new Edge(nodeFrom, nodeTo);
        graph.addEdge(edge);
    }
}
