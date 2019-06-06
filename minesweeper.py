#Basic 9x9 Minesweeper Program, Justin Womack
#-*- coding: utf-8 -*-
#Explanation of code and algorithm created listed under f(recheck)
#runs on python 2.7.  Not tested on python 3.

import sys, random
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


class MainWidget(QtGui.QWidget):

	def __init__(self, parent = None):

		super(MainWidget, self).__init__()
		#all print functions throughout program are commented now.  They were used to check the program 
		#at different steps to work through errors.  Kept for curosity and possible revisions

		#Be careful playing with window size in .SetFixedSize. Could create problems with playing grid
		#.setGeometry sets position on screen.
		self.setGeometry(200, 300, 500,650)
		self.setWindowTitle("Minesweeper")
		self.setFixedSize(180,250)

		#creates a position list records the positions on board. Used for many things.  
		self.plist = []
		#list created to store buttons that will be added to the grid in for loop
		self.buttons = []
		#keeps track of bomb variable
		self.bomb_count = 0
		#initiate variable used in recheck
		self.recheck_list = []
		#initiates flag variable, position
		self.flags = 10
		self.flag_positions = []
		#allows program to run first recheck fxn.  Once ran this variable will change to false
		self.first_recheck = True

		self.container = QtGui.QVBoxLayout()

		#Creates LCD counter.  This one is for flags system
		self.lcd_flag_count = QtGui.QLCDNumber(self)
		self.lcd_flag_count.setObjectName("lcd_flag_count")
		self.lcd_flag_count.setSegmentStyle(QtGui.QLCDNumber.Flat)
		self.lcd_flag_count.setFixedSize(40,30)
		self.lcd_flag_count.display('0%d ' %self.flags)

		#creates 2nd LCD counter.  This one is for clock.
		self.lcd_time = QtGui.QLCDNumber(self)
		self.lcd_time.setObjectName("lcd_time")
		self.lcd_time.setSegmentStyle(QtGui.QLCDNumber.Flat)
		self.lcd_time.setFixedSize(40,30)

		#creates timer, sets starting time variable, places to lcd display, and sets variable that will trigger clock on click
		self.timer = QtCore.QTimer(self)
		self.start_time = 0
		self.lcd_time.display('00%d ' %self.start_time)
		self.no_buttons_clicked = True
		# print('no buttons: ', self.no_buttons_clicked)
		self.timer.timeout.connect(self.updateLCD) 

		#creates middle smiley/devil face thing.  This button should reset the game.
		self.reset_button = QtGui.QPushButton()
		self.reset_button.setIcon(QtGui.QIcon('big_smile.jpeg'))
		self.reset_button.setIconSize(QtCore.QSize(39,39))
		self.reset_button.setFixedSize(40,30)
		self.reset_button.clicked.connect(self.reset_game)

		#Creates horizontal layout and places buttons on them.  Standard spacing seems fine.
		self.infobox = QtGui.QHBoxLayout()
		self.infobox.addWidget(self.lcd_flag_count)
		self.infobox.addWidget(self.reset_button)
		self.infobox.addWidget(self.lcd_time)

		self.gridcontainer = QtGui.QHBoxLayout()
		self.gridLayout = QtGui.QGridLayout()

		#creating of lists that store index values of positions already clicked or checked.
		#the to check list is compared to the checked list in order to skip excess searches and hopefully to 
		#get rid of my infinite loop issue.
		self.positions_to_check = []
		self.positions_checked = []

		#creation of board buttons.  Its hard to get teh sizes to work well without extra space in the last columns
		#But this setup seems to work. Any changes in board dimensions may cause a revertion in size to undesirable state.  IDK.
		for i in xrange(9):
			l=[]
			for j in xrange(9):
				self.b=QtGui.QPushButton()
				self.b.clicked.connect(self.click)
				self.b.setFixedSize(20,20)
				#sets up the right click function on each button
				self.b.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
				self.b.customContextMenuRequested.connect(self.on_right_click)
				l.append(self.b)
				self.gridLayout.addWidget(self.b, i, j)
				self.position = [i, j]
				self.plist.append(self.position)
				self.buttons.append(l)
		# print('plist length: ', len(self.plist))
		# print(self.plist[80])

		#creates bomb positons thorugh a random sample. For loop places bombs in button matrix
		#plist is the game grid that is used.  I might say game grid throughout these notes on accident
		self.bomb_positions = (sorted(random.sample(range(0,81),10), reverse=True))
		for i in range(len(self.bomb_positions)):
			self.plist[self.bomb_positions[i]] = 'BOMB'
		# print('plist: ', self.plist)

		#initiates lists/variables used in check for winning game.
		self.victory_list = []
		self.victory_list_in_indices = []
		self.victory_counter = 0

		#creates final victory in index values list my adding all grid positions that are not bombs to victory list
		#called fxn will then convert this positions to index values and place into final list
		for i in self.plist:
			if i != 'BOMB':
				self.victory_list.append(i)
		# print('victory_list: ', self.victory_list)
		self.convert_list_to_idx(self.victory_list)
		# print 'Victory for index: ', self.victory_list_in_indices

		#Just typical container in container Gui board situation nonsense.
		self.gridcontainer.addLayout(self.gridLayout)
		self.container.addLayout(self.infobox)
		self.container.addLayout(self.gridcontainer)
		self.container.addStretch(1)

		self.setLayout(self.container)
		self.set_stylesheet()

	def convert_list_to_idx(self, list_to_convert):
		#converts grid locations to indexs i.e [0,0], [8,8] ----> 0, 81
		#this specific system works for 9x9 grid only 

		for i in list_to_convert:
			if i[0] == 0:
				victory_idx = i[1]
				self.victory_list_in_indices.append(victory_idx)

			elif i[0] == 1:
				victory_idx = int(str(i[0]) + str(i[1])) - 1
				self.victory_list_in_indices.append(victory_idx)

			elif i[0] == 2:
				victory_idx = int(str(i[0]) + str(i[1])) - 2
				self.victory_list_in_indices.append(victory_idx)

			elif i[0] == 3:
				victory_idx = int(str(i[0]) + str(i[1])) - 3
				self.victory_list_in_indices.append(victory_idx)

			elif i[0] == 4:
				victory_idx = int(str(i[0]) + str(i[1])) - 4
				self.victory_list_in_indices.append(victory_idx)

			elif i[0] == 5:
				victory_idx = int(str(i[0]) + str(i[1])) - 5
				self.victory_list_in_indices.append(victory_idx)

			elif i[0] == 6:
				victory_idx = int(str(i[0]) + str(i[1])) - 6
				self.victory_list_in_indices.append(victory_idx)

			elif i[0] == 7:
				victory_idx = int(str(i[0]) + str(i[1])) - 7
				self.victory_list_in_indices.append(victory_idx)

			else:
				victory_idx = int(str(i[0]) + str(i[1])) - 8
				self.victory_list_in_indices.append(victory_idx)


		# print(self.victory_list_in_indices)
		# print len(self.victory_list_in_indices)

	def remaining_bombs_2_flags(self):
		#fxn triggers after f(check_victory) determines victory.  
		#fxn checks for remaining bombs that weren't flagged and flags them.
		#also stops timer, disables some buttons, etc.

		index_counter = -1
		# print("Victory Plist: ", self.plist)
		# print("VICTORY Positions checked: ", sorted(self.positions_checked, key = int))
		
		for i in self.plist:

			index_counter += 1

			if i == 'BOMB':

				#if bomb matched on plist then the icon will be replaced with a flag.  
				self.location = self.gridLayout.getItemPosition(index_counter)
				self.loc = list(self.location[0:2])
				self.item = self.gridLayout.itemAtPosition(self.loc[0], self.loc[1])
				self.item.widget().setIcon(QtGui.QIcon('flag.jpeg'))
				self.item.widget().setEnabled(False)
				self.item.widget().setStyleSheet('background-color:#C0C0C0')
				self.reset_button.setIcon(QtGui.QIcon('shade_2.jpeg'))
				self.timer.stop()

	def check_victory(self):
		#fxn checks for victory
		#victory_list_in_indices will lose elements as each grid location is cleared.  
		#Since this list contains all locations but bombs, when the list is empty the game is won

		if self.victory_list_in_indices == []:
			# print "victory PLEBIAN"
			self.remaining_bombs_2_flags()
		# else:
		# 	print 'victory_list_in_indices: ', self.victory_list_in_indices

	def on_right_click(self, point):
		#fxn sets up flags on grid positions when right click is used 

		# print('Right Click') 

		self.btn = self.sender()
		self.idx = self.gridLayout.indexOf(self.btn)

		#removes flag from a position if flag is already there.
		#as right clicks are used they go into the flag_position list and this check to see if 
		#the right-clicked position is in that list.  If it is it removes it and returns button to normal appearance
		if self.idx in self.flag_positions:
			# print('Remove Flag')
			self.btn.setIcon(QtGui.QIcon())
			self.flag_positions.remove(self.idx)
			self.positions_checked.remove(self.idx)
			self.flags += 1
			# print len(self.positions_checked)

			if self.flags == 10:
				self.lcd_flag_count.display('0%d ' %self.flags)

			else:
				self.lcd_flag_count.display('00%d ' %self.flags)

			# print('Flags ', self.flags)

		else:

			#if all flags are used this stops more from being used.  10 flag limit.  obvs.
			if self.flags == 0:
				# print("No flags left")
				self.lcd_flag_count.display('00%d ' %self.flags)

			else:
				#starts timer on the bizare case where user opens with a flag and not a click
				if self.no_buttons_clicked == True:
					self.timer.start(1000)
					self.no_buttons_clicked = False	

				#adds flag to square.  adds index position to flag_position list and positions_checked list
				# print('Add Flag')
				self.btn.setIcon(QtGui.QIcon('flag.jpeg'))
				self.flag_positions.append(self.idx)
				self.positions_checked.append(self.idx)
				self.flags -= 1
				self.lcd_flag_count.display('00%d ' %self.flags)
				# print('Flags ', self.flags)
				# print len(self.positions_checked)

	def reset_game(self):
		#fxn does exactly what it says

		#resets all game variables
		self.positions_to_check = []
		self.positions_checked = []
		index_counter = -1
		self.victory_list_in_indices = []
		self.victory_list = []
		self.bomb_count = 0
		self.flags = 10
		self.lcd_flag_count.display('0%d ' %self.flags)
		self.flag_positions = []
		self.first_recheck = True
		self.no_buttons_clicked = True
		self.victory_counter = 0
		self.reset_button.setIcon(QtGui.QIcon('smile.png'))
		self.timer.stop()
		self.start_time = 0
		self.lcd_time.display('00%d ' %self.start_time)

		#resets the buttons.  Removes bomb icons, reactivates buttons, resets coloring system
		for i in self.plist:

			index_counter += 1
			self.location = self.gridLayout.getItemPosition(index_counter)
			self.loc = list(self.location[0:2])
			self.item = self.gridLayout.itemAtPosition(self.loc[0], self.loc[1])
			self.item.widget().setEnabled(True)
			self.item.widget().setText('')
			self.item.widget().setIcon(QtGui.QIcon())
			self.item.widget().setStyleSheet('background-color:#C0C0C0')
		
		#recreates game grid and places bombs
		self.plist = []
		# print 'plist: ', self.plist

		for i in xrange(9):
			for j in xrange(9):
				self.position = [i, j]
				self.plist.append(self.position)
		self.bomb_positions = (sorted(random.sample(range(0,81),10), reverse=True))
		
		for i in range(len(self.bomb_positions)):
			self.plist[self.bomb_positions[i]] = 'BOMB'
		# print(self.plist)

		#loop recreates the list needed to check the games victory
		for i in self.plist:

			if i != 'BOMB':
				self.victory_list.append(i)
		# print('Victory list :', self.victory_list)
		self.convert_list_to_idx(self.victory_list)
		# print('victory_list_in_indices: ', self.victory_list_in_indices)

	def updateLCD(self):
		#updates time by one second.  The different if commands are to keep
		#the time centered on screen since I can't get any css functions to work with lcd

		self.start_time += 1

		if self.start_time > 999:
			self.lcd_time.display(' %d' %self.start_time)

		if self.start_time > 99:
			self.lcd_time.display('%d ' %self.start_time)

		elif self.start_time > 9:
			self.lcd_time.display('0%d ' %self.start_time)

		else: 
			self.lcd_time.display('00%d ' %self.start_time)	

	def click(self):

		#Determines signal source i.e. which button was pressed
		self.button = self.sender()

		#usings the signal to determine index position on grid
		self.idx = self.gridLayout.indexOf(self.button)
		# print('idx', self.idx)
		
		#Converts index number into x,y coordinate positions in  4 number tuple.
		self.location = self.gridLayout.getItemPosition(self.idx)
		#Converts tuple to list and takes the x,y coordinates from the list
		self.loc = list(self.location[0:2])
		# print('loc: ', self.loc)

		#I honestly can't recall why I had to use this item variable.  It disables the cliked button
		#from being disabled again. However it seems to call a different object then the original clicked
		#button signal. Strange.  It works tho, so leave it for now.
		self.item = self.gridLayout.itemAtPosition(self.loc[0], self.loc[1])
		
		if self.idx in self.flag_positions:
			#since disabling a flaged position makes it a pain to undisable with right click, I use this work around
			#when a left click happens on a flag position nothing will happen. It just passes.  
			pass

		else:
			#if not a flag, then button gets disabled and background color changed.
			self.item.widget().setEnabled(False)
			self.item.widget().setStyleSheet('background-color: #282827')
		# print('self.button: ', self.button)
		# print('self.item: ', self.item)
		# print(self.plist[int(self.idx)])

			if self.no_buttons_clicked == True:
				self.timer.start(1000)
				self.no_buttons_clicked = False		

			#This varable must be set so that when for loop executes later, the first clicked bomb position is stored
			#And is converted to a red color to let the user know which bomb was clicked.
			self.first_bomb_clicked = self.item

			#checks clicked position which plist created game grid. If values match up then play continues.
			#if values don't, then bomb was hit and game is over.  If loop uses css style fxns to add
			#bomb picture and color change to game.  Must add popup window.
			if self.plist[int(self.idx)] == self.loc:
				# print('true')
				#calls the check fxn on index location which will search surrounding squares for clear spaces
				self.positions_checked.append(self.idx)
				self.victory_list_in_indices.remove(self.idx)
				self.check_nearby_squares(self.idx)
				self.check_victory()

			else:
				#if bomb hit, selected bomb is shown and highlighted red
				# print('bomb')
				self.reset_button.setIcon(QtGui.QIcon('devil.jpeg'))
				self.item.widget().setIcon(QtGui.QIcon('bomb.png'))
				self.item.widget().setStyleSheet('background-color: red')

				#set at -1 since each iteration of the loop adds 1 and we need it to start on 0
				index_counter = -1	

				# print(self.positions_checked)
				#runs through position lists, converting indices to location and showing all remaining bombs
				for i in self.plist:
					index_counter += 1
					self.location = self.gridLayout.getItemPosition(index_counter)
					self.loc = list(self.location[0:2])
					self.item = self.gridLayout.itemAtPosition(self.loc[0], self.loc[1])

					if i == 'BOMB':

						#if bomb matched on plist then the icon will be replaced with a bomb.  
						#keeps game board color
						self.item.widget().setIcon(QtGui.QIcon('bomb.png'))
						self.item.widget().setEnabled(False)
						self.item.widget().setStyleSheet('background-color:#C0C0C0')
						self.timer.stop()


					else:

						#This resets and disables all the buttons to normal.  Which is not what I want.  
						#have to create list and compare which values to change.  Gonna be a bitch.
						#Created list.  Did everything I said would be a bitch to do.
						if index_counter in self.positions_checked:
							#disables all buttons on grid that were checked but not removed because of bomb placement.
							self.item.widget().setEnabled(False)
						else:
							#disables remaining buttons
							self.item.widget().setEnabled(False)
							self.item.widget().setStyleSheet('background-color:#C0C0C0')

				self.first_bomb_clicked.widget().setStyleSheet('background-color: red')			

		
		# print '----------'
		# print len(self.positions_checked)

	def check_nearby_squares(self, index):
		#checks surrounding grid locations for bombs 
		
		# print('CHECK_NEarby_SQUARES')
		# print('ITEM CHECK: ', index)

		#has to call this fxn to determine the index positions to check
		self.determining_nearby_idxs(index)
		#I have too many lists to initialize.  
		self.final_list_of_checks = []
		#BOMB variable is false since clicked square doesn't contain bomb.  Variable will change if surrounding squares have a bomb.
		BOMB = False
		
		#f(determining_nearby_idxs) creats positions_to_check list based on idx position.
		#this loop checks the positions to determine if they are a bomb and counts how many bombs are located near the original position
		#if no bombs then that adj positon to the orginal clicked gets addes to a different list to be checked later.
		#By using multiple lists this way, the algorithm is created to scan through the board and clears excess spaces.
		for i in self.positions_to_check:

			if self.plist[i] == 'BOMB':
				# print('Bomb located')
				self.bomb_count += 1
				# print("Positions to Check: ", self.positions_to_check)
				# print("Positions Checked: ", self.positions_checked)
				BOMB = True
				

			else:
				# print('CHECK: NO BOMB')
				self.final_list_of_checks.append(i)
				# print('Final List: ', self.final_list_of_checks)
				# print("Positions to Check: ", self.positions_to_check)
				# print("Positions Checked: ", self.positions_checked)

		#If a bomb is located at adj squares then this command resets the transport list and adds the number and color of bombs
		if BOMB:
			self.final_list_of_checks = []

			location = self.gridLayout.getItemPosition(index)
			loc = list(location[0:2])
			item = self.gridLayout.itemAtPosition(loc[0], loc[1])

			if self.bomb_count == 1:
				item.widget().setText('1')
				item.widget().setStyleSheet('color:blue; background-color: #7e7e7e')
			elif self.bomb_count == 2:
				item.widget().setText('2')
				item.widget().setStyleSheet('color:green; background-color: #7e7e7e')
			elif self.bomb_count == 3:
				item.widget().setText('3')
				item.widget().setStyleSheet('color:red; background-color: #7e7e7e')
			elif self.bomb_count == 4:
				item.widget().setText('4')
				item.widget().setStyleSheet('color:dark-blue; background-color: #7e7e7e')
			elif self.bomb_count == 5:
				item.widget().setText('5')
				item.widget().setStyleSheet('color:dark-red; background-color: #7e7e7e')
			elif self.bomb_count == 6:
				item.widget().setText('6')
				item.widget().setStyleSheet('color:light-blue; background-color: #7e7e7e')

			self.bomb_count = 0	
			BOMB = False

		self.remove_excess_spaces()

	def determining_nearby_idxs(self, idx):
		#determines the grid positions of surrounding buttons based on grid position of original button clicked and all following buttons in algorithm

		location = self.gridLayout.getItemPosition(idx)
		loc = list(location[0:2])
		# print('ind: ', idx, ' location: ', location, ' loc: ', loc)


		#I think this is all pretty self explanitory but I know I'll look at it in a week and wonder wtf I did
		#so, loc positoins will determine whether position checked is on the edge, which edge, corner, etc
		#loc returns a list with 2 items in it.  i.e [0,1].  First value is row, second is column.
		#so if the loc[0] = 0 then its in the first row and on an edge.  Adj idx values are calculated depending on what is positioned near
		#added to another transport list and eventaully added to a positions to be checked list.

		if loc[0] == 0:
			
			if loc[1] == 0:
				# print('top left corner')
				self.sqC1 = int(idx) + 1
				self.sqC2 = int(idx) + 9
				self.sqC3 = int(idx) + 10
				self.storage_list = [self.sqC1, self.sqC2, self.sqC3]
				# print(self.sqC1, self.sqC2, self.sqC3)

			elif loc[1] == 8:
				# print('top right corner')
				self.sqC1 = int(idx) - 1
				self.sqC2 = int(idx) + 8
				self.sqC3 = int(idx) + 9
				self.storage_list = [self.sqC1, self.sqC2, self.sqC3]
				# print(self.sqC1, self.sqC2, self.sqC3)

			else:
				# print('top row')
				self.sqE1 = int(idx) - 1
				self.sqE2 = int(idx) + 1
				self.sqE3 = int(idx) + 8
				self.sqE4 = int(idx) + 9
				self.sqE5 = int(idx) + 10
				self.storage_list = [self.sqE1, self.sqE2, self.sqE3, self.sqE4, self.sqE5]
				# print(self.sqE1, self.sqE2, self.sqE3, self.sqE4, self.sqE5)

		elif loc[0] == 8:
			

			if loc[1] == 0:
				# print('BOTTOM LEFT CORNER')
				self.sqC1 = int(idx) - 9
				self.sqC2 = int(idx) - 8
				self.sqC3 = int(idx) + 1
				self.storage_list = [self.sqC1, self.sqC2, self.sqC3]
				# print(self.sqC1, self.sqC2, self.sqC3)

			elif loc[1] == 8:
				# print('BOTTOM RIGHT CORNER')
				self.sqC1 = int(idx) - 10
				self.sqC2 = int(idx) - 9
				self.sqC3 = int(idx) - 1
				self.storage_list = [self.sqC1, self.sqC2, self.sqC3]
				# print(self.sqC1, self.sqC2, self.sqC3)

			else:
				# print('BOTTOM ROW')
				self.sqE1 = int(idx) - 10
				self.sqE2 = int(idx) - 9
				self.sqE3 = int(idx) - 8
				self.sqE4 = int(idx) - 1
				self.sqE5 = int(idx) + 1
				self.storage_list = [self.sqE1, self.sqE2, self.sqE3, self.sqE4, self.sqE5]
				# print(self.sqE1, self.sqE2, self.sqE3, self.sqE4, self.sqE5)

		elif loc[1] == 0:
			# print('FIRST COLUMN')
			self.sqE1 = int(idx) - 9
			self.sqE2 = int(idx) - 8
			self.sqE3 = int(idx) + 1
			self.sqE4 = int(idx) + 9
			self.sqE5 = int(idx) + 10
			self.storage_list = [self.sqE1, self.sqE2, self.sqE3, self.sqE4, self.sqE5]
			# print(self.sqE1, self.sqE2, self.sqE3, self.sqE4, self.sqE5)
			
		elif loc[1] == 8:
			# print('Last Column')
			self.sqE1 = int(idx) - 10
			self.sqE2 = int(idx) - 9
			self.sqE3 = int(idx) - 1
			self.sqE4 = int(idx) + 8 
			self.sqE5 = int(idx) + 9
			self.storage_list = [self.sqE1, self.sqE2, self.sqE3, self.sqE4, self.sqE5]
			# print(self.sqE1, self.sqE2, self.sqE3, self.sqE4, self.sqE5)

		else:
			# print('middle squares')
			self.sqU1 = int(idx) - 10
			self.sqU2 = int(idx) - 9
			self.sqU3 = int(idx) - 8
			self.sqL = int(idx) - 1
			self.sqR = int(idx) + 1
			self.sqL1 = int(idx) + 8
			self.sqL2 = int(idx) + 9
			self.sqL3 = int(idx) + 10

			self.storage_list = [self.sqU1, self.sqU2, self.sqU3, self.sqL, self.sqR, self.sqL1, self.sqL2, self.sqL3]
			# print(self.storage_list)

		for i in range(len(self.storage_list)):

			#this for loop is important.  But i guess all the loops are otherwise this wouldn't run.
			#checks transport list values.  If the same value is in flag positions list or positions already checked then 
			#these values don't leave the transport list.  Don't want to check the same values over and over.  Done that already.

			if self.storage_list[i] in self.flag_positions:
				self.positions_to_check.append(self.storage_list[i])

			elif self.storage_list[i] in self.positions_checked:
				pass
				#maybe I have to remove it from the list
				#game works so not going to play with it

			else:
				self.positions_to_check.append(self.storage_list[i])
		# print('Positions to check: ', self.positions_to_check)

	def remove_excess_spaces(self):
		#runs final transport list through f(idx2loc) which ultimately removes excess spaces.  
		#i guess I should swap the names. 

		for i in self.final_list_of_checks:
			self.idx2loc(i)

			if i not in self.recheck_list:
				self.recheck_list.append(i)
				# print('recheck_list: ', self.recheck_list)

		#reset transport list for next value list transport
		self.final_list_of_checks = []

		#want to only check everyitem on the recheck list once.  So this passes to check the first item and then will
		#remove the first item each time it cycles through.
		if self.first_recheck:
			pass

		else:
			self.recheck_list.pop(0)

		self.recheck()

	def recheck(self):
		#recheck is the final list to be checked.  
		#User clicks a square 
		#program checks nearby idxs generating a list of adj grid positions in storage list.
		#storage list is checked against flag_positions and positions_checked.
		#idx values in storage list but not in either of the checked lists added to positions_to_check
		#idx values in positions_to_check are compared against the game grid, plist to determine if a bomb is located.
		#Remember this isnt the first clicked square being checked but the adjacent squares.
		#Each bomb located is counted and this terminates the adjancent square from algorithm.
		#If not bombs are located in adj squares, then they are added to the transport list, final_list_of_checks
		#They are put into f(idx2loc) (poorly named) which addeds the idx value to positions_checked and removes it from victory_list_indices
		#f(idx2loc) will also disable the button from being pressed again changing the look of the game.
		#transport list, final_list_of_checks then checks if its value is in the recheck list, which is the final list to be checked
		#the recheck list means that no bombs were around this position so it was added to be ran through algorithm again.
		#So, you click, no bombs in adj squares, they go to the recheck list to be run through again as if you clicked them all yourself.

		#resets intermediate transport lists
		self.storage_list = []
		self.positions_to_check = []
		self.first_recheck = False

		if len(self.recheck_list) > 0:

			# print('RECHECK INITIATED')
			for i in self.recheck_list:
				# print('RL: ', self.recheck_list)
				self.check_nearby_squares(i)
				# print('A-RL:', self.recheck_list)

		else:
			#I really don't recall what this does.  Perhaps resets the variable in case of a reset button.  
			#but then I should have just reset it in the reset fxn.
			self.first_recheck = True
			# print('no more squares to recheck')

	def idx2loc(self, index):
		#fxn takes in an index value on button grid, converts it to a location and disables the button
		#adds and removes values from lists. 

		self.positions_checked.append(index)
		self.victory_list_in_indices.remove(index)
		# print('Positions_checked: ', self.positions_checked)
		# print('Length of position checked: ', len(self.positions_checked))
		self.location2 = self.gridLayout.getItemPosition(index)
		self.loc2 = list(self.location2[0:2])
		self.item2 = self.gridLayout.itemAtPosition(self.loc2[0], self.loc2[1])
		self.item2.widget().setEnabled(False)
		self.item2.widget().setStyleSheet('background-color: #282827')

	def set_stylesheet(self):
		#basic css sytle sheet used to set up color of game amoung other things such as button hovering
		#wasn't used much.  Most css actually done within coding in this actual program. 
		#But still used for design of overall GUI
		sheet = open('minesweeper.css')
		sheet_read = sheet.read()
		self.setStyleSheet(sheet_read)
		sheet.close()

def main():

	#basic nonsense necessary to run this file.  
	app = QtGui.QApplication(sys.argv)
	start = MainWidget()
	start.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
    main()

'''

Issues

#trying to figure out how to set up loops to set up continuous algorithms to clear buttons.
#have to figure out to remove values from lists and set lists up to stop terminating loop.

		<Done>

#Algorithm seems to be doing well.  have to play more minesweeper to know for sure.

	<Algorithm works well but at times seems to hit the wrong squares or misses some.  Have to check with detail>
		
		<Algorithm fixed.  Problem was with the positions_checked list. list was taking all functions checked when
		 it needed only take the buttons that have been deactivated.  This discrepancy caused positions to be left
		 untouched and others to be cleared when they clearly shouldn't have been.>

	#Runs a little slow but thats expected with all i have it doing.  Adding the number icons
	really slowed it down.  Perhaps find a quicker way to put those icons on there.
	Hopefully getting rid of all the printing to system will speed it up as well.

		<Problem with speed resolved by replacing using pictures with seting the buttons text and color through python fxns>

Things to still do:

Put timer on and get timer to function on first click

	 <Timer function functionally.  Works on reset.  On game loss. Good to go>

Change restart button picture to smiley while playing, sad face when losing, and 
devil face when won.
	
	<Done>

Still have to created the actual algorithm for winning.

	<Done, incorporated a list that records all grid values but bomb positions and then removes them as game goes on>

Have to install 'flag' for right click on squares and hook count of those up to lcd2
		
	<Done, right click functoinality is a bitch>

Future Improvements:

Drop down menu to increase to intermediate, and expert version of game.  Could include quit function.

'''




