import os
import shutil
import tarfile

def archive(src,dst):
    #directory to extract the files
    extract_path=os.getenv("HOME")+"/"+"extract/" 

    #check if extract_path exists
    if os.path.isdir(extract_path)==False:
        os.mkdir(extract_path)
    
    
    os.chdir(src) #go in dir files to archive 
    files=os.listdir(".")#list of files to archive


    #open file tar and archive files
    tar=tarfile.open(dst,"w")
    #archive files
    for target in files:
        print("add",target)
        tar.add(target)

    tar.close()


    

def split_file(filename,chunk_size,dst):
    ''' This function take a file as an input and split it into files of chunk_size size.
    If the filename size is not a multiple of chunk_size, the last chunk will have smaller size.
    
    :param filename: the path of the file to split
    :param chunk_size: the size of the desired chunks in Bytes
    :param dst: the output directory
    '''
    
    offset=0
    x=0
    #get file size
    all_info=os.stat(filename)
    size_file=all_info.st_size
    
    #check if file is greater than the size supported by Telegram (for upload) https://core.telegram.org/bots/api#sending-files
    if size_file <=1073741824:
        print("file ok for upload to bot")
        exit(0)

    fd=open(filename,"rb")

    #split file 
    while offset<size_file:

        name=dst+"part"+str(x) #name parts 
        fout=open(name,"wb")
        fd.seek(offset,0)
        data=fd.read(chunk_size)#read chunk size for write a part
        fout.write(data)
        fout.close()
        offset=offset+chunk_size
        x=x+1
    fd.close()



#message of welcome
def show_info():
    print("Name: DIVIFILE")
    print("Os support: Gnu/Linux Mac Os")
    print("Status: Alpha\nVersion: 0.4")
    print("Release date: 21/09/2019")
    print("-"*25)

    choice=input("exit? [Y/N]: ")
    
    if choice =="Y" or choice=="y":
        print("Bye...")
        exit(0)


def show_options():
    print("[1] Help\n[2] Start program\n[3] Info\n[4] Exit")

def start_split():
    dst=filename=os.getenv("HOME")+"/"+"extract/archive.tar"#name and path of archive to split
    dst_split=os.getenv("HOME")+"/"+"extract/" #destination of part file
    chunk_size=524288000#size of 1 part

    #take input of dir where files are place
    src=input("Insert folder files: ")
    
    #check if directory source is valid and not empty
    if os.path.isdir(src)==False:
        print(src," is not valid directory retype please..")
        return start_split()

    if  not os.listdir(src):
        print("Directory is empty retype please...")
        return start_split()

    #archive files
    print("[*]archive..")
    archive(src,dst)

    #split files and save 
    print("[*]split..")
    split_file(filename,chunk_size,dst_split)

    print("Done!")

    print("files save at: %s"%dst)

    #remove archive.tar
    os.remove(filename)

    choice=input("exit? [Y/N]: ")
    
    if choice =="Y" or choice=="y":
        print("Bye...")
        exit(0)

def help():
    print("(1) Save all files that you would archive in to a folder")
    print("(2) Start software to archive and split files with option 2")

    choice=input("exit? [Y/N]: ")
    
    if choice =="Y" or choice=="y":
        print("Bye...")
        exit(0)

    

#-----main-----#
k=0
while k==0:
    show_options()

    choice=int(input("Insert option: "))
    

    if choice==1:
        help()
        

    elif choice==2:
        start_split()
        

    elif choice==3:
        show_info()
        

    elif choice==4:
        print("Bye...")
        k=1

    else:
        print("Invalid Option",choice)
        






   
   




