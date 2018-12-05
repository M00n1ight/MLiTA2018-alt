let Node = require('./node');

function Edge(nodeFrom, nodeTo){

    this.nodeFrom = nodeFrom;
    this.nodeTo = nodeTo;

}

Edge.prototype.toJSON = function(){
    return {
        idFrom: this.nodeFrom.id,
        idTo: this.nodeTo.id,
    }
};

Edge.prototype.toViewJSON = function(){
    return {
        from: this.nodeFrom,
        to: this.nodeTo,
    }
};

module.exports = Edge;