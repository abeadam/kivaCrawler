var express = require('express');
var app = express();
var http = require('http');
var fs = require('fs');
var start = process.argv[2],
	end = process.argv[1],
	current = start;


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
				console.log(options.path);
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
	debugger;
	var str = fs.readFileSync(file, {encoding: 'utf8'} );
	return JSON.parse(str);
}

function getFileContent(num) {
	var json = readFile('./kiva_ds_json/lenders/'+num+'.json');
	return json;
}

function processJson (num) {
		var i = 0,
		json = getFileContent(num),
		len = json.header.page_size,
		lenders = json.lenders,
		lenderTeamObject = {},
		currentLender,
		getInfo = function(i) {
			var strInfo;
			if (i < len) {
				var currentLender = {},
				lenderId = lenders[i].lender_id;
				getJSONData(lenderId, function(data) {
					currentLender[lenderId] = data;
					strInfo = JSON.stringify(currentLender, function(key, value) {
						if (key === 'paging') {
							return undefined;
						} 
						return value;
					}, 4);
					fs.writeFile('teams/teams'+num+'.json',strInfo, {
						encoding: 'utf8',
						flag: 'a+'
					},function(err){
						if(err) {
							console.log('error writing file, contact Abe');
						}
					})
				});
				
				setTimeout(function () {
					getInfo(i+1);
				},2000);
			} else {
				if(current < end) {
					current++;
					console.log('reading file'+current);
					processJson(current);
				}
			}
		};

	getInfo(0);
}

console.log('starting');
console.log('reading file '+current);
processJson(current);
