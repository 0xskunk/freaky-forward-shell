# freaky-forward-shell

Shell that uses pipes to create a persistent session by writing to and reading from a stateful session. Based heavily on the work by Ippsec demonstrated in his Stratosphere video. Allows the bypassing of outbound firewalls as it communicates over HTTP and sends commands to an input pipe, which then processes it, and simple sends a second command to read back from the output pipe. Currently set up to work with a jwt exploit that I was working on, but can easily be edited to work with exploits such as shellshock.
x
