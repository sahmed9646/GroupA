import console
from console import coloredText
import copy
## -------------------------------------------------------------------------- ##
## Constant for windows I/O ops
## -------------------------------------------------------------------------- ##



colorCode = [ 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE', 'ORANGE',]
Front_Colors = { 'RED': console.RED, 'GREEN': console.GREEN, 'YELLOW': console.YELLOW,
                       'BLUE': console.BLUE, 'MAGENTA': console.MAGENTA,
                       'CYAN': console.CYAN, 'WHITE': console.WHITE, 'ORANGE':console.ORANGE,
                       }

'''
Class for printing colorful text
'''
class colorPrinter(object):

    def __init__(self):
        pass

    def __call__(self, info, color = 'WHITE', end = ''):
        colored_text = console.coloredText(info, Front_Colors[color])
        print(colored_text, end=end)



colorPrint = colorPrinter()

##--------------------------------------------------------------------------- ##
## Uitility Functions for class Display_RR
##--------------------------------------------------------------------------- ##

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

class RR_displayer_M(object):
    '''
    Parameters:
        score_matri: M by M two-dim lists storing final scores in the competition , M is the number of the players
                     example  score_matri[2][3] = (4,6) i.e 4 : 6 and  score_matri[3][2] must be (6,4)
        Player_num: number of all players including AI
        player_names: name of all players including AI
    '''
    def __init__(self,scores_matri, player_names = None, player_num=8):
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
'''
Class for Display Round-Robin results in a list style
'''

class RR_displayer_L():


    def __init__(self, players):

        self.ranking = players.copy()
        self.round = 0
        self.matchIndex = 0
        self.colorSetting = {player.name: Front_Colors[colorCode[i]] for i, player in enumerate(players)}
        playersSortedByNameLen = sorted(players, key=lambda x:len(x.name), reverse=True)
        self.namesLen = len(playersSortedByNameLen[0].name) + len(playersSortedByNameLen[1].name) + len('-')
        self.scoreLen = 3
        self.blanksAside = 2
        self.blanksBetween = 1
        self.columnLen = self.namesLen + self.blanksAside + self.blanksBetween + self.scoreLen
        self.BlanksBeforeRoundName = (self.columnLen - 7) // 2
        self.BlanksAfterRoundName = self.columnLen - 7 - self.BlanksBeforeRoundName
        self.rows = [['|' for _ in range(5)] for _ in range(2)]
        self.rows[0][0] = ''
        self.rows[1][0] = ''
        self.SpaceBetweenItems = 2 * ' '

    def add_record(self, result, player0, player1):

        if self.matchIndex == 0:
            self.round += 1
            self.rows[self.round//5][0] += ' ' + self.BlanksBeforeRoundName * ' ' + coloredText('Round '+str(self.round), Front_Colors[colorCode[self.round-1]] ) + ' ' * self.BlanksAfterRoundName + ' '

        record = ' ' + coloredText(player0.name, self.colorSetting[player0.name]) + '-' + coloredText(player1.name, self.colorSetting[player1.name]) + ' '
        BlanksToAdd = ' ' * (self.namesLen - len(player0.name) - len(player1.name))
        record += BlanksToAdd

        if result == 1:
            player0.winCount += 1
            player1.loseCount += 1
            record += '1:0'


        elif result == 0:
            player1.winCount += 1
            player0.loseCount += 1
            record += '0:1'

        elif result == 0.5:
            player0.tieCount += 1
            player1.tieCount += 1
            record += '0:0'

        record += ' |'
        self.rows[self.round//5][self.matchIndex+1] += record
        self.matchIndex = (self.matchIndex+1) % 4


    def printRecord(self):
        for text in self.rows[0]:
            print(text)

        if self.round > 4:
            print("")
            for text in self.rows[1]:
                print(text)


    def printRanking(self):
        self.ranking.sort(key=lambda x: (x.score, x.winCount), reverse=True)
        rankPresent = 'Rank' + self.SpaceBetweenItems + 'Name        ' + self.SpaceBetweenItems + 'Win' + self.SpaceBetweenItems + 'Lose' + self.SpaceBetweenItems + 'Tie' + self.SpaceBetweenItems + 'Score\n'
        for i, player in enumerate(self.ranking):
            newLine = ''
            rank = str(i+1)
            newLine += str(i) + (4 - len(rank)) * ' ' + self.SpaceBetweenItems
            newLine += coloredText(player.name, self.colorSetting[player.name]) + (12 - len(player.name)) * ' ' + self.SpaceBetweenItems
            newLine += coloredText(str(player.winCount), 225) + (3 - len(str(player.winCount))) * ' ' + self.SpaceBetweenItems
            newLine += coloredText(str(player.loseCount), 196) + (4 - len(str(player.loseCount))) * ' ' + self.SpaceBetweenItems
            newLine += coloredText(str(player.tieCount), 190) + (3 - len(str(player.tieCount))) * ' ' + self.SpaceBetweenItems
            newLine += coloredText(str(player.score), 99) + (5 - len(str(player.score))) * ' ' + '\n'
            rankPresent += newLine
        print(rankPresent)



## -------------------------------------------------------------------------- ##
##    Utility Function for KO_displayer
## -------------------------------------------------------------------------- ##
def choose_first(elem):

    return elem[0]


## -------------------------------------------------------------------------- ##
##    KO_displayer class
## -------------------------------------------------------------------------- ##

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
    def __init__(self, firstBracket, sx=0, sy=0, hlength = 15, vlength=5, interval=3, name_blank = 2, line_colors = [0,1,2]):
        self.cx = 0
        self.cy = 0
        self.sx = sx
        self.sy = sy
        self.hlength = hlength
        self.vlength = vlength
        self.interval = interval
        self.name_blank = name_blank
        self.line_colors = line_colors
        self.Brackets = firstBracket
        self.stage = 0
        self.plot_pos = {}
        self._buildTracker()
        self._draw_diagram()

    def _buildTracker(self):

        self.playerList = []
        for i in range(4):
            player0 = self.Brackets[i].player0.name
            player1 = self.Brackets[i].player1.name
            self.playerList.append(player0)
            self.playerList.append(player1)

    def _draw_hline(self, y, x1, x2, char='-', color=0):

        if y in self.plot_pos.keys():
            self.plot_pos[y].append((x1, x2, char, color, 0))

        else:
            self.plot_pos[y] = []
            self.plot_pos[y].append((x1, x2, char, color, 0))


    def _draw_vline(self, x, y1, y2, char='|', color=0):

        for y in range(y1, y2):

            if y in self.plot_pos.keys():
                self.plot_pos[y].append((x, x+1, char, color, 0))

            else:
                self.plot_pos[y] = []
                self.plot_pos[y].append((x, x+1, char, color, 0))

    def _draw_name(self, sx, sy, playername, color):

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
        #Back to  default
        self.cx = 0
        self.cy = 0

    def add_bracket(self, brackets):

        self.stage += 1
        self.Brackets = brackets
        self._draw_diagram()

    def add_winner(self, winner):

        self.stage += 1
        self.winner = winner
        self._draw_diagram()

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

    def _draw_diagram(self):

        hlength = self.hlength
        vlength = self.vlength
        name_blank = self.name_blank
        colors = self.line_colors
        interval = self.interval

        #Draw 4 brackets in round 1
        if self.stage == 0:
            self.y_r2 = []
            self.y_r3 = []

            for i in range(4):

                playername0 = self.Brackets[i].player0.name
                playername1 = self.Brackets[i].player1.name
                color_player0 = self.playerList.index(playername0)
                color_player1 = self.playerList.index(playername1)

                self._draw_hline(self.sy, self.sx, self.sx + hlength, color=colors[0])
                self._draw_name(self.sx+hlength + name_blank, self.sy, playername0, color=color_player0)
                self._draw_name(self.sx + hlength + name_blank, self.sy + vlength - 1, playername1, color=color_player1)
                self._draw_vline(self.sx + hlength - 1, self.sy+1, self.sy + vlength -1, color=colors[0])
                self._draw_hline(self.sy + vlength -1, self.sx, self.sx + hlength, color=colors[0])
                self._draw_hline(self.sy + vlength//2, self.sx + hlength, self.sx + 2*hlength, color=colors[1])
                self.y_r2.append(self.sy + vlength//2)
                self.sy = self.sy + vlength + interval

        # If in round 2 draw 2 more brackets
        elif self.stage == 1:

            self.sx = self.sx + 2*hlength - 1

            for i in range(2):

                playername0 = self.Brackets[i].player0.name
                playername1 = self.Brackets[i].player1.name
                color_player0 = self.playerList.index(playername0)
                color_player1 = self.playerList.index(playername1)

                y0 = self.y_r2[i*2]
                y1 = self.y_r2[i*2+1]
                self.y_r3.append((y0 + y1)//2)
                self._draw_name(self.sx + name_blank + 1, y0, playername0, color = color_player0)
                self._draw_name(self.sx + name_blank + 1, y1, playername1, color= color_player1)
                self._draw_vline(self.sx, y0+1, y1, color=colors[1])
                self._draw_hline(self.y_r3[-1], self.sx+1, self.sx + 1 + hlength, color=colors[2])

        # If in final round draw one more brackets

        elif self.stage == 2:

            playername0 = self.Brackets.player0.name
            playername1 = self.Brackets.player1.name
            color_player0 = self.playerList.index(playername0)
            color_player1 = self.playerList.index(playername1)

            self.sx = self.sx + hlength
            y0 = self.y_r3[0]
            y1 = self.y_r3[1]
            self.sy = (y0 + y1) // 2
            self._draw_name(self.sx + name_blank + 1, y0, playername0, color=color_player0)
            self._draw_name(self.sx + name_blank + 1, y1, playername1, color=color_player1)
            self._draw_vline(self.sx, y0+1, y1, color=colors[2])
            self._draw_hline(self.sy, self.sx+1, self.sx + 1 + hlength, color=colors[2])

        # Draw winner's name
        elif self.stage == 3:

            winner_color = self.playerList.index(self.winner.name)
            self.sx = self.sx + hlength + 1
            self._draw_name(self.sx + name_blank, self.sy, self.winner.name, color= winner_color)