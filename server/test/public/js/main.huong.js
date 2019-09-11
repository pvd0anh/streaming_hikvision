var video;
var IMAGE = document.getElementById('bbox-image');
var cropper = undefined;
var send = true;

(function () {
  var onError, onSuccess, update, ws;

  onError = function (e) {
    $("#btnSubmit").attr("disabled", true);
    alert("Camera is not supported");
    return console.log("Rejected", e);
  };

  onSuccess = function (localMediaStream) {
    try {
      video.srcObject = localMediaStream;
    }
    catch{
      video.src = webkitURL.createObjectURL(localMediaStream);
    }
    video.play();

    ws =  io.connect(window.location.href);
    ws.on('connect', function(){
      ws.on('clientInfo', function(data){
        $("#clientID").val(data);
      });
      return console.log("Connected server");
    });

    ws.on('message', function(data){
      if($('#divSpinner').is(':visible')){
        $("#divSpinner").fadeOut("slow");
      }
      $("#cam").attr('src', 'data:image/jpg;base64,' + data);
    });

    ws.on('disconnect', function(){
      send = false;
      alert("Disconnected from server");
      return console.log("Disconnected from server");
    });

    ws.on('connect_error', function(){
      alert("Can not connect to server!");
      ws.disconnect();
    });
    return setInterval(update, 125);
  };

  update = function () {
    var canvas = document.createElement('canvas');
    canvas.width = 1280;
    canvas.height = 720;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toBlob(function (blob) {
      if(send){
        ws.emit('message', blob);
      }
    }, 'image/jpeg');
  };

  video = document.querySelector('video');

  navigator.getMedia = (
    navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia
  );

  navigator.getMedia({
    'video': true,
    'audio': false
  }, onSuccess, onError);

}).call(this);

$("#algorithm").on("change", function () {
  var model_name = this.value;
  var must_bb = parseInt($(this).find(':selected').attr('data-bb'));
  if (must_bb) {
    $(".bbox-container").show();
  } else {
    $(".bbox-container").hide();
    IMAGE.src = "";
    if (cropper !== undefined) {
      cropper.destroy();
    }
  }
});

function captureImage() {
  var canvas = document.createElement('canvas');
  canvas.width = 1280;
  canvas.height = 720;
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(function (blob) {
    IMAGE.src = URL.createObjectURL(blob);
    if (cropper !== undefined) {
      cropper.destroy();
    }
    cropper = new Cropper(IMAGE, {
      viewMode: 1,
      movable: false,
      zoomable: false,
      rotatable: false,
      scalable: false,
      autoCropArea: 0.25,
      crop: function (event) {
        let data = event.detail;
        $("#dataX").val(Math.round(data.x));
        $("#dataY").val(Math.round(data.y));
        $("#dataHeight").val(Math.round(data.height));
        $("#dataWidth").val(Math.round(data.width));
      }
    });
  });
}

$("#categories").submit(function(e) {
  e.preventDefault();
  $("#divSpinner").fadeIn("slow");
  var form = $(this);
  var url = form.attr('action');
  $.ajax({
         type: "POST",
         url: url,
         data: form.serialize(),
         success: function(data)
         {
           console.log("success");
           if($('.bbox-container').is(':visible')){
             $('html, body').animate({scrollTop:$(document).height()/3}, 'slow');
           }
         }
  });
});