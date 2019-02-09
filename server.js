const net = require('net')
const readline = require('readline');
const server = new net.Server();
const sockets = []

server.on('connection', (socket) => {
  console.log('New connection')
  socket.name = socket.remoteAddress + ":" + socket.remotePort
  sockets.push(socket)
  socket.on('end', () => {
    console.log(socket.name + " left the broadcast.\n")
    sockets.splice(sockets.indexOf(socket), 1)
  })
  socket.on('data', data => {
    console.log(data)
    sockets.forEach(s => s.write(data))
  })
  socket.on('error', data => {
    console.log('Error', data)
    sockets.splice(sockets.indexOf(socket), 1)
  })
})

server.listen(8000, () => console.log('Listening for connections'));