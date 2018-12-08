module.exports = function(res, points){
    let net = require('net');

    let client = new net.Socket();
    client.connect(8081, 'localhost', function(){
        console.log('Connected!');
        client.write(points.from.lon + ' ' + points.from.lat + ' ' + points.to.lon + ' ' + points.to.lat);
    });

    client.on('data', function(data){
        console.log('Received: ' + data);
        client.destroy();
    });

    res.send('ajax done');
};