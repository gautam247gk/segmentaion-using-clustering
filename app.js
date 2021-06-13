var express=require('express');
var app=express();
app.listen(3000,'0.0.0.0');
app.get('/', (req, res) => {
    res.send('Hello World!')
  })
app.get('/run',ps);
var spawn = require('child_process').spawn;
function ps(req,res)
{
    
    process=spawn('python3',['./mc/prj.py']);
    process.stdout.on('data', function(data) {
        //console.log(data.toString());
        res.send(data.toString());
    })
    process.stderr.on('data', (data) => {
        console.log(`error:${data}`);
      });
    process.on('close', () => {
        console.log("Closed");
    });
}
app.get('/web',(req,res)=>{
    const rtype=req.query.RequestType;
    const date=req.query.Date;
    if(rtype=='Quarter')
    {
        process=spawn('python3',['./mc/quarter.py']);
        process.stdout.on('data', function(data) {
            //console.log(data.toString());
            res.send(data.toString());
        })
        process.stderr.on('data', (data) => {
            console.log(`error:${data}`);
          });
        process.on('close', () => {
            console.log("Closed");
        });
    }
    else if(rtype=='Graph')
    {
        process=spawn('python3',['./mc/graphrequest.py',date]);
        process.stdout.on('data', function(data) {
            //console.log(data.toString());
            res.send(data.toString());
        })
        process.stderr.on('data', (data) => {
            console.log(`error:${data}`);
          });
        process.on('close', () => {
            console.log("Closed");
        });
    }
    else if(rtype=='Trends')
    {
        process=spawn('python3',['./mc/trendsrequest.py']);
        process.stdout.on('data', function(data) {
            //console.log(data.toString());
            res.send(data.toString());
        })
        process.stderr.on('data', (data) => {
            console.log(`error:${data}`);
          });
        process.on('close', () => {
            console.log("Closed");
        });
    }
});