function $(string) {
  return document.getElementById(string);
}

function $$(string) {
  return document.getElementsByName(string);
}

var timer;
var delay = 200;

window.onload = function () {
  // initializations
  $("Start").disabled = false;
  $("Stop").disabled = true;
  $("Turbo").checked = false;
  $("Animation").disabled = false;

  // events
  $("Start").onclick = function() {
    play($("Animation").value);
  }
  $("Stop").onclick = stop_or_change;
  $("Animation").onchange = stop_or_change;

  // a simple way to change the size.
  $$("Size")[0].onclick = function() {
    $("displayarea").className = $$("Size")[0].value;
  }
  $$("Size")[1].onclick = function() {
    $("displayarea").className = $$("Size")[1].value;
  }
  $$("Size")[2].onclick = function() {
    $("displayarea").className = $$("Size")[2].value;
  }
  $("Turbo").onchange = changeSpeed;
}

function play(type, delay) {
  var i = 0;
  $("Animation").disabled = true;
  $("Start").disabled = true;
  $("Stop").disabled = false;
  if (timer == null) timer = setTimeout(display, delay, i, type);
}

function display(i, type) {
  var action = ANIMATIONS[type].split("=====\n");
  $("displayarea").innerText = action[i % action.length];
  timer = setTimeout(display, delay, i + 1, type);
}

function stop_or_change() {
  if (timer != null) {
    clearTimeout(timer);
    timer = null;
  }
  $("displayarea").innerText = ANIMATIONS[$("Animation").value];
  $("Start").disabled = false;
  $("Animation").disabled = false;
}

function changeSpeed() {
  if ($("Turbo").checked)
    delay = 50;
  else
    delay = 200;
}
