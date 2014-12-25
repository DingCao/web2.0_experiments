// CSE 190 M, Spring 2009, Marty Stepp
// JavaScript code for colored rectangles example

var NUM_RECT_BABIES = 100;
/*
$ = function(id) {
    return document.getElementById(id);
}

$$ = function(selector) {
    return document.querySelector(selector);
}
*/
window.onload = function() {
    var a = 1;
    $("color").onclick = colorClick;

    // create many rectangles and add them to the page
    for (var i = 0; i < NUM_RECT_BABIES; i++) {
        var rect = document.createElement("div");
        rect.className = "rectangle";
        var x = Math.floor(Math.random() * 750);
        var y = Math.floor(Math.random() * 250);
        rect.style.left = x + "px";
        rect.style.top = y + "px";
        $("rectanglearea").appendChild(rect);
    }

    // self-add codes.

    // binding click on each rect
    var rects = $$("div.rectangle");
    for (var i = 0; i < $$("div.rectangle").length; i++) {
        $$("div.rectangle")[i].onclick = Click($$("div.rectangle")[i]);
        $$("div.rectangle")[i].ondbclick = dbClick($$("div.rectangle")[i]);
    }

    function Click(rect) {
        return function() {
            $("rectanglearea").removeChild(rect);
            $("rectanglearea").appendChild(rect);
        }
    }

    function dbClick(rect) {
        return function() {
            $("rectanglearea").removeChild(rect);
        }
    }
};

// Called when the Color button is pressed.
// Gives every rectangle on the page a random color.
function colorClick() {
    // in the CSS, we would have written:
    // color: rgb(255, 192, 187);
    var rects = $$("div.rectangle");
    for (var i = 0; i < rects.length; i++) {
        var r = Math.floor(Math.random() * 256);
        var g = Math.floor(Math.random() * 256);
        var b = Math.floor(Math.random() * 256);
        rects[i].style.backgroundColor = "rgb(" + r + ", " + g + ", " + b + ")";
    }
}
