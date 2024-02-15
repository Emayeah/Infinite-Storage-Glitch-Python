import cv2 #imports opencv, make sure that you have opencv installed
import numpy as np #imports numpy and makes it callable with np cus lazy

def decode_video(video_path, output_file_path, width=1280, height=720, pix=5): #set this exactly like how you set the encoding, otherwise it breaks
    video_reader = cv2.VideoCapture(video_path) #initialize the video reader
    binary_data = '' #declares binary_data
    index = 0 #declares index, it 
    add = int(width * height / (pix * pix)) #declares add and makes it the amount that needs to be added for each time a frame is completed
    m = True #declares m to check if the 1st frame has been read, m=True = no, m=False = yes
    with open(output_file_path, 'ab') as output_file: #declares output_file as the output file, and makes every write function append data
        while True: #loop forever
            ret, frame = video_reader.read() #ret = if the frame exsists or not, frame = the frame data itself
            if not ret: #if the frame doesn't exsist break
               print("a") #prints a if the condition is true, so if you see an a the video may be fried of you just reached the end (the latter is 100000000000 times more likely)
               break #breaks if the condition is true
            frame = cv2.resize(frame, (int(width / pix), int(height / pix)), interpolation=cv2.INTER_NEAREST) #resize the frame so that each bit is 1 pixel wide
            if frame.size == 0: #if the frame is corrupt it breaks
                break #it breaks if the frame is corrupt
            intensity = np.mean(frame, axis=(2 if len(frame.shape) == 3 else 0))
            index += add #adds the amount of bits it has already converted
            print(index) #prints the amount of bits it has converted in the 1st frame
            if m == False: #checks if the 1st frame has already been done
                binary_data = ''.join(np.where(intensity.flatten() > 127, '1', '0').astype(str)) #writes the data in the frame into a variable
                binary_array = np.array([int(bit) for bit in binary_data]) #transforms the data into an array
                bytes_array = np.packbits(binary_array) #transforms the binary array into a bytes array
                output_file.write(bytes_array) #appends the bytes array (the data itself)
            if m == True: #checks if the 1st frame has not been done
                binary_data = ''.join(np.where(intensity.flatten() > 127, '1', '0').astype(str)) #writes the data in the frame into a variable
                first_one_index = binary_data.find('1') #checks where the 1st 1 is in the 1st frame
                binary_data = binary_data[first_one_index + 1:] #scraps all the data including the extra 1
                binary_array = np.array([int(bit) for bit in binary_data]) #transforms the data into an array
                bytes_array = np.packbits(binary_array) #transforms the binary array into a bytes array
                output_file.write(bytes_array)#appends the bytes array (the data itself)
                m = False #sets the 1st frame check to false (1st frame has already been done)
                print(f"file decoded and written to {output_file}") #tells the user where the file is, useless since it can be found down a few lines from here


if __name__ == "__main__": #checks if the program has already been run
    video_path = "/home/ema/Desktop/Out1.avi" #input the video file
    output_file_path = "/home/ema/Desktop/bk foot lettuce2.txt" #input the file output
    decode_video(video_path, output_file_path) #calls decode video
