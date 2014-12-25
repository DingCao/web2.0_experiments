function $(string) {
  return document.getElementById(string);
}

function $$(string) {
  return document.getElementsByName(string);
}

var timer = null;  // the timer to control whether an animation should be played
var delay = 200;  // default speed of the animations

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

  // a more universal way to change the size.
  for (var i =0; i < $$("Size").length; i++) {
    $$("Size")[i].onclick = changeSize;
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

function changeSize() {
  $("displayarea").className = this.value;
}
