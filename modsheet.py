import numpy as np
import fileinput
import subprocess
import os

draw_n = 4
tex_file = "modsheet.tex"
output_file = "output" #will be pdf, make sure no other files with this name exist
sheets_to_generate = 5
latex_exec = "pdflatex"

def seq_line():
    ret = "Sequence: "
    for n in np.random.permutation(range(1,17)):
        ret += f'& {n} '
    ret += '\\\\ \n'
    return ret


draw_head = "Draws: "

def draw_line(nums):
    ret = ""
    for n in nums:
        ret += f'& {n} '
    ret += '\\\\ \n'
    return ret

latex = [[], [], []]
i = 0
with open(tex_file, "r") as f:
    for line in f:
        latex[i].append(line)
        if "%77" in line:
            i+=1

with open(f'{output_file}.tex', "w") as f:
    for line in latex[0]:
        f.write(line)
    for i in range(sheets_to_generate):
        draws_done = 0
        for line in latex[1]:
            if "Sequence:" in line:
                f.write(seq_line())
            elif "Draws:" in line:
                f.write(draw_head + draw_line(np.random.randint(1,17,16)))
                draws_done += 1
            elif 0 < draws_done and draws_done < draw_n:
                f.write(draw_line(np.random.randint(1,17,16)))
                draws_done += 1
            else:
                f.write(line)
        f.write("\\newpage \n")
    for line in latex[2]:
        f.write(line)

subprocess.run([latex_exec, f'{output_file}.tex'])

for f in os.listdir("."):
    if f[0:(len(output_file)+1)] == output_file + "." and f[-3:] != "pdf":
        os.remove(f)