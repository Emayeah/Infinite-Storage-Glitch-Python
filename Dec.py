import cv2
import numpy as np

def decode_video(video_path, output_file_path, width=1280, height=720, pix=5): #set this exactly like how you set the encoding, otherwise it breaks
    video_reader = cv2.VideoCapture(video_path)
    binary_data = ''
    index = 0 #counter of the bits already converted
    add = int(width * height / (pix * pix))
    m = 1 #declares m to check if the 1st frame has been read, m=1 = no, m=0 = yes
    with open(output_file_path, 'ab') as output_file: #declares output_file as the output file, and makes every write function append data
        while True:
            ret, frame = video_reader.read() #ret = if the frame exsists or not, frame = the frame data itself
            if not ret:
               print("finished") #prints this if it finished going through the video
               break
            frame = cv2.resize(frame, (int(width / pix), int(height / pix)), interpolation=cv2.INTER_NEAREST) #resize the frame so that each bit is 1 pixel wide, in the encoder each pixel is much wider to resist compression
            if frame.size == 0: #if the frame is corrupt it breaks
                break
            intensity = np.mean(frame, axis=(2 if len(frame.shape) == 3 else 0))
            index += add
            print(index)
            if m == 0:
                binary_data = ''.join(np.where(intensity.flatten() > 127, '1', '0').astype(str)) #writes the data in the frame into a variable
                binary_array = np.array([int(bit) for bit in binary_data]) #transforms the data into an array
                bytes_array = np.packbits(binary_array) #transforms the binary array into a bytes array
                output_file.write(bytes_array)
            else:
                binary_data = ''.join(np.where(intensity.flatten() > 127, '1', '0').astype(str))
                first_one_index = binary_data.find('1')
                binary_data = binary_data[first_one_index + 1:] #scraps all the data including the extra 1, all of this is because it needs to scrap the gap left by files that don't perfectly fit into the video without leaving some gaps (the gap is at the beginning for efficiency reasons)
                if binary_data == "": #scraps the 1st frame if the 1st frame is empty, happens when the file perfectly fits into the video without leaving any gap
                    m = 0 
                else:
                    binary_array = np.array([int(bit) for bit in binary_data]) #transforms the data into an array
                    bytes_array = np.packbits(binary_array) #transforms the binary array into a bytes array
                    output_file.write(bytes_array)
                    m = 0
                print("file decoded and written to" + output_file_path)


if __name__ == "__main__":
    video_path = "input.avi" #input the video file
    output_file_path = "output.txt" #input the file output
    decode_video(video_path, output_file_path)
