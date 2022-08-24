#!/usr/bin/env python
# cli tool for displaying shortcuts

import argparse

import os, sys
import textwrap

parser = argparse.ArgumentParser()

SHELL_PROFILE='zshrc' # or bashrc, etc ($HOME parent directory is assumed)
TERMINAL='terminal.md' 
PYCHARM='pycharm.md'
COLOR=3 # currently yellow
# 1 = red, 2 = green, 3 = yellow, 4 = blue, 5 = pink, ...

class bcolors:
    YELLOW_IN = '\033[33m'
    YELLOW_OUT = '\033[43m' 
    RED_IN = '\033[31m'
    RED_OUT = '\033[41m'
    CYAN_IN = '\033[96m'
    CEND = '\033[0m'


# def cat_shortcuts(filename): # colors the whole output in the same color
    # file_dir = '$SHORTCUTS_DIR_PATH/{}'.format(filename)

    # color_filter = 'tput setaf {}; cat; tput sgr0;'.format(COLOR)
    # pipe = "clrfilter() { " + color_filter + " }"

    # os.system('{} && cat {} | clrfilter && echo \"\\n\"'.format(pipe, file_dir))
    # sys.exit()

def cat_shortcuts_liner(filename): # color only `` strings

    # if not filename[len(filename)-3:] == '.md':
        # return cat_shortcuts(filename)

    import subprocess
    path = subprocess.check_output(['echo $SHORTCUTS_DIR_PATH'], shell=True).decode('utf-8')
    

    file_dir = '{}/{}'.format(path[0: -1], filename) # .replace("\\n", '')

    lines = None
    with open(file_dir, 'r') as file:
        lines = file.readlines()

    MAX_CAPACITY_STRING = 25
    SPACE_BEFORE_HEADER = 18

    print() # newline
    
    
    for line in lines:
        is_format_correct = True
        output_string = ""
        
        count_backticks = line.count('`')
        if count_backticks == 1 or count_backticks > 2:
            raise Exception("Error parsing backticks")

        index_of_first_md_char = line.find('`')
        index_of_second_md_char = line.rfind('`')

        if line[0] == '#':
            line = bcolors.CYAN_IN + SPACE_BEFORE_HEADER * ' ' + line + bcolors.CEND
            output = line.replace('#', '')
            print(output)
            continue

        # if not index_of_first_md_char == -1 and (index_of_first_md_char == index_of_second_md_char or index_of_first_md_char > index_of_second_md_char):
            # raise Exception("Document is formated incorrectly")
        
        if index_of_first_md_char != -1:
            
            shortcut = line[index_of_first_md_char:index_of_second_md_char+1]
            
            edited_shortcut = bcolors.YELLOW_IN + shortcut + bcolors.CEND
            
            edited_shortcut = edited_shortcut + " " * (MAX_CAPACITY_STRING - len(shortcut))

            output_string = line.replace(shortcut, edited_shortcut).replace('`', '')

        else:
            output_string = line

        print(output_string) # print each line


# set path to shortcuts
parser.add_argument(
        '-p', '--path',
        type=str,
        help='Path to the directory where you store the documents populated with shortcuts')

# terminal shortcuts
parser.add_argument(
        '-t', '--terminal',
        action='store_true',
        help='Display terminal shortcuts'
        )

parser.add_argument(
        '-c', '--pycharm',
        action='store_true', 
        help='Display pycharm shortcuts'
        )

parser.add_argument(
        '-r', '--read',
        help='Read shortcut file from default directory'
        )

parser.add_argument(
        '-ro', '--read_not_default', 
        help='Pass full path to shortcut file'
        )

args = parser.parse_args()

directory_path = args.path


if args.path:
    if not os.path.isdir(args.path):
        print('The specified path does not exist')
        sys.exit()
    else:
        command = 'echo \"export SHORTCUTS_DIR_PATH=\'{}\'\n$(cat $HOME/.{})\" > $HOME/.{}'.format(args.path, SHELL_PROFILE, SHELL_PROFILE) # :))))))
        # command = 'echo \"export SHORCUTS_DIR_PATH=\'{}\'\" >> $HOME/.{}'.format(args.path, SHELL_PROFILE)
        if os.system(command) != 0:
            sys.exit()

        print(" ... ")

        if os.system("source $HOME/.{} > /dev/null 2>&1".format(SHELL_PROFILE)) == 0:
            print("Path set successfully")
        else: 
            print("Something went wrong executing the shell")

        sys.exit()

def sandboxed_liner_call(args):
    try:
        cat_shortcuts_liner(args)
    except Exception as e:
        print(e)
        sys.exit(1)
        

# TERMINAL SHORTCUTS
if args.terminal:
    sandboxed_liner_call(TERMINAL)


# PYCHARM SHORTCUTS
if args.pycharm:
    sandboxed_liner_call(PYCHARM)

if args.read:
    if not '/' in args.read: # we may read files without extensions
        sandboxed_liner_call(args.read)
    else:
        print('Argument should like: readme.txt')
        sys.exit()


if args.read_not_default:
    print(os.path.abspath(args.read_not_default))


# TBA:
# Remove start at the beginning of the lines
# Pass full path to a file outside of default dir (-ro)


