import tkinter as tk
import random
import threading
import math
import GameMethods
import operator
from itertools import combinations
from operator import mul


def poly(args):
    '''Kudos to @hansaplast for figuring out how to do this.'''
    return [sum([reduce(mul,c,1) for c in combinations(args,i)]) 
                                 for i in range(len(args)+1)]

class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("800x500+500+200")

        self.choices = list()
        self.teams = dict()
        self.directions_location = 0

        self.directions_string = """Hello! Thank you for choosing to play MathQuiz.
Here are your instructions:
To begin with, divide yourselves into teams.

When you're ready, press "Enter" to continue. """
        self.bind("<Return>", self.continuater)
        
        self.directions_output = tk.Label(self, text = self.directions_string, font = "Times 14", justify=tk.LEFT)
        self.directions_output.grid(padx=200, pady=25)

        self.mainloop()

    def continuater(self, *args):
        self.directions_location += 1
        
        if self.directions_location == 1:
            
            self.directions_output['text'] = """Now that you have divided into teams, choose team names.
Names may not include numbers or special characters.
When you have finished doing so, each team should enter its 
name below, and click "Submit name". 
It is suggested that you choose something short.

Press "Enter" to continue."""
            self.directions_output.update()

            self.name_submission = tk.Entry(self, font="Times 14", relief=tk.GROOVE)
            self.name_submission.grid(padx=150, pady=30)

            global EntryImage
            EntryImage = tk.PhotoImage(file="submit.png")
            self.sumbitter = tk.Button(self, command=self.AddTeam, image=EntryImage)
            self.sumbitter.grid(padx=230, pady=10)
        
        elif self.directions_location == 2:
            self.name_submission.destroy()
            self.sumbitter.destroy()
            self.WhoFirst = random.choice(self.choices)
            self.directions_output['text'] = """The sequence of play is as follows:

1. The current level's problem will be displayed.

2. Each team will solve the problem, and then type
   in the answer. For answers, use the format:
   "<team-name>  <answer-number>".
   When the result of a problem is a non-integer,
   round to two places.

   Please do not put fractions ("# / #") in your
   answers, this messes things up.

3. After all the questions have been answered, the
   winning team will be announced.

        Press "Enter" to begin."""
            return None
        
        elif self.directions_location == 3:
            print(self.choices)
            if len(self.choices) > 1:
                self.onused_team = random.choice(self.choices)
            else:
                self.onused_team = self.choices[0]

            self.directions_output['text'] = f'''
            Team "{self.onused_team}" has the onus.

            Press "Enter" to begin. '''
            
        elif self.directions_location == 4:
            self.directions_output.destroy()
            self.begin()

    def begin(self, *args, **kwargs):
        self.name_submission.destroy()
        self.directions_output.destroy()
        del self.directions_output
        del self.name_submission
        self.update()
        print("Beginning.")
        self.MakeProblems()
        self.MakeQuestions()
        self.which_question = 0
        self.unbind("<Return>")
        self.AdvanceQuestion()

    def AdvanceQuestion(self):
        if self.which_question != 0:
            self.questions[self.which_question - 1].destroy()
            if self.which_question > len(self.questions):
                self.EndGame()

        
        self.questions[self.which_question].ShowMe()

        self.which_question += 1

        return None

    def EndGame(self):
        self.winner = max(self.teams.items(), key=operator.itemgetter(1))[0]
        self.score = self.teams[self.winner]
        print(self.winner)
        print(self.score)

        self.alerter = tk.Label(self, text=f"Team {self.winner} has won with a score of {self.score}!", font="Centaur 20 bold", foreground = "green")
        self.alerter.grid(padx=150, pady=200)



    def MakeQuestions(self) -> None:
        self.questions = list()
        for i in range(len(self.problems)):
            self.questions.append(GameMethods.Question(self, str(self.problems[i][0]), str(self.problems[i][1])))
        
        return None

    def MakeProblems(self):
        self.problems = [None, None, None, None, None, None, None, None, None, None]
        what_row = 1
        counter = 0
        for i in range(len(self.problems)):
            counter += 1
            if counter % 2 == 0:
                what_row += 1
            if what_row == 1:
                self.problems[i] = self.make_arith1()
                
            elif what_row == 2:
                self.problems[i] = self.make_arith2()
            
            elif what_row == 3:
                self.problems[i] = self.MakeOrderOfOperations()
            
            elif what_row == 4:
                self.problems[i] = self.MakeOrderOfOperations()
            
            elif what_row == 5:
                self.problems[i] = self.MakeEquations(minlength=2, maxlength=5)
            
            elif what_row == 6:
                self.problems[i] = self.MakeEquations(minlength=4, maxlength=6)
                

        print(self.problems)
        return None

    def make_arith2(self, *args, **kwargs):
        number_of_factors = random.randint(2, 3)
        math_problem = str()

        for i in range(number_of_factors):
            mode = random.randint(0, 1)
            if i != number_of_factors:
                x = random.randint(1, 50)
                math_problem += str(x)
                print(x)
                if mode == 0:
                    math_problem += " * "
                else:
                    math_problem += " / "
            else:
                math_problem += random.randint(0, 100)
        math_problem = math_problem[0:-2]
        print(math_problem)
        solution = math.ceil((eval(math_problem)))
        print(solution)
        return (math_problem, solution)

    def make_arith1(self, *args, **kwargs):
        number_of_factors = random.randint(2, 4)
        math_problem = str()

        for i in range(number_of_factors):
            mode = random.randint(0, 1)
            if i != number_of_factors:
                x = random.randint(0, 50)
                math_problem += str(x)
                print(x)
                if mode == 0:
                    math_problem += " + "
                else:
                    math_problem += " - "
            else:
                math_problem += random.randint(0, 100)
        math_problem = math_problem[0:-2]
        print(math_problem)
        solution = eval(math_problem)
        print(solution)
        return (math_problem, solution)

    def MakeOrderOfOperations(self, already_have_one = False, *args, **kwargs):
        number_of_factors = random.randint(3, 6)
        math_problem = ''

        try:
            for i in range(number_of_factors):
                mode = random.randint(1, 5)
                if i != number_of_factors:
                    try:
                        if mode == 1:
                            x = random.randint(0, 50)
                            math_problem += str(x)
                            math_problem += ' + '
                            print(x)
                        elif mode == 2:
                            x = random.randint(0, 50)
                            math_problem += str(x)
                            math_problem += " - "
                        elif mode == 3:
                            x = random.randint(0, 50)
                            math_problem += str(x)
                            math_problem += ' + '
                        elif mode == 4:
                            if already_have_one == False:
                                math_problem += ("(" + (self.MakeOrderOfOperations(already_have_one=True)[0]) + ")")
                                second_mode = random.randint(1, 4)
                                if second_mode == 1:
                                    math_problem += ' + '
                                elif second_mode == 2:
                                    math_problem += ' - '
                                elif second_mode == 3:
                                    math_problem += ' * '
                                elif second_mode == 4:
                                    math_problem += ' / '

                        elif mode == 5:
                            if already_have_one == False:
                                math_problem += ("(" + str(random.randint(0, 50)) + f" ** {str(random.randint(2, 4))})")
                                if (second_mode := random.randint(1, 4)) == 1:
                                    math_problem += ' + '
                                elif second_mode == 2:
                                    math_problem += ' - '
                                elif second_mode == 3:
                                    math_problem += ' * '
                                elif second_mode == 4:
                                    math_problem += ' / '
                    except ZeroDivisionError:
                        print("Oopsies.")
        
        except SyntaxError:
            results = self.MakeOrderOfOperations()
            return (results[0], results[1])
            
        math_problem = math_problem[0:-2]
        print(math_problem)
        try:
            solution = eval(math_problem)
            solution = math.ceil(solution)
        except:
            solution = self.MakeOrderOfOperations()
            return (solution[0], solution[1])
        print(math_problem)
        return (math_problem, solution)


    def MakeEquations(self, minlength: int = 3, maxlength: int = 5):
        x = random.randint(-25, 25)
        y = random.randint(-25, 25)
        length1 = random.randint(minlength, maxlength)
        length2 = random.randint(minlength, maxlength)

        equation_1 = self._MakeEqua(x, y, length1)
        equation_2 = self._MakeEqua(x, y, length2)

        math_problem = f"""Solve for x:
    (1): {equation_1}
    (2): {equation_2} """
    
        return math_problem, x

    def _MakeEqua(self, x, y, length: int):
        '''Uses the input to generate an equation, which it then returns.'''
        values = list()
        math_problem = str()
        equa = str()
        already_have_one = False

        for i in range(length):
            values.append(random.randint(1, 35))
        
        x_pos = values.index(random.choice(values))
        y_pos = values.index(random.choice(values))
        print(str(x_pos) + " " + str(y_pos))

        for i in values:
            where = values.index(i)
            mode = random.randint(1, 6)
            if where == x_pos:
                try:
                    if mode == 1:
                        z = random.randint(0, 50)
                        math_problem += str(z)
                        math_problem += "x"
                        math_problem += ' + '
                        equa += "(" + str(z) + ' * ' + str(x) + ")" + " + "
                        
                    elif mode == 2:
                        z = random.randint(0, 50)
                        math_problem += str(z)
                        math_problem += "x"
                        math_problem += " - "
                        equa += "(" + str(z) + " * " + str(x) + ")" + " - "

                    elif mode == 3:
                        z = random.randint(0, 50)
                        math_problem += str(z)
                        math_problem += "x"
                        math_problem += ' * '
                        equa += '(' + str(z) + ' * ' + str(x) + ")" + " * "

                    elif mode == 4:
                        z = random.randint(0, 50)
                        math_problem += str(z)
                        math_problem += "x"
                        math_problem += ' / '
                        equa += '(' + str(z) + ' * ' + str(x) + ")" + " / "

                    elif mode == 5:
                        if already_have_one == False:
                            math_problem += 'x'
                            z = ("(" + (self.MakeOrderOfOperations(already_have_one=True)[0]) + ")")
                            math_problem += z
                            equa += "(" + str(x) + "*" + str(z) + ")"
                            second_mode = random.randint(1, 4)
                            if second_mode == 1:
                                math_problem += ' + '
                                equa += ' + '
                            elif second_mode == 2:
                                math_problem += ' - '
                                equa += ' - '
                            elif second_mode == 3:
                                math_problem += ' * '
                                equa += ' * '
                            elif second_mode == 4:
                                equa += ' / '
                                math_problem += ' / '

                    elif mode == 6:
                        if already_have_one == False:
                            z = str(random.randint(2, 4))
                            math_problem += ("x" + f"**{z}")
                            equa += (f"{str(x)}**{z}")
                            if (second_mode := random.randint(1, 4)) == 1:
                                math_problem += ' + '
                                equa += ' + '
                            elif second_mode == 2:
                                math_problem += ' - '
                                equa += ' - '
                            elif second_mode == 3:
                                math_problem += ' * '
                                equa += ' * '
                            elif second_mode == 4:
                                math_problem += ' / '
                                equa == ' / '
                except ZeroDivisionError:
                    print("Oopsies.")
                
            elif where == y_pos:
                try:
                    if mode == 1:
                        z = random.randint(0, 50)
                        math_problem += str(z)
                        math_problem += "y"
                        math_problem += ' + '
                        equa += "(" + str(z) + ' * ' + str(y) + ")" + " + "
                        
                    elif mode == 2:
                        z = random.randint(0, 50)
                        math_problem += str(z)
                        math_problem += "y"
                        math_problem += " - "
                        equa += "(" + str(z) + " * " + str(y) + ")" + " - "

                    elif mode == 3:
                        z = random.randint(0, 50)
                        math_problem += str(z)
                        math_problem += "y"
                        math_problem += ' * '
                        equa += '(' + str(z) + ' * ' + str(y) + ")" + " * "

                    elif mode == 4:
                        z = random.randint(0, 50)
                        math_problem += str(z)
                        math_problem += "y"
                        math_problem += ' / '
                        equa += '(' + str(z) + ' * ' + str(y) + ")" + " / "

                    elif mode == 5:
                        if already_have_one == False:
                            math_problem += 'y'
                            z = ("(" + (self.MakeOrderOfOperations(already_have_one=True)[0]) + ")")
                            math_problem += z
                            equa += "(" + str(y) + "*" + str(z) + ")"
                            second_mode = random.randint(1, 4)
                            if second_mode == 1:
                                math_problem += ' + '
                                equa += ' + '
                            elif second_mode == 2:
                                math_problem += ' - '
                                equa += ' - '
                            elif second_mode == 3:
                                math_problem += ' * '
                                equa += ' * '
                            elif second_mode == 4:
                                equa += ' / '
                                math_problem += ' / '

                    elif mode == 6:
                        if already_have_one == False:
                            z = str(random.randint(2, 4))
                            math_problem += ("y" + f"**{z}")
                            equa += (f"{str(y)}**{z}")
                            if (second_mode := random.randint(1, 4)) == 1:
                                math_problem += ' + '
                                equa += ' + '
                            elif second_mode == 2:
                                math_problem += ' - '
                                equa += ' - '
                            elif second_mode == 3:
                                math_problem += ' * '
                                equa += ' * '
                            elif second_mode == 4:
                                math_problem += ' / '
                                equa == ' / '
                except ZeroDivisionError:
                    print("Oopsies.")

            try:
                if mode == 1:
                    x = random.randint(0, 50)
                    math_problem += str(x)
                    math_problem += ' + '
                    print(x)
                elif mode == 2:
                    x = random.randint(0, 50)
                    math_problem += str(x)
                    math_problem += " - "
                elif mode == 3:
                    x = random.randint(0, 50)
                    math_problem += str(x)
                    math_problem += ' + '
                elif mode == 4:
                    if already_have_one == False:
                        math_problem += ("(" + (self.MakeOrderOfOperations(already_have_one=True)[0]) + ")")
                        second_mode = random.randint(1, 4)
                        if second_mode == 1:
                            math_problem += ' + '
                        elif second_mode == 2:
                            math_problem += ' - '
                        elif second_mode == 3:
                            math_problem += ' * '
                        elif second_mode == 4:
                            math_problem += ' / '

                elif mode == 5:
                    if already_have_one == False:
                        math_problem += ("(" + str(random.randint(0, 50)) + f" ** {str(random.randint(2, 4))})")
                        if (second_mode := random.randint(1, 4)) == 1:
                            math_problem += ' + '
                        elif second_mode == 2:
                            math_problem += ' - '
                        elif second_mode == 3:
                            math_problem += ' * '
                        elif second_mode == 4:
                            math_problem += ' / '
            except ZeroDivisionError:
                print("Oopsies.")

        math_problem = math_problem[0:-2]
        equa = equa[0:-2]

        '''
        I realize that the following approach is not recommended in courses, but this is still the best approach I 
        was able to figure out.
        '''
        try:
            solution = eval(equa)
            solution = math.ceil(solution)
        except:
            full_equation = self._MakeEqua(x, y, length)
            return full_equation

        math_problem += f" = {str(solution)}"
        return math_problem

    def AddTeam(self, *args):
        self.name_submission['text'] = ''
        self.name_submission.update()
        exec(f"self.teams['{self.name_submission.get()}'] = 0")
        exec(f"self.choices.append('{self.name_submission.get()}')")
        print(self.teams)



if __name__ == "__main__":
    MainWindow()
