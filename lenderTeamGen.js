const path = 'teams/',
    lenderTeamsFile = 'lenderTeams.txt',
    jsonCheck = /\.json$/,
    lineBreaks = /(\r\n|\n|\r|\s+)/gm;
var fs = require('fs'),
    lenderTeam = {};


function getObjects(str) {
    var objects = [],
        currentString = '',
        len = str.length,
        count = 0,
        current = 0;
    for (; current < len; current++) {
        currentString += str.charAt(current);
        if (str.charAt(current) === '{') {
            count++;
        } else if (str.charAt(current) === '}') {
            count--;
        }
        if (count === 0) {
            objects.push(JSON.parse(currentString));
            currentString = '';
        }
    }
    return objects;
}

function readFiles(err, files) {
    var len = err || files.length,
        current = 0,
        lenders = [],
        str;
    if (err) {
        console.log('error reading directory');
        console.log(err);
        return;
    }
    for (; current < len; current++) {
        if (jsonCheck.test(files[current])) {
            str = fs.readFileSync(path + files[current], {
                encoding: 'utf8'
            });
            // remove all the line breaks that will cause problem in json parse
            str = str.replace(lineBreaks, ' ');
            try {
                lenders = getObjects(str);
                lenders.forEach(function(lender) {
                    var key = Object.keys(lender),
                        teams;
                    if (lender[key].teams.length > 0) {
                        teams = lender[key].teams.map(function(team) {
                            return team.id;
                        });
                        teams.forEach(function(team) {
                            var string = key + "\t" + team + '\n';
                            fs.writeFileSync(lenderTeamsFile, string, {
                                encoding: 'utf8',
                                flag: 'a+'
                            }, function(err) {
                                console.log(err);
                            });
                        });
                    }
                });
            } catch (e) {
                console.log('couldnt parse ' + files[current]);
                console.log(e);
            }
        }
    }
}

//delete the file just in case
try {
    fs.unlinkSync(lenderTeamsFile);
    console.log('removed old file, generating new one now');
} catch (e) {
    console.log("file didn't exist, we will add it now");
}

fs.readdir(path, readFiles);