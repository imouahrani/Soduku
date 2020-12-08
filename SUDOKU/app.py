#!/usr/bin/python3

import tkinter as tk
import random
import sys
import os
import time
import timeit

# Démarrez tkinter, nous en avons besoin pour StringVar ()
# Créer une fenêtre de base
root = tk.Tk()

class solver:
	
	def __init__(self):
		# initier une matrice vide
		
		# sera mappé aux entrées
		self.matrixa = [[1 for x in range(10)] for y in range(10)]
		
		# contient le domaine [1,1] = [-1, 1, 1, 0, 1, 0, 0, 0, 0, 0]
		self.matrix_domains = [[1 for x in range(10)] for y in range(10)]
		
		# pour garder une trace de l'état principal
		self.matrix_lock = [[1 for x in range(10)] for y in range(10)]
		
		# pour garder une trace des entrées - changer leur attr si nous en avons besoin
		self.entryList = [[1 for x in range(10)] for y in range(10)]
		
		# la valeur par défaut est de rechercher les entrées avec le domaine minimal
		self.rvt = 'min' # Valeur min restée / Max ...
		
		# remplir de quoi
		self.fill_with = 'min' # Effet min sur d'autres domaines / Aléatoire
		
		self.entry_stack = [] # pile de solutions (retour arrière:backtracking)
		self.stack_save = [] # utilisation: pour enregistrer la solution
		self.backtrack_times = 1
		self.notbf = 0 # ne choisissez pas toujours le meilleur
		

	# Mettre des étiquettes 
    # Créer des entrées 
    # Mapper la matrice aux entrées
	def new(self):
        # effacez la pile pour vous assurer que rien ne s'y trouve (après plusieurs exécutions)
		self.entry_stack = []
		self.backtrack_times = 1
		
		# les étiquettes verticales ne sont pas encore définies :)
		label_flag = 0
		
		for i in range(0, 10):
			# si la colonne est une et que les étiquettes verticales ne sont pas encore définies, définissez-les
			if i == 1 and label_flag == 0:
				for z in range(1,10):
					tk.Label(table, text=z).grid(row = z, column = 0)
				label_flag = 1
		
			# Créer des entrées
			for j in range(1, 10):
				# Commencez par créer des étiquettes horizontales (première fois - i = 0)
				if i == 0:
					tk.Label(table, text=j).grid(row = 0, column = j)
				# when i> 0 puis créer des étiquettes
				else:	
					# init matrixa pour le mapper dans les entrées tkinter
					self.matrixa[i][j] = tk.StringVar()
					# ajouter l'entrée correspondante
					self.entryList[i][j] = tk.Entry(table, width=4, justify='center', textvariable=self.matrixa[i][j])
					self.entryList[i][j].grid(row = i, column = j)
		self.colorize();
		
	# créer une copie de la solution à utiliser avec la prochaine
	def save(self):
		for i in range(1,10):
			for j in range(1,10):
				# effacez cette entrée si elle n'est pas prédéfinie
				if self.matrix_lock[i][j] != 1:
					self.matrixa[i][j].set('')
		
		self.stack_save = self.entry_stack
		self.stack_save.reverse() # quand on apparaît, on commence par le début
		print(colors.fail, "Saved in memory.", colors.endc);
	   
	def notb(self):
		if self.notbf == 0:
			self.notbf = 1
			print(colors.warning,"Don't always choose the best one", colors.endc)
		else:
			self.notbf = 0
			print(colors.green,"Always choose the best one", colors.endc)

	def h1(self):
		self.rvt = 'min' 
		self.fill_with = 'min' # random/min
		print(colors.header,"Select an entry with:", colors.endc , colors.green, " min remained value", colors.endc)
		print(colors.header,"Select an value for entry:", colors.endc, colors.blue, " with min effect on other domains", colors.endc)

	def h2(self):
		self.rvt = 'min'
		self.fill_with = 'random' # random/min
		print(colors.header,"Select an entry with:", colors.endc , colors.green, " min remained value", colors.endc)
		print(colors.header,"Select an value for entry:", colors.endc, colors.blue, " random", colors.endc)
	
	def next(self):
		# si la table était pleine
		if self.stack_save == []:
                    print(colors.warning, "It's done :)", colors.endc);
		else:
			# pop un élément de la copie de pile
			e = self.stack_save.pop()
			# récupérer sa valeur
			self.matrixa[e[0]][e[1]].set(e[2])
	# rechercher et remplacer (remplir)
	def sr(self):
		nextEntry = self.nextEntry()
		x = nextEntry[0]
		y = nextEntry[1]
		val = self.withWhat(x, y)
		self.matrixa[x][y].set(val)
		
		# ajouter la valeur à la pile
		tmp = self.entry_stack.pop()
		self.entry_stack.append([x, y, val])
		
		# domaines pour les entrées effectuées
		self.calDomains(self.row(x,y), self.col(x,y), self.box(x,y));
	
	def nextLive(self):
		if self.checkDone() == 1:
			print("--- DONE ---")
		else:
			self.sr(); # rechercher et remplir
				
	def search(self):
		#self.out('search will started in 1 sec...')
		#self.out('entry stack: ', self.entry_stack)
		#time.sleep(1)
		start = timeit.default_timer()
		while 1:	
			self.sr(); # search and fill
			if self.checkDone() == 1:
				print("--- DONE ---")
				break;
			#os.system("sleep 0.0005")
			#time.sleep(0.025)
			
		stop = timeit.default_timer()
		timeLabel['text'] = str( round(stop - start, 2) ) + " SEC" 
		print("in: ", stop - start, "sec.")		

	def finalize(self):

		self.setPrimaryState()

		self.calDomains()
		
		os.system('cls' if os.name == 'nt' else 'clear')

	def checkDone(self):
		for i in range(1, 10):
			for j in range(1, 10):
				if not self.matrixa[i][j].get().isdigit() :
					return 0
		
		return 1
					 
	# ----------------------------------------------------------------------
	# Domaines et matrices
	# ----------------------------------------------------------------------

	# sélectionnez et renvoie une entrée avec l'heuristique demandée à remplir ensuite
	# self.rvt: max/min 
	def nextEntry(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		self.out("start looking for a domain with ", self.rvt, " value.")
	
		# créer une liste de toutes les entrées sans valeur et leur nombre de domaines
		lst = []
		for i in range(1, 10):
			for j in range(1, 10):
				# ajoutez-le si cette entrée n'a pas de valeur
                # pour éviter de proposer une entrée avec une valeur
				if not self.matrixa[i][j].get().isdigit() :
					domain = int(self.matrix_domains[i][j][0]);
					lst.append([i, j, domain ]) # [ [x,y, domainCount], ... ]
	
		# créer une liste de valeurs de domaine à partir d'entrées sans valeur
		nlst = [] # [1, 2, ...]
		for i in lst:
			nlst.append(i[2])
		
		# supprimer les numéros en double
		nlst = self.rmDup(nlst);
		# supprimer zéro [pour revenir en arrière]
		if nlst.count(0) > 0:
			nlst.remove(0);

		self.out("Select from this domains:", nlst);
		
		# il n'y a pas de domaine pour sélectionner un min / max parmi eux	
		if nlst == []:
			self.out("All domains are taken.")
			# commencer le backtracking
			self.backtrack()
			return self.nextEntry()
		else:
			# sélectionner min ou max dépend de h1 / h2
			if self.rvt == 'min':
				# trouver le min
				val = min(nlst)
				#print("max: ", val)
			else:
				#find the max
				val = max(nlst)
				#print("max: ", val)

			# some log
			self.out("Selected domain: ", val)
		
			# créer une liste de toutes les entrées avec le même domaine sélectionné (valeur)
			nlst = []
			for i in lst:
				if val == i[2]:
					nlst.append([i[0], i[1]])
				
			# sélectionnez un index aléatoire et renvoyez-le
			choice = random.choice(nlst)

			self.out("Choiced entry: ", choice)
			# imprimer le domaine d'entrée des choix :)
			self.out("With the domain of: ", self.matrix_domains[choice[0]] [choice[1]])
		
			# ajouter l'entrée sélectionnée au stock d'entrée à des fins de retour en arrière
			self.entry_stack.append(choice)
		
			# affichage de la pile d'entrées
			self.out("\nEntry Stack: ", self.entry_stack, "\n")
		
			return choice

	# renvoie la meilleure valeur pour remplir une entrée
	def withWhat(self, x, y):
		# obtenir les valeurs disponibles dans ce domaine d'entrée
		lst = self.availVals(x,y)
		
		self.out("Available values for this entry are:", lst)
		self.out("Select form is: ", self.fill_with) 
		
		# basé sur h1 / h2 renvoie une valeur de choix
		if self.fill_with == 'random':
			choice = random.choice(lst);
		elif self.fill_with == 'min':

			# obtenir une liste des entrées qui seront affectées par cette valeur
			elst = self.row(x,y) + self.col(x,y) + self.box(x,y)
			elst.remove([x, y]) # remove the entry itself
			self.out("\nEntries that will be effected by this entry:", elst)
			# ne conserver que les entrées vides
			elst = self.onlyEmpty(elst)
			self.out("\nThe empty ones:", elst)
			
			# Somme de toutes les entrées qui seront effectuées [avant toute modification]
			sum_d = 0
			for e in elst:
				sum_d += self.domainCount(e[0], e[1]) 
			self.out("\nSum of available value in all these entries domains:", sum_d)
			
			# conserver une copie pour réinitialiser après le calcul
			domains_copy = self.matrix_domains
			matrixa_copy = self.matrixa
			
			# sélectionnez une valeur qui a moins d'effet sur les autres domaines d'entrées
            # si 1 fait que les domaines totalisent 20, et 2 en font 40, alors choisissez le 2 cuse
            # ça les change moins que de 1
			
			choice_domain_range = 0 # disons que le changement maximum est nul

			# pas toujours les meilleures listes de fonctionnalités
			if self.notbf == 1:
				d = [] # liste de domaines pour choisir l'un des meilleurs (PAS LE MEILLEUR)
				v_d = {} # dictionnaire de domaines et la valeur qui fait que ce domaine choisit la valeur
			
			# lst = valeurs disponibles pour cette entrée (sélectionnée)
            # vérifier chaque valeur, voir laquelle affecte le moins
			for i in lst:	
				# réinitialiser pour le calcul
				self.matrixa = matrixa_copy
				self.matrix_domains = domains_copy
					
				# définir une valeur de test (à partir des valeurs disponibles pour cette entrée)
				self.matrixa[x][y].set(i)
				
				# calculer les domaines après avoir défini la valeur de test
				self.calDomains(elst)
				
				# compter les valeurs disponibles dans le domaine des entrées après avoir défini la valeur de test
				sum_d = 0
				for e in elst:
					sum_d += self.domainCount(e[0], e[1])
				
				# si cette valeur élargit les domaines, choisissez-la pour le moment
				if sum_d >= choice_domain_range:
					choice_domain_range = sum_d
					choice = i
					
					# créer une liste pour ne pas toujours choisir la meilleure fonctionnalité
					if self.notbf == 1:
						# dict du domaine et la valeur qui rend ce domaine
						v_d[sum_d] = choice
						d.append(sum_d) # seuls domaines, pour trier, inverser et trouver un bon domaine
			
			# sinon toujours le meilleur drapeau est défini
			if self.notbf == 1:
				self.out("Available values changes on domains are like: ", d);
				d = self.rmDup(d)
				d.sort() # [1,2,3,4]
				d.reverse() # [4,2,3,1]
				if len(d) >= 2:
					choice_domain_range = d[1] # 2 => 2th mailleur domain
					self.out("The second best is (domain range): ", d[1]);
				else:
					choice_domain_range = d[0]
					self.out("I can only choose the best (domain range) right now and its: ", d[0]);
					
				choice = v_d[choice_domain_range] # v_d[2] = ? (la valeur fait la somme des domaines: 2)
					
			self.out("this whill change domains to: ",  choice_domain_range)
			#self.matrixa = matrixa_copy
		
		self.out("choice is: ", choice)
		return choice
		
	# obtient une liste d'entrées
    # renvoie uniquement les vides
	def onlyEmpty(self, lst):
		nlst = []
		for e in lst:
			if self.matrixa[e[0]][e[1]].get() == '':
				nlst.append([ e[0],  e[1] ])
		return nlst
		
	# renvoie les valeurs disponibles dans un domaine
	def availVals(self, x, y):
		# obtenir le domaine d'entrée
		domain = self.matrix_domains[x][y] # [-1, 1, 0, ..., 1]
		# créer une liste des valeurs disponibles dans ce domaine
		lst = []
		for i in range(1,10):
			if domain[i] == 1:
				lst.append(i)
		return lst
				
	def backtrack(self):
		self.out("Backtracking ...")
		# PAS D'IDÉE: D # alors supprimons certaines des entrées 
        # augmentons le retour en arrière à chaque fois
		self.backtrack_times += 1
		#if self.backtrack_f == 10:
		#	self.backtrack_f = 1
		r = 5 * self.backtrack_times
		
		# s'il y a quelque chose dans le backtrack de la pile
		if r > len(self.entry_stack):		
			r = len(self.entry_stack);
			self.backtrack_times = 1
			
		for i in range(r):
			entry = self.entry_stack.pop();
			x = entry[0]
			y = entry[1]
			self.matrixa[x][y].set('');
			# calculer le domaine de toutes les entités concernées
			self.calDomains( self.row(x,y), self.col(x,y), self.box(x,y) ); 

	# calculer le domaine d'une ENTRÉE
	def calDomain(self, x, y):
		# obtenir toutes les valeurs qui affectent ce domaine de point d'entrée
		entries = self.row(x,y) + self.col(x,y) + self.box(x,y)
		entries.remove([x, y]) # remove itself from entries
		vals = self.getVals(entries) 

		# réinitialiser le domaine
		self.matrix_domains[x][y] = [-1,1,1,1,1,1,1,1,1,1]
		
		# puis désactivez les bits en conflit en ce moment
		for i in vals:
			self.matrix_domains[x][y][int(i)] = 0
		
		# nombre défini de bits on dans ce domaine
		self.matrix_domains[x][y][0] = self.domainCount(x, y)
		
		# afficher le domaine TST
        #print (self.matrix_domains [x] [y])

	# calculer le domaine d'une LISTE D'ENTRÉES
	def calDomains(self, *args):
		listOfEntries = []  # pour clac domaine pour
# si nous avons une liste uniquement calc pour ces entrées
		if len(args) > 0:
			# créer une liste de listes
			for arg in args:
				listOfEntries += arg
		else:
		# sinon calc pour toutes les entrées 
        # créer une liste de toutes les entrées de la matrice
			for i in range(1,10):
				for j in range(1,10):
					listOfEntries.append([i, j])
					
		# domaine calc pour chaque entrée
		for i in listOfEntries:
			self.calDomain(i[0], i[1])

	# renvoie le nombre de bits sur (1) dans un domaine d'entrée 
    # nombre des valeurs restantes dans un domaine d'entrées 
    # [-1,1,1,1,1,1,1,1,0,1]: 8
	def domainCount(self, x, y):
		count = 0
		for i in self.matrix_domains[x][y]:
			if i == 1:
				count += 1
		return count
	
	# créer une liste de numéros d'état primaire 
    # afin de ne pas les modifier lors du retour en arrière
	def setPrimaryState(self):
		for i in range(1, 10):
			for j in range(1, 10):
				# entrée a une valeur
				if self.matrixa[i][j].get() != '' :
					# verrouiller - lors de l'enregistrement (effacement), nous ignorons cette entrée
					self.matrix_lock[i][j] = 1
					self.entryList[i][j]['fg'] = 'red'
					#self.entryList[i][j]['state'] = 'disabled'
				else:
					self.matrix_lock[i][j] = 0

	# ------------------------------------------------- ---------------------
    # Ligne et valeurs
    # ------------------------------------------------- ---------------------

    # créer une liste de valeurs à partir des entrées sélectionnées
    # entrées doivent être spécifiées sous forme de liste de listes
    # [[1,2], [2,5], [4,8], ...] renverra la valeur de 1,2 etc.
	def getVals(self, *args):
		# combiner les listes d'entrées passées en argument
        # exemple retVals (row (), col ())
        # combine la ligne et les cols [[1,2] ... [1,3]]
		listOfEntries = []
		for arg in args:
			listOfEntries += arg

		# supprimer les entrées en double
		listOfEntries = self.rmDup(listOfEntries)
		
		# créer une liste de valeurs
		lst = []
		for i in listOfEntries:
			# n'ajoutez pas de valeurs vides
			if self.matrixa[i[0]][i[1]].get() != '':
				lst.append( self.matrixa[i[0]][i[1]].get() ) # ajouter la valeur de matrixa [1] [3]
		return lst

	# renvoie une liste de tous les points d'entrée dans une même ligne
	def row(self, x, y):
		lst = []
		for i in range(1,10):
			# ignorer l'entrée sélectionnée
			if i != y:
				lst.append([x, i])
		return lst

	# renvoie une liste de tous les points d'entrée dans une même colonne
	def col(self, x, y):
		lst = []
		for i in range(1,10):
			# ignorer l'entrée sélectionnée
			if i != x:
				lst.append([i, y])
		return lst
	
	# renvoie une liste de toutes les entrées dans une même boîte que matrixa [x] [y]
	def box(self, x, y):
        # pointer le centre :)
		if x == 3 or x == 6 or x == 9:
			x = x-1;
		if x == 1 or x == 4 or x == 7:
			x = x+1;
		if y == 1 or y == 4 or y == 7:
			y = y+1;
		if y == 3 or y == 6 or y == 9:
			y = y-1;
		
		# chacun des deux est un point d'entrée
		lst = [	[x-1, y-1], 
			[x-1, y],
			[x-1, y+1],
			[x, y-1],
			[x, y],
			[x, y+1],
			[x+1, y-1],
			[x+1, y],
			[x+1, y+1]
		      ]
		return lst

# ----------------------------------------------------------------------
#                               --- AIDES --- 
# ----------------------------------------------------------------------

    # supprimer les éléments en double d'une liste
	def rmDup(self, lst):
		# creer une nouvelle liste
		nlist = []
	
		for i in lst:
			if i not in nlist:
				nlist.append(i)
		return nlist
		
	def out(self, *args):
		if len(sys.argv) > 1 :
			if sys.argv[1] == '-v':
				text = ''
				for arg in args:
					text += str(arg)
				
				print(text)
	def colorize(self):
		lst = [ [2,2], [2,4], [2,8],
			[5,2], [5,4], [5,8],
			[8,2], [8,4], [8,8] 
		]
		color = '#e5e5e5'
		for e in lst:
			nlst = self.box(e[0], e[1])
			for i in nlst:
				self.entryList[i[0]][i[1]]['bg'] = color
		    
			if color == '#e5e5e5' :
				color = '#c9c9c9'
			else:
				color = '#e5e5e5';

class colors:
    header = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
    
# init classe de base
solver = solver()
	
# ------------------------------------------------- ---------------------
# --- GUI --- #
# ------------------------------------------------- ---------------------


# table frame
table = tk.Frame(root, width=350, height=200)
table.grid(row = 1, column = 0, sticky="w")

# seperator
tk.Frame(root, height=200, width=10).grid(row = 1, column = 1)

# left buttons (#start, search)
buttons = tk.Frame(root, height=200, width=140)
buttons.grid(row = 1, column = 2,  sticky="e")

# seperator
tk.Frame(root, height=10, width=350).grid(row = 2, column = 0)

# down buttons (#next)
dbuttons = tk.Frame(root, height=50, width=350)
dbuttons.grid(row = 3, column = 0)

# Créer un objet de menu et l'ajouter à la racine
menubar = tk.Menu(root)

# Créer un menu de fichiers en cascade
filemenu = tk.Menu(menubar, tearoff=0)

filemenu.add_command(label="New",  command=solver.new)
filemenu.add_command(label="Save", command=solver.save)
filemenu.add_command(label="NaTb", command=solver.notb)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

# Ajouter le menu du fichier en cascade à l'objet de la barre de menus
menubar.add_cascade(label="File", menu=filemenu)

# Ajouter deux autres éléments indépendants à la barre de menu
menubar.add_command(label="First way", command=solver.h1)
menubar.add_command(label="Second way", command=solver.h2)


# Afficher le menu (barre de menus sous forme de menu)
root.config(menu=menubar)

# refuser le redimensionnement
root.resizable(0,0)
table.pack_propagate(0)
#buttons.pack_propagate(0)
#dbuttons.pack_propagate(0)

# set root geometry
root.geometry("500x275")

# buttons
tk.Button(buttons, width=12, text='Create start state', command = solver.finalize).pack()
tk.Button(buttons, width=12, text='Start searching', command = solver.search).pack()
tk.Button(dbuttons, width=12, text='Next', command = solver.next).pack()
tk.Button(dbuttons, width=12, text='Next Live', command = solver.nextLive).pack()
timeLabel = tk.Label(buttons, width=12, text='00')
timeLabel.pack()

root.title("Python CSP Sudoku Solver - by: Imene & Othmane ");

tk.mainloop()

# --------------------------------------------
