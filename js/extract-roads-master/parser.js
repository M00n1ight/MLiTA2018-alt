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

// module.exports = function(res){
//     graphLoad.on('loaded', ()=>{
//         console.log('GRAPHLOAD EMITTED');
//         res.json(graph.toViewJSON());
//         console.log('JSON Done');
//     });
//     fs.createReadStream('extract-roads-master/maps/Toronto.json', {encoding: 'utf8'})
//         .pipe(JSONStream.parse('elements.*'))
//         .pipe(es.mapSync(callback))
//         .on('end', done);
// };

module.exports = function(res, current_city){
    fs.open('extract-roads-master/maps/'+ current_city + '_bin', 'r', function(err, fd) {
        fs.fstat(fd, function(err, stats) {
            var bufferSize=stats.size,
                chunkSize=512,
                buffer=new Buffer(bufferSize),
                bytesRead = 0;

            while (bytesRead < bufferSize) {
                if ((bytesRead + chunkSize) > bufferSize) {
                    chunkSize = (bufferSize - bytesRead);
                }
                fs.read(fd, buffer, bytesRead, chunkSize, bytesRead);
                bytesRead += chunkSize;
            }
            //console.log(buffer.toString('utf8', 0, bufferSize));
            fs.close(fd, function(err){
                //console.log('fs close error: ' + err);
                res.json(JSON.parse(buffer));
            });
        });
    });
};

function callback(el) {
    testCounter++;
    if (!(testCounter % 1000)) console.log(testCounter);
    if (el.type === 'node') processOSMNode(el);
    else if (el.type === 'way') processOSMWay(el);
}

function done() {
    console.log('file read');
    graphLoad.emit('loaded');
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

// function saveResults() {
//     console.log('Graph loaded');
//     // graph.forEachNode(function (node) {
//     //     console.log(node);
//     // });
//     //saveRoadsAsCsv();
//     //saveAllForOutput();
//     //saveNodesAsCsv();
// }

// function saveAllForOutput() {
//     const createCsvWriter = require('csv-writer').createObjectCsvWriter;
//     const csvWriter = createCsvWriter({
//         path: 'diagram.csv',
//         header: [
//             {id: 'fromId', title: 'fromId'},
//             {id: 'toId', title: 'toId'},
//             {id: 'lat', title: 'lat'},
//             {id: 'lon', title: 'lon'},
//             {id: 'weight', title: 'weight'}
//         ]
//     });
//     let tempRoads = [{}];
//     graph.forEachNode(function (node) {
//         let temp
//         tempRoads.push({
//             'fromId': road.fromId,
//             'toId': road.toId,
//             'lat' : 0,
//             'lon' : 0,
//             'weight': road.data
//         });
//     });
//     csvWriter.writeRecords(tempRoads).then(() => {
//         console.log('...roads are recorded');
//     });
// }
//
// function saveRoadsAsCsv() {
//     const createCsvWriter = require('csv-writer').createObjectCsvWriter;
//     const csvWriter = createCsvWriter({
//         path: 'roads.csv',
//         header: [
//             {id: 'fromId', title: 'fromId'},
//             {id: 'toId', title: 'toId'},
//             {id: 'weight', title: 'weight'}
//         ]
//     });
//     let tempRoads = [{}];
//     graph.forEachLink(function (road) {
//         tempRoads.push({
//             'fromId': road.fromId,
//             'toId': road.toId,
//             'weight': road.data
//         });
//     });
//     csvWriter.writeRecords(tempRoads).then(() => {
//         console.log('...roads are recorded');
//     });
// }
//
// function saveNodesAsCsv() {
//     const createCsvWriter = require('csv-writer').createObjectCsvWriter;
//     const csvWriter = createCsvWriter({
//         path: 'nodes.csv',
//         header: [
//             {id: 'id', title: 'id'},
//             {id: 'lat', title: 'lat'},
//             {id: 'lon', title: 'lon'}
//         ]
//     });
//     let tempNodes = [{}];
//     graph.forEachNode(function (node) {
//         let temp = nodes.get(node.id);
//         tempNodes.push({
//             'id'  : node.id,
//             'lat' : temp.lat,
//             'lon' : temp.lon
//         });
//     });
//     csvWriter.writeRecords(tempNodes).then(() => {
//         console.log('...nodes are recorded');
//     });
// }