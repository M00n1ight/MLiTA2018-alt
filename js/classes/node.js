let Edge = require('./edge');

function Node(id, lon, lat){

    this.id = id;
    this.lon = lon;
    this.lat = lat;
    this.iEdges = [];

}

Node.prototype.addIncidentEdge = function(edge){
    if (edge instanceof Edge) {
        this.iEdges.push(edge);
    }
    else{
        console.log("Edge is'n instance of Edge:\n" + edge + '\n');

    }
};

Node.prototype.setParams = function(id, lon, lat){
    this.id = id;
    this.lon = lon;
    this.lat = lat;
};

Node.prototype.toJSON = function(){
     return {
        nodeId: this.id,
        nodeLon: this.lon,
        nodeLat: this.lat,
    }
};

module.exports = Node;