const mysql = require('mysql');
const config = require('./config')

const connection = mysql.createPool(config)

module.exports = connection