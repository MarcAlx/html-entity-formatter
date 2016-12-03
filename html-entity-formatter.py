# -*- coding: utf-8 -*-
#Crée par Marc-Alexandre Blanchard

from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askopenfilename

class Application(object):
    """ classe application """
    #Dictionnaire contenant les conversion caractère/code HTML
    dico = {}

    def LoadDico(self,filename):
        f = open(filename,'r',encoding='utf-8')
        lignes  = f.readlines()
        f.close()
 
        for ligne in lignes:
            res = ligne.split()
            self.dico[str(res[0])]=str(res[1])
        
        
    #Remplace les caractères non HTML d'une chaine de caractère par leur code HTML
    def Convert(self,chaineEntree):
        chaineSortie=""
        for c in chaineEntree:
            if(c in self.dico):
                chaineSortie+=self.dico[c]
            else:
                chaineSortie+=c
        return chaineSortie

    #Remplace le contenu de la case inferieur par le contenu "convertit" de la case superieure
    def Format(self):
        self.sortie.delete(1.0, END)
        self.sortie.insert(END,self.Convert(self.entree.get(1.0, END)))

    #Remplace le contenu de la case inferieur par le contenue "convertit" du presse papier 
    def CB2Format(self):
        #Ajout du contenu du presse papier dans la case superieure : affichage user-friendly
        self.entree.delete(1.0, END)
        self.entree.insert(END,self._tk.selection_get(selection='CLIPBOARD'))
        self.Format()

    #Remplace le contenu du presse papier par la conversion de la case supérieur
    def Format2CB(self):
        self.Format()
        self._tk.clipboard_clear()
        self._tk.clipboard_append(self.sortie.get(1.0, END))
        
    #Remplace le contenu du presse papier par la conversion de ce même contenu
    def CB2Format2CB(self):
        self.entree.delete(1.0, END)
        self.entree.insert(END,self._tk.selection_get(selection='CLIPBOARD'))
        self.Format2CB()

    #Formate le contenu d'un fichier à l'interieur même de ce fichier
    def FileFormat(self):
        #Affichage du filechooser
        filename = askopenfilename()
        #Si le fichier est choisi
        if filename:
            #Lecture du contenu du fichier
            obFichier = open(filename,'r',encoding='utf-8')
            temp = ""
            while 1:
                #Ajout de chaque caractère à une chaine temporaire
                car=obFichier.read(1)
                temp+=car
                #On sort de la boucle lorsque l'on tombe sur une chaine vide
                if(car ==""):
                    break
            obFichier.close()
            #Phase de conversion 
            obFichier =open(filename,'w',encoding='utf-8')
            #Remplacement du fichier par sa conversion 
            obFichier.write(self.Convert(temp))
            obFichier.close()
            #Affichage d'une message box pour signaler la fin de conversion
            tkinter.messagebox.showinfo("Done","Formatting done !")

    def __init__(self):
        #Définition self._tk 
        self._tk = Tk()
        #Titre de la self._tk
        self._tk.title("WebStringFormater")
        #On bloque le resize
        self._tk.resizable(width=False, height=False)

        #Bouton FileFormat
        self.boutonFileFormat = Button(self._tk,text='Format a file', command=self.FileFormat)
        #Affichage du bouton FileFormat
        self.boutonFileFormat.pack(fill = X)
        
        #Zone de texte supérieure
        self.entree = Text(self._tk, height=15, width=50,background = 'blue',font = "Ar")
        #Affichage de la zone de texte superieure
        self.entree.pack()
        #Ajout d'une barre de défilement invisible
        self.scroll = Scrollbar(self._tk, command=self.entree.yview)
        self.entree.configure(yscrollcommand=self.scroll.set)

        #Céation d'un conteneur pour pouvoir aligner horizontalement les boutons entre les deux zones de texte
        self.conteneurBouton = Frame(self._tk)
        
        #Bouton CB2Format - Ajout au conteneur pas à la self._tk, le conteneur sera ajouté à la self._tk après
        self.boutonCB2Format = Button(self.conteneurBouton,text='Clipboard -> Format', command=self.CB2Format)
        #Affichage du bouton CB2Format dans le conteneur
        self.boutonCB2Format.pack(side = LEFT,fill = X)
        
        #Bouton format - Ajout au conteneur pas à la self._tk, le conteneur sera ajouté à la self._tk après
        self.boutonFormat = Button(self.conteneurBouton,text='Format', command=self.Format)
        #Affichage du bouton format dans le conteneur
        self.boutonFormat.pack(side = LEFT,fill = X)

        #Bouton Format2CB - Ajout au conteneur, pas à la self._tk le conteneur sera ajouté à la self._tk après
        self.boutonFormat2CB = Button(self.conteneurBouton,text='Format -> Clipboard', command=self.Format2CB)
        #Affichage du bouton Format2CB dans le conteneur
        self.boutonFormat2CB.pack(side = RIGHT,fill = X)
        #Affichage et ajout du conteneur à la self._tk
        self.conteneurBouton.pack()

        #Bouton format
        self.boutonFormat = Button(self._tk,text='Clipboard -> Format -> Clipboard', command=self.CB2Format2CB)
        #Affichage du bouton format
        self.boutonFormat.pack(fill = X)

        #Zone de texte inférieure
        self.sortie = Text(self._tk, height=15, width=50,background = 'blue',font = "Ar")
        #Affichage de la zone de texte inférieure
        self.sortie.pack(fill = X)
        #Ajout d'une barre de défilement invisible
        self.scroll2 = Scrollbar(self._tk, command=self.sortie.yview)
        self.sortie.configure(yscrollcommand=self.scroll2.set)

        #Bouton quitter
        self.boutonquitter = Button(text='Quit', command = self._tk.destroy)
        #Affichage du bouton quitter
        self.boutonquitter.pack(fill = X)

        #Chargement du dictionnaire
        self.LoadDico("dico.txt");

    def mainloop(self):
        self._tk.mainloop()
    
if __name__ == '__main__':
    Application().mainloop()
