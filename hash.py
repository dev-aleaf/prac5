"""                             HASH using hashlib with sha256()
authors: Alvarez Alejandro
         Tovar Brisa
version 1.5
April 2020
"""
import hashlib;
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


#---------------------------------------------------
#this function receives a file, get its digest and paste the digest at the end of the file
def getHash(file):
    hashedFileName = file.split(".")[0]+"_HASH.txt"
    tam= os.path.getsize(file)
    print("File size: "+str(tam))
    #rb= read in bynary format
    with open(file, 'rb') as fbytes:
        text = fbytes.read()
        #SHA256 returs a 32 length digest, it returns double size (64) for hexdigest
        result = hashlib.sha256(text)
        #There are 2 options of digest:binary and hex,
        #I chose hex in order to write it on file later
        digesto = result.hexdigest()

        #a= add information to the file
        with open(hashedFileName, 'w') as f:
            f.write(text.decode("utf-8"))
            f.write(digesto)
            f.close()
        fbytes.close()

        messagebox.showinfo("Hashed", "Succesfully Hashed")

#------------------------------------------------------

def verifyHash(file):
    #get length of file in bytes
    tam=0
    tam= os.path.getsize(file)
    print("File size: "+str(tam))

    #get position where digest starts
    posDigest=0
    posDigest= tam-64
    print(posDigest)

    #rb= read in bynary format
    with open(file, 'rb') as f:
        text = f.read(posDigest)
        #calculate digest of the text
        result = hashlib.sha256(text)
        digestoCal= result.hexdigest()
        #get digest pasted at the end of file
        digestoOrg= f.read(64).decode("utf-8")
    #print(digestoOrg)
    #print(digestoCal)
    if(digestoOrg==digestoCal):
        #means the file hasn't been corrupted
        return 0;
    else:
        #The file has been modified at some point
        return 1;

"""
Is triggered when the Load File is clicked,
checks the value of the Radiobutton doHash to see
if it is going to get the hash or verify it.
Receives/Returns: nothing
"""
def start():
    fileName = askopenfilename()
    gettingHash = doHash.get()

    if gettingHash == 1:
        getHash(fileName)
    else:
        resutlMessage = ''
        if (verifyHash(fileName)==1):
            resultMessage = "The FILE has been CORRUPTED"
        else:
            resultMessage = "The FILE remains UNCHANGED"
        messagebox.showinfo("CHECKED", resultMessage)


#------------------------main------------------
#create the GUI
root=Tk()
root.title("Prac 5 Hash")

doHash = BooleanVar()
yRbMode = 150

frame = Frame(root,width="800", height="600" )
frame.pack(anchor="n")
frame.config(bg="gray65")

lb=Label(frame, text="Select task", fg="black", font=(18), bg="white")
lb.place(x=340, y=50)

rECB = Radiobutton(frame)
rECB.config(text="Hash FILE", variable = doHash, value = True)
rECB.place(x = 200, y = yRbMode)

rCBC = Radiobutton(frame)
rCBC.config(text="Verify Hash", variable = doHash, value = False)
rCBC.place(x = 470, y = yRbMode)

encBtn=Button(frame)
encBtn.config(text="Upload File", bg="green", fg="white", width=10,command = start)
encBtn.place(x=340, y=540)

root.mainloop()
