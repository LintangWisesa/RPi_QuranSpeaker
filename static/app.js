
$(document).ready(function() {
         
    // sending a connect request to the server.
    var socket = io.connect('http://' + window.location.host);
  
    // An event handler for submit button & get input value 
    $('#playsurah').on('click', function(event) {
        socket.emit('playsurah', {
            surah: $('.surah option:selected').text(),
            surahval: $('.surah').val(),
            awal: $('.awal').val(),
            akhir: $('.akhir').val()
        });
        return false;
    });

    $('#playjuz').on('click', function(event) {
        socket.emit('playjuz', {
            juz: $('.juz option:selected').text(),
            juzval: $('.juz').val(),
        });
        return false;
    });

    $('#playstream').on('click', function (event) {
        socket.emit('playstream', {
            sheikh: $('.streamsheikh option:selected').text(),
            sheikhval: $('.streamsheikh').val(),
            surah: $('.streamsura option:selected').text(),
            surahval: $('.streamsura').val()
        });
        return false;
    });

    // event 'after connect'   
    socket.on('after connect', function(msg) {
        console.log('After connect', msg);
    });
  
    // event 'update value'
    socket.on('update surah', function(msg) {
        console.log('Value updated');
        $('#textoutput').text(msg.surah);
        $('#now').text(msg.surah);
    });

    socket.on('update juz', function(msg) {
        console.log('Value updated');
        $('#textoutput').text(msg.juz);
        $('#now').text(msg.juz);
    });

    socket.on('update stream', function (msg) {
        console.log('Value updated');
        $('#textoutput').text(msg.surah);
        $('#now').text(msg.sheikh);
    });

    // stop
    $('.stop').on('click', function(event) {
        socket.emit('stop', {
            stop: 'stop',
        });
        return false;
    });

});
