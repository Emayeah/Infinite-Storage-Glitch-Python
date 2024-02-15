import cv2 #imports opencv, make sure that you have opencv installed
import numpy as np #imports numpy and makes it be called with np because lazy
import os #imports os, needed for reading file size

def create_video(output_video_path, inputf, width=1280, height=720, frame_rate=12, pix=5): #change the width and height however you like, width is the width, height is the height and pix is the bit size in pixels (you need to check if your desired height and width can be divided with pix, if not change pix or height and width)
    with open(inputf, 'rb') as file: #declares file as the input file
        size = os.path.getsize(inputf) #gets the size of the file
        print(size) #prints the size
        chunk = int(width*height/(pix*pix)) #get the chunk, or in better terms how many bits a single frame can contain
        width1 = width #i could just divide height1 and width1 directly, but it breaks compatibility since i need to swap all the var names and im lazy
        height1 = height #i could just divide height1 and width1 directly, but it breaks compatibility since i need to swap all the var names and im lazy
        width = int(width / pix) #i could just divide height1 and width1 directly, but it breaks compatibility since i need to swap all the var names and im lazy
        height = int(height / pix) #i could just divide height1 and width1 directly, but it breaks compatibility since i need to swap all the var names and im lazy
        add = height * width #declares add so that basically i dont need to multiply height and width over and over when trying to add the elapsed bits
        total_bits = size * 8 #gets the total bits
        print(total_bits) #prints the total bits amount
        if total_bits <= chunk: #if the file fits in one frame or less, then set the bits amount to the chunk
            total_bits = chunk #sets bit length as the chunk if previous condition is true
            print(total_bits) #prints bit length if the condition is true, for debugging purposes (kinda useless)
        total_frames = int(np.ceil(total_bits / (width * height))) #gets the total frames amount
        print(total_frames) #prints the total frames
        fourcc = cv2.VideoWriter_fourcc(*'png ') #codec (fourcc)
        index = 0 #this number is totally useless except for the fact that it prints how many buts it has converted, updates each frame
        video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width1, height1), isColor=False) #DONT SWAP WIDTH1 AND HEIGHT1, OTHERWISE OPENCV GETS REAL MAD AND IT WILL MURDER YOUR HOPES AND DREAMS BY NOT CREATING THE VIDEO (empty video file) AND TELL YOU NOTHING ABOUT WHY IT HAPPENED 
        m = 1 #just an indicator to check if the first frame has been done, m=1 = no, m=0 = yes
        for _ in range(total_frames): #do the frames after the 1st
            if m == 0: #checks if the 1st frame is done, it is important
                frame = np.zeros((height, width), dtype=np.uint8) #create the frame
                content = file.read(int(chunk / 8)) #read the portion of the file needed to fill 1 frame (resulting in less ram usage), the divide by 8 is there since chunk represents of the bits that can fit in one frame, and this converts it into bytes
                content = ''.join(format(byte, '08b') for byte in content) #converts content into a string otherwise the program will get pretty mad
                values = np.array([int(content[bit2]) * 255 for bit2 in range (chunk)]) #basically if it is reading a 1 it will multiply it by 255, resulting in 255 (white), otherwise it'll multiply 0 by 255 resulting in 0 (black)
                values = values.reshape(-1) #idk what it does honestly, afaik it reshapes values into a 1d array
                index += add #increments index by the amount of bits it has converted
                print(f"{index} 1") #prints the bits it has converted in total, if you get the bits amount of the file and compare it with the output you can get a pseudo progress percentage
                frame.flat = values #writes the bits to the frame right after flattening the frame into a 1d picture
                frame = frame.reshape((height, width)) #converts the frame back into 2d
                frame = cv2.resize(frame, (width1, height1), interpolation=cv2.INTER_NEAREST) #enlargens the frame back into the original resolution, instead of writing each bit (it will take longer if i do the latter)
                video_writer.write(frame) #writes the frame instead of caching it in ram, resulting in less ram usage
            else: #PRETTY SMART STUFF, I SUGGEST TO NOT EDIT (except the one that declares size2, but it still works as it is tho, so maybe dont change it)
                frame = np.zeros((height, width), dtype=np.uint8) #create the frame
                size2 = size * 8 #converts the total bytes amount into bits, didnt want to use the other variable because uhh idk feel free to change it i did not test it
                size3 = size2 % chunk #gets the bits it needs to write
                temp = chunk - size3 #gets the padding bits it will write at the beginning of the 1st frame, this is basically why i split the stuff that makes the 1st frame from the others
                print(temp)
                content = file.read(int(size3 / 8)) #read the bits needed for the 1st frame
                binary_data = '0' * (temp - 1) #creates the padding 0s (except for the last 0 where it is swapped for a 1, for decoding purposes)
                binary_data += '1' #puts the 1 at the end of the padding, i made room specifically for that
                content = ''.join(format(byte, '08b') for byte in content) #converts content into a string otherwise the program will get pretty mad
                binary_data += content #appends at the end the data itself
                values = np.array([int(binary_data[bit]) * 255 for bit in range(chunk)]) #basically if it is reading a 1 it will multiply it by 255, resulting in 255 (white), otherwise it'll multiply 0 by 255 resulting in 0 (black)
                values = values.reshape(-1) #idk what it does honestly, afaik it reshapes values into a 1d array
                index += add #increments index by the amount of bits it has converted
                print(f"{index} 0") #prints the bits it has converted in the 1st frame
                frame.flat = values #writes the bits to the frame right after flattening the frame into a 1d picture
                frame = frame.reshape((height, width)) #converts the frame back into 2d
                frame = cv2.resize(frame, (width1, height1), interpolation=cv2.INTER_NEAREST) #enlargens the frame back into the original resolution
                video_writer.write(frame) #writes the frame instead of caching it in ram, resulting in less ram usage
                m = 0 #changes the indicator to say that the 1st frame has been done
        video_writer.release()

if __name__ == "__main__": #checks if the program has already been run
    input_file_path = "/home/ema/Desktop/bk foot lettuce2.txt" #replace with the path to your input file
    output_video_path = "/home/ema/Desktop/Out1.avi" #replace with the desired output video path
    create_video(output_video_path, input_file_path) #calls create_video function


