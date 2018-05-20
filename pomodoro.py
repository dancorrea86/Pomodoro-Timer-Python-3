from tkinter import *
import pygame

class Relogio(object):

    def __init__(self, master):
        self.master = master
        self.master.geometry('300x200')

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.title('Pomodoro')

        self.barraMenu = Menu(master)

        # Definingo opções
        self.menuOpcoes = Menu(self.barraMenu, tearoff=0)

        self.menuConfigTempo = Menu(self.barraMenu, tearoff=0)
        self.menuOpcoes.add_command(label='Config. time', accelerator='Ctrl+t', compound=LEFT, command=self.telaConfigTempo)

        self.opcoes_menusom = Menu(self.barraMenu, tearoff=0)
        self.menuOpcoes.add_cascade(label='Alarms',  menu=self.opcoes_menusom)

        self.opcoesAlarmes = {'1. Firestation Bell': 'sons/firestation_bell.wav',
                           '2. Burglar Bell': 'sons/burglar_bell.wav'}

        self.alarme = StringVar()
        self.alarme.set('1. Firestation Bell')

        for k in sorted(self.opcoesAlarmes):
            self.opcoes_menusom.add_radiobutton(label=k, variable=self.alarme, command=self.som)

        self.barraMenu.add_cascade(label='Options', menu=self.menuOpcoes)

        self.infoMenu = Menu(self.barraMenu, tearoff=0)
        self.infoMenu.add_command(label='Info', accelerator='Ctrl+I', compound=LEFT, command=self.telaInfo)
        self.barraMenu.add_cascade(label='File', menu=self.infoMenu)

        self.master.config(menu=self.barraMenu)

        self.frame_show()

    def alteraTempo(self):
        self.initTempoPomodoro = self.entry_var.get()
        self.labelClock['text'] = ("%.2f" % self.initTempoPomodoro)
        self.toplevel.destroy()

    def telaConfigTempo(self):
        self.toplevel = Toplevel(self.master)
        self.entry_var = DoubleVar()
        self.entryTime = Entry(self.toplevel, textvariable=self.entry_var)
        self.entryTime.grid()

        self.btnSetTime = Button(self.toplevel, text='Ok', command=self.alteraTempo)
        self.btnSetTime.grid()

    def telaInfo(self):
        toplevelInfo = Toplevel(self.master)
        toplevelInfo.geometry('100x50')
        self.labelInfo = Label(toplevelInfo, text='Simple pomodoro timer')
        self.labelInfo.grid()

    def som(self):
        self.som_nome = self.alarme.get()
        self.som_escolhido = self.opcoesAlarmes.get(self.som_nome)

    def frame_show(self):
        self.frame = Frame(self.master, bg='green')
        self.frame.grid(row=0, column=0, sticky='WE')
        self.frame.columnconfigure(0, weight=1)

        self.initTimePomodoro = 25.00
        self.timePomodoro = 25.00

        self.labelClock = Label(self.frame, text=("%.2f" % self.timePomodoro))
        self.labelClock['font'] = 'Helvetica 80 bold'
        self.labelClock.grid(sticky='we')

        self.btnStart = Button(self.frame, text='Start', command=self.startPomodoro)
        self.btnStart.grid(row=1, sticky='we')

        self.btnCancel = Button(self.frame, text='Cancel', command=self.cancelPomodoro)
        self.btnCancel.grid(row=2, sticky='we')
        self.statusCancel = False

    def startPomodoro(self):
        self.statusCancel = False
        self.timePomodoro = self.initTimePomodoro
        self.labelClock['text'] = ('%.2f' % self.timePomodoro)
        self.ticClock()

    def cancelPomodoro(self):
        self.statusCancel = True

    def ticClock(self):
        if self.timePomodoro < 0.01:
            self.labelClock['text'] = ('0.00')
            pygame.init()
            audio = pygame.mixer.Sound(self.opcoesAlarmes.get(self.alarme.get()))
            self.master.lift()
            audio.play()
        elif (self.statusCancel == True):
            print (self.initTimePomodoro)
            self.labelClock['text'] = ('%.2f' % self.initTimePomodoro)
        else:
            self.timePomodoro = self.timePomodoro - 0.01
            self.labelClock['text'] = ('%.2f' % self.timePomodoro)
            self.master.after(1000, self.ticClock)

def main():
    root = Tk()
    app = Relogio(root)
    root.mainloop()

if __name__ == '__main__':
    main()
