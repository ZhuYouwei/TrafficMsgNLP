const express = require('express')
const app = express()
app.use(express.static('public'))

var webscrap = require('./traffic_scraping.js')
var spawn = require("child_process").spawn
var jsonParser = require('body-parser').json()


// 1.request msgs using date
app.get('/api/msgs/:day/:month', function (req, res) {
  var results = req.params
  console.log("/api/msgs")
  webscrap.get_day(req.params.day,req.params.month).then(function(rs){
  	var tmp = {}
  	tmp.data = rs
  	res.json(tmp)
  })

  
})

// 2.request attri using msg
app.post('/api/attri',jsonParser,function (req,res){
	//call python script with the body using input
	console.log('/api/attri:' + JSON.stringify(req.body))
	var process = spawn('python',["analysis.py",req.body.msg])
	process.stdout.on('data',function(chunk){
	    var output = chunk.toString('utf8')
	    res.send(output)
	})
})

// 3.entry point 
app.get('/', function (req, res) {
  res.sendFile('public/main.html', {root: __dirname })
})
// webscrap(30,10)
app.listen(8000, function () {
  console.log('Example app listening on port 8000!')
})