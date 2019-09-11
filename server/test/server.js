var express    = require("express");
var fs         = require("fs");
var morgan     = require("morgan");
var grpc       = require("grpc");
var protoLoader = require("@grpc/proto-loader");
var bodyParser  = require('body-parser');
const process   = require('process');
const path      = require('path');

///////////////////////////////////////
var passport    = require('passport');
var flash       = require('connect-flash');
var session     = require('express-session');
// var mongoose    = require('mongoose');
// var configDB = require('./config/database.js');
// mongoose.connect(configDB.url, {useNewUrlParser: true});
require('./config/passport')(passport);
///////////////////////////////////////

var options = {
    key: fs.readFileSync('../privkey.pem'),
    cert: fs.readFileSync('../fullchain.pem')
};
var app        = express();
app.use(bodyParser.urlencoded({ extended: false }))
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public')); 
if(show_debug){
    app.use(morgan("dev"));
}

///////////////////////////////////////
app.use(session({ secret: 'b.FeWHv3peF_"l`0WqE/Im[a+j"#`Y#$6EP^-jPZ,R2LSut(dd&BuHJ}yhBTK?w', resave: true, saveUninitialized: true})); 
app.use(passport.initialize());
app.use(passport.session()); 
app.use(flash()); 
require('./app/routes.js')(app, passport);
///////////////////////////////////////

var num = 8007;
var port = process.env.PORT || num;
var use_https = process.argv.slice(2).length === 0 ? true : process.argv.slice(2)[0] == 'true';
var show_debug = false;
var server = null;

if (use_https){
    server = require('https').createServer(options, app);
}else{
    server = require("http").Server(app);
}
var io = require("socket.io")(server);
var CLIENTS = {};
var CURRENT_TASK = '';


// app.get("*", function(req, res) {
//     res.render('index.ejs');
// });

app.post("/job", function(req, res) {
    var task_name = req.body.algorithm;
    var x = parseInt(req.body.dataX);
    var y = parseInt(req.body.dataY);
    var w = parseInt(req.body.dataWidth);
    var h = parseInt(req.body.dataHeight);
    var clientID = req.body.clientID;
    var bbox = x + ',' + y + ',' + (x+w) + ',' + (y+h);
    CURRENT_TASK = task_name
    if (clientID !== "" && clientID in CLIENTS){
        CLIENTS[clientID] = {
            'task_name' : task_name,
            'bbox' : bbox
        }
    }
    console.log('ClientID: ', clientID, 'Task: ', task_name);
    return res.send("1");
});

const REMOTE_SERVER = "0.0.0.0:50051";
const PROTO_PATH = __dirname + '/protos/dl_server.proto';
var packageDefinition = protoLoader.loadSync(PROTO_PATH, {
      keepCase: true,
      longs: String,
      enums: String,
      defaults: true,
      oneofs: true
});

var dl_server = grpc.loadPackageDefinition(packageDefinition);
var client = new dl_server.DLServer(
    REMOTE_SERVER,
    grpc.credentials.createInsecure()
);

// Start Server
server.listen(port, function () {
    if (use_https){
        console.log("Server listening on https://localhost:" + port);
    }
    else{
        console.log("Server listening on http://localhost:" + port);
    }
});

io.on("connection", function(socket){
    CLIENTS[socket.id] = {
        'task_name' : '',
        'bbox' : ''
    }
    // socket.emit('clientInfo', socket.id);
    io.to(socket.id).emit("clientInfo", socket.id);
    socket.on("disconnect", function(){
        console.log('SocketID stop: ', socket.id);
        if(socket.id in CLIENTS){
            delete CLIENTS[socket.id];
        }
    });

    socket.on("message", function(data){
        // var imageName = 'static/test.jpg';
        // fs.createWriteStream(imageName).write(data);
        // console.log('Socket Id is connecting: ', socket.id);
        // console.log('Number Client: ', Object.keys(CLIENTS).length);
        if(socket.id in CLIENTS){
            if(CLIENTS[socket.id].task_name !== ""){
                if (CLIENTS[socket.id].task_name === CURRENT_TASK){
                    client.proceed_image_task({task_name:CLIENTS[socket.id].task_name, image:data, bbox:CLIENTS[socket.id].bbox }, (err, res) => {
                        if(res){
                            if(socket.id in CLIENTS){
                                if(res.task_name === CLIENTS[socket.id].task_name){
                                    var bufferBase64 = new Buffer( res.image, 'binary' ).toString('base64');
                                    io.to(socket.id).emit("message", bufferBase64);
                                    console.log('Send to ', socket.id);
                                    // socket.emit("message", bufferBase64);
                                }
                            }
                        }
                    });
                }
                else{
                    socket.disconnect();
                }
            }
            else{
                var bufferBase64 = new Buffer( data, 'binary' ).toString('base64');
                // socket.emit("message", bufferBase64);
                io.to(socket.id).emit("message", bufferBase64);
            }
        }
    });
});

// protoc -I=. protos/dl_server.proto --js_out=import_style=commonjs:. --grpc-web_out=import_style=commonjs,mode=grpcwebtext:.
