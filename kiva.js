var http = require('http');
var fs = require('fs');
var http5Socket = require('socks5-http-client');
var start = process.argv[2],
	end = process.argv[3],
	current = start;
var proxies = [{
	host: "54.68.46.84",
	port: "80"
},{
	host: "54.82.89.226",
	port: "443"
}];

var currentProxy = 0;


var getRequestOptions = function (lender) {
	var self = this;
	//host = proxies[currentProxy].host;
	self.hostname = 'api.kivaws.org';
	self.socksPort = '9050';
	//self.port = proxies[currentProxy].port,
	self.path = 'http://api.kivaws.org/v1/lenders/'+lender+'/teams.json';
	self.method = 'GET';
	self.headers = {
		HOST: 'api.kivaws.org'
	};
}

// sending the request to get teams
function getJSONData(lender, setTeam, retry) {
	var options = new getRequestOptions(lender),
		req;
	req = http5Socket.get(options, function(res) {
		var teamData = "";
		res.setEncoding('utf8');
		res.on('data', function (teamChunk) {
			teamData += teamChunk;
		});

		res.on('end', function() {
			//currentProxy = (currentProxy+1) %  (proxies.length-1)
			if (res.statusCode === 200) {
				try {
					setTeam(JSON.parse(teamData));
					console.log(teamData);
				}catch(e) {
					console.log('parse fail');
					setTimeout(function () {
						retry(lender);
					},100);	
				}
			} else {
				console.log(res.statusCode);
				console.log(options.path);
				console.log('please send Abe an email if you see this');
				if (res.statusCode === 403) {
					retry(lender);
				}
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
				}, function (lenderId) {
					console.log('sleeping');
					setTimeout(function(){
						//getJSONData(lenderId);
					}, 10000);
				});
				
				setTimeout(function () {
					getInfo(i+1);
				},500);
			} else {
				current++;
				if(current < end) {
					console.log('reading file '+current);
					processJson(current);
				}
			}
		};
	getInfo(0);
}

console.log('starting');
console.log('reading file '+current);
processJson(current);
