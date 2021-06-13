var express=require('express');
var app=express();
const p=process.env.PORT;
app.listen(p);
app.get('/', (req, res) => {
    res.send('Hello Guis!')
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
    const username=req.query.Username;
    const password=req.query.Password;
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
    else if(rtype=='Auth')
    {
        if(username=='John240') AND (password=='password')
        {
            details = {
                "Name" : "John Lennon" ,
                "Username" : "John240",
                "Email" : "john240@gmail.com",
                "Phone" : "269-748-9882",
                "Gender" : "Male",
                "DOB" : "10/04/1997"
            }
            res.send(details.toString());

        }
        
        
    }
});