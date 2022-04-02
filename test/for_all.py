content = r"""Случайные величины $X$ и $Y$ независимы и имеют равномерное
распределение на отрезке $[{5};{15}]$. Для случайной величины $Z=X-Y$ найдите:
1) функцию распределения $F_Z(x)$;
2) плотность распределения $f_Z(x)$ и постройте график плотности;
3) найдите такое значение $c$, для которого вероятность $\P(|Z|\leqslant c)={0.363}$."""

print(content)
print()
newContent = ""
isOpen = False
for i in content:
    if (i == "$"):
        if (isOpen == False):
            print(123)
            newContent += "\("
            isOpen = True
        else:
            newContent += "\)"
            isOpen = False
    else:
        newContent += i
print(newContent)