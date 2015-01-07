window.onload = function() {
  $('.replyBtn').click(addReply);
}

function addReply(){
  var form = $('<form></form>').attr({
      'id': 'response',
      'method': 'post',
      'action': '/response'
    });
    $(this).parent().append(
      $('<textarea></textarea>').attr({
        'class': 'jumbotron reply col-sm-10 col-sm-offset-2',
        'id': 'secrettext'
      }),
      $('<button></button>').attr({
        'id':'decipher',
        'class': 'replyBtn btn btn-primary'
      }).text('默认解密↓'),
      $('<button></button>').attr({
        'id':'encrypt',
        'class': 'replyBtn btn btn-primary'
      }).text('默认加密↓')
    );
    form.append(
      $('<textarea></textarea>').attr({
        'class': 'jumbotron reply col-sm-10 col-sm-offset-2',
        'name': 'responsetext',
        'id': 'responsetext'
      }),
      $('<input/>').attr({
        'name': 'title',
        'style': 'display:none',
        'value': $(this).prevAll('.title').text()
      }),
      $('<button></button>').attr({
        'class': 'replyBtn btn btn-primary',
        'type': 'submit'
      }).text('回复')
    );
    $(this).parent().append(form);
    $(this).remove();
    $('#decipher').click(function(){
      var code = MorseDecode($('#secrettext').val());
      if (Judge(code)) {
        $('#responsetext').val($('#responsetext').val()+code);
      } else {
        $('#secrettext').val('Sorry, try again!  ∩＿∩');
      }
    });
    $('#encrypt').click(function(){
      var code = MorseEncode($('#secrettext').val());
      if (Judge(code)) {
        $('#responsetext').val($('#responsetext').val()+code);
      } else {
        $('#secrettext').val('Sorry, try again!  ∩＿∩');
      }
    });
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
