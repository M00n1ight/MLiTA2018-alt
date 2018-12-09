module.exports = function(res, points){
    let net = require('net');

    let client = new net.Socket();
    client.setEncoding('utf-8');
    client.connect(8081, 'localhost', function(){
        console.log('Connected!');
        let str = points.from.lon + ' ' + points.from.lat + ' ' + points.to.lon + ' ' + points.to.lat;
        console.log(str);
        client.write(str, 'utf-8', function(){
            console.log('Sent: ' + str)
        });
    });

    client.on('data', function(data){
        console.log('Received: ' + data);
        client.destroy();

        let data_f = data.toString().split(' ');
        console.log(data_f.length);

        let path = [];

        for (let i = 0; i < data_f.length - 1; i += 2){
            path.push({
                x: Number(data_f[i]),
                y: Number(data_f[i+1])
            })
        }

        console.log(path);

        res.json(path);
    });
};