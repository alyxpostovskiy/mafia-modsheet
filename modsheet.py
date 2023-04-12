import random
import subprocess
import os

tex_file = "modsheet.tex"
output_file = "output" #will be pdf, make sure no other files with this name exist
latex_exec = "pdflatex"

sheets_to_generate = 2
players = 16
actions = 8
draw_lines = 4

def players_line(i):
    return f'{i}' + r" & & & & & & " + f'{i}' + r""". & \\
    \cline{2-4} \cline{8-8}
    """

def actions_line():
    return r"""
    & & & & & & \\[1.9ex]
    \hline"""

def seq_line(n):
    seq = list(range(1,n+1))
    random.shuffle(seq)
    return "".join([f'& {i} ' for i in seq]) + "\\\\ \n"

def draw_line(n):
    return "".join([f'& {random.randint(1,n)} ' for i in range(16)]) + "\\\\ \n"

def players_table():
    return r"""
    \noindent\large
    \begin{tabular}{ c | p{1.25in} | p{1.25in} | p{1.25in} | c c c p{1.9in} }
        \cline{2-4}
        & Role & Name & Notes & & \multicolumn{3}{l}{List of players in game:} \\
        \cline{2-4}
    """ + "".join([players_line(i+1) for i in range(players)]) + r"""
    \end{tabular}
    \vspace{0.25in}
    """
def actions_table():
    return r"""
    \noindent
    \begin{tabular}{|p{0.9in}|p{0.9in}|p{0.9in}|p{0.9in}|p{0.9in}|p{0.9in}|p{0.9in}|}
        \hline
        Action & 1 & 2 & 3 & 4 & 5 & 6 \\
        \hline
    """ + "".join([actions_line() for i in range(actions)]) + r"""
    \end{tabular}
    \vspace{0.25in}
    """

def rng_table():
    return r"""
    \noindent
    \begin{tabular}{ l *{16}{p{0.2in}} }
        Sequence: """ + seq_line(players) + r"Draws: " + "".join([draw_line(players) for i in range(draw_lines)]) + r"""
    \end{tabular}    
    """

def body():
    return players_table() + actions_table() + rng_table() + "\\clearpage \n"


preamble = r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}

\usepackage[top=0.5in, bottom=0.5in, left=0.5in, right=0.5in]{geometry}
\pagestyle{empty}

\begin{document}
"""
postamble = r"""
\end{document}
"""



with open(f'{output_file}.tex', "w") as f:
    f.write(preamble)
    for i in range(sheets_to_generate):
        f.write(body())
    f.write(postamble)

subprocess.run([latex_exec, f'{output_file}.tex'])

for f in os.listdir("."):
    if f[0:(len(output_file)+1)] == output_file + "." and f[-3:] != "pdf":
        os.remove(f)
