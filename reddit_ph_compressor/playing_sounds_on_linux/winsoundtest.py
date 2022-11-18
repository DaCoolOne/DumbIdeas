__IMPORT = __import__
def __import__(name):
    try: return __IMPORT(name)
    except ModuleNotFoundError as e:
        if name != 'winsound': raise e
    try:
        import playsound
    except ModuleNotFoundError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'playsound'])
    w = OSError()
    def b(x,y):
        import playsound
        import wave
        import math
        with wave.open('beep.wav', 'wb') as w:
            frames = int(y * 44.1)
            w.setparams((1, 2, 44100, frames, "NONE", "not compressed"))
            for i in range(frames):
                sample = math.sin(2 * math.pi * x * ( i / 44100 ))
                w.writeframes(__import__('struct').pack('h', int(sample * 32767.0)))
        playsound.playsound('beep.wav', True)
    w.Beep = b
    return w