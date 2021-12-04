import random
import itertools


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
            return False

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

        for hole in self.board[(self.current_player + 1) % 2]:
            other_player_sum += hole

        if current_player_sum == 0 or other_player_sum == 0:
            if current_player_sum != 0:
                self.pot[self.current_player] += current_player_sum
                for i in range(len(self.board[self.current_player])):
                    self.board[self.current_player][i] = 0

            elif other_player_sum != 0:
                other_i = (self.current_player + 1) % 2
                self.pot[other_i] += other_player_sum
                for i in range(len(self.board[other_i])):
                    self.board[other_i][i] = 0

            self.game_over = True
            return

        self.move_history.append([self.current_player, hole_choice])

        # Check if player gets second turn
        if hand_index != 0 or current_side == self.current_player:
            self.current_player = (self.current_player + 1) % 2

    def print_board(self):
        print(' __________________________________________________________________________')
        print('|   P2                                                                    |')
        print('|  _____     _____    _____    _____    _____    _____    _____    _____  |')

        # Opponent side
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

        print('| |     |   [_____]  [_____]  [_____]  [_____]  [_____]  [_____]  |     | |')

        # Mancala scores
        if self.pot[1] > 9:
            print('| |  %s |                                                         ' % self.pot[1], end='')
        else:
            print('| |  %s  |                                                         ' % self.pot[1], end='')

        # Player mancala
        if self.pot[0] > 9:
            print('|  %s | |' % self.pot[0])
        else:
            print('|  %s  | |' % self.pot[0])

        print('| |     |    _____    _____    _____    _____    _____    _____   |     | |')

        # Player side
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

        print('| |_____|   [_____]  [_____]  [_____]  [_____]  [_____]  [_____]  |_____| |')
        print('|              1        2        3        4        5        6        P1   |')
        print(' __________________________________________________________________________')


# Returns list of holes which have the highest value for current player using passed value function
# [hole index, move value]
def find_highest_value(game: object, func):
    if game is None:
        game = Mancala()

    best_ut = [0, 0]
    possible_moves = []
    secondary = []

    for h in range(0, game.max_index + 1):
        ut = func(game, h)
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
    def offensive_value_function(game_: object, hole_choice: int):
        if game_ is None:
            game_ = Mancala()

        if game_.board[game_.current_player][hole_choice] == 0:
            return False

        hole_choice = hole_choice % (game_.max_index + 1)
        bead_count = game_.board[game_.current_player][hole_choice]
        cycle_number = (((game_.max_index + 1) * 2) + 1)
        opp_player = (game_.current_player + 1) % 2
        final_index = (hole_choice + bead_count) % cycle_number
        full_passes = int((bead_count - 1) / cycle_number)
        utility = 0

        # If move results in 2nd turn
        if (game_.max_index + 1) - hole_choice == bead_count % cycle_number:
            utility += 1.5

        # Number of beads landing in pot
        if (game_.max_index + 1) - hole_choice <= bead_count:
            utility += (1 + int(bead_count / cycle_number))

        # If move captures opposing beads
        if full_passes == 0 and 0 <= final_index <= game_.max_index:
            if final_index == hole_choice or game_.board[game_.current_player][final_index] == 0:
                utility += (game_.board[opp_player][game_.max_index - final_index]) * 2

        return utility

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


def defensive_strategy(game: object, give_name=False):
    def defensive_value_function(game_: object, hole_choice: int):
        if game_ is None:
            game_ = Mancala()

        if game_.board[game_.current_player][hole_choice] == 0:
            return False

        hole_choice = hole_choice % (game_.max_index + 1)
        bead_count = game_.board[game_.current_player][hole_choice]
        cycle_number = (((game_.max_index + 1) * 2) + 1)
        opp_player = (game_.current_player + 1) % 2
        final_index = (hole_choice + bead_count) % cycle_number
        full_passes = int((bead_count - 1) / cycle_number)
        utility = 0

        # If move results in 2nd turn
        if (game_.max_index + 1) - hole_choice == bead_count % cycle_number:
            utility += 10

        # Number of beads landing in pot
        if (game_.max_index + 1) - hole_choice <= bead_count:
            utility += (1 + int(bead_count / cycle_number))

        # If move ends on opposing players side
        if final_index >= 7:
            new_index = final_index - (game_.max_index + 2)
            for i in reversed(range(0, new_index)):
                # If move blocks opposing player from potential capture
                if game_.board[opp_player][new_index] == 0:
                    utility += game_.board[game_.current_player][game_.max_index - (new_index - i)]

        # If opposing player has any empty holes
        for i in range(0, game_.max_index):
            if game_.board[opp_player][i] == 0 and (game_.max_index - i) == hole_choice:
                utility += 20

        # If move captures opposing beads
        if full_passes == 0 and 0 <= final_index <= game_.max_index:
            if final_index == hole_choice or game_.board[game_.current_player][final_index] == 0:
                utility += 3

        return utility

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
    def second_turn_value_function(game_: object, hole_choice: int):
        if game_ is None:
            game_ = Mancala()
        if game_.board[game_.current_player][hole_choice] == 0:
            return False

        hole_choice = hole_choice % (game_.max_index + 1)
        bead_count = game_.board[game_.current_player][hole_choice]
        cycle_number = (((game_.max_index + 1) * 2) + 1)
        # opp_player = (game_.current_player + 1) % 2
        final_index = (hole_choice + bead_count) % cycle_number
        full_passes = int((bead_count - 1) / cycle_number)
        utility = 0

        # If move results in 2nd turn
        if (game_.max_index + 1) - hole_choice == bead_count % cycle_number:
            utility += 10

        # Number of beads landing in pot
        if (game_.max_index + 1) - hole_choice <= bead_count:
            utility += (1 + int(bead_count / cycle_number))

        # If move captures opposing beads
        if full_passes == 0 and 0 <= final_index <= game_.max_index:
            if final_index == hole_choice or game_.board[game_.current_player][final_index] == 0:
                utility += 2

        return utility

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
    if strat1 is None or strat2 is None:
        return False

    game = Mancala()
    strategy = ''

    if strat1 is not None and strat2 is not None:
        strat1_name = strat1(game, give_name=True)
        strat2_name = strat2(game, give_name=True)
        strategy = strat1_name + ' vs ' + strat2_name

    score_count = [0, 0]
    longest_game = None
    shortest_game = None
    win_count = [0, 0, 0]
    counter = 0

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
        if longest_game is None:
            longest_game = Mancala(game)
        elif len(game.move_history) > len(longest_game.move_history):
            longest_game = Mancala(game)

        if shortest_game is None:
            shortest_game = Mancala(game)
        elif len(game.move_history) < len(longest_game.move_history):
            shortest_game = Mancala(game)

        game.__init__()
        counter += 1

        if show_progress:
            print('\r' + str(counter) + ' of ' + str(depth) + ' :: ' + str(int((counter / depth) * 10000) / 100) + '%',
                  end='')
            print(' :: %s' % strategy, end='')

        if counter != depth:
            continue

        print('', end='')
        score_norm = [score_count[0], score_count[1]]

        if score_norm[0] >= score_norm[1]:
            score_norm[0] = int((score_norm[0] / score_norm[1]) * 10000)
            score_norm[0] /= 10000
            score_norm[1] = 1.0
        else:
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

        if print_result:
            print('\r%s games played:' % str(depth))
            print(strategy)
            print('Total Scores: %s / %s [%s to %s]' %
                  (score_count[0], score_count[1], score_norm[0], score_norm[1]))
            if win_ratio[0] != 0 and win_ratio[1] != 0:
                print('Win count: %s / %s [%s to %s] | Tie %s' %
                      (win_count[0], win_count[1], win_ratio[0], win_ratio[1], win_count[2]))
            else:
                print('Win count: %s / %s | Tie %s' % (win_count[0], win_count[1], win_count[2]))
            print('Win Percentage: %s / %s' % (win_percentage[0], win_percentage[1]))
            print('Longest game: %s moves' % len(longest_game.move_history))
            print('Shortest game: %s moves' % len(shortest_game.move_history))
            print('\n')

        return [score_count, score_norm, win_count, strategy, longest_game, shortest_game]


def human_game(game: object, computer_strat=None):
    if game is None:
        game = Mancala()
    if computer_strat is None:
        computer_strat = random_hole_strategy

    if game.current_player == 0:
        def player1_move(move=-1):
            if move == -1:
                try:
                    move = int(input('Select hole:\n'))
                except ValueError:
                    move = 0

                if 1 > move or move > game.max_index + 1:
                    player1_move(move)
                return move

            else:
                try:
                    move = int(input('Invalid selection; Select: 1 - %s\n' % (game.max_index + 1)))
                except ValueError:
                    move = 0

                if 1 > move or move > game.max_index + 1:
                    player1_move(move)
                return move

        move_ = player1_move() - 1
        game.play_move(move_)
        game.print_board()
        print('P1 plays hole %s' % str(move_ + 1))
        if game.current_player == 0:
            print('Play Again')
    else:
        computer_strat(game)
        game.print_board()
        print('P2 plays hole %s' % str(game.move_history[-1][1] + 1))

    if not game.game_over:
        human_game(game)


sim_depth = 1000
strategies = [random_hole_strategy, offensive_strategy, defensive_strategy, second_turn_strategy, first_hole_strategy,
              last_hole_strategy, heaviest_hole_strategy, lightest_hole_strategy]
sim_all_strat_combos = True
human_play = True

if not human_play:
    if sim_all_strat_combos:
        all_combinations = []
        for strat in itertools.product(strategies, strategies):
            if strat not in all_combinations:
                all_combinations.append(strat)

        # Remove deterministic games
        deterministic = [first_hole_strategy, last_hole_strategy, heaviest_hole_strategy, lightest_hole_strategy]
        d = []
        pop_list = []
        for strat in itertools.product(deterministic, deterministic):
            d.append(strat)

        for fight in all_combinations:
            for deez_nuts in d:
                if deez_nuts == fight:
                    pop_list.append(all_combinations.index(fight))

        pop_list.sort(reverse=True)
        for pop_i in pop_list:
            all_combinations.pop(pop_i)

        # Simulate games
        for s in all_combinations:
            simulate_games(sim_depth, strat1=s[0], strat2=s[1])

        # Run small sample of determinist games
        for s in d:
            simulate_games(10, strat1=s[0], strat2=s[1])
    elif len(strategies) != 0:
        simulate_games(sim_depth, strat1=strategies[0], strat2=strategies[1])

else:
    g = Mancala()
    g.print_board()
    human_game(g, offensive_strategy)
