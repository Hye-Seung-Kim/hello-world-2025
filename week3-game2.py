# saw_escape_enhanced.py
# SAW-Style Escape Room with Conditional Probability Puzzle
# Enhanced Puzzle 2 with strategic first-die reveal mechanic

import random
import sys
import time

# Game state tracking
game_state = {
    "player_name": "",
    "attempts_remaining": 3,
    "total_score": 0,
    "puzzles_solved": 0,
    "hints_used": 0,
    "start_time": 0,
    "difficulty": "normal"
}

def display_saw_ascii():
    """Display SAW character ASCII art"""
    print("""
════════════════════════════════════════════════════════════════
    ███████╗ █████╗ ██╗    ██╗    ███████╗███████╗ ██████╗ █████╗ ██████╗ ███████╗
    ██╔════╝██╔══██╗██║    ██║    ██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝
    ███████╗███████║██║ █╗ ██║    █████╗  ███████╗██║     ███████║██████╔╝█████╗  
    ╚════██║██╔══██║██║███╗██║    ██╔══╝  ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝  
    ███████║██║  ██║╚███╔███╔╝    ███████╗███████║╚██████╗██║  ██║██║     ███████╗
    ╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝     ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝
════════════════════════════════════════════════════════════════
....................................................................................................
..............                                                                       .:.............
..............                                                                       :^.............
..............                               .:^^:.                                  :^.............
..............                           :75G#&@@@&BGBBBPY7^.                        :^.............
..............                        :~7P@@@@@@@@@@@@@@@@@@#PJ~:                    :^.............
..............                  .^!JPB&@@@@@@&BBGPPPPGGGBB#&@@@@&GY~.                :^.............
..............              :!YG#@@@@@@@B5?~:.            .:^!JG&@@@#J:              :^.............
..............             .J@@@@@@@@B?^                        :7G@@@&?             :^.............
..............            ^G@@@@@@@P~                              ~G@@@G^           :^.............
..............           :&@@@@@@B!                                  Y@@@&J          :^.............
..............           Y@@@@@@5                                     J@@@@G:        :^.............
..............         .Y@@@@@@J:!?JYYJJ?!~:.              .:~~!777!~^.5@@@@#:       :^.............
..............        7B@@@@@@J^?7~^:..::^!7J?!.        ^?J?!~^^::^^!77:#@@@B:       :^.............
..............       :?G@@@@@B               :!5Y:    ?PY~.             7@@@@!       :^.............
..............       .Y@@@@@@5    :YPP5YYYJ7.   ?B. ^GY:  .!JJJJYP5?^   :&@@@P       :^.............
..............      ~G#@@@@@@G    P@@?^Y5~^B&J~::#! #?.^?P&B~^7!.!@@@~   B@@@&.      :^.............
..............      ^.Y@@@@@@P    J@@7:PG^.B@&J7?7. ?YJ7J@@P !BP ^@@&~   P@@@@?      :^.............
..............       ~@@@@@@@Y:~^: ^JGPYYP#&G^..       ..7B&GJ77YBG?. ...J@@@@#:     :^.............
..............       !J@@@@@BJ?JJJ5?. .^^^:.  B7       Y5  :~!!~^. ^J5J?7Y&@@@5      :^.............
..............         #@@@&Y7?JP5!?#J       :@!       7B        ~B#?~7??JB@@@J      :^.............
..............         5@@@G?Y57:J@?^&5      ~&:       :&^      ^&P.?#Y!7??&@@Y      :^.............
..............         7@B&G7Y?GB:Y@~!@^     YP         P5      GB ?@7^B?7J&@@?      :^.............
..............         :7.J&#PP^@G.&5:@!    ^&^         :#~    :@? &#.#G 5?#@@^      :^.............
..............            ^@@GJYBJ^&??&:  .!#?           !B:   .#5 G#:?GYP#@@Y       :^.............
..............            .^Y@&GPGPY5#J7YP#@@!           ~@&5?~^!GGJJJPG#BJ~7        :^.............
..............              ^G!~75#@P7!G&~^~?GG?:     :75BGP5P@@5?5@&&@@Y.           :^.............
..............                    .5B   !BGGBBGGG5JJYPB@@PJ?JG#7  ~&@@#~             :^.............
..............                      BJ   !@P55YY55PGGPPPPP&@?:.  ~&@@#^              :^.............
..............                      !@^  7&.        ..    J@:   ~&@Y~:               :^.............
..............                       GG  ?&.              7@^  ^&?:                  :^.............
..............                       :#! 7#.              !@^ ^#J .:^.               :^.............
..............                      .:?&PBB               ~@Y5@@B#&@@#^              :^.............
..............                     7#@@@@@#:              7@@@@@@@@@@#:              :^.............
..............                     #@@@@@@@#5J???JYJJ?!~!Y&@@@@@@@@@@~               :^.............
..............                    :&@@@@@@@@@@@@@@&@@@@@@@@@@@@@@@@@?                :^.............
..............                    ~@@@@@@@@@@@#5!..:?B&@@@@@@@@@@@@B                 :^.............
..............                    ~@@@@@@@#P?^.       :~7J5GB#&@@@@J                 :^.............
..............                     7GBGY7^.                  .:^~!!.                 :^.............
..............:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::^:.............
....................................................................................................
""")

def say(line, delay=0.0):
    """SAW-tone dialogue output with optional delay"""
    print(line)
    if delay > 0:
        time.sleep(delay)

def calculate_final_score():
    """Calculate final score using arithmetic operators"""
    base_score = game_state["puzzles_solved"] * 100
    time_bonus = max(0, 300 - int(time.time() - game_state["start_time"]))
    hint_penalty = game_state["hints_used"] * 25
    attempts_bonus = game_state["attempts_remaining"] * 50
    
    final_score = base_score + time_bonus + attempts_bonus - hint_penalty
    return max(0, final_score)

def game_over(reason=""):
    """Enhanced game over routine with scoring"""
    if reason:
        say(f"\n[JIGSAW] {reason}")
    
    final_score = calculate_final_score()
    
    if game_state["puzzles_solved"] == 0:
        say("\n[JIGSAW] You failed before you even began. Pathetic.")
    elif game_state["puzzles_solved"] == 1:
        say("\n[JIGSAW] One puzzle... barely a warm-up. Disappointing.")
    elif game_state["puzzles_solved"] == 2:
        say("\n[JIGSAW] So close, yet so far. The final test proved too much.")
    elif game_state["puzzles_solved"] == 3:
        say("\n[JIGSAW] Three puzzles solved, yet you fell at the final gate.")
    
    say(f"\nGAME OVER")
    say(f"Final Score: {final_score}")
    say(f"Puzzles Solved: {game_state['puzzles_solved']}/4")
    say(f"Hints Used: {game_state['hints_used']}")
    
    replay = input("\nPlay again? (y/n): ").strip().lower()
    if replay == 'y' or replay == 'yes':
        restart_game()
    else:
        sys.exit(0)

def game_clear():
    """Enhanced escape success with scoring"""
    final_score = calculate_final_score()
    elapsed_time = int(time.time() - game_state["start_time"])
    
    say("\n*CLANK* The final lock opens...")
    say("[JIGSAW] Impressive. You've proven your worth today.")
    say("ESCAPE SUCCESSFUL!")
    say(f"\n FINAL RESULTS:")
    say(f"   Player: {game_state['player_name']}")
    say(f"   Score: {final_score}")
    say(f"   Time: {elapsed_time} seconds")
    say(f"   Hints Used: {game_state['hints_used']}")
    
    if final_score >= 400:
        say("   Grade: *** MASTER ESCAPIST ***")
    elif final_score >= 300:
        say("   Grade: ** SKILLED SOLVER **")
    elif final_score >= 200:
        say("   Grade: * DECENT ATTEMPT *")
    else:
        say("   Grade: NEEDS IMPROVEMENT")
    
    replay = input("\n Play again? (y/n): ").strip().lower()
    if replay == 'y' or replay == 'yes':
        restart_game()
    else:
        sys.exit(0)

def get_hint(puzzle_name, hint_text):
    """Hint system with penalty tracking"""
    if game_state["hints_used"] >= 2:
        say("[JIGSAW] You've exhausted your hints. Face the challenge alone.")
        return False
    
    if game_state["difficulty"] == "hard":
        say("[JIGSAW] No hints in hard mode. Survive on your own.")
        return False
    
    choice = input(f"\n Use a hint for {puzzle_name}? (y/n): ").strip().lower()
    if choice == 'y' or choice == 'yes':
        game_state["hints_used"] += 1
        say(f"[JIGSAW] Fine. Here's your hint: {hint_text}")
        say(f" Score penalty: -25 points (Hints used: {game_state['hints_used']}/2)")
        return True
    return False

# ================== PUZZLE 1: Lock Combination ==================
def puzzle1():
    """
    Lock combination puzzle with multiple conditions
    Solution: 645 (6+4+5=15, 645%15==0, 6==5+2, 4%2==0)
    """
    say("\n [PUZZLE 1] THE LOCK OF LOGIC")
    say("[JIGSAW] Your first test. A combination lock holds your fate.")
    say("        Listen carefully to the conditions:")
    say("        • Three digits must sum to exactly 15")
    say("        • The number must be divisible by both 3 and 5")
    say("        • First digit equals last digit plus 2")
    say("        • Middle digit must be odd")
    say("        You have one chance. Choose wisely.")
    
    get_hint("Lock Puzzle", "Think about multiples of 15: 150, 165, 180, 195...")
    
    code = input("\nEnter three-digit code: ").strip()
    
    if not code.isdigit() or len(code) != 3:
        say("[JIGSAW] Format error. Precision matters in life and death.")
        return False
    
    first, middle, last = int(code[0]), int(code[1]), int(code[2])
    digit_sum = first + middle + last
    number = int(code)
    
    condition1 = (digit_sum == 15)
    condition2 = (number % 3 == 0) and (number % 5 == 0)
    condition3 = (first == last + 2)
    condition4 = (middle % 2 == 1)
    
    all_conditions_met = condition1 and condition2 and condition3 and condition4
    
    if all_conditions_met:
        say("*CLICK* The lock opens.")
        say("[JIGSAW] Adequate. Mathematics serves you well.")
        game_state["puzzles_solved"] += 1
        return True
    else:
        say("*BUZZ* Incorrect combination.")
        if not condition1:
            say(f"    Sum was {digit_sum}, needed 15")
        if not condition2:
            say(f"    {number} is not divisible by both 3 and 5")
        if not condition3:
            say(f"    First digit {first} ≠ last digit {last} + 2")
        if not condition4:
            say(f"    Middle digit {middle} is not even")
        return False

# ================== PUZZLE 2: Conditional Probability Dice ==================
def calculate_conditional_probability(die1):
    """Calculate P(sum > 7 | first die = die1)"""
    favorable_cases = 0
    for die2 in range(1, 7):
        if die1 + die2 > 7:
            favorable_cases += 1
    
    probability = (favorable_cases / 6) * 100
    recommendation = "YES" if favorable_cases >= 3 else "NO"
    
    return {
        "probability": round(probability, 1),
        "recommendation": recommendation,
        "favorable_cases": favorable_cases
    }

def puzzle2():
    """
    Enhanced dice puzzle with conditional probability
    First die is revealed, then player predicts based on that information
    """
    say("\n [PUZZLE 2] THE DICE OF DESTINY")
    say("[JIGSAW] Two dice will determine your next step.")
    say("        But this isn't just luck... it's probability.")
    say("        The first die will be revealed to you.")
    say("        You must predict TWO things based on conditional probability:")
    say("        1. Will the sum be ODD or EVEN?")
    say("        2. Will the sum be GREATER than 7?")
    say("        Use the information wisely. Get both predictions right to proceed.")
    
    # Step 1: Reveal first die
    die1 = random.randint(1, 6)
    say(f"\n FIRST DIE REVEALED: {die1}")
    time.sleep(1)
    
    # Calculate and display conditional probability
    prob_data = calculate_conditional_probability(die1)
    
    if game_state["difficulty"] == "easy":
        say(f"\n[JIGSAW] I'll give you the math:")
        say(f"Conditional Probability Analysis:")
        say(f"• P(sum > 7 | die1={die1}) = {prob_data['probability']}%")
        say(f"• P(sum is odd | die1={die1}) = 50%")
        say(f"\nOptimal strategy:")
        say(f"> 7: Choose {prob_data['recommendation']}")
        say(f"Odd/Even: Either choice is 50/50")
    elif game_state["difficulty"] == "normal":
        say(f"\n[JIGSAW] Let me show you the odds:")
        say(f"Conditional Probability:")
        say(f"• P(sum > 7 | die1={die1}) = {prob_data['probability']}%")
        say(f"• P(sum is odd) = 50%")
        say(f"\nChoose wisely. Your life depends on mathematics.")
    else:  # hard mode
        say(f"\n[JIGSAW] The first die shows {die1}.")
        say(f"Calculate the rest yourself.")
        say(f"Your survival depends on your reasoning.")
    
    # Get predictions
    while True:
        odd_even = input("\n🎯 Predict: Will sum be (O)dd or (E)ven? ").strip().upper()
        if odd_even in ['O', 'E', 'ODD', 'EVEN']:
            break
        say("Enter O for Odd or E for Even.")
    
    while True:
        greater_seven = input("Will sum be greater than 7? (Y/N): ").strip().upper()
        if greater_seven in ['Y', 'N', 'YES', 'NO']:
            break
        say("Enter Y for Yes or N for No.")
    
    # Step 2: Roll second die
    say("\n Rolling second die...")
    time.sleep(1.5)
    die2 = random.randint(1, 6)
    total = die1 + die2
    
    say(f"\n FINAL RESULTS:")
    say(f"Die 1: {die1}")
    say(f"Die 2: {die2}")
    say(f"Sum: {total}")
    
    # Check predictions
    is_odd = (total % 2 == 1)
    is_greater_than_seven = (total > 7)
    
    odd_even_correct = False
    if (odd_even in ['O', 'ODD'] and is_odd) or (odd_even in ['E', 'EVEN'] and not is_odd):
        odd_even_correct = True
    
    greater_seven_correct = False
    if (greater_seven in ['Y', 'YES'] and is_greater_than_seven) or \
       (greater_seven in ['N', 'NO'] and not is_greater_than_seven):
        greater_seven_correct = True
    
    both_correct = odd_even_correct and greater_seven_correct
    
    say(f"\nActual outcome:")
    say(f"• Sum is {'ODD' if is_odd else 'EVEN'}")
    say(f"• Sum is {'GREATER' if is_greater_than_seven else 'NOT GREATER'} than 7")
    
    if both_correct:
        say("\n BOTH PREDICTIONS CORRECT!")
        say("[JIGSAW] Impressive. You understand probability.")
        say("Those who master mathematics... survive.")
        game_state["puzzles_solved"] += 1
        return True
    else:
        say("\n PREDICTION FAILED:")
        say(f"Your predictions:")
        say(f"• Odd/Even: {odd_even} {'✓' if odd_even_correct else '✗'}")
        say(f"• Greater than 7: {greater_seven} {'✓' if greater_seven_correct else '✗'}")
        say("[JIGSAW] Mathematics doesn't lie. You failed to see the truth.")
        return False

# ================== PUZZLE 3: Positional Cipher ==================
def puzzle3():
    """
    Cipher where each letter is shifted by its position
    ESCAPE -> FUFEUK
    """
    say("\n [PUZZLE 3] THE CIPHER OF SECRETS")
    say("[JIGSAW] Words hold power. Decode this message.")
    say("        Each letter has been shifted by its position:")
    say("        1st letter shifted +1, 2nd letter +2, 3rd +3, etc.")
    
    encoded = "FUFEUK"
    say(f"        Encoded message: {encoded}")
    
    get_hint("Cipher Puzzle", "E becomes F (+1), S becomes U (+2)... find the pattern!")
    
    answer = input("\n Enter the decoded message: ").strip().upper()
    
    def decode_positional_cipher(text):
        result = ""
        for i in range(len(text)):
            char = text[i]
            if 'A' <= char <= 'Z':
                shifted_val = (ord(char) - ord('A') - (i + 1)) % 26
                result += chr(ord('A') + shifted_val)
            else:
                result += char
        return result
    
    correct_answer = decode_positional_cipher(encoded)
    
    if answer == correct_answer:
        say(" Cipher cracked!")
        say(f"[JIGSAW] '{correct_answer}' - exactly what you seek.")
        say("Words are power. You understand.")
        game_state["puzzles_solved"] += 1
        return True
    else:
        say(f" Incorrect. The answer was '{correct_answer}'")
        say("[JIGSAW] Words matter. Precision matters more.")
        return False

# ================== PUZZLE 4: Logic Gates ==================
def puzzle4():
    """
    Logic gate puzzle: (A AND B) OR (NOT C) must be TRUE
    """
    say("\n⚡ [PUZZLE 4] THE FINAL GATE")
    say("[JIGSAW] Your last test. Three switches control your fate.")
    say("        The logic gate equation: (A AND B) OR (NOT C)")
    say("        Set A, B, C to make the output TRUE.")
    say("        This is your final judgment.")
    
    get_hint("Logic Gate", "Try A=True, B=True, C=any value OR A=any, B=any, C=False")
    
    def get_boolean_input(prompt):
        while True:
            value = input(prompt).strip().upper()
            if value in ['T', 'TRUE', '1', 'Y', 'YES']:
                return True
            elif value in ['F', 'FALSE', '0', 'N', 'NO']:
                return False
            else:
                say("Enter T/F, True/False, 1/0, or Y/N")
    
    A = get_boolean_input("Set switch A (T/F): ")
    B = get_boolean_input("Set switch B (T/F): ")
    C = get_boolean_input("Set switch C (T/F): ")
    
    result = (A and B) or (not C)
    
    say(f"\n⚡ Logic gate evaluation:")
    say(f"   A = {A}")
    say(f"   B = {B}")
    say(f"   C = {C}")
    say(f"   (A AND B) = {A and B}")
    say(f"   (NOT C) = {not C}")
    say(f"   Final: ({A and B}) OR ({not C}) = {result}")
    
    if result == True:
        say("\n Output: TRUE - Gate unlocked!")
        say("[JIGSAW] Logic is the key to freedom. You understand the final truth.")
        game_state["puzzles_solved"] += 1
        return True
    else:
        say("\n Output: FALSE - Gate remains locked.")
        say("[JIGSAW] Boolean logic defeats you. How fitting for your final failure.")
        return False

def restart_game():
    """Reset game state for new game"""
    global game_state
    game_state = {
        "player_name": "",
        "attempts_remaining": 3,
        "total_score": 0,
        "puzzles_solved": 0,
        "hints_used": 0,
        "start_time": 0,
        "difficulty": "normal"
    }
    main()

def main():
    """Main game loop with difficulty selection"""
    display_saw_ascii()
    
    say(" I WANT TO PLAY A GAME \n")
    
    game_state["player_name"] = input(" Enter your name, test subject: ").strip()
    if not game_state["player_name"]:
        game_state["player_name"] = "Unknown"
    
    say(f"\nWelcome, {game_state['player_name']}.")
    say("🎚️ Select difficulty:")
    say("   1. EASY (Extra hints, more attempts, probability auto-set)")
    say("   2. NORMAL (Standard challenge, probability shown)")
    say("   3. HARD (Limited attempts, no hints, minimal info)")
    
    while True:
        difficulty = input("Choose (1/2/3): ").strip()
        if difficulty == '1':
            game_state["difficulty"] = "easy"
            game_state["attempts_remaining"] = 5
            break
        elif difficulty == '2':
            game_state["difficulty"] = "normal"
            game_state["attempts_remaining"] = 3
            break
        elif difficulty == '3':
            game_state["difficulty"] = "hard"
            game_state["attempts_remaining"] = 1
            break
        else:
            say("Invalid choice. Enter 1, 2, or 3.")
    
    game_state["start_time"] = time.time()
    
    say("\n*Static crackles... screen flickers*")
    say("[JIGSAW] Hello, test subject.", 1.0)
    say("        Four puzzles stand between you and freedom.", 0.5)
    say("        Each failure brings consequences.", 0.5)
    say(f"        You have {game_state['attempts_remaining']} attempts total.", 0.5)
    say("        Live or die. Make your choice.", 1.0)
    
    puzzles = [puzzle1, puzzle2, puzzle3, puzzle4]
    puzzle_names = ["Lock Combination", "Conditional Probability", "Cipher Decode", "Logic Gates"]
    
    for i, puzzle_func in enumerate(puzzles):
        say(f"\n{'='*60}")
        say(f"🎯 CHALLENGE {i+1}/4: {puzzle_names[i]}")
        say(f"{'='*60}")
        
        success = False
        while game_state["attempts_remaining"] > 0:
            success = puzzle_func()
            if success:
                break
            else:
                game_state["attempts_remaining"] -= 1
                
                if game_state["attempts_remaining"] > 0:
                    say(f"\n[JIGSAW] Failure. {game_state['attempts_remaining']} attempts remain.")
                    retry = input(" Try this puzzle again? (y/n): ").strip().lower()
                    if retry not in ['y', 'yes']:
                        break
                else:
                    game_over("No attempts remaining. The chamber seals forever.")
                    return
        
        if not success:
            game_over(f"Puzzle {i+1} defeated you. The exit remains sealed.")
            return
    
    game_clear()

if __name__ == "__main__":
    main()