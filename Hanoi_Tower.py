import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Set up constants for the game window and tower
WIDTH, HEIGHT = 1200, 600
DISK_HEIGHT = 20
DISK_WIDTH_FACTOR = 20
BASE_HEIGHT = 20
BASE_Y = 200
ROD_Y = HEIGHT - BASE_HEIGHT
RODS = {'A': (200, ROD_Y), 'B': (600, ROD_Y), 'C': (1000, ROD_Y)}
time_check = False
game_delay = 1

# Function to draw disks on the screen
def draw_disks(screen, disks, disk_colors):
    for rod, stack in disks.items():
        x, y = RODS[rod]
        for i, disk in enumerate(stack, start=1):
            color = disk_colors[disk]
            pygame.draw.rect(screen, color, (
                x - disk * DISK_WIDTH_FACTOR // 2, y - i * DISK_HEIGHT, disk * DISK_WIDTH_FACTOR, DISK_HEIGHT))

# Function to move a disk from one rod to another and record the move
def move_disk(disks, from_rod, to_rod, moves):
    disk = disks[from_rod].pop()
    disks[to_rod].append(disk)
    moves.append(f"Disk {disk} is moved from {from_rod} to {to_rod}")

# Function to draw the towers and bases on the screen
def draw_tower(screen, disks, disk_colors):
    screen.fill((255, 255, 255))
    for rod, (x, _) in RODS.items():
        base_width = 200
        pygame.draw.rect(screen, (0, 0, 0), (x - base_width // 2, HEIGHT - BASE_HEIGHT,
                                             base_width, BASE_HEIGHT))

    for rod in RODS.values():
        pygame.draw.line(screen, (0, 0, 0), (rod[0], 161), rod, 5)
    draw_disks(screen, disks, disk_colors)

# Function to draw buttons on the screen
def draw_buttons(screen, font, recursive_button_rect, iterative_button_rect):
    # Draw black border around buttons
    pygame.draw.rect(screen, (0, 0, 0), recursive_button_rect, 2)
    pygame.draw.rect(screen, (0, 0, 0), iterative_button_rect, 2)

    # Draw transparent rectangles
    pygame.draw.rect(screen, (255, 255, 255), recursive_button_rect)
    pygame.draw.rect(screen, (255, 255, 255), iterative_button_rect)

    # Display text on buttons
    display_text(screen, "Recursive Algorithm", (recursive_button_rect.x + 10,
                                                 recursive_button_rect.y + 10), font_size=28, color=(0, 0, 0))
    display_text(screen, "Iterative Algorithm", (iterative_button_rect.x + 10,
                                                 iterative_button_rect.y + 10), font_size=28, color=(0, 0, 0))

# Set up rectangles for buttons and input fields
recursive_button_rect = pygame.Rect(WIDTH + 10, HEIGHT // 2 - 50, 210, 30)
iterative_button_rect = pygame.Rect(WIDTH + 10, HEIGHT // 2 + 50, 210, 30)
restart_button = pygame.Rect(WIDTH + 10, HEIGHT + 20, 210, 30)
font = pygame.font.Font(None, 24)

# Function to get the number of disks and delay time from the user
def get_num_disks(screen):
    input_text1 = ""
    input_text2 = ""
    clock = pygame.time.Clock()
    color_text1 = 0
    color_text2 = 0
    input_active1 = True
    input_active2 = False
    check = True
    while check:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_active1:
                        try:
                            num_disks = int(input_text1)
                            color_text1 = 1
                            if ((input_text2 != "") and (input_text1 != "")):
                                print("Ready")
                                return num_disks, delay
                        except ValueError:
                            input_text1 = ""
                            continue
                    elif input_active2:
                        try:
                            color_text2 = 1
                            delay = int(input_text2)
                            if ((input_text2 != "") and (input_text1 != "")):
                                print("Ready")
                                return num_disks, delay

                        except ValueError:
                            input_text2 = ""
                            continue
                elif event.key == pygame.K_TAB:
                    input_active1 = not input_active1
                    input_active2 = not input_active2
                elif event.key == pygame.K_BACKSPACE:
                    if input_active1:
                        input_text1 = input_text1[:-1]
                    elif input_active2:
                        input_text2 = input_text2[:-1]
                else:
                    if input_active1:
                        input_text1 += event.unicode
                    elif input_active2:
                        input_text2 += event.unicode

        screen.fill((255, 255, 255))
        main_menu(input_text1, input_text2, color_text1, color_text2)
        pygame.display.flip()
        clock.tick(20)

# Function to generate colors for each disk
def generate_colors(num_disks):
    colors = [
        (0, 0, 139),
        (255, 255, 0),
        (144, 238, 144),
        (255, 0, 0),
        (255, 165, 0),
        (255, 192, 203),
        (128, 0, 128),
        (0, 0, 255)
    ]
    return {i: colors[i % len(colors)] for i in range(1, num_disks + 1)}

# Function to display text on the screen
def display_text(screen, text, position, font_size=24, color=(0, 0, 0)):
    font = pygame.font.Font(None, font_size)
    display_text_surface = font.render(text, True, color)
    screen.blit(display_text_surface, position)

# Function to display information about moves and total moves
def display_info(screen, moves, total_moves, disk_colors):
    display_text(screen, "Tower of Hanoi Moves:", (WIDTH + 10, 10), font_size=24)
    y_position = 40
    for move in moves:
        if ((y_position < HEIGHT - 80) and (move is not None)):
            y_position += 20
            font = pygame.font.Font(None, 24)
            display_text_surface = font.render(move, True, (0, 0, 0))
            screen.blit(display_text_surface, (WIDTH + 10, y_position))

    display_text(screen, f"Total Moves: {total_moves}", (WIDTH + 10, HEIGHT - 40), font_size=24)

# Recursive algorithm for Tower of Hanoi
def recursive_hanoi(n,

 from_rod, to_rod, aux_rod, disks, moves, screen, game_delay):
    if n == 1:
        move_disk(disks, from_rod, to_rod, moves)
        draw_tower(screen, disks, disk_colors)
        display_info(screen, moves, len(moves), disk_colors)
        pygame.display.flip()
        pygame.time.delay(game_delay)
    else:
        recursive_hanoi(n - 1, from_rod, aux_rod, to_rod, disks, moves, screen, game_delay)
        move_disk(disks, from_rod, to_rod, moves)
        draw_tower(screen, disks, disk_colors)
        display_info(screen, moves, len(moves), disk_colors)
        pygame.display.flip()
        pygame.time.delay(game_delay)
        recursive_hanoi(n - 1, aux_rod, to_rod, from_rod, disks, moves, screen, game_delay)

# Iterative algorithm for Tower of Hanoi
def iterative_hanoi(n, source, target, auxiliary, disks, moves, screen, game_delay):
    stack = []
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if n > 0:
            stack.append((n, source, target, auxiliary))
            n -= 1
            target, auxiliary = auxiliary, target
        elif stack:
            n, source, target, auxiliary = stack.pop()
            move_disk(disks, source, target, moves)
            draw_tower(screen, disks, disk_colors)
            display_info(screen, moves, len(moves), disk_colors)
            pygame.display.flip()
            pygame.time.delay(game_delay)
            n -= 1
            source, auxiliary = auxiliary, source
        else:
            done = True

# Function to display the main menu
def main_menu(input_text, input_delay_text, color_text1, color_text2):
    # Check if the input are entered:
    color1 = (192, 192, 192)
    color2 = (192, 192, 192)
    if color_text1:
        color1 = (124, 252, 0)
    if color_text2:
        color2 = (124, 252, 0)
    font = pygame.font.Font(None, 36)
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2 - 130, HEIGHT // 2 - 30, 400, 50), 5)
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2 - 130, HEIGHT // 2 + 20, 400, 50), 5)
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2 - 130, HEIGHT // 2 + 70, 400, 50), 5)
    # Display the user's input box
    pygame.draw.rect(screen, color1, (WIDTH // 2 + 200, HEIGHT // 2 - 20, 61, 30))
    text_surface = font.render(input_text, True, (0, 0, 0))
    screen.blit(text_surface, (WIDTH // 2 + 215, HEIGHT // 2 - 15))

    pygame.draw.rect(screen, color2, (WIDTH // 2 + 200, HEIGHT // 2 + 30, 61, 30))
    text_surface = font.render(input_delay_text, True, (0, 0, 0))
    screen.blit(text_surface, (WIDTH // 2 + 215, (HEIGHT // 2) + 35))
    # The size of the header
    header_font = pygame.font.Font(None, 120)
    header_text = header_font.render("Tower of Hanoi", True, (0, 0, 0))
    screen.blit(header_text, ((WIDTH // 2) - header_text.get_width() // 4, 35))
    # Explanation
    explain_font = pygame.font.Font(None, 34)
    explanation = "Welcome to Tower of Hanoi game."
    explanation_text = explain_font.render(explanation, True, (0, 0, 0))
    screen.blit(explanation_text, ((WIDTH // 2 - 80), 125))

    explanation = "You can select delay time and number of disk."
    explanation_text = explain_font.render(explanation, True, (0, 0, 0))
    screen.blit(explanation_text, ((WIDTH // 2) - 80, 155))

    explanation = "After that you can select the algorithm."
    explanation_text = explain_font.render(explanation, True, (0, 0, 0))
    screen.blit(explanation_text, ((WIDTH // 2) - 80, 185))

    explanation = "Press TAB to change features."
    explanation_text = explain_font.render(explanation, True, (0, 0, 0))
    screen.blit(explanation_text, ((WIDTH // 2) - 80, 210))
    explanation = "If everything is ready press Enter."
    explanation_text = explain_font.render(explanation, True, (0, 0, 0))
    screen.blit(explanation_text, ((WIDTH // 2) - 80, 235))
    # Display the user's input
    text_surface = font.render("Enter the number of disks:", True, (0, 0, 0))
    screen.blit(text_surface, (WIDTH // 2 - 120, HEIGHT // 2 - 15))

    # Display delay time input
    delay_text = font.render("Enter the delay time (ms):", True, (0, 0, 0))
    screen.blit(delay_text, (WIDTH // 2 - 120, HEIGHT // 2 + 35))
    # Restart button
    pygame.draw.rect(screen, (0, 0, 0), restart_button, 2)
    pygame.draw.rect(screen, (255, 255, 255), restart_button)
    display_text(screen, "Restart", (restart_button.x + 10, restart_button.y + 10), font_size=28, color=(0, 0, 0))

# A function that helps to scrooling the moves. It clear the old displays.
def clear_info():
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH + 10, 40, 250, 510))
    pygame.draw.rect(screen, (255, 0, 0), (WIDTH + 10, 40, 250, 510), 2)

# A function that display the total time, algorithm name, moves and the restart option, when algorithm finished.
def finish_screen(run_time, moves, text_y, algorithm, restart_button):
    # Display the total time, algorithm and restart button optipn.
    if time_check:
        display_text(screen, f"Total Time: {run_time / 1000:.3f}s", (WIDTH + 10, HEIGHT - 20), font_size=24)
        display_text(screen, f"Algorithm: {algorithm}", (WIDTH + 10, HEIGHT), font_size=24)
        pygame.draw.rect(screen, (0, 0, 0), restart_button, 2)
        pygame.draw.rect(screen, (255, 255, 255), restart_button)
        display_text(screen, "Restart", (restart_button.x + 10, restart_button.y + 10), font_size=28, color=(0, 0, 0))
    # Convert list to string and display the moves with numbers.
    numbered_list = [f"{i + 1}-{item}" for i, item in enumerate(moves)]
    string_list = "\n".join(map(str, numbered_list))
    lines = string_list.split("\n")
    render_y = text_y
    for line in lines:
        text_surface = font.render(line, True, (0, 0, 0))
        if render_y >= 50 and render_y <= 50 + box_height:
            screen.blit(text_surface, (WIDTH + 20, render_y))
        render_y += 24
    return string_list, False


screen = pygame.display.set_mode((WIDTH + 300, HEIGHT + 100))
pygame.display.set_caption("Tower of Hanoi")

# Variables to use interface and algorithms.
num_disks, delay = get_num_disks(screen)
disks = {'A': list(reversed(range(1, num_disks + 1))), 'B': [], 'C': []}

disk_colors = generate_colors(num_disks)
moves = []
running = True
algorithm = None
algorithm_runtime = 2
algorithm_name = None
game_not_end = True
game_end = False
scroll_speed = 20
disk_restart = False
box_width, box_height = 500, 480
text_y = 40

# Main game loop
while running:
    for event in pygame.event.get():
        # Check for quit event
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if (game_not_end):  # Check if the algorithm has finished
                # Check if the recursive button is clicked
                if recursive_button_rect.collidepoint(pos):
                    algorithm = recursive_hanoi
                    algorithm_name = "Recursive"
                # Check if the iterative button is clicked
                elif iterative_button_rect.collidepoint(pos):
                    algorithm = iterative_hanoi
                    algorithm_name = "Iterative"
            else:
                # Check if the restart button is clicked after the game has ended
                if restart_button.collidepoint(pos):
                    game_not_end = True
                    game_end = False
                    disk_restart = True
                    screen.fill((0, 0, 0))
            # Check for mouse scroll events
            if event.button == 4:  # Scroll up
                text_y = min(text_y + scroll_speed, 50)  # If at the top, stop
            elif event.button == 5:  # Scroll down
                text_y = max(text_y - scroll_speed,
                             50 - (len(text_content.split("\n")) * 24 - box_height))  # If at the bottom, stop

    if algorithm:
        time_check = False
        print(disks)

        # Start measuring algorithm execution time
        algorithm_start = float(round(time.time() * 1000))
        algorithm(num_disks, 'A', 'C', 'B', disks, moves, screen, delay)
        algorithm = None
        # End measuring algorithm execution time
        algorithm_end = float(round(time.time() * 1000))
        algorithm_runtime = algorithm_end - algorithm_start
        print(disks)
        time_check = True
        game_not_end = False
        game_end = True

    if game_not_end:
        # Reset the game state if the disks need to be restarted
        if disk_restart:
            print(num_disks)
            disks = {'A': list(reversed(range(1, num_disks + 1))), 'B': [], 'C': []}
            disk_restart = False
            moves = []

        # Draw the current state of disks and towers
        draw_disks(screen, disks, disk_colors)
        draw_tower(screen, disks, disk_colors)
        draw_buttons(screen, font, recursive_button_rect, iterative_button_rect)

    if game_end:
        # Clear the information and display the finish screen
        clear_info()
        text_content, time_check = finish_screen(algorithm_runtime, moves, text_y, algorithm_name, restart_button)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()