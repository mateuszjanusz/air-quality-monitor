const mysql = require('mysql')
const express = require('express')
const bodyParser = require('body-parser')

const db = require('./db')
const port = process.env.PORT || 3000

const app = express()

app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())

app.get('/', function (req, res) {
	res.status(200).send('OK');
});

app.get('/now', function (req, res) {
	return db.query('SELECT * FROM readings ORDER BY timestamp DESC LIMIT 1', function (error, results, fields) {
		
		if(error) return res.status(500).send(error);
		res.status(200).send(results[0]);
	});	
});


app.get('/today', function (req, res) {
	return db.query(`SELECT * FROM readings 
		WHERE DATE(timestamp) >= DATE((SELECT timestamp FROM readings ORDER BY timestamp DESC LIMIT 1))
		AND DATE(timestamp) < DATE((SELECT timestamp FROM readings ORDER BY timestamp DESC LIMIT 1)) + INTERVAL 1 DAY`, 
		function (error, results, fields) {
	
		if(error) return res.status(500).send(error);
		res.status(200).send(results);
	});	
});

app.get('/last-week', function (req, res) {
	return db.query(`SELECT * FROM readings 
			WHERE DATE(timestamp) >= DATE((SELECT timestamp FROM readings ORDER BY timestamp DESC LIMIT 1)) - INTERVAL 7 DAY
			AND DATE(timestamp) < DATE((SELECT timestamp FROM readings ORDER BY timestamp DESC LIMIT 1)) + INTERVAL 1 DAY`, function (error, results, fields) {
		
		if(error) return res.status(500).send(error);
		res.status(200).send(results);
	});	
});

app.get('*', function(req, res){
	res.status(404).send('you shall not pass');
})

app.listen(port, () => {
	console.log('Express server listening on port ' + port)
})