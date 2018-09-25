import random
import os, sys, ctypes

##-------Constant for windows I/O ops--------##
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

if os.name == 'posix':
    colorCode = [ 'RED', 'GREEN', 'YELLOW', 'BLUE', 'PURPEL', 'DARK_GREEN', 'WHITE', 'BLACK',]
else:
    colorCode = ['RED', 'GREEN', 'YELLOW', 'BLUE', 'PINK', 'SKYBLUE', 'WHITE', 'GREY', ]

'''
Temporary Class Definition for Test. Should be imported when hooked up with tournament
'''

class BracketKO:
    def __init__(self, player0, player1):
        self.player0 = player0
        self.player1 = player1
        self.result = -1

    def setResult(self, result):
        self.result = result
'''
Class for printing colorful text
'''
class colorPrinter(object):

    def __init__(self):
        self.Front_Colors = { 'RED': '\033[31m', 'GREEN': '\033[32m', 'YELLOW': '\033[33m',
                       'BLUE': '\033[34m', 'PURPEL': '\033[35m',
                       'DARK_GREEN': '\033[36m', 'WHITE': '\033[37m','BLACK': '\033[30m',
                       }

        self.Front_Colors_win = {'RED': 0x0c, 'GREEN': 0x0a, 'YELLOW': 0x0e,
                       'BLUE': 0x09 , 'PINK': 0x0d,
                       'SKYBLUE': 0x0b, 'WHITE': 0x0f, 'GREY': 0x08}

        self.Endc = '\033[0m'

        if os.name == 'nt':
            self.std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    if os.name == 'posix':
        def __call__(self, info, color = 'WHITE', end = ''):
            printStr = self.Front_Colors[color] + info + self.Endc
            print(printStr, end=end)

    else:
        def __call__(self, info, color = 'WHITE', end = ''):
            ctypes.windll.kernel32.SetConsoleTextAttribute(self.std_out_handle, self.Front_Colors_win[color])
            info = info + end
            sys.stdout.write(info)
            sys.stdout.flush()
            ctypes.windll.kernel32.SetConsoleTextAttribute(self.std_out_handle, self.Front_Colors_win['WHITE'])



colorPrint = colorPrinter()

##-----------------------------------------------------------------------------##
## Uitility Functions for class Display_RR
##-----------------------------------------------------------------------------##

def display_score(score_tuple, player_m_index, player_n_index):
    if isinstance(score_tuple, tuple):
        score_m = str(score_tuple[0])
        score_n = str(score_tuple[1])
        colorPrint(score_m , color = colorCode[player_m_index])
        print(':', end = '')
        colorPrint(score_n, color = colorCode[player_n_index])

    else:
        print('-',end = '')

def score_len(score_tuple, blank_betw_scores = 0):
    if isinstance(score_tuple, tuple):
        score_m = str(score_tuple[0])
        score_n = str(score_tuple[1])
        score_length = len(score_m)+len(score_n) + 1 +  blank_betw_scores * 2
    else:
        score_length = 1
    return score_length

def max_score_lens(score_matri, size):
    max_lens = []
    score_lens = [[0 for _ in range(size)] for _ in range(size)]
    for col in range(size):
        max_len_in_col = 0
        for row in range(size):
            length = score_len(score_matri[row][col])
            score_lens[row][col] = length
            if length > max_len_in_col:
                max_len_in_col = length
        max_lens.append(max_len_in_col)
    return max_lens, score_lens

'''
Class for Printing Table in RR mode
'''

class display_RR(object):
    '''
    Parameters:
        score_matri: M by M two-dim lists storing final scores in the competition , M is the number of the players
                     example  score_matri[2][3] = (4,6) i.e 4 : 6 and  score_matri[3][2] must be (6,4)
        Player_num: number of all players including AI
        player_names: name of all players including AI
    '''
    def __init__(self,scores_matri, player_num, player_names = None):
        self.player_num = player_num
        self.scores = scores_matri
        if player_names == None:
            self.player_names = ['player'+str(i) for i in range(player_num)]
        else:
            self.player_names = player_names

    def show(self):
        # Decide the  widths for each column
        interval = 2
        name_lengths = [len(name) for name in self.player_names]
        first_col_width = max(name_lengths) + interval
        score_max_lens, score_lens = max_score_lens(self.scores, self.player_num)
        max_lens =  [max(name_len , score_len) for name_len, score_len in zip(name_lengths, score_max_lens)]
        table_widths = [l + interval for l in max_lens]


        #print first line (Player Names)
        print(first_col_width * ' ', end='')

        for i in range(self.player_num):
            colorPrint(self.player_names[i], color = colorCode[i])
            pad_len = table_widths[i] - name_lengths[i]
            print(' ' * pad_len, end = '')

        #Print  All Scores
        for r in range(self.player_num):

            print('')
            #Print Name

            colorPrint(self.player_names[r], color = colorCode[r])
            pad_len = first_col_width - name_lengths[r]
            print(' ' * pad_len, end='')

            #Print result scores in the competition with other people
            for c in range(self.player_num):
                display_score(self.scores[r][c], r, c)
                pad_len = table_widths[c] - score_lens[r][c]
                print(' ' * pad_len, end='')

#Test Code for RR results display

if __name__ == '__main__':

    players = ['Yilun Wu', 'Genius', 'Idiot', 'Batman', 'No_one_beats_me', 'Oooops']
    players_n = len(players)
    score_m = [[0 for _ in range(players_n)] for _ in range(players_n)]

    # Randomly generate scores
    for ri in range(players_n):
        for ci in range(ri, players_n):
            type = random.randint(0, 1)
            if type:
                score_m[ri][ci] = (random.randint(0, 10), random.randint(0, 10))
                score_m[ci][ri] = (score_m[ri][ci][1], score_m[ri][ci][0])
    displayer_R = display_RR(score_m, 6, players)
    displayer_R.show()

##-------------------------------------------------------------##
##    Utility Function for KO_displayer
##-------------------------------------------------------------##
def choose_first(elem):

    return elem[0]


##-------------------------------------------------------------##
##    KO_displayer class
##-------------------------------------------------------------##

'''
Class for Displaying KO Bracket view on terminal implemented from scratch

Use 4/5-tuple (Start_X, End_X/Name, (Character),  Color, Type(0/1) ) to represent info(Lines, names) to print on the terminal

If Type = 0 (Not a Name) Then Tuple = (Start_X, End_X, Character,  Color, 0 ) , Line = [ Start_X , End_X )
Else Tuple = Tuple = (Start_X, Name, Color, 1) 

Use a dictionary indexed by  Y Coordinate Value to store all the  information for plotting
Dic[Y] = [ info_tuple_1, info_tuple_2,.... ]

'''

class KO_displayer():
    '''
    Parameters:
        Bracket_KO: list of Bracket_KO_Round_X list
        Usage: [Brackets_R0, ..., ], Brackets_RX is a list of Brackets in a round
    '''
    def __init__(self, Brackets_KO = [], winner = None):
        self.cx = 0
        self.cy = 0
        self.Brackets = Brackets_KO
        self.winner = winner
        self.plot_pos = {}

    def draw_hline(self, y, x1, x2, char='-', color=0):

        if y in self.plot_pos.keys():
            self.plot_pos[y].append((x1, x2, char, color, 0))

        else:
            self.plot_pos[y] = []
            self.plot_pos[y].append((x1, x2, char, color, 0))


    def draw_vline(self, x, y1, y2, char='|', color=0):

        for y in range(y1, y2):

            if y in self.plot_pos.keys():
                self.plot_pos[y].append((x, x+1, char, color, 0))

            else:
                self.plot_pos[y] = []
                self.plot_pos[y].append((x, x+1, char, color, 0))

    def draw_name(self, sx, sy, playername, color):

        if sy in self.plot_pos.keys():
            self.plot_pos[sy].append((sx, playername, color,  1))

        else:
            self.plot_pos[sy] = []
            self.plot_pos[sy].append((sx, playername, color,  1))

    '''
    Print out the Diagram after draw_diagram is runned
    '''
    def show(self):

        plot_pos = self.plot_pos

        for y in sorted(list(plot_pos.keys())):
            plot_pos[y].sort(key = choose_first)

            for plot_info in plot_pos[y]:

                while self.cy != y:
                    print('')
                    self.cy += 1

                if plot_info[-1] == 0: #If it's not a name

                    x1, x2, char, color = plot_info[:4]

                    if self.cx > x1:
                        print(y, plot_info)
                        raise Exception("Error in ploting lines")


                    print(' ' * (x1 - self.cx), end='')

                    if  x2 - x1 > 1:
                        colorPrint(char * (x2 - x1 - 1), color=colorCode[color])
                        colorPrint('+', color=colorCode[color])

                    else:
                        colorPrint(char * (x2 - x1), color=colorCode[color])

                    self.cx = x2

                else:

                    sx, name, color = plot_info[:3]

                    if self.cx > sx:
                        raise Exception("Error in ploting lines")

                    print(' ' * (sx - self.cx), end='')

                    colorPrint(name, color=colorCode[color])

                    self.cx = sx + len(name)

            self.cx = 0
            self.cy += 1
            print("")
    '''
    Plan the layout of the diagram
    Parameter:
            sx : x coordinate of the start position of the diagram
            sy : y coordinate of the start position of the diagram
            hlength : length of all the horizontal line in the diagram
            vlength : length of all the vertical line in the diagram
            interval : length of all the interval between brackets in the first round
            name_blank: number of blanks between the '+' and the showing name
            color: color codes for the three rounds
    '''
    def draw_diagram(self, sx, sy, hlength = 15, vlength=5, interval=3, name_blank = 2, colors = [0,1,2]):

        rounds_done = len(self.Brackets) - 1

        #Draw 4 brackets in round 1
        y_r2 = []
        y_r3 = []
        for i in range(4):


            playername0 = self.Brackets[0][i].player0

            playername1 = self.Brackets[0][i].player1

            self.draw_hline(sy, sx, sx + hlength, color=colors[0])
            self.draw_name(sx+hlength + name_blank, sy, playername0, color=2*i)
            self.draw_name(sx + hlength + name_blank, sy + vlength - 1, playername1, color=(2*i + 1))
            self.draw_vline(sx + hlength - 1, sy+1, sy + vlength -1, color=colors[0])
            self.draw_hline(sy + vlength -1, sx, sx + hlength, color=colors[0])
            self.draw_hline(sy + vlength//2, sx + hlength, sx + 2*hlength, color=colors[1])
            y_r2.append(sy + vlength//2)
            sy = sy + vlength + interval

        # If in round 2 draw 2 more brackets
        if rounds_done > 0:

            sx = sx + 2*hlength - 1

            for i in range(2):

                playername0 = self.Brackets[1][i].player0

                playername1 = self.Brackets[1][i].player1

                y0 = y_r2[i*2]
                y1 = y_r2[i*2+1]
                y_r3.append((y0 + y1)//2)
                self.draw_name(sx + name_blank + 1, y0, playername0, color = 2*i)
                self.draw_name(sx + name_blank + 1, y1, playername1, color= (2 * i + 1))
                self.draw_vline(sx, y0+1, y1, color=colors[1])
                self.draw_hline(y_r3[-1], sx+1, sx + 1 + hlength, color=colors[2])

        # If in final round draw one more brackets

        if rounds_done > 1:

            playername0 = self.Brackets[1][0].player0

            playername1 = self.Brackets[1][0].player1
            sx = sx + hlength
            y0 = y_r3[0]
            y1 = y_r3[1]
            sy = (y0 + y1) // 2
            self.draw_name(sx + name_blank + 1, y0, playername0, color=0)
            self.draw_name(sx + name_blank + 1, y1, playername1, color=1)
            self.draw_vline(sx, y0+1, y1, color=colors[2])
            self.draw_hline(sy, sx+1, sx + 1 + hlength, color=colors[2])

        # Draw winner's name
        if self.winner != None:

            sx = sx + hlength + 1
            self.draw_name(sx + name_blank, sy, self.winner, color= 0)


##-------------------------------------------------------------##
##    Test code for KO display
##-------------------------------------------------------------##

if __name__ == '__main__':
    BR0 = []

    for i in range(4):
        bko = BracketKO('Player'+str(2*i), 'Player'+str(2*i+1))
        BR0.append(bko)
    BR1 = []

    for i in range(2):
        bko = BracketKO('Player' + str(4 * i), 'Player' + str(4 * i + 2))
        BR1.append(bko)

    BR2 = []
    bko = BracketKO('Player' + str(0), 'Player' + str(4))
    BR2.append(bko)

    displayer = KO_displayer([BR0, BR1, BR2], winner='Player0')
    displayer.draw_diagram(10,10)
    displayer.show()

