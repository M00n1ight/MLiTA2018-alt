module.exports = function(res, points){
    let net = require('net');

    let client = new net.Socket();
    client.setEncoding('utf-8');
    client.connect(8081, 'localhost', function(){
        console.log('Connected!');
        let str = points.from.lon + ' ' + points.from.lat + ' '
            + points.to.lon + ' ' + points.to.lat + ' ' + points.algo;
        console.log(str);
        client.write(str, 'utf-8', function(){
            console.log('Sent: ' + str)
        });
    });

    client.on('data', function(data){
        console.log('Received: ' + data);
        client.destroy();

        let data_f = data.toString().split(' ');
        //console.log(data_f.length);

        let formatted_data = {};

        formatted_data.time = Math.floor(data_f[data_f.length - 1] * 1000) / 1000;
        formatted_data.path = [];

        for (let i = 0; i < data_f.length - 2; i += 2){
            formatted_data.path.push({
                x: Number(data_f[i]),
                y: Number(data_f[i+1])
            })
        }

        console.log(formatted_data);

        res.json(formatted_data);
    });
};