window.onload = function() {
  // js of index.html
  $('.replyBtn').click(addReply);

  // js of question.html
  $('.decipher').click(Decode);
  $('.encrypt').click(Encode);
  $('#secretproblem').click(function() {
    $('#content').val($('#content').val()+$('#secrettext').val());
  });
  $('#code-type').change(typeChange);
}

// when click on the "回复TA" button, add a new form for users to encode,
// decode and reply to a question.
function addReply(){
  var form = $('<form></form>').attr({
    'id': 'response',
    'method': 'post',
    'action': '/response'
  });

  if ($('#reply').val() != undefined) {
    var reply_parent = $('#reply').parent();
    var reply_btn = $('<button></button>').attr({
          'class': 'replyBtn btn btn-primary'
        }).text("回复TA");
    reply_btn.click(addReply);  // new elements need to blind events again
    $('#reply').remove();
    reply_parent.append(reply_btn);
  }
  $(this).parent().append(
    $('<div></div>').attr({
      'id': 'reply'
    })
  );

  $('#reply').append(
    $('<textarea></textarea>').attr({
      'class': 'jumbotron reply col-sm-10 col-sm-offset-2',
      'id': 'secrettext',
      'style':'width:83.2%'
    }),
    $('<select></select>').attr({
      'id': 'code-type',
      'class': 'replyBtn btn btn-primary'
    }).css('margin-left', '80%'),
    $('<button></button>').attr({
      'class': 'replyBtn btn btn-primary appendBtn'
    }).text('推送↓'),
    $('<button></button>').attr({
      'class': 'replyBtn btn btn-primary decipher'
    }).text('解密'),
    $('<button></button>').attr({
      'class': 'replyBtn btn btn-primary encrypt'
    }).text('加密')
  );

  $('#code-type').append(
    $('<option></option>').attr({
      'value': 'morse'
    }).text('摩斯密码（默认）'),
    $('<option></option>').attr({
      'value': 'reverse'
    }).text('逆序密码'),
    $('<option></option>').attr({
      'value': 'caesar'
    }).text('恺撒密码')
  )
  form.append(
    $('<textarea></textarea>').attr({
      'class': 'jumbotron reply col-sm-10 col-sm-offset-2',
      'name': 'responsetext',
      'id': 'responsetext',
      'style':'width:83.2%',
      'required': 'required'
    }),
    $('<input/>').attr({
      'name': 'title',
      'style': 'display:none',
      'value': $(this).prevAll('.title').text()
    }),
    $('<button></button>').attr({
      'class': 'replyBtn btn btn-primary',
      'type': 'submit'
    }).text('发送')
  );
  $('#reply').append(form);
  $(this).remove();  // delete the button we clicked on

  // events of the buttons in a new form
  $('.decipher').click(Decode);
  $('.encrypt').click(Encode);
  $('.appendBtn').click(function() {
    $('#responsetext').val($('#responsetext').val()+$('#secrettext').val());
  });
  $('#code-type').change(typeChange);
}

// operations of encoding and decoding
function Decode() {
  var text;
  if ($('#code-type').val() == 'morse')
    text = MorseDecode($('#secrettext').val());
  else if ($('#code-type').val() == 'reverse')
    text = Reverse($('#secrettext').val());
  else if ($('#code-type').val() == 'caesar')
    text = Caesar($('#secrettext').val(), $('#move').val());

  if (Judge(text)) {
    $('#secrettext').val(text);
  } else {
    $('#secrettext').val('Sorry, try again!  ∩＿∩');
  }
}
function Encode() {
  var code;
  if ($('#code-type').val() == 'morse')
    code = MorseEncode($('#secrettext').val().toLowerCase());
  else if ($('#code-type').val() == 'reverse')
    code = Reverse($('#secrettext').val());
  else if ($('#code-type').val() == 'caesar')
    code = Caesar($('#secrettext').val(), $('#move').val());

  if (Judge(code)) {
    $('#secrettext').val(code);
  } else {
    $('#secrettext').val('Sorry, try again!  ∩＿∩');
  }
}

// other functions
function typeChange() {
  if ($('#code-type').val() == 'caesar' && $('#move').val() == undefined) {
    $(this).before(
      $('<input></input>').attr({
        'typt': 'input',
        'id': 'move',
        'value': '4',
        'class': 'btn btn-primary'
      })
    );
  } else if ($('#code-type').val() != 'caesar' && $('#move').val()) {
    $('#move').remove();
  }
}

function Judge(input) {
  // judge whether users input in English
  var re = new RegExp("undefined");
  if (re.test(input)) {
    return false;
  } else {
    return true;
  }
}
