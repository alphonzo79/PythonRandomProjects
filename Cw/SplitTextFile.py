import os
import subprocess

text_input_directory = "/home/joe/Dropbox/CWStuff/500MostCommon"
text_input_file = "500_most_common_x_3.txt"

text_output_directory = "/home/joe/Dropbox/CWStuff/500MostCommon/IndividualFiles/Text"
text_file_appendix = ".txt"
text_file_name_format = '%(number)03d_%(word)s.txt'

filename_replacements = {"?": "QuestionMark", "/": "Slash", ".": "Period", ",": "Comma", "-": "Dash",
                        "<bt>": "Pro_BT", "<bk>": "Pro_BK", "<ar>": "Pro_AR", "<as>": "Pro_AS", "<sk>": "Pro_SK"}

audio_directory = "/home/joe/Dropbox/CWStuff/500MostCommon/IndividualFiles/Audio/"
ebook_command_format = 'ebook2cw -w 20 -W 5 -a "500 Most Common" -t %(title)s -o "%(out_file)s_" "%(in_file)s"'

file_start_text = "<bt>"

split_char = " "


def load_file():
    directory = os.path.relpath(text_input_directory)
    file_path = os.path.join(directory, text_input_file)

    if os.path.isfile(file_path):
        f = open(file_path, 'r')
        text = f.read()
        f.close()
        return text


def split_and_dedupe_file_contents(file_contents):
    split = file_contents.split(split_char)

    consolidated = []
    for i in range(0, len(split), 3):
        consolidated.append(split[i])

    return consolidated


def save_file(file_contents, filename):
    directory = os.path.relpath(text_output_directory)
    file_path = os.path.join(directory, filename)

    f = open(file_path, 'w')
    f.write(file_contents)
    f.close()


def save_new_text_files(words_array):
    index = 0
    created_files_out = []
    for word in words_array:
        file_contents = file_start_text
        for i in range(0, 5):
            file_contents += " " + word
        if filename_replacements.__contains__(word):
            word = filename_replacements[word]
        file_name = text_file_name_format % {"number": index, "word": word}
        save_file(file_contents, file_name)
        created_files_out.append(file_name)
        index += 1

    return created_files_out


def create_audio_files(created_files_in):
    # subprocess.check_call(audio_directory_command, shell=True)
    # print subprocess.call("pwd")
    for in_file in created_files_in:
        split_one = in_file.split(".")
        out_file = split_one[0]
        split_two = out_file.split("_")
        # title = split_two[1]
        title = out_file
        # print 'title: %(title)s outFile: %(outfile)s, inFile: %(infile)s' % {"title": title, "outfile": out_file, "infile": in_file}
        out_file = audio_directory + out_file
        command = ebook_command_format % {"title": title, "out_file": out_file, "in_file": text_output_directory + "/" + in_file}
        print "running: " + command
        subprocess.check_output(command, shell=True)


def fix_file_names():
    for current in os.listdir(audio_directory):
        split = current.split("_0000")
        os.rename(audio_directory + "/" + current, audio_directory + "/" + split[0] + ".mp3")


file_text = load_file()
words = split_and_dedupe_file_contents(file_text)
created_files = save_new_text_files(words)
create_audio_files(created_files)
fix_file_names()
