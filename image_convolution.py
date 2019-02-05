from PIL import Image
ima=""

def recall(im,main,width,height,ch):
    if ch==1:
        main1=noise(main,width,height)
        displayImage(im,main1)
    elif ch==2:
         gray=rgbtogray(pix,width*height)
         grayscaledisplay(im,gray)
    elif ch==3:
        kern=kernel()
        div=int(input('enter divisor'))
        off=int(input('enter offset'))
        inp=int(input('enter 1 for color image 2 for greyscale'))
        if inp==1:
            main1=kernel_multiplication(main,width,height,kern,div,off)
            displayImage(im,main1)
        elif inp==2:
            main1=greykern(pix,width,height,kern,div,off)
            grayscaledisplay(im,main1)


    elif ch==4:
        kern=[0,-1,0,-1,5,-1,0,-1,0]
        main1=kernel_multiplication(main,width,height,kern,2,40)
        per=int(input('enter the degree of sharpness'))
        main2=merge(main,main1,width,height,per)
        displayImage(im,main2)
    elif ch==5:
        kern=[6,2,6,2,1,2,6,2,6]
        main1=kernel_multiplication(main,width,height,kern,32,0)
        main1=kernel_multiplication(main1,width,height,kern,32,0)

        displayImage(im,main1)
    elif ch==6:
        main1=invert_image(main,width,height)
        displayImage(im,main1)
    elif ch==7:
        lkern=[1,0,-1,2,0,-2,1,0,-1]
        gl=greykern(pix,width,height,lkern,4,0)
        rkern=[-1,0,1,-2,0,2,-1,0,1]
        gr=greykern(pix,width,height,rkern,5,-100)
        g=mergegrey(gl,gr,width*height)
        graydisplay(im,g)
    elif ch==8:
        a=int(input('enter the horizontal degree '))
        b=int(input('enter the vertical degree '))
        main1=channelshift(main,width,height,a,b)
        displayImage(im,main1)





def invert_image(main,width,height):
    main1=main
    for i in range(height):
        for j in range(width):
            R=255-main[i][j][0]
            G=255-main[i][j][1]
            B=255-main[i][j][2]
            t=(R,G,B)
            main1[i][j]=t
    return main1
def channelshift(main,width,height,a,b):
    main1=main
    for i in range(a,height-a):
        for j in range(b,width-b):
            R=main[i-a][j-b][0]
            G=main[i][j][1]
            B=main[i+a][j+b][2]
            t=(R,G,B)
            main1[i][j]=t

    return main1
def mergegrey(g1,g2,size):
    g3=g1
    for i in range(size):
        a=g1[i]+g2[i]
        g3[i]=a
    return g3
def merge(main1,main2,width,height,per):
    p=per/100
    main3=main1
    for i in range(height):
        for j in range(width):
            R=int((1-p)*main1[i][j][0]+p*main2[i][j][0])
            G=int((1-p)*main1[i][j][1]+p*main2[i][j][1])
            B=int((1-p)*main1[i][j][2]+p*main2[i][j][2])
            if R>255:
                R=255
            if G>255:
                G=255
            if B>255:
                B=255
            t=(R,G,B)
            main3[i][j]=t
    return main3

def greykern(pix,width,height,kern,div,off):
    g=rgbtogray(pix,width*height)
    main1=[]
    i=0
    for row in range(height):
        l=[]
        for column in range(width):
           l.append(g[i])
           i+=1
        main1.append(l)
    Gr=[]
    for i in range(height-3):
        for j in range(width-3):
            n=0
            for l in [i,i+1,i+2]:
                for m in [j,j+1,j+2]:
                    Gr.append(main1[l][m]*kern[n])
                    n+=1

            if(sum(Gr)/div+off>255):
                a=255
            elif(sum(Gr)<0):
                a=0
            else:
                a=int(sum(Gr)/div)+off
            main1[i+1][j+1]=a
            Gr=[]
    main2=convertlist(main1,width,height)
    return main2


def kernel_multiplication(main,width,height,kern,div,off):
    R=[]
    G=[]
    B=[]
    main1=main
    for i in range(height-3):
        for j in range(width-3):
            n=0
            for l in [i,i+1,i+2]:
                for m in [j,j+1,j+2]:
                    R.append(main[l][m][0]*kern[n])
                    G.append(main[l][m][1]*kern[n])
                    B.append(main[l][m][2]*kern[n])
                    n=n+1

            if((sum(R)/div)>255):
                a=255
            else:
                a=int(sum(R)/div)+off
            if((sum(G)/div)>255):
                b=255
            else:
                b=int(sum(G)/div)+off
            if((sum(B)/div)>255):
                c=255
            else:
                c=int(sum(B)/div)+off
            '''
            a=int(sum(R))
            b=int(sum(G))
            c=int(sum(B))
            '''
            t=(a,b,c)
            main1[i+1][j+1]=t
            R=[]
            G=[]
            B=[]
    return main1
def noise(main,width,height):
    i=0
    j=0
    t=()
    R=[]
    G=[]
    B=[]
    main1=main
    for i in range(height-3):
        for j in range(width-3):
            for l in [i,i+1,i+2]:
                for m in [j,j+1,j+2]:
                    R.append(main[l][m][0])
                    G.append(main[l][m][1])
                    B.append(main[l][m][2])
            R.sort()
            G.sort()
            B.sort()
            t=(R[4],G[4],B[4])
            R=[]
            G=[]
            B=[]
            main1[i+1][j+1]=t
    return main1
def rgbtogray(pix,size):

    gray=0

    i=0

    g=[]
    for i in range(size):

        gray=(pix[i][0]*0.299)+(pix[i][1]*0.587)+(pix[i][2]*0.114)

        g.append(gray)

    return g
def graydisplay(im,gray):
    saved_size=im.size
    im2=Image.new('1',saved_size)
    im2.putdata(gray)
    im2.show()

def grayscaledisplay(im,gray):
    saved_size=im.size
    im2=Image.new('L',saved_size)
    im2.putdata(gray)
    im2.show()
def displayImage(im,main):

    file=im

    saved_mode=file.mode

    saved_size=file.size

    width,height=file.size

    im2=Image.new(saved_mode,saved_size)

    pix2=convertlist(main,width,height)

    im2.putdata(pix2)

    im2.show()



def convertlist(main,width,height):

    pix2=[]

    for k in range (height):
        for l in range(width):
            pix2.append(main[k][l])
    return pix2

def convertPix(ima,width,height,ch):
    im=Image.open(ima,'r')
    pix=list(im.getdata())
    main=[]
    i=0
    for row in range(height):
        l=[]
        for column in range(width):
           l.append(pix[i])
           i+=1
        main.append(l)
    if ch==1:
        main1=noise(main,width,height)
        displayImage(im,main1)
    elif ch==2:
         gray=rgbtogray(pix,width*height)
         grayscaledisplay(im,gray)
    elif ch==3:
        kern=kernel()
        div=int(input('enter divisor'))
        off=int(input('enter offset'))
        inp=int(input('enter 1 for color image 2 for greyscale'))
        if inp==1:
            main1=kernel_multiplication(main,width,height,kern,div,off)
            displayImage(im,main1)
        elif inp==2:
            main1=greykern(pix,width,height,kern,div,off)
            grayscaledisplay(im,main1)


    elif ch==4:
        kern=[0,-1,0,-1,5,-1,0,-1,0]
        main1=kernel_multiplication(main,width,height,kern,2,40)
        per=int(input('enter the degree of sharpness'))
        main2=merge(main,main1,width,height,per)
        displayImage(im,main2)
    elif ch==5:
        kern=[6,2,6,2,1,2,6,2,6]
        main1=kernel_multiplication(main,width,height,kern,32,0)
        main1=kernel_multiplication(main1,width,height,kern,32,0)

        displayImage(im,main1)
    elif ch==6:
        main1=invert_image(main,width,height)
        displayImage(im,main1)
    elif ch==7:
        lkern=[1,0,-1,2,0,-2,1,0,-1]
        gl=greykern(pix,width,height,lkern,4,0)
        rkern=[-1,0,1,-2,0,2,-1,0,1]
        gr=greykern(pix,width,height,rkern,5,-100)
        g=mergegrey(gl,gr,width*height)
        graydisplay(im,g)
    elif ch==8:
       a=int(input('enter the horizontal degree '))
       b=int(input('enter the vertical degree '))
       main1=channelshift(main,width,height,a,b)
       displayImage(im,main1)


    print('would you like to continue with the same image')
    c=input('YES/NO')
    if c=='YES':
        ch1=int(input('enter your option'))
        recall(im,main1,width,height,ch1)



    #main3=grekern(pix,width,height)
    #grayscaledisplay(im,main3)
def getImage():
    width=0;height=0;
    b=[1,2,3,4,5,6,7,8]
    print('Welcome to S cube editor')
    while 1:
        print('1.Noise Reduction')
        print('2.Gray Scale')
        print('3.Your kernel')
        print('4.Sharpness')
        print('5.Blur')
        print('6.Negative image')
        print('7.sobel')
        print('8.channelshift')
        print('100.exit')
        ch=int(input('Enter your choice'))
        if ch==100:
            print('thank you')
            break
        elif(ch in b):
            ima=input('Enter the source of the image with the directory ')
            im=ima
            with Image.open(ima,'r') as img:
                width,height = img.size
            print('The size of the image is:')
            print(width,height)
            convertPix(im,width,height,ch)


        else:
            print('WRONG VALUES')
            print('ENTER AGAIN')


def kernel():
    a=[0,0,0,0,0,0,0,0,0]

    print('enter your kernel values row wise')
    for i in range(0,9):
        a[i]=int(input())

getImage()
