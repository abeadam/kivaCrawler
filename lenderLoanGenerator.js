const LENDER_PATH = 'kiva_ds_json/lenders',
	  LOANS_PATH = 'kiva_ds_json/loans',
	  LOANS_LENDER = 'kiva_ds_json/loans_lenders',
	  OUTPUT_FILE = 'lender_loans.txt';
var fs = require('fs'),
	counter = 0,
	giantLenderLoanMap = {};
if (fs.existsSync(LOANS_PATH)) {
	counter++;
} else {
	console.log('please make sure your loans are in the folder'+LOANS_PATH);
	throw {
		message:'cant find loans',
		title: 'missing loans'
	};
}

if (fs.existsSync(LENDER_PATH)) {
	counter++;
} else {
	console.log('please make sure your loans are in the folder'+ LENDER_PATH);
	throw {
		message: 'cant find lenders',
		title: 'missing lenders'
	}
}

if (fs.existsSync(LENDER_PATH)) {
	counter++;
} else {
	console.log('please make sure your loans_lenders are in the folder'+ LOANS_LENDER);
	throw {
		message: 'cant find lenders',
		title: 'missing lenders'
	}
}

function addLoanToFile (lendersToLoanString) {
	fs.appendFile(OUTPUT_FILE, lendersToLoanString, function (err) {
		if (err) {
			console.log('problem appending data to file');
		}
	});
}

function processJSON (file) {
	var saveData = function (err, content) {
		var length,
			lendersLength,
			currentString = "",
			x = 0,
			i = 0,
			loan,
			loans;
		if (err) {
			console.log('cant find file '+ file);
			throw {
				message: 'check that file exists',
				title: 'missing file'
			}
		}
		var parsedJSON = JSON.parse(content, function(k, v) {
			if (k === 'paging') {
				return undefined;
			}
			return v;
		});
		loans = parsedJSON.loans_lenders;
		length = loans.length;
		currentString = "";
		for ( ; i < length ; i++) {
			loan = loans[i];
			if (loan.lender_ids) {
				lendersLength = loan.lender_ids.length;
			} else {
				lendersLength = 0;
			}
			x = 0;
			for ( ; x < lendersLength ; x++) {
				currentString += loan.id+'\t'+loan.lender_ids[x]+'\n';
			}
		}
		addLoanToFile(currentString);
	};
	fs.readFile(file, {
		encode: 'utf8'
	}, saveData);
}

function matchLendersToLoans() {
	fs.readdir(LOANS_LENDER, function (err, files) {
		var length,
			loc = 0;
		if (err) {
			console.log(err)
			return;
		}
		length = files.length;
		for ( ; loc < length ; loc++) {
			processJSON(LOANS_LENDER+'/'+files[loc]);
		}
	});
}


matchLendersToLoans();


