import array as arr
from pynput import keyboard 
import time
import pyaudio
import wave 


i = False
stop_time = None
start_time = None
record_time = None
line = []
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
frames = []
filename = None
stream = [0]
arr = [0]
audio = [0]

def read_text_by_line(arr):
    with open('news.txt', 'r') as f:
        for line in f:
            arr.append(line)

p = [0]
    
def switch():
    f1 = open("result.txt", "a")
    global i, frames, line, start_time, stop_time, record_time, filename, stream, p
    # print(i)
    if i == False:
        frames = []
        p.append(pyaudio.PyAudio())
        i = True
        print('Recording')
        line.append(1)
        stream.append(p[len(line)].open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True))

        start_time = time.time()
        filename = 'line' + str(len(line)) + '.wav'

        listener1 = keyboard.Listener(
            on_press=on_press1)
        listener1.start()
        print(arr[len(line)])
        j = len(line)
        f1.write(arr[j])
        try:
            a = 0
            while (i != False):
                data = stream[j].read(chunk, exception_on_overflow = False)
                frames.append(data)
                a += 1
        
        except :
            i == False
            listener1.join()
        
        i = True
        
    else:
        
        j = len(line)
        print(filename)
        stop_time = time.time() 
        record_time = stop_time - start_time

        audio.append(filename)
        f1.write(audio[j]+ "\n")
        # Close the stream
        stream[j].stop_stream()
        stream[j].close()

        # Terminate the PortAudio interface
        p[j].terminate()
        print('Finished recording')
        print(record_time)
        
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p[j].get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        i = False

def stop():
    i = False
    return i 

def count():
    i = 0
    while(i<10):
        i += 1
    return i

def on_press(key):
    if key == keyboard.Key.space:
        switch()
    else :
        print('end')
        return False

def on_press1(key):
    global i
    if key == keyboard.Key.space:
        i = False
        return i
    else :
        return True


def news_speech_record():
    f = open("result.txt", "w")
    f.write('https://vnexpress.net/the-gioi/my-thanh-vung-dich-lon-nhat-the-gioi-4075427.html')
    read_text_by_line(arr)
    with keyboard.Listener(   
        on_press = on_press) as listener:
        listener.join()

news_speech_record()
