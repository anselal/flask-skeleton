// custom javascript

$(document).ready( () => {

    alertify.set('notifier', 'position', 'top-right')

    let socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    socket.on('client notification', (msg) => {
        alertify.notify(msg.data, msg.result != undefined ? msg.result : "success")
    });
})