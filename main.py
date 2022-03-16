from Generator import Ticket, Task

if __name__ == '__main__':
    ticket1 = Ticket()

    task1 = Task()
    task1.setTaskDescription("Решите интеграл")
    task1.setIntRangeValues(-10, 10)
    task1.setLatexTask(r"\int_{{?}}^{{?}} \frac{\exp(\frac{?}{x})dx}{x^{?}}")
    #task1.setBindings(1, 2, 1, 2)

    task2 = Task()
    task2.setTaskDescription("Решите предел")
    task2.setIntRangeValues(-15, 15)
    task2.setLatexTask(r"""\lim_{x \to ?} \frac{?x^{?}+?x+?}{\sqrt{?x + ?} +?}""")
    #task2.setBindings(-2, 1, 2, 1, -2, 1, 6, -2)

    for i in range(5):
        ticket1.addTask(task1)
        ticket1.addTask(task2)

    ticket1.setCalculateAttempts(10)
    ticket1.setCalculateTimeout(15)

    answers = ticket1.getAnswers()
    print(len(answers))
    #ticket1.getTicketLatex()