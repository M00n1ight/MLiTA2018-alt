let Node = require('./node');
let Edge = require('./edge');

function Graph(nodes, edges){

    this.nodes = [];
    this.edges = [];

    this.maxLon = -180;
    this.minLon = 180;

    this.maxLat = -180;
    this.minLat = 180;

    this.nodesAmount = 0;
    this.edgesAmount = 0;

    if (nodes !== undefined && edges !== undefined){
        this.nodes = nodes;
        this.edges = edges;
    }

}

Graph.prototype.addNode = function(node){
    this.nodes.push(node);

    this.nodesAmount++;

    if (node.lon > this.maxLon) {
        this.maxLon = node.lon;
    } else
        if (node.lon < this.minLon) {
            this.minLon = node.lon;
        }

    if (node.lat > this.maxLat){
        this.maxLat = node.lat;
    } else
        if (node.lat < this.minLat){
            this.minLat = node.lat;
        }

};

Graph.prototype.addEdge = function(edge){
    this.edges.push(edge);
    this.edgesAmount++;
};

Graph.prototype.addNodes = function(nodes){
    this.nodes = nodes;
};

Graph.prototype.addEdges = function(edges){
    this.edges = edges;
};

Graph.prototype.findNodeById = function(id){
    for (let i = 0; i < this.nodes.length; i++){
        if (this.nodes[i].id === id)
            return this.nodes[i];
    }
};

Graph.prototype.normalize = function(){
    for (let i = 0; i < this.nodes.length; i++){
        for (let j = 0; j < this.edges; j++){
            if (this.edges[j].nodeFrom === this.nodes[i] || this.edges[j].nodeTo === this.nodes[i]) {
                this.nodes[i].addIncidentEdge(this.edges[j])
            }
        }
    }
};

Graph.prototype.toJSON = function(){
    let nodes = {};
    for (let i = 0; i < this.nodes.length; i++){
        nodes['node' + i] = this.nodes[i].toJSON();
    }
    let edges = {};
    for (let i = 0; i < this.edges.length; i++){
        nodes['edge' + i] = this.edges[i].toJSON();
    }

    return {
        nodes: nodes,
        edges: edges,
    };
};

Graph.prototype.toViewJSON = function(){
    let view = {
        minLon: this.minLon,
        maxLon: this.maxLon,
        minLat: this.minLat,
        maxLat: this.maxLat,

        nodesAmount: this.nodesAmount,
        edgesAmount: this.edgesAmount,
    };
    for (let i = 0; i < this.edges.length; i++){
        let fromLatLon = {
            lon: this.edges[i].nodeFrom.lon,
            lat: this.edges[i].nodeFrom.lat,
        };
        let toLatLon = {
            lon: this.edges[i].nodeTo.lon,
            lat: this.edges[i].nodeTo.lat,
        };
        view[i] = {
            from: fromLatLon,
            to: toLatLon,
        }
    }
    return view;
};

module.exports = Graph;