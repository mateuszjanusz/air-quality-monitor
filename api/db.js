const mysql = require('mysql')
console.log(process.env)
const config = require('./config')

const connection = mysql.createPool({
	host: process.env.host || config.host,
	database: process.env.database || config.database,
	user: process.env.user || config.user,
	password: process.env.password || config.password,
})

module.exports = connection