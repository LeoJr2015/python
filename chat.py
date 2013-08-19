from Tkinter import *
from socket import *
import cPickle, threading, sys
CMD_JOINED,CMD_LEFT,CMD_MSG,CMD_LINE,CMD_JOINRESP=range(5)
people={}

def sendMsg(msg):
    sendSock.send(msg,0)

def onQuit():
    'user clicked on quit button'
    sendMsg(chr(CMD_LEFT))
    root.quit()

def onMove(e):
    'Called when button is down and mouse is moved'
    global lastLine,mx,my
    canvas.delete(lastLine)
    mx,my=e.x,e.y

    # draw a new temp line
    lastLine=canvas.create_line(dx,dy,mx,my,width=2,fill='Black')

def onBDown(e):
    'User presses left button'
    global lastLine,dx,dy,mx,my
    canvas.bind('<Motion>',onMove) #start receiving move msgs
    dx,dy=e.x,e.y
    mx,my=e.x,e.y

    # draw a temp line
    lastLine=canvas.create_line(dx,dy,mx,my,width=2,fill='Black')

def onBUp(e):
    'User release left mouse button'
    canvas.delete(lastLine)
    canvas.unbind('<Motion>')

    #send out the draw-a-line command
    sendMsg(chr(CMD_LINE)+cPickle.dumps((dx,dy,e.x,e.y),1))

def onEnter(foo):
    'User hit the [Enter] key'
    sendMsg(chr(CMD_MSG)+entry.get())
    entry.delete(0,END) #clears the entry widget

def setup(root):
    'Creates the user interface'
    global msgs,entry,canvas

    #the big window holding everybody's messages
    msgs=Text(root,width=60,height=20)
    msgs.grid(row=0,column=0,columnspan=3)

    #hook up a scrollbar to see old messages
    s=Scrollbar(root,orient=VERTICAL)

    s.grid(row=0,column=3,sticky=N+S)

    #where you type your message
    entry=Entry(root)
    entry.grid(row=1,column=0,columnspan=2,sticky=W+E)
    entry.bind('<Return>',onEnter)
    entry.focus_set()

    b=Button(root,text='Quit',command=onQuit)
    b.grid(row=1,column=2)

    # A place to draw
    canvas=Canvas(root,bg='White')
    canvas.grid(row=0,column=5)
    #notify me button press and release messages
    canvas.bind('<ButtonPress-1>',onBDown)
    canvas.bind('<ButtonRelease-1>',onBUp)

def msgThread(addr,port,name):
    'Listen for and processes messages'

    #create a listen socket
    s=socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(('',port))

    #Join a muslticast group
    s.setsockopt(SOL_IP,IP_ADD_MEMBERSHIP,inet_aton(addr)+inet_aton(''))

    while 1:
        # get the message and strip off the command byte
        msg,msgFrom=s.recvfrom(2048)
        cmd,msg=ord(msg[0]),msg[1:]

        if cmd==CMD_JOINED: #new join
            msgs.insert(END,'(%s joined the chat)\n' % msg)
            #introduce myself
            sendMsg(chr(CMD_JOINRESP)+cPickle.dumps((name,myColor),1))

        elif cmd==CMD_LEFT: #somebody left
            who=people[msgFrom][0]
            if who==name:
                break
            msgs.insert(END,'%s left the chat\n'% who,'color_'+who)

        elif cmd==CMD_MSG: #new message to display
            who=people[msgFrom][0]
            msgs.insert(END,who,'color_%s' %who)
            msgs.insert(END,':%s\n' %msg)

        elif cmd==CMD_LINE: #DRAW A LINE
            dx,dy,ex,ey=cPickle.loads(msg)
            canvas.create_line(dx,dy,ex,ey,width=2,fill=people[msgFrom][1])
        elif cmd==CMD_JOINRESP: # INTRODUCING THEMSELVES
            people[msgFrom]=cPickle.loads(msg)
            who,color=people[msgFrom]

            #create a tag to draw a text in theie color
            msgs.tag_configure('color_'+who,foreground=color)

            #leave the multicast group
            s.socketopt(SOL_IP,IP_DROP_MEMBERSHIP,inet_aton(addr)+inet_aton(''))

if __name__=='__main__':
    argv=sys.argv
    if len(argv)<3:
        print 'Usage:',argv[0],'<name><color>''[addr=<multicast address>][port=<port>]'
        sys.exit(1)

    global name, addr, port, myColor
    addr='127.0.0.1' #default ip address
    port= 50000 # default port
    name,myColor=argv[1:3]
    for arg in argv[3:]:
        if arg.startswith('addr='):
            addr=arg[len('addr='):]
        elif arg.startswith('port='):
            port=int(arg[len('port='):])

    #starts up a new thread to process messages
    threading.Thread(target=msgThread,args=(addr,port,name)).start()

    #this is socket over which we send out messages
    global sendSock
    sendSock=socket(AF_INET,SOCK_DGRAM)
    sendSock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sendSock.connect((addr,port))

    #dont let the packets let die too soon
    sendSock.setsockopt(SOL_IP,IP_MULTICAST_TTL,2)

    #Create a Tk window and create the GUI
    root=Tk()
    root.title('%s chatting on channel %s:%d' %(name,addr,port))

    setup(root)

    #Join the chat!
    sendMsg(chr(CMD_JOINED)+name)
    root.mainloop()
