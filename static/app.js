
$(document).ready(function() {
         
    // sending a connect request to the server.
    var send_pause = false
    var socket = io.connect('http://' + window.location.host);
  
    $('#playstream').on('click', function (event) {
        if (send_pause) {
            socket.emit('pausestream', {})
        }
        else {
            socket.emit('playstream', {
                sheikh: $('.streamsheikh').val(),
                surah: $('.streamsura').val()
            });
        }
        return false;
    });

    // event 'stream_status'
    socket.on('stream_status', function(msg) {
        console.log('Received event stream_status', msg);
        // update buttons
        switch(msg.status.playback) {
            case 'playing':
                $("#playstream").text("Pause")
                $("#stopstream").show()
                send_pause = true
                break
            case 'stopped':
                $("#playstream").text("Play")
                $("#stopstream").hide()
                send_pause = false
                break
            case 'paused':
                $("#playstream").text("Resume")
                $("#stopstream").show()
                send_pause = true
                break
        }
        // update selects
        $('.streamsheikh').val(msg.status.sheikh)
        $('.streamsura').val(msg.status.surah)
        // update main display
        $('#now').text($('.streamsheikh option:selected').text())
        $('#textoutput').text($('.streamsura option:selected').text())
    });
  
    // stop
    $('.stop').on('click', function(event) {
        socket.emit('stop', {
            stop: 'stop',
        });
        return false;
    });

});
