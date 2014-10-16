var express = require('express');
var app = express();
var http = require('http');
var fs = require('fs');

var getRequestOptions = function (lender) {
	var self = this;
	self.host = 'api.kivaws.org';
	self.path = '/v1/lenders/'+lender+'/teams.json';
	self.method = 'GET';
}

// sending the request to get teams
function getJSONData(lender, setTeam) {
	var options = new getRequestOptions(lender),
		req;
	req = http.request(options, function(res) {
		var teamData = "";
		res.on('data', function (teamChunk) {
			teamData += teamChunk;
		});

		res.on('end', function() {
			if (res.statusCode === 200) {
				setTeam(JSON.parse(teamData));
			} else {
				console.log(res.statusCode);
				console.log('please send Abe an email if you see this');
			}
		})
	});

	req.on('error', function (error) {
		console.log(error);
		console.log('something broke in this request, if happens to many times, please email Abe !');
	});

	req.end();
}

function readFile(file) {
	var str = fs.readFileSync(file, {encoding: 'utf8'} );
	return JSON.parse(str);
}

function getFileContent() {
	var json = readFile('../kiva_ds_json/lenders/1.json');
	return json;
}

app.get('/', function(req, res) {
	var i = 0,
		json = getFileContent(),
		len = json.header.page_size,
		lenders = json.lenders,
		lenderTeamObject = {},
		currentLender,
		getInfo = function(i) {
			if (i < len) {
				var currentLender = {},
				lenderId = lenders[i].lender_id;
				getJSONData(lenderId, function(data) {
					currentLender[lenderId] = data;
					console.log(currentLender);
				});
				
				setTimeout(function () {
					getInfo(i+1);
				},2000);
			}
		};

	getInfo(0);
	res.send(json.lenders);
});

var server = app.listen(5000);