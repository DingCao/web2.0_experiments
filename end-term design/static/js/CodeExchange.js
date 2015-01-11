// Copyright (c) 2014-2015 HuangJunjie, YaoShaoling & ZhangTingting@SYSU
// All Rights Reserved.

// the dictionary of Morse codes.
var enMorse = {
  // letters
  'a': ".-",   'b': "-...", 'c': "-.-.", 'd': "-..",  'e': ".",    'f': "..-.",
  'g': "--.",  'h': "....", 'i': "..",   'j': ".---", 'k': "-.-",  'l': ".-..",
  'm': "--",   'n': "-.",   'o': "---",  'p': ".--.", 'q': "--.-", 'r': ".-.",
  's': "...",  't': "-",    'u': "..-",  'v': "...-", 'w': ".--",  'x': "-..-",
  'y': "-.--", 'z': "--..",

  // nubmers
  '0': "-----", '1': ".----", '2': "..---", '3': "...--", '4': "....-",
  '5': ".....", '6': "-....", '7': "--...", '8': "---..", '9': "----.",

  // signs.
  // the space and the '\n' are here to simplify the encoding operation.
  ' ': "/", '\n': "\n",
  '.': ".-.-.-",  ',': "--..--", '?': "..--..", '\'': ".----.", '!': "-.-.--",
  '/': "-..-.",   '(': "-.--.",  ')': "-.--.-", '&': ".-...",   ':': "---...",
  ';': "-.-.-.",  '=': "-...-",  '+': ".-.-.",  '-': "-....-",  '_': "..--.-",
  '\"': ".-..-.", '$': "...-..-", '@': ".--.-."
}
var deMorse = {
  // letters
  ".-": 'a',   "-...": 'b', "-.-.": 'c', "-..": 'd',  ".": 'e',    "..-.": 'f',
  "--.": 'g',  "....": 'h', "..": 'i',   ".---": 'j', "-.-": 'k',  ".-..": 'l',
  "--": 'm',   "-.": 'n',   "---": 'o',  ".--.": 'p', "--.-": 'q', ".-.": 'r',
  "...": 's',  "-": 't',    "..-": 'u',  "...-": 'v', ".--": 'w',  "-..-": 'x',
  "-.--": 'y', "--..": 'z',

  // nubmers
  "-----": '0', ".----": '1', "..---": '2', "...--": '3', "....-": '4',
  ".....": '5', "-....": '6', "--...": '7', "---..": '8', "----.": '9',

  // signs.
  // the space and the '\n' are here to simplify the decoding operation.
  "/": ' ', "\n": '\n',
  ".-.-.-": '.',  "--..--": ',', "..--..": '?', ".----.": '\'', "-.-.--": '!',
  "-..-.": '/',   "-.--.": '(',  "-.--.-": ')', ".-...": '&',   "---...": ':',
  "-.-.-.": ';',  "-...-": '=',  ".-.-.": '+',  "-....-": '-',  "..--.-": '_',
  ".-..-.": '\"', "...-..-": '$', ".--.-.": '@'
}

function MorseEncode(text) {
  // post: default text is consist of ascii codes, such as letters, nubmers,
  // and some usual signs. Otherwise it can't be encode
  var code = "";
  var words = text.trim().split(/\s+/);
  for (var i = 0; i < words.length; i++) {
    if(i) code += ' ';
    for (var j = 0; j < words[i].length; j++) {
      if (j) code += '/';
      if (enMorse[words[i][j]])
        code += enMorse[words[i][j]];
      else
        code +=words[i][j];
    }
  }
  return code;
}

function MorseDecode(code) {
  // post: the encoded Morse code must be in this format so that it can to be
  // decoded:  "letter_code/letter_code letter_code/letter_code/letter_code"
  var text = "";
  var words = code.trim().split(/\s+/);
  for (var i = 0; i < words.length; i++) {
    if (i) text +=' ';
    var letters = words[i].split('/');
    for (var j = 0; j < letters.length; j++) {
      if (deMorse[letters[j]])
        text += deMorse[letters[j]];
      else
        text += letters[j];
    }
  }
  return text;
}

function Reverse(string) {
  return string.split("").reverse().join("");
}

function Caesar(string, move) {
  move = parseInt(move);
  if (move == NaN || move <= 0 || move >=26)
    return "请输入1~25的位移量！";

  var code = "";
  var str = string.toLowerCase();
  for (var i = 0; i < string.length; i++) {
    if (str[i] >= 'a' && str[i]<= 'z') {
      // A little bug is that when |move| is nagetive, the function can't
      // transform the letters correctly. So |move| will be limitted
      // from 1 to 25
      for (var temp = (str.charCodeAt(i)-97+move) % 26; temp < 97; temp += 97);
      code += String.fromCharCode(temp);
    } else {
      code += str[i];
    }
  }
  return code;
}
