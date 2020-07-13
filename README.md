# Serial-UDP-Bridge
A bridge between several custom serial devices (arduino) and one UDP port.

Serial devices are expected to have the same baudrate andfolow a simple protocol:
If they get asked for an id ('I?\n') they should answer with a unique id ('1','2',...)

Messages from the serial devices going to the UDP connection are prefixed with that id followed by a ':' and the message.
For example: '1:test'

Likewise messges from the UDP connection to serial devices should be prefixed so that they can get routed correctly.
For example: '1:test' will send 'test\n' to the serial device with id 1
