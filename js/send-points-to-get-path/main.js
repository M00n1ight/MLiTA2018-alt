module.exports = function(res, points){
    let net = require('net');

    try {
        let client = new net.Socket();
        client.setEncoding('utf-8');
        client.setTimeout(13000);
        client.connect(8081, 'localhost', function () {
            try {
                console.log('Connected!');
                let str = points.from.lon + ' ' + points.from.lat + ' '
                    + points.to.lon + ' ' + points.to.lat + ' ' + points.algo;
                console.log(str);
                client.write(str, 'utf-8', function () {
                    console.log('Sent: ' + str)
                });
            } catch (e) {
                console.log(e.message);
                res.json({error: 1});
            }
        });

        client.on('data', function (data) {
            console.log('Received: ' + data);
            client.destroy();

            let data_f = data.toString().split(' ');
            //console.log(data_f.length);

            let formatted_data = {};

            formatted_data.time = Math.floor(data_f[data_f.length - 1] * 1000) / 1000;
            formatted_data.path = [];
            formatted_data.error = 0;

            for (let i = 0; i < data_f.length - 2; i += 2) {
                formatted_data.path.push({
                    x: Number(data_f[i]),
                    y: Number(data_f[i + 1])
                })
            }

            console.log(formatted_data);

            res.json(formatted_data);
        });

        client.on('timeout', function () {
            client.destroy();
            console.log('Socket timeout');
            res.json({error: 1});
        });
        
        client.on('error', function (e) {
           client.destroy();
           console.log(e);
           res.json({error: 1});
        })
    } catch(e){
        console.log(e.message);
        res.json({error: 1});
    }
};