const mysql = require('mysql')
let connection 

if(process.env.NODE_ENV === 'production' ){
	connection = mysql.createPool({
		host: process.env.host,
		database: process.env.database,
		user: process.env.user,
		password: process.env.password,
	})
} else {
	const config = require('./config')
	connection = mysql.createPool(config)
}

module.exports = connection