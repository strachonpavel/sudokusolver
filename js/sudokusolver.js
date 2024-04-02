

function emptySolutionState() {
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

function getCurrState() {
	s = [];
	for(var r=0;r<9;r++) {
		s[r] = [];
		for(var c=0;c<9;c++) {
			var idx = r.toString()+"_"+c.toString();
			var v = document.getElementById(idx).textContent; //elm is span
			if (v!='1' && v!='2' && v!='3' && v!='4' && v!='5' && v!='6' && v!='7' && v!='8' && v!='9') v = '';
			s[r][c] = v;
		}
	}
	return s;
}

function getSolutionState(sval, currState) {
	for(var r=0;r<9;r++) {
		for(var c=0;c<9;c++) {
			var v = currState[r][c];
			if (v!='1' && v!='2' && v!='3' && v!='4' && v!='5' && v!='6' && v!='7' && v!='8' && v!='9') v = '';
			if (v!='') sval = setCell(sval,r,c,v);
		}
	}
	return sval;
}

function initSolutionState(currState) {
	var sval = emptySolutionState();
	sval = getSolutionState(sval, currState);
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

function Solver(elId) {
	var currState = getCurrState();
	var sval = initSolutionState(currState);
	var ret = solve(sval);
	generate(elId, ret, currState);
}

function EraseAll(elId) {
	generate(elId);
}

function addMod(t) {
	var v = parseInt(t.textContent); //it is span
	if (v==undefined || v==null|| isNaN(v)) v = 0;
	v = (1 + v)%10;
	t.textContent = v==0?'\u00A0':v.toString(); //0 is nbsp
}



function generate(elId="sudoku", result, originalstate) {
	function showState(state, original) {
		o = "<table>";
		for (let r=0;r<9;r++) {
			o += "<tr>";
			for (let c=0;c<9;c++) {
				cell_bg = (((~~(r/3))+(~~(c/3)))%2)==1?"dark":"";
				v = (state!=undefined && state[r][c].length==1)?state[r][c].toString():'\u00A0';
				cell_color = (state!=undefined && original!=undefined && state[r][c].length==1 && original[r][c].length!=1 && state[r][c]!=original[r][c])?"solution":"";

				o += `<td><span id=\"${r.toString()}_${c.toString()}\" class=\"cell ${cell_bg} ${cell_color}\" onclick=\"addMod(this)\">${v}</span></td>`;
			}
			o += "</tr>";
		}
		o += "</table>";
		return o;
	}
	if (result!=undefined) {
		if (result.isTerminal===true) {
			o = 'Solution :<br />'+showState(result.state, originalstate);
		} else if(result.isTerminal===null) {
			o = 'No solution'+showState(originalstate);
		} else {
			o = 'Not finished:<br />'+showState(result.state, originalstate);
		}
	} else {
		o = showState();
	}

	var sudt = document.getElementById(elId);
	sudt.innerHTML = o;
	//return o;
}

function Load(elId) {
	generate(elId);
	//testState1();
	loadFromDisk();
}

function Save(elId) {
	//var contentType = 'text/plain';
	var contentType = 'application/json';
	var filename = 'sudoku.json';
	var content = new Blob([JSON.stringify(getCurrState())], {type: contentType});
	if (window.navigator.msSaveOrOpenBlob) // IE10+
		window.navigator.msSaveOrOpenBlob(content, filename);
	else { // Others
		var a = document.createElement("a"), url = URL.createObjectURL(content);
		a.href = url;
		a.download = filename;
		document.body.appendChild(a);
		a.click();
		setTimeout(function() {
			document.body.removeChild(a);
			window.URL.revokeObjectURL(url);  
		}, 0); 
	}
}

function loadFromDisk() {
	console.log("aa");
	var files = document.getElementById('loadDiskFile').files;
	if (files.length <= 0) return false;
	var fr = new FileReader();
	fr.onload = function(e) { 
		if (e.target.result) {
			try {
				
				var d = JSON.parse(e.target.result);
				for (let r=0;r<9;r++) {
					for (let c=0;c<9;c++) {
						var idx = r.toString()+"_"+c.toString();
						document.getElementById(idx).textContent = d[r][c];
					}
				}
			} catch(er) {
				showMessage('Error')
			}
		}
	}
	fr.readAsText(files.item(0));

}



function testState1() {
	document.getElementById("0_1").textContent = "6";
	document.getElementById("0_5").textContent = "5";
	document.getElementById("0_6").textContent = "8";
	document.getElementById("0_8").textContent = "4";

	document.getElementById("1_0").textContent = "2";
	document.getElementById("1_1").textContent = "7";
	document.getElementById("1_3").textContent = "6";
	document.getElementById("1_4").textContent = "9";

	document.getElementById("2_1").textContent = "4";
	document.getElementById("2_3").textContent = "8";

	document.getElementById("3_6").textContent = "5";
	document.getElementById("3_8").textContent = "8";

	document.getElementById("4_1").textContent = "5";
	document.getElementById("4_2").textContent = "6";
	document.getElementById("4_4").textContent = "4";
	document.getElementById("4_6").textContent = "3";
	document.getElementById("4_7").textContent = "1";

	document.getElementById("5_0").textContent = "8";
	document.getElementById("5_2").textContent = "9";

	document.getElementById("6_5").textContent = "6";
	document.getElementById("6_7").textContent = "5";

	document.getElementById("7_4").textContent = "3";
	document.getElementById("7_5").textContent = "9";
	document.getElementById("7_7").textContent = "8";
	document.getElementById("7_8").textContent = "7";

	document.getElementById("8_0").textContent = "6";
	document.getElementById("8_2").textContent = "1";
	document.getElementById("8_3").textContent = "5";
	document.getElementById("8_7").textContent = "2";

}