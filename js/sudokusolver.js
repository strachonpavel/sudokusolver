

function emptyState() {
	var sval = [];
	for(var r=0;r<9;r++) {
		var rval = [];
		for(var c=0;c<9;c++) {
			rval.push('123456789');
	    }
		sval.push(rval);
	}
	return sval;
}

function setCell(so,r,c,v) {
	var cr = Math.floor(r/3);
	var cc = Math.floor(c/3);
	var s = JSON.parse(JSON.stringify(so));
	var nv;
	var reCheck = {};
	s[r][c] = v;
	for(var i=0;i<9;i++) {
		if(r!=i) {
			nv = s[i][c].replace(v,'');
			if (s[i][c]!=nv) {
				s[i][c] = nv;
				if (nv.length==1) { reCheck[[i,c]] = nv; }
			}
		}
		if(c!=i) {
			nv = s[r][i].replace(v,'');
			if (s[r][i]!=nv) {
				s[r][i] = nv;
				if (nv.length==1) { reCheck[[r,i]] = nv; }
			}
		}
		for(var j=0;j<9;j++) {
			if (Math.floor(i/3)==cr && Math.floor(j/3)==cc) {
				if(r!=i && c!=j) {
					nv = s[i][j].replace(v,'');
					if (s[i][j]!=nv) {
						s[i][j] = nv;
						if (nv.length==1) { reCheck[[i,j]] = nv; }
					}
				}
			}
		}
	}
	for (var k in reCheck) {
		var ki = k.split(",");
		if (reCheck[k]!=s[ki[0]][ki[1]]) continue;
		//console.log("b", r,c,v,reCheck);
		s = setCell(s,ki[0],ki[1],reCheck[k]);
	}
	return s;
}

function loadForm(sval) {
	for(var r=0;r<9;r++) {
		for(var c=0;c<9;c++) {
			var idx = r.toString()+"_"+c.toString();
			var v = document.getElementById(idx).value;
			if (v!='1' && v!='2' && v!='3' && v!='4' && v!='5' && v!='6' && v!='7' && v!='8' && v!='9') v = '';
			if (v!='') sval = setCell(sval,r,c,v);
		}
	}
	return sval;
}

function loadTestData1(sval) {
	sval = setCell(sval,0,0,'1');
	sval = setCell(sval,0,1,'2');
	sval = setCell(sval,0,2,'3');
	sval = setCell(sval,1,0,'4');
	sval = setCell(sval,1,1,'5');
	sval = setCell(sval,1,2,'6');
	sval = setCell(sval,2,0,'7');
	sval = setCell(sval,2,1,'8');
	sval = setCell(sval,2,2,'9');
	
	sval = setCell(sval,3,3,'1');
	sval = setCell(sval,3,4,'2');
	sval = setCell(sval,3,5,'3');
	sval = setCell(sval,4,3,'4');
	sval = setCell(sval,4,4,'5');
	sval = setCell(sval,4,5,'6');
	sval = setCell(sval,5,3,'7');
	sval = setCell(sval,5,4,'8');
	sval = setCell(sval,5,5,'9');
	return sval;
}

function loadTestData2(sval) {
	sval = setCell(sval,0,0,'1');
	sval = setCell(sval,0,1,'2');
	sval = setCell(sval,0,2,'3');
	sval = setCell(sval,0,3,'4');
	sval = setCell(sval,0,4,'5');
	sval = setCell(sval,0,5,'6');
	sval = setCell(sval,0,6,'7');
	sval = setCell(sval,0,7,'8');
	
	sval = setCell(sval,3,0,'2');
	sval = setCell(sval,3,1,'3');
	sval = setCell(sval,3,2,'4');
	sval = setCell(sval,3,3,'5');
	sval = setCell(sval,3,4,'6');
	sval = setCell(sval,3,5,'7');
	sval = setCell(sval,3,6,'8');
	sval = setCell(sval,3,7,'1');
	return sval;
}

function initState() {
	var sval = emptyState();
	sval = loadForm(sval);
	//sval = loadTestData1(sval);
	return sval;
}

function checkTerminalState(s) {
	var l;
	var ret = true;
	var v = [10,0,0];
	for(var r=0;r<9;r++) {
		for(var c=0;c<9;c++) {
			l = (s[r][c]).length;
			if (l<1) { return { isTerminal: null, value: v};}
			else if (l>1) {
				ret =  false;
				if (l<v[0]) { v = [l, r, c]; }
			}
		}
	}
	return {isTerminal: ret, value:  v};
}

function showResult(r) {
	function showState(s) {
		var t = '<table>';
		for(var r=0;r<9;r++) {
			t += '<tr>';
			for(var c=0;c<9;c++) {
				t += '<td>'+s[r][c].toString()+'</td>';
			}
			t += '</tr>';
		}
		t += '</table>';
		return t;
	}
	
	var sudt = document.getElementById("test");
	var m;
	if (r.isTerminal===true) {
		m = 'Reseni:<br />'+showState(r.state);
	} else if(r.isTerminal===null) {
		m = 'Nelze vyresit';
	} else {
		 m = 'Nedokonceno:<br />'+showState(r.state);
	}
	sudt.innerHTML = m;
}

function solve(s) {
	var t = checkTerminalState(s);
	if (t.isTerminal===false) {
		var r = t.value[1];
		var c = t.value[2];
		cs = s[r][c].split("");
		for(cv of cs) {
			var ns = setCell(s,r,c,cv);
			var ri =  solve(ns);
			if (ri.isTerminal===true) return ri;
		}
		
		return {isTerminal:null, state:s};
	} 
	return {isTerminal: t.isTerminal, state: s}
}

function Solver() {
	var sval = initState();
	var ret = solve(sval);
	showResult(ret);
}
