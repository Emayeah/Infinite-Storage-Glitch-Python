import cv2
import numpy as np
import os

def create_video(output_video_path, inputf, width=1280, height=720, frame_rate=12, pix=5): #change the width and height however you like, pix is the size of each bit in pixels (to resist compression, 5 means each bit is 5x5)
    with open(inputf, 'rb') as file:
        size = os.path.getsize(inputf) #gets the size of the file
        print(size)
        chunk = int(width*height/(pix*pix)) #get the chunk, basically how many bits a single frame can contain
        width1 = width #i could just divide height1 and width1 directly, but it breaks compatibility since i need to swap all the var names and im lazy
        height1 = height
        width = int(width / pix)
        height = int(height / pix)
        add = height * width
        total_bits = size * 8 #gets the total bits
        print(total_bits)
        if total_bits < chunk: #if the file fits in less than one frame, set the bits amount to the chunk
            total_bits = chunk
            print(total_bits)
        total_frames = int(np.ceil(total_bits / (width * height))) #gets the total frames amount
        if (size*8) % (width*height) == 0: #if the file does NOT leave a gap then it makes an empty 1st frame
            total_frames += 1
        print(total_frames)
        fourcc = cv2.VideoWriter_fourcc(*'png ') #codec (fourcc)
        index = 0
        video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width1, height1), isColor=False) #DONT SWAP WIDTH1 AND HEIGHT1, OTHERWISE OPENCV GETS REAL MAD
        m = 1 #just an indicator to check if the first frame has been done, m=1 = no, m=0 = yes
        for _ in range(total_frames):
            if m == 0:
                frame = np.zeros((height, width), dtype=np.uint8)
                content = file.read(int(chunk / 8)) #read the portion of the file needed to fill 1 frame (resulting in less ram usage), the divide by 8 is there since chunk represents of the bits that can fit in one frame, and this converts it into bytes
                content = ''.join(format(byte, '08b') for byte in content)
                values = np.array([int(content[bit2]) * 255 for bit2 in range (chunk)]) #basically if it is reading a 1 it will multiply it by 255, resulting in 255 (white), otherwise it'll multiply 0 by 255 resulting in 0 (black)
                values = values.reshape(-1) #vectoring stuff, efficiency reasons
                index += add
                print(f"{index} 1")
                frame.flat = values
                frame = frame.reshape((height, width)) #converts the frame back into 2d
                frame = cv2.resize(frame, (width1, height1), interpolation=cv2.INTER_NEAREST) #enlargens the frame back into the original resolution, instead of writing each bit, this is to resist compression
                video_writer.write(frame)
            else:
                if (size*8) % (width*height) == 0: #if the file does NOT leave a gap then i'm making an empty 1st frame
                    temp = chunk
                    frame = np.zeros((height, width), dtype=np.uint8)
                    binary_data = '0' * (temp - 1)
                    binary_data += '1'
                    print(temp)
                    values = np.array([int(binary_data[bit]) * 255 for bit in range(chunk)])
                    values = values.reshape(-1)
                    frame.flat = values
                    frame = frame.reshape((height, width))
                    frame = cv2.resize(frame, (width1, height1), interpolation=cv2.INTER_NEAREST)
                    video_writer.write(frame)
                    m = 0
                else:
                    frame = np.zeros((height, width), dtype=np.uint8)
                    size2 = size * 8
                    size3 = size2 % chunk #gets the bits it needs to write
                    temp = chunk - size3 #gets the padding bits it will write at the beginning of the 1st frame
                    print(temp)
                    content = file.read(int(size3 / 8)) #read the bits needed for the 1st frame
                    binary_data = '0' * (temp - 1) #creates the padding 0s (except for the last 0 where it is swapped for a 1, for decoding purposes)
                    binary_data += '1'
                    content = ''.join(format(byte, '08b') for byte in content)
                    binary_data += content
                    values = np.array([int(binary_data[bit]) * 255 for bit in range(chunk)])
                    values = values.reshape(-1) #vectoring stuff, efficiency reasons
                    index += add
                    print(f"{index} 0")
                    frame.flat = values #writes the bits to the frame right after flattening the frame into a 1d picture
                    frame = frame.reshape((height, width)) #converts the frame back into 2d
                    frame = cv2.resize(frame, (width1, height1), interpolation=cv2.INTER_NEAREST) #enlargens the frame back into the original resolution, it's to resist compression
                    video_writer.write(frame)
                    m = 0
        video_writer.release()

if __name__ == "__main__":
    input_file_path = "input.txt" #replace with the path to your input file
    output_video_path = "output.avi" #replace with the desired output video path
    create_video(output_video_path, input_file_path)


