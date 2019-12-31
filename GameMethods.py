import tkinter as tk

class Question(tk.Frame):
    def __init__(self, master, text, answer):
        tk.Frame.__init__(self, master=master)
        
        self.master = master
        self.texted = text
        self.correct_answer = answer

        self.texter = tk.Label(self, text=text, font="Times 14")
        self.texter.grid(padx=20, pady=10)

        self.alerter = tk.Label(self, text = '                                  ', font="Terminal 14 bold", foreground="crimson")
        self.alerter.grid()

        self.answer_entry = tk.Entry(self, font="Times 14")
        self.answer_entry.grid(padx=50, pady=10)

        self.submit_answer_button = tk.Button(self, font="Times 14 bold", text="Submit answer", command=self.OnButtonPress)
        self.submit_answer_button.grid(padx=50, pady=0)
        self.bind("<Return>", self.OnButtonPress)

    def ShowMe(self, *args):
        self.grid(padx=70, pady=20)

    def OnButtonPress(self, *args, **kwargs):
        print("An answer has been submitted.")
        answer = self.answer_entry.get().split()
        self.who = answer[0]
        
        try:
            what = answer[1]
        except IndexError:
            self.alerter['text'] = "    **INCORRECT ANSWER FORMAT!**    "
            self.alerter.update()
            self.master.after(3000, self.RemoveAlert)
            return None

        if str(what) != str(self.correct_answer):
            self.alerter['text'] = "     **INCORRECT! INCORRECT!**     "
            self.alerter.update()
            self.master.after(3000, self.RemoveAlert)
        
        else:
            self.alerter['text'] = f"**{self.who.upper()} HAS ANSWERED CORRECTLY! **"
            self.alerter['fg'] = "green"
            self.alerter.update()
            self.destroy()
            self.master.after(2000, self.AlertNextQuestion)
        
        print(answer)

    def RemoveAlert(self, *args):
        self.alerter['text'] = ""
        self.alerter.update()

    def AlertNextQuestion(self, *args):
        self.master.teams[self.who] += 1
        print(self.master.teams)
        self.master.AdvanceQuestion()

if __name__ == "__main__":
    root = tk.Tk()
    Questioner= Question(root, "Hello, world!", "Hello, world!")
    Questioner.grid()
    root.mainloop()
