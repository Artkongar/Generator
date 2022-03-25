from sympy import *
import re
import os



mainPath = os.sep.join(os.getcwd().split(os.sep)[:-1])
filePath = os.path.join(mainPath, "tex", "Q1", "t1_1.tex")

f = open(filePath, encoding="utf-8")
text = f.read()
f.close()

l = r"\begin{problem*}Решите интеграл: [test text] \\\\Задание: $ \int_{<a>}^{<b>} \frac{\exp(\frac{<c>}{x})dx}{x^{<d>}} $\end{problem*}"

res = re.findall(r"\\begin\{solution\*}([\s\S]*?)\\end\{solution\*}", l)

print(latex("asdasd"))

line = re.sub(r"\$([\s\S]*?)\$", r"\int_{{1}}^{{2}} \frac{\exp(\frac{{1}}{x})dx}{x^{{2}}} ".replace("\\", "\\\\"), l)

print(line)