import random
import itertools


class Mancala:
    def __init__(self):
        self.board = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.max_index = len(self.board[0]) - 1
        self.pot = [0, 0]
        self.move_count = 0
        self.move_count_fine = [0, 0]
        self.hand = 0
        self.current_player = 0
        self.game_over = False
        self.move_history = []

    def ending_condition_check(self):
        current_player_sum = 0

        for hole in self.board[self.current_player]:
            current_player_sum += hole

        other_player_sum = 0

        for hole in self.board[(self.current_player + 1) % 2]:
            other_player_sum += hole

        if current_player_sum != 0 and other_player_sum != 0:
            return

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

    def play_move(self, hole_choice: int):
        hole_choice = hole_choice % (self.max_index + 1)

        if self.board[self.current_player][hole_choice] == 0:
            return False

        self.move_count += 1
        self.move_count_fine[self.current_player] += 1
        hand_index = hole_choice + 1
        current_side = self.current_player
        self.hand = self.board[self.current_player][hole_choice]
        self.board[self.current_player][hole_choice] = 0

        if self.hand == 0:
            return

        # Distribute beads
        while self.hand > 0:
            if 0 <= hand_index <= self.max_index:
                self.board[current_side][hand_index] += 1
                self.hand -= 1
                hand_index += 1

            elif current_side == self.current_player and hand_index > self.max_index:
                self.pot[current_side] += 1
                self.hand -= 1
                hand_index = 0
                current_side = (current_side + 1) % 2

            else:
                hand_index = 0
                current_side = (current_side + 1) % 2
                self.board[current_side][hand_index] += 1
                self.hand -= 1
                hand_index += 1

        # Special condition for capture
        if current_side == self.current_player and self.board[current_side][hand_index - 1] == 1:
            other_i = (current_side + 1) % 2
            self.board[current_side][hand_index - 1] = 0
            self.pot[self.current_player] += self.board[other_i][(len(self.board[other_i]) - 1) - (hand_index - 1)] + 1
            self.board[other_i][(len(self.board[other_i]) - 1) - (hand_index - 1)] = 0

        self.ending_condition_check()
        self.move_history.append([self.current_player, hole_choice])

        # Check if player gets second turn
        if hand_index != 0 or current_side == self.current_player:
            self.current_player = (self.current_player + 1) % 2

    def utility_function(self, hole_choice: int):
        if self.board[self.current_player][hole_choice] == 0:
            return False

        hole_choice = hole_choice % (self.max_index + 1)
        bead_count = self.board[self.current_player][hole_choice]
        cycle_number = (((self.max_index + 1) * 2) + 1)
        opp_player = (self.current_player + 1) % 2
        final_index = (hole_choice + bead_count) % cycle_number
        full_passes = int((bead_count - 1) / cycle_number)
        utility = 0

        # If move results in 2nd turn
        if (self.max_index + 1) - hole_choice == bead_count % cycle_number:
            utility += 1.5

        # Number of beads landing in pot
        if (self.max_index + 1) - hole_choice <= bead_count:
            utility += (1 + int(bead_count / cycle_number))

        # If move ends on opposing players side
        if final_index >= 7:
            for i in reversed(range(0, final_index - (self.max_index + 1))):
                # If move blocks opposing player from potential 2nd turn
                if ((self.max_index + 1) - i) == self.board[opp_player][i] % cycle_number:
                    utility += 0.5

                # If move gives opposing player a potential 2nd turn
                elif ((self.max_index + 1) - i) == (self.board[opp_player][i] + full_passes + 1) % cycle_number:
                    utility -= 0.5

        # If move captures opposing beads
        if full_passes == 0 and 0 <= final_index <= self.max_index:
            if final_index == hole_choice or self.board[self.current_player][final_index] == 0:
                utility += (self.board[opp_player][self.max_index - final_index]) * 2

        return utility

    def utility_function_alt(self, hole_choice: int):
        if self.board[self.current_player][hole_choice] == 0:
            return False

        hole_choice = hole_choice % (self.max_index + 1)
        bead_count = self.board[self.current_player][hole_choice]
        cycle_number = (((self.max_index + 1) * 2) + 1)
        opp_player = (self.current_player + 1) % 2
        final_index = (hole_choice + bead_count) % cycle_number
        full_passes = int((bead_count - 1) / cycle_number)
        utility = 0

        # If move results in 2nd turn
        if (self.max_index + 1) - hole_choice == bead_count % cycle_number:
            utility += 10

        # Number of beads landing in pot
        if (self.max_index + 1) - hole_choice <= bead_count:
            utility += (1 + int(bead_count / cycle_number))

        # If move ends on opposing players side
        if final_index >= 7:
            for i in reversed(range(0, final_index - (self.max_index + 1))):
                # If move blocks opposing player from potential 2nd turn
                if ((self.max_index + 1) - i) == self.board[opp_player][i] % cycle_number:
                    utility += 0.5

                # If move gives opposing player a potential 2nd turn
                elif ((self.max_index + 1) - i) == (self.board[opp_player][i] + full_passes + 1) % cycle_number:
                    utility -= 0.5

        # If move captures opposing beads
        if full_passes == 0 and 0 <= final_index <= self.max_index:
            if final_index == hole_choice or self.board[self.current_player][final_index] == 0:
                utility += 2

        return utility

    def find_highest_utility(self, func):
        # Returns list of holes which have the highest utility for current player
        # [hole index, utility value]
        best_ut = [0, 0]
        possible_moves = []
        secondary = []

        for h in range(0, self.max_index + 1):
            ut = func(h)
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
        for h in reversed(range(game.max_index + 1)):
            if game.board[game.current_player][h] > game.board[game.current_player][heaviest]:
                heaviest = h

        game.play_move(heaviest)
        return

    heaviest = 0
    for h in range(game.max_index + 1):
        if game.board[game.current_player][h] > game.board[game.current_player][heaviest]:
            heaviest = h

    game.play_move(heaviest)


def utility_strategy(game: object, give_name=False):
    if give_name:
        return 'utility'
    if game is None:
        game = Mancala()

    best_moves = game.find_highest_utility(game.utility_function)

    if best_moves[0][1] == 0:
        random_hole_strategy(game)
    elif len(best_moves) == 1:
        game.play_move(best_moves[0][0])
    else:
        ran = random.randint(0, len(best_moves) - 1)
        game.play_move((best_moves[ran][0]))


def alt_utility_strategy(game: object, give_name=False):
    if give_name:
        return 'alt utility'
    if game is None:
        game = Mancala()

    best_moves = game.find_highest_utility(game.utility_function)

    if best_moves[0][1] == 0:
        random_hole_strategy(game)
    elif len(best_moves) == 1:
        game.play_move(best_moves[0][0])
    else:
        ran = random.randint(0, len(best_moves) - 1)
        game.play_move((best_moves[ran][0]))


# Simulation function; Simulates [depth] number of games with player 1 using Strat1
def simulate_games(depth: int, strat1=None, strat2=None, show_progress=False, print_result=True):
    if strat1 is None or strat2 is None:
        return False

    game = Mancala()
    strategy = ''

    if strat1 is not None and strat2 is not None:
        strat1_name = strat1(game, give_name=True)
        strat2_name = strat2(game, give_name=True)
        strategy = strat1_name + ' vs ' + strat2_name

    score_count = [0, 0]
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
        game.__init__()
        counter += 1

        if show_progress and counter % int(depth / 10) == 0:
            print(str(counter) + ' / ' + str(depth))

        if counter != depth:
            continue

        score_norm = [score_count[0], score_count[1]]

        if score_norm[0] >= score_norm[1]:
            score_norm[0] = int((score_norm[0] / score_norm[1]) * 10000)
            score_norm[0] /= 10000
            score_norm[1] = 1.0
        else:
            score_norm[1] = int((score_norm[1] / score_norm[0]) * 10000)
            score_norm[1] /= 10000
            score_norm[0] = 1.0

        if print_result:
            print(strategy)
            print('Score:', score_count, 'Normalized:', score_norm)
            print('Win Count:', win_count)
            print('\n')

        return [score_count, score_norm, win_count, strategy]


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
                    print('Invalid selection; Select: 1 - %s' % (game.max_index + 1))
                    move = int(input('Select hole:\n'))
                except ValueError:
                    move = 0

                if 1 > move or move > game.max_index + 1:
                    player1_move(move)
                return move

        move_ = player1_move() - 1
        game.play_move(move_)
        print('P1 plays hole %s' % str(move_ + 1), game.board, game.pot)
        if game.current_player == 0:
            print('Play Again')
    else:
        computer_strat(game)
        print('P2 plays hole %s' % str(game.move_history[-1][1] + 1), game.board, game.pot)

    if not game.game_over:
        human_game(game)


sim_depth = 10000
strategies = [random_hole_strategy, heaviest_hole_strategy, utility_strategy, alt_utility_strategy]
sim_all_strategies = False
human_play = True

if not human_play:
    if sim_all_strategies:
        all_combinations = []
        for strat in itertools.product(strategies, strategies):
            all_combinations.append(strat)

        for s in all_combinations:
            simulate_games(sim_depth, strat1=s[0], strat2=s[1])
    else:
        simulate_games(sim_depth, strat1=utility_strategy, strat2=random_hole_strategy, show_progress=True)

g = Mancala()
print('Board Format:')
print('[[P1 Side], [P2 Side]] [P1 Mancala, P2 Mancala]')
print(g.board, g.pot)
human_game(g, utility_strategy)
