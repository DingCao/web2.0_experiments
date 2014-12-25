// Copyright (c) 2014 Junjie_Huang@SYSU(SNO:13331087). All Rights Reserved.
function $(string) {
	return document.getElementById(string);
}

window.onload = function() {
	var puzzlepieces = $("puzzlearea").getElementsByTagName("div");
	for (var i = 0; i < puzzlepieces.length;i++) {
		puzzlepieces[i].className = "puzzlepiece";
	}
}
