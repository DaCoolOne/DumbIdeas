import PySimpleGUI as sg
import sys
import warnings

if sys.version_info[0] != 3 or sys.version_info[1] < 10:
    warnings.warn("The python interpreter may break on versions earlier than 3.10 (see https://github.com/DaCoolOne/DumbIdeas/issues/1)", stacklevel=2)

UNKNOWN_CHAR_MAP = { 0: 'Null (\\0)', 1: 'SOH', 2: 'STX', 3: 'ETX', 4: 'EOT', 5: 'ENQ', 6: 'ACK', 7: 'BEL', 8: 'Backspace (\\b)', 9: 'Tab (\\t) (Did you mean to indent with spaces?)', 11: 'Vertical Tab (\\v)', 12: 'Form Feed (\\f)', 14: 'SO', 15: 'SI', 16: 'DLE', 17: 'DC1', 18: 'DC2', 19: 'DC3', 20: 'DC4', 21: 'NAK', 22: 'SYN', 23: 'ETB', 24: 'CAN', 25: 'EM', 26: 'SUB', 27: 'ESC', 28: 'FS', 29: 'GS', 30: 'RS', 31: 'US', 127: 'DEL' }

class UnknownCharacterException(ValueError):
    def __init__(self, character: int, line: int) -> None:
        if character < 128:
            descriptor = UNKNOWN_CHAR_MAP[character] if character in UNKNOWN_CHAR_MAP else f"ASCII {character}"
            super().__init__(f"{line}: Cannot encode {descriptor} character.")
        else:
            super().__init__(f"{line}: Attempt to encode UTF8 character sequence. (This program only can encode ascii non-control characters and newlines)")
def unicode_compress(bytes):
    o = bytearray(b'E')
    line = 1
    for c in bytes:
        # Skip carriage returns (This should be done by Python in the file read, but just in case this gets called elsewhere)
        if c == 13:
            warnings.warn("Non-unix line endings detected", stacklevel=2)
            continue
        # Newlines increase line count (For error messagse).
        if c == 10:
            line += 1
        # Check for invalid code points
        if (c < 32 or c > 126) and c != 10:
            raise UnknownCharacterException(c, line)
        # Code point translation
        v = (c-11)%133-21
        o += ((v >> 6) & 1 | 0b11001100).to_bytes(1,'big')
        o += ((v & 63) | 0b10000000).to_bytes(1,'big')
    return o

# Decompress algorithm (Code golfed)
def unicode_decompress(b):
    return ''.join([chr(((h<<6&64|c&63)+22)%133+10)for h,c in zip(b[1::2],b[2::2])])

# Compressing
def compress_file():
    with open(inputFile, 'r', encoding='utf8') as inp:
        with open(outputFile, 'wb') as out:
            # Read input file.
            orig = inp.read()
            
            if '\t' in orig:
                warnings.warn("File cannot contain tabs. Converting each tab to 4 spaces.", stacklevel=2)
                orig = orig.replace('\t', '    ')

            # Compress
            E = unicode_compress(orig.encode('utf8'))

            # Check that everything worked according to keikaku
            test_back = unicode_decompress(E)
            if all(a == b for a,b in zip(orig.splitlines(),test_back.splitlines())):
                print("Success!")

                # Write output to file, along with code-golfed decompressor.
                out.write(b"b='"+E+b"'.encode();exec(''.join(chr(((h<<6&64|c&63)+22)%133+10)for h,c in zip(b[1::2],b[2::2])))")
                return True
            else:
                raise ValueError("An unknown error occured. Compression/decompression cycle failed. Output file unmodified.")

# Args
if __name__ == "__main__" and len(sys.argv) >= 3:
	inputFile = sys.argv[1]
	outputFile = sys.argv[2]
	
	if compress_file():
		sg.popup_notify('The script is successfully compressed at: ' + outputFile)
	exit()
	

# GUI
sg.theme('DarkBlue')
GUI = [
[sg.T("")], 
[sg.Text("input file:		"), 
sg.Input(), 
sg.FileBrowse(key="-IN-", file_types=(("Python scripts", ".py"),))],
[sg.T("")], 
[sg.Text("output folder:	"), 
sg.Input(), 
sg.FolderBrowse(key="-OUT-")],
[sg.Button("Submit")],
]

window = sg.Window('Python compressor', GUI)
    
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit":
        if values["-IN-"] == '' or values["-OUT-"] == '':
            sg.popup('ERROR: These fields may not be empty.')
        else:
            inputFile = values["-IN-"]
            outputFile = values["-OUT-"] + (values["-IN-"])[(values["-IN-"]).rfind('/'):].replace('.py', '_compressed.py')
            sg.popup_notify('Compressing the script...')
            if compress_file():
                sg.popup_notify('The script is successfully compressed at: ' + values["-IN-"])
