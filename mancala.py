import random
import itertools
import time


class Mancala:
    def __init__(self, copy_obj=None):
        if copy_obj is None:
            self.board = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
            self.max_index = len(self.board[0]) - 1
            self.pot = [0, 0]
            self.move_count = 0
            self.move_count_fine = [0, 0]
            self.current_player = 0
            self.game_over = False
            self.move_history = []
            return

        self.board = copy_obj.board
        self.max_index = copy_obj.max_index
        self.pot = copy_obj.pot
        self.move_count = copy_obj.move_count
        self.move_count_fine = copy_obj.move_count_fine
        self.current_player = copy_obj.current_player
        self.game_over = copy_obj.game_over
        self.move_history = copy_obj.move_history

    def play_move(self, hole_choice: int):
        hole_choice = hole_choice % (self.max_index + 1)

        if self.board[self.current_player][hole_choice] == 0:
            # Ending condition check
            current_player_sum = 0

            for hole in self.board[self.current_player]:
                current_player_sum += hole

            other_player_sum = 0
            other_i = (self.current_player + 1) % 2

            for hole in self.board[other_i]:
                other_player_sum += hole

            if current_player_sum == 0 or other_player_sum == 0:
                if current_player_sum != 0:
                    self.pot[self.current_player] += current_player_sum
                    for i in range(len(self.board[self.current_player])):
                        self.board[self.current_player][i] = 0

                if other_player_sum != 0:
                    self.pot[other_i] += other_player_sum
                    for i in range(len(self.board[other_i])):
                        self.board[other_i][i] = 0

                self.game_over = True
                return

            return False

        if self.current_player == 0:
            self.move_history.append(['P1', hole_choice + 1])
        else:
            self.move_history.append(['P2', hole_choice + 1])

        self.move_count += 1
        self.move_count_fine[self.current_player] += 1
        hand_index = hole_choice + 1
        current_side = self.current_player
        hand = self.board[self.current_player][hole_choice]
        self.board[self.current_player][hole_choice] = 0

        # Distribute beads
        for i in range(0, hand):
            if 0 <= hand_index <= self.max_index:
                self.board[current_side][hand_index] += 1
                hand_index += 1

            elif current_side == self.current_player and hand_index > self.max_index:
                self.pot[current_side] += 1
                hand_index = 0
                current_side = (current_side + 1) % 2

            else:
                hand_index = 0
                current_side = (current_side + 1) % 2
                self.board[current_side][hand_index] += 1
                hand_index += 1

        # Special condition for capture
        if current_side == self.current_player and self.board[current_side][hand_index - 1] == 1:
            other_i = (current_side + 1) % 2
            self.board[current_side][hand_index - 1] = 0
            self.pot[self.current_player] += self.board[other_i][(len(self.board[other_i]) - 1) - (hand_index - 1)] + 1
            self.board[other_i][(len(self.board[other_i]) - 1) - (hand_index - 1)] = 0

        # Ending condition check
        current_player_sum = 0

        for hole in self.board[self.current_player]:
            current_player_sum += hole

        other_player_sum = 0
        other_i = (self.current_player + 1) % 2

        for hole in self.board[other_i]:
            other_player_sum += hole

        if current_player_sum == 0 or other_player_sum == 0:
            if current_player_sum != 0:
                self.pot[self.current_player] += current_player_sum
                for i in range(len(self.board[self.current_player])):
                    self.board[self.current_player][i] = 0

            if other_player_sum != 0:
                self.pot[other_i] += other_player_sum
                for i in range(len(self.board[other_i])):
                    self.board[other_i][i] = 0

            self.game_over = True
            return

        # Check if player gets second turn
        if hand_index != 0 or current_side == self.current_player:
            self.current_player = (self.current_player + 1) % 2

    def print_board(self, player=-1, last_hole=0):
        print(' __________________________________________________________________________')
        if player == 1:
            print('|   P2         6        5        4        3        2        1             |')
        else:
            print('|   P2                                                                    |')
        print('|  _____     _____    _____    _____    _____    _____    _____    _____  |')

        # P2 side
        print('| |     |   |', end='')
        for i in reversed(range(0, self.max_index + 1)):
            if i == 0:
                if self.board[1][i] > 9:
                    print('  %s |  |     | |' % str(self.board[1][i]))
                else:
                    print('  %s  |  |     | |' % str(self.board[1][i]))
                continue
            if self.board[1][i] > 9:
                print('  %s |  |' % str(self.board[1][i]), end='')
            else:
                print('  %s  |  |' % str(self.board[1][i]), end='')

        print('| |     |   |_____|  |_____|  |_____|  |_____|  |_____|  |_____|  |     | |')

        # P2 Mancala and last hole played
        if self.pot[1] > 9:
            temp = '| |  %s |' % self.pot[1]
        else:
            temp = '| |  %s  |' % self.pot[1]
        p2_last_hole = ['                                                   ^     ',
                        '                                          ^              ',
                        '                                 ^                       ',
                        '                        ^                                ',
                        '               ^                                         ',
                        '      ^                                                  ']
        p1_last_hole = ['      v                                                  ',
                        '               v                                         ',
                        '                        v                                ',
                        '                                 v                       ',
                        '                                          v              ',
                        '                                                   v     ']
        for i in range(len(p2_last_hole)):
            p2_last_hole[i] = temp + p2_last_hole[i]
        for i in range(len(p1_last_hole)):
            p1_last_hole[i] = temp + p1_last_hole[i]
        if last_hole < 0:
            print(p2_last_hole[(last_hole * -1) - 1], end='')
        elif last_hole > 0:
            print(p1_last_hole[last_hole - 1], end='')
        else:
            if self.pot[1] > 9:
                print('| |  %s |                                                         ' % self.pot[1], end='')
            else:
                print('| |  %s  |                                                         ' % self.pot[1], end='')

        # P1 mancala
        if self.pot[0] > 9:
            print('|  %s | |' % self.pot[0])
        else:
            print('|  %s  | |' % self.pot[0])

        print('| |     |    _____    _____    _____    _____    _____    _____   |     | |')

        # P1 side
        print('| |     |   |', end='')
        for i in range(0, self.max_index + 1):
            if i == self.max_index:
                if self.board[0][i] > 9:
                    print('  %s |  |     | |' % str(self.board[0][i]))
                else:
                    print('  %s  |  |     | |' % str(self.board[0][i]))
                continue
            if self.board[0][i] > 9:
                print('  %s |  |' % str(self.board[0][i]), end='')
            else:
                print('  %s  |  |' % str(self.board[0][i]), end='')

        print('| |_____|   |_____|  |_____|  |_____|  |_____|  |_____|  |_____|  |_____| |')
        if player == 0:
            print('|              1        2        3        4        5        6        P1   |')
        else:
            print('|                                                                    P1   |')
        print('|_________________________________________________________________________|')


# Returns list of holes which have the highest value for current player using passed value function
# [hole index, move value]
def find_highest_value(game: object, value_func):
    if game is None:
        game = Mancala()

    best_ut = [0, 0]
    possible_moves = []
    secondary = []

    for h in range(0, game.max_index + 1):
        ut = value_func(game, h)
        possible_moves.append([h, ut])
        if ut > best_ut[1]:
            best_ut = [h, ut]

    possible_moves = sorted(possible_moves, key=lambda x: x[1], reverse=True)
    for h in range(1, len(possible_moves)):
        if possible_moves[h][1] == possible_moves[0][1]:
            secondary.append(possible_moves[h])

    if len(secondary) == 0:
        return [best_ut]

    secondary.insert(0, possible_moves[0])
    return secondary


# Value Functions; returns value for hole choice for current player
def offensive_value_function(game: object, hole_choice: int):
    if game is None:
        game = Mancala()

    if game.board[game.current_player][hole_choice] == 0:
        return False

    hole_choice = hole_choice % (game.max_index + 1)
    bead_count = game.board[game.current_player][hole_choice]
    cycle_number = (((game.max_index + 1) * 2) + 1)
    opp_player = (game.current_player + 1) % 2
    final_index = (hole_choice + bead_count) % cycle_number
    full_passes = int((bead_count - 1) / cycle_number)
    utility = 0

    # If move results in 2nd turn
    if (game.max_index + 1) - hole_choice == bead_count % cycle_number:
        utility += 1.5

    # Number of beads landing in pot
    if (game.max_index + 1) - hole_choice <= bead_count:
        utility += (1 + int(bead_count / cycle_number))

    # If move captures opposing beads
    if full_passes == 0 and 0 <= final_index <= game.max_index:
        if final_index == hole_choice or game.board[game.current_player][final_index] == 0:
            utility += (game.board[opp_player][game.max_index - final_index]) * 2

    return utility


def offensive_value_function2(game: object, hole_choice: int):
    if game is None:
        game = Mancala()

    if game.board[game.current_player][hole_choice] == 0:
        return False

    hole_choice = hole_choice % (game.max_index + 1)
    bead_count = game.board[game.current_player][hole_choice]
    cycle_number = (((game.max_index + 1) * 2) + 1)
    opp_player = (game.current_player + 1) % 2
    final_index = (hole_choice + bead_count) % cycle_number
    full_passes = int((bead_count - 1) / cycle_number)
    utility = 0

    # If move results in 2nd turn
    if (game.max_index + 1) - hole_choice == bead_count % cycle_number:
        utility += 1.5

        # If move results in 3rd turn
        new_game = Mancala(game)
        new_game.play_move(hole_choice)
        for i in range(new_game.max_index + 1):
            if (new_game.max_index + 1) - i == new_game.board[new_game.current_player][i] % cycle_number:
                utility += 1.5
                break

    # Number of beads landing in pot
    if (game.max_index + 1) - hole_choice <= bead_count:
        utility += (1 + int(bead_count / cycle_number))

    # If move captures opposing beads
    if full_passes == 0 and 0 <= final_index <= game.max_index:
        if final_index == hole_choice or game.board[game.current_player][final_index] == 0:
            utility += (game.board[opp_player][game.max_index - final_index]) * 2

    return utility


def defensive_value_function(game: object, hole_choice: int):
    if game is None:
        game = Mancala()

    if game.board[game.current_player][hole_choice] == 0:
        return False

    hole_choice = hole_choice % (game.max_index + 1)
    bead_count = game.board[game.current_player][hole_choice]
    cycle_number = (((game.max_index + 1) * 2) + 1)
    opp_player = (game.current_player + 1) % 2
    final_index = (hole_choice + bead_count) % cycle_number
    full_passes = int((bead_count - 1) / cycle_number)
    utility = 0

    # If move results in 2nd turn
    if (game.max_index + 1) - hole_choice == bead_count % cycle_number:
        utility += 10

    # Number of beads landing in pot
    if (game.max_index + 1) - hole_choice <= bead_count:
        utility += (1 + int(bead_count / cycle_number))

    # If move ends on opposing players side
    if final_index >= 7:
        new_index = final_index - (game.max_index + 2)
        for i in reversed(range(0, new_index)):
            # If move blocks opposing player from potential capture
            if game.board[opp_player][new_index] == 0:
                utility += game.board[game.current_player][game.max_index - (new_index - i)]

    # If opposing player has any empty holes
    for i in range(0, game.max_index):
        if game.board[opp_player][i] == 0 and (game.max_index - i) == hole_choice:
            utility += 20

    # If move captures opposing beads
    if full_passes == 0 and 0 <= final_index <= game.max_index:
        if final_index == hole_choice or game.board[game.current_player][final_index] == 0:
            utility += 3

    return utility


def second_turn_value_function(game: object, hole_choice: int):
    if game is None:
        game = Mancala()
    if game.board[game.current_player][hole_choice] == 0:
        return False

    hole_choice = hole_choice % (game.max_index + 1)
    bead_count = game.board[game.current_player][hole_choice]
    cycle_number = (((game.max_index + 1) * 2) + 1)
    # opp_player = (game_.current_player + 1) % 2
    final_index = (hole_choice + bead_count) % cycle_number
    full_passes = int((bead_count - 1) / cycle_number)
    utility = 0

    # If move results in 2nd turn
    if (game.max_index + 1) - hole_choice == bead_count % cycle_number:
        utility += 10

    # Number of beads landing in pot
    if (game.max_index + 1) - hole_choice <= bead_count:
        utility += (1 + int(bead_count / cycle_number))

    # If move captures opposing beads
    if full_passes == 0 and 0 <= final_index <= game.max_index:
        if final_index == hole_choice or game.board[game.current_player][final_index] == 0:
            utility += 2

    return utility


# Strategies; These functions play a move for current player
def first_hole_strategy(game: object, give_name=False):
    if give_name:
        return 'first hole'
    if game is None:
        game = Mancala()

    no_move_available = True
    for i in range(len(game.board[game.current_player])):
        if game.board[game.current_player][i] != 0:
            game.play_move(i)
            return

    if no_move_available:
        game.current_player = (game.current_player + 1) % 2


def last_hole_strategy(game: object, give_name=False):
    if give_name:
        return 'last hole'
    if game is None:
        game = Mancala()

    no_move_available = True
    for i in reversed(range(len(game.board[game.current_player]))):
        if game.board[game.current_player][i] != 0:
            game.play_move(i)
            return

    if no_move_available:
        game.current_player = (game.current_player + 1) % 2


def random_hole_strategy(game: object, give_name=False):
    if give_name:
        return 'random hole'
    if game is None:
        game = Mancala()

    random_hole = random.randint(0, game.max_index)

    if game.board[game.current_player][random_hole] == 0:
        random_hole_strategy(game)
        return

    game.play_move(random_hole)


def heaviest_hole_strategy(game: object, prefer_closest=True, give_name=False):
    if give_name:
        return 'heaviest hole'
    if game is None:
        game = Mancala()

    if prefer_closest:
        heaviest = game.max_index
        for h in reversed(range(0, game.max_index + 1)):
            if game.board[game.current_player][h] > game.board[game.current_player][heaviest]:
                heaviest = h

        game.play_move(heaviest)
        return

    heaviest = 0
    for h in range(0, game.max_index + 1):
        if game.board[game.current_player][h] > game.board[game.current_player][heaviest]:
            heaviest = h

    game.play_move(heaviest)


def lightest_hole_strategy(game: object, prefer_closest=True, give_name=False):
    if give_name:
        return 'lightest hole'
    if game is None:
        game = Mancala()

    if prefer_closest:
        lightest = None
        for l in reversed(range(0, game.max_index + 1)):
            if game.board[game.current_player][l] == 0:
                continue
            if lightest is None:
                lightest = l
            elif game.board[game.current_player][l] < game.board[game.current_player][lightest]:
                lightest = l

        game.play_move(lightest)
        return

    lightest = None
    for l in range(0, game.max_index + 1):
        if game.board[game.current_player][l] == 0:
            continue
        if lightest is None:
            lightest = l
        elif game.board[game.current_player][l] < game.board[game.current_player][lightest]:
            lightest = l

    game.play_move(lightest)


def offensive_strategy(game: object, give_name=False):
    if give_name:
        return 'offensive'
    if game is None:
        game = Mancala()

    best_moves = find_highest_value(game, offensive_value_function)

    if best_moves[0][1] == 0:
        random_hole_strategy(game)
    elif len(best_moves) == 1:
        game.play_move(best_moves[0][0])
    else:
        ran = random.randint(0, len(best_moves) - 1)
        game.play_move((best_moves[ran][0]))


def offensive2_strategy(game: object, give_name=False):
    if give_name:
        return 'offensive2'
    if game is None:
        game = Mancala()

    best_moves = find_highest_value(game, offensive_value_function2)

    if best_moves[0][1] == 0:
        random_hole_strategy(game)
    elif len(best_moves) == 1:
        game.play_move(best_moves[0][0])
    else:
        ran = random.randint(0, len(best_moves) - 1)
        game.play_move((best_moves[ran][0]))


def defensive_strategy(game: object, give_name=False):
    if give_name:
        return 'defensive'
    if game is None:
        game = Mancala()

    best_moves = find_highest_value(game, defensive_value_function)

    if best_moves[0][1] == 0:
        random_hole_strategy(game)
    elif len(best_moves) == 1:
        game.play_move(best_moves[0][0])
    else:
        ran = random.randint(0, len(best_moves) - 1)
        game.play_move((best_moves[ran][0]))


def second_turn_strategy(game: object, give_name=False):
    if give_name:
        return 'prefer second turn'
    if game is None:
        game = Mancala()

    best_moves = find_highest_value(game, second_turn_value_function)

    if best_moves[0][1] == 0:
        random_hole_strategy(game)
    elif len(best_moves) == 1:
        game.play_move(best_moves[0][0])
    else:
        ran = random.randint(0, len(best_moves) - 1)
        game.play_move((best_moves[ran][0]))


# Simulation function; Simulates [depth] number of games with player 1 using Strat1
def simulate_games(depth: int, strat1=None, strat2=None, show_progress=True, print_result=True):
    # Keep empty list at end of list; 0: current percentage complete, 1: time when last tenth percentage was reached
    # 2: current time, 3: current estimated completion time based on last tenth percentage increase
    book_of_time = [0.0, 0.0, 0.0, 0.0, []]
    book_length = 100
    avg_sum = 0
    avg_est_time = 0
    game_lengths = []
    game_histories = []
    deterministic = False
    det_check = True

    if strat1 is None or strat2 is None:
        return False

    game = Mancala()
    strategy = strat1(game, give_name=True) + ' vs ' + strat2(game, give_name=True)
    score_count = [0, 0]
    longest_game = None
    shortest_game = None
    win_count = [0, 0, 0]
    counter = 0
    book_of_time[1] = time.time()

    while True:
        # Strat vs Strat
        while not game.game_over:
            if game.current_player == 0:
                strat1(game)
            else:
                strat2(game)

        # Tally score
        score_count[0] += game.pot[0]
        score_count[1] += game.pot[1]

        if game.pot[0] > game.pot[1]:
            win_count[0] += 1
        elif game.pot[1] > game.pot[0]:
            win_count[1] += 1
        else:
            win_count[2] += 1

        # Start new game
        if longest_game is None or len(game.move_history) > len(longest_game.move_history):
            longest_game = Mancala(game)

        if shortest_game is None or len(game.move_history) < len(shortest_game.move_history):
            shortest_game = Mancala(game)

        game_lengths.append(len(game.move_history))

        if det_check:
            game_histories.append(game.move_history)
        game.__init__()
        counter += 1

        if show_progress:
            book_of_time[2] = time.time()
            if (int((counter / depth) * 10000) / 100) != book_of_time[0]:
                book_of_time[0] = int((counter / depth) * 10000) / 100
                book_of_time[3] = ((book_of_time[2] - book_of_time[1]) * ((100 - book_of_time[0]) * 100)) / 60
                book_of_time[3] = int(book_of_time[3] * 100) / 100
                book_of_time[1] = time.time()

                if len(book_of_time[-1]) < book_length:
                    book_of_time[-1].append(book_of_time[3])
                    avg_sum = 0
                    for i in range(0, len(book_of_time[-1])):
                        avg_sum += book_of_time[-1][i]
                    avg_est_time = int(avg_sum / len(book_of_time[-1]) * 100) / 100
                else:
                    avg_sum -= book_of_time[-1][0]
                    avg_sum += book_of_time[3]
                    book_of_time[-1].pop(0)
                    book_of_time[-1].append(book_of_time[3])
                    avg_est_time = int(avg_sum / len(book_of_time[-1]) * 100) / 100

            print('\r' + str(counter) + ' of ' + str(depth) + ' :: ' + str(book_of_time[0]) + '%',
                  end='')

            print(' :: %s :: Estimated time remaining: %s minutes' % (strategy, avg_est_time), end='')

        # Check if games play out deterministically
        if counter == 69:
            deterministic = True
            for history in game_histories:
                for history2 in game_histories:
                    if history != history2:
                        deterministic = False
                        det_check = False
                        game_histories = []
                        break

        if counter != depth and not deterministic:
            continue

        print('', end='')
        score_norm = [score_count[0], score_count[1]]

        if score_norm[0] >= score_norm[1] != 0:
            score_norm[0] = int((score_norm[0] / score_norm[1]) * 10000)
            score_norm[0] /= 10000
            score_norm[1] = 1.0
        elif score_norm[0] != 0:
            score_norm[1] = int((score_norm[1] / score_norm[0]) * 10000)
            score_norm[1] /= 10000
            score_norm[0] = 1.0

        win_ratio = [win_count[0], win_count[1]]

        if win_ratio[0] >= win_ratio[1] != 0:
            win_ratio[0] = int((win_ratio[0] / win_ratio[1]) * 10000)
            win_ratio[0] /= 10000
            win_ratio[1] = 1.0

        elif win_ratio[0] != 0:
            win_ratio[1] = int((win_ratio[1] / win_ratio[0]) * 10000)
            win_ratio[1] /= 10000
            win_ratio[0] = 1.0

        win_percentage = [str(int((win_count[0] / depth) * 10000) / 100) + '%',
                          str(int((win_count[1] / depth) * 10000) / 100) + '%']

        average_game_length = 0
        for i in range(len(game_lengths)):
            average_game_length += game_lengths[i]
        average_game_length /= len(game_lengths)

        if print_result:
            if counter != depth:
                print('\rDETERMINISTIC: Stopped simulation after %s games' % str(counter))
            else:
                print('\r%s games played:' % str(counter))
            print(strategy)
            print('Total Scores: %s / %s [%s to %s]' %
                  (score_count[0], score_count[1], score_norm[0], score_norm[1]))
            if win_ratio[0] != 0 and win_ratio[1] != 0:
                print('Win count: %s / %s [%s to %s] | Tie %s' %
                      (win_count[0], win_count[1], win_ratio[0], win_ratio[1], win_count[2]))
            else:
                print('Win count: %s / %s | Tie %s' % (win_count[0], win_count[1], win_count[2]))
            print('Win Percentage: %s / %s' % (win_percentage[0], win_percentage[1]))
            print('Average game: %s moves' % average_game_length)
            print('Longest game: %s moves' % len(longest_game.move_history))
            print('Shortest game: %s moves' % len(shortest_game.move_history))
            print(shortest_game.move_history)
            print('\n')

        return [score_count, score_norm, win_count, strategy, longest_game, shortest_game, average_game_length]


def human_game(game: object, computer_strat=None, two_player=None):
    if game is None:
        game = Mancala()
    if computer_strat is None:
        computer_strat = random_hole_strategy
    if two_player is None:
        two_player = False

    def human_move(move=-1, player='P1'):
        if move == -1:
            try:
                move = int(input('%s Select hole:\n' % player))
            except ValueError:
                move = 420

            if 1 > move or move > game.max_index + 1:
                if player != 'P1':
                    move = human_move(move, player=player)
                else:
                    move = human_move(move)
            return move

        else:
            try:
                move = int(input('Invalid selection; Select: 1 - %s\n' % (game.max_index + 1)))
            except ValueError:
                move = 420

            if 1 > move or move > game.max_index + 1:
                if player != 'P1':
                    move = human_move(move, player=player)
                else:
                    move = human_move(move)
            return move

    if game.current_player == 0:
        play = human_move() - 1
        game.play_move(play)
        game.print_board(player=game.current_player, last_hole=game.move_history[-1][1])
        print('P1 plays hole %s' % str(play + 1))
        if game.current_player == 0:
            print('Play Again')

    elif two_player:
        play = human_move(player='P2') - 1
        game.play_move(play)
        game.print_board(player=game.current_player, last_hole=(game.move_history[-1][1] * -1))
        print('P2 plays hole %s' % str(play + 1))
        if game.current_player == 1:
            print('Play Again')

    else:
        computer_strat(game)
        game.print_board(player=game.current_player, last_hole=(game.move_history[-1][1] * -1))
        print('P2 plays hole %s' % str(game.move_history[-1][1]))

    if not game.game_over:
        human_game(game, computer_strat=computer_strat, two_player=two_player)
    else:
        game.print_board()
        if game.pot[0] > game.pot[1]:
            print('P1 Wins')
        else:
            print('P2 Wins')


sim_depth = 10000
strategies = [random_hole_strategy, offensive_strategy,
              offensive2_strategy, defensive_strategy, second_turn_strategy, first_hole_strategy,
              last_hole_strategy, heaviest_hole_strategy, lightest_hole_strategy]

# If false: will simulate the first two strategies in above list
sim_all_strat_combos = True

# If true: will override simulation and present human vs computer game with computer using strategy below
human_play = True

# Two Player Game
human_vs_human = False

# Computer strategy
opponent_strat = offensive2_strategy

if not human_play:
    if sim_all_strat_combos:

        # Make list of all combinations of strategies
        all_combinations = []
        for strat in itertools.product(strategies, strategies):
            if strat not in all_combinations:
                all_combinations.append(strat)

        # Simulate games
        for s in all_combinations:
            simulate_games(sim_depth, strat1=s[0], strat2=s[1])

    elif len(strategies) > 1:
        simulate_games(sim_depth, strat1=strategies[0], strat2=strategies[1])

else:
    g = Mancala()
    g.print_board(player=g.current_player)
    human_game(g, computer_strat=opponent_strat, two_player=human_vs_human)
