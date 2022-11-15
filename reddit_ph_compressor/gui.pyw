import PySimpleGUI as sg
import sys
from compress import compress_file

if len(sys.argv) >= 3:
    compress_file(sys.argv[1], sys.argv[2])
    exit()

if __name__ == "__main__":
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
                if compress_file(inputFile, outputFile):
                    sg.popup_notify('The script is successfully compressed at: ' + values["-IN-"])
