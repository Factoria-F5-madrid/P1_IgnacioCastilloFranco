#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import logging
import colorlog #adds color formatting capabilities to the standard Python logging module.
from blessed import Terminal #enhanced terminal capabilities
from datetime import datetime

'''
Libraries like blessed and colorlog provide convenient abstractions that generate escape 
sequences ((example, \033[31m turns text red) behind the scenes. Methods like term.bold 
or term.blue(), are actually producing the appropriate ANSI escape sequences for those 
effects. This approach lets you create visually appealing terminal applications without 
having to memorize or directly write the raw escape sequences.
'''
term = Terminal()
log_filename = f"taximeter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# --------------Configure logging---------------
# Create a custom formatter with colorlog (which passes this data to the logging module)
log_handler = colorlog.StreamHandler() #directs log messages to a stream, typically the console (stdout) (¡¡¡not the log file!!!)
log_handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s', # only %(message)s is recorded in the log file
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
))#stdout example ---> 2025-06-27 09:04:03,608 - INFO - Welcome screen displayed

logger = logging.getLogger("taximeter")
logger.setLevel(logging.INFO) # Set the logging level to INFO to only handle messages at this level and above
logger.addHandler(log_handler) #Each handler determines where the log message goes (console, file, network, etc.) and how it's formatted
logger.addHandler(logging.FileHandler(log_filename))
logger.info(f"{term.bold}Taximeter application started{term.normal}") #first log when this file is executed. The info() method will process this message only if the logger's level is set to INFO or lower 

# --------------Global variables----------------
STOPPED_RATE = 0.02  # 2 cents per second
MOVING_RATE = 0.05  # 5 cents per second
trip_in_progress = False
current_state = "stopped"  # "stopped" or "moving"
start_time = None
last_change_time = None
accumulated_total = 0.0

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls') # unix or Windows
    logger.debug("Screen cleared")

def show_welcome():
    print(term.bold + term.blue("=" * 60) + term.normal)
    print(term.bold + " " * 16 + f"🚖  {term.gold}DIGITAL TAXIMETER{term.normal}{term.bold}  🚖" + term.normal)
    print(term.bold + term.blue("=" * 60) + term.normal)
    print("\n📋 " + term.bold + "RATES:" + term.normal)
    print(f"   • {term.yellow}Stopped{term.normal}: {term.bold}{STOPPED_RATE:.2f}€{term.normal} per second")
    print(f"   • {term.green}Moving{term.normal}: {term.bold}{MOVING_RATE:.2f}€{term.normal} per second")
    print("\n⌨️  " + term.bold + "AVAILABLE COMMANDS:" + term.normal)
    print(f"   • {term.bold_green}'start'{term.normal}    - Begin new trip")
    print(f"   • {term.bold_green}'moving'{term.normal}   - Change to moving rate")
    print(f"   • {term.bold_green}'stopped'{term.normal}  - Change to stopped rate") 
    print(f"   • {term.bold_green}'status'{term.normal}   - View current status and fare")
    print(f"   • {term.bold_green}'finish'{term.normal}   - End trip and show total")
    print(f"   • {term.bold_green}'exit'{term.normal}     - Close the program")
    print(term.bold + term.blue("=" * 60) + term.normal)
    logger.info("Welcome screen displayed")

def get_increment(update_accumulated = True):# since last accumulated (accumulated is updated whenever state changes between stopped and moving, or whenever a trip is finished ,in these cases update_accumulated = True)
    """Calculates the accumulated total based on elapsed time"""
    global last_change_time, current_state, accumulated_total
    
    if not trip_in_progress:
        logger.debug("No trip in progress, returning 0.0")
        return 0.0
        
    elapsed_time = time.time() - last_change_time
    
    if current_state == "stopped":
        increment = elapsed_time * STOPPED_RATE
        logger.debug(f"Calculated stopped fare: {increment:.4f}€ for {elapsed_time:.2f} seconds")
    else:
        increment = elapsed_time * MOVING_RATE
        logger.debug(f"Calculated moving fare: {increment:.4f}€ for {elapsed_time:.2f} seconds")
        
    if update_accumulated:
        accumulated_total += increment
        logger.debug(f"Updated total: +{increment:.4f}€ = {accumulated_total:.4f}€")
        last_change_time = last_change_time + elapsed_time
    return increment

def start_trip():
    global trip_in_progress, current_state, start_time, last_change_time, accumulated_total
    
    if trip_in_progress:
        logger.warning("Attempted to start a trip while another is in progress")
        print(term.bold_red("⚠️  A trip is already in progress. Finish the current one first."))
        return
        
    trip_in_progress = True
    current_state = "stopped" #trips start in stopped mode
    start_time = time.time()
    last_change_time = start_time
    accumulated_total = 0.0
    
    print(term.bold_green("🚀 Trip started!"))
    print(f"📍 Initial state: {term.yellow(current_state.upper())}")
    print(f"⏰ Start time: {term.bold}{time.strftime('%H:%M:%S', time.localtime(start_time))}{term.normal}")
    logger.info(f"Trip started at {time.strftime('%H:%M:%S', time.localtime(start_time))}, initial state: {current_state}")

def change_state(new_state):
    global current_state
    
    if not trip_in_progress:
        logger.warning(f"Attempted state change to {new_state} without active trip")
        print(term.bold_red("❌ No trip in progress. Use 'start' first."))
        return
        
    if current_state == new_state:
        logger.debug(f"State change ignored - already in {new_state} state")
        print(f"ℹ️  Already in state: {term.bold}{new_state.upper()}{term.normal}")
        return
        
    # Update total before changing state
    old_state = current_state
    get_increment(update_accumulated = True)
    current_state = new_state
    
    state_color = term.green if new_state == "moving" else term.yellow
    print(f"🔄 State changed to: {state_color(new_state.upper())}{term.normal}")
    
    if new_state == "moving":
        print(f"🚗 Taxi moving - Rate: {term.bold}5 cents/second{term.normal}")
    else:
        print(f"🛑 Taxi stopped - Rate: {term.bold}2 cents/second{term.normal}")
    logger.info(f"State changed: {old_state} → {new_state}")

def show_status():
    if not trip_in_progress:
        logger.warning("Status check attempted without active trip")
        print(term.bold_red("❌ No trip currently in progress. Start a trip before checking status"))
        return
        
    # Calculate current total (without updating the accumulated total)
    current_total = accumulated_total + get_increment(update_accumulated = False)
    elapsed_time = time.time() - start_time
    
    state_color = term.green if current_state == "moving" else term.yellow
    
    print("\n" + term.blue("─" * 40))
    print(term.bold_blue("📊 CURRENT TAXIMETER STATUS"))
    print(term.blue("─" * 40))
    print(f"🚦 State: {state_color(current_state.upper())}")
    print(f"⏱️  Elapsed time: {term.bold}{elapsed_time:.1f}{term.normal} seconds")
    print(f"💰 Current total: {term.bold_green(f'{current_total:.2f}€')}")
    
    if current_state == "stopped":
        print(f"📈 Current rate: {term.bold}2 cents{term.normal} per second")
    else:
        print(f"📈 Current rate: {term.bold}5 cents{term.normal} per second")
    print(term.blue("─" * 40))
    logger.info(f"Status check: state={current_state}, elapsed={elapsed_time:.1f}s, total={current_total:.2f}€")

def finish_trip():
    global trip_in_progress, accumulated_total, start_time, last_change_time
    
    if not trip_in_progress:
        logger.warning("Attempted to finish a non-existent trip")
        print(term.bold_red("❌ No trip currently in progress."))
        return
        
    # Calculate final total
    get_increment(update_accumulated = True)
    
    print("\n" + term.bold_green("=" * 50))
    print(term.bold_green("🏁 TRIP FINISHED"))
    print(term.bold_green("=" * 50))
    print(f"⏱️  Total duration: {term.bold}{last_change_time - start_time:.1f}{term.normal} seconds")
    print(f"💰 TOTAL TO PAY: {term.bold_green(f'{accumulated_total:.2f}€')}")
    print(f"⏰ End time: {term.bold}{time.strftime('%H:%M:%S', time.localtime(last_change_time))}{term.normal}")
    print(term.bold_green("=" * 50))
    
    logger.info(f"Trip finished: duration={last_change_time - start_time:.1f}s, total={accumulated_total:.2f}€")
    
    # Reset state
    trip_in_progress = False
    accumulated_total = 0.0
    start_time = None
    last_change_time = None
    logger.debug("Trip state reset")

def run_taximeter():
    logger.info("Starting taximeter interface")
    show_welcome()
    
    while True:
        try:
            status = term.green('[IN PROGRESS]') if trip_in_progress else term.yellow('[INACTIVE]')
            print(f"\n🚖 Taximeter {status}")
             
            with term.location(0, term.height-2): # Position cursor at the bottom of the terminal. When the WITH block ends, the cursor automatically returns to its original position before the with statement. This enables you to create fixed-position elements in your interface, such as status bars or help text at the bottom of the screen, without disrupting the main content flow.
                print(term.clear_eol + term.bold_blue("Press Ctrl+C to interrupt"))
            
            command = input(f"{term.bold}➤ Enter a command: {term.normal}").strip().lower()
            logger.debug(f"User entered command: '{command}'")
            
            if command == "exit":
                if trip_in_progress:
                    response = input(term.yellow("⚠️  A trip is in progress. Finish and exit? (y/n): "))
                    logger.debug(f"Exit confirmation response: {response}")
                    if response.lower() == 'y':
                        finish_trip()
                    else:
                        continue
                logger.info("Exiting application")
                print(f"\n{term.bold_green('👋 Thank you for using Digital Taximeter!')}")
                break
                
            elif command == "start":
                start_trip()
                
            elif command == "moving":
                change_state("moving")
                
            elif command == "stopped":
                change_state("stopped")
                
            elif command == "status":
                show_status()
                
            elif command == "finish":
                finish_trip()
                
            elif command == "help":
                logger.debug("Help command received")
                show_welcome()
                
            else:
                logger.warning(f"Unrecognized command: '{command}'")
                print(term.bold_red("❌ Command not recognized. Use 'help' to see available commands."))
                
        except KeyboardInterrupt:
            logger.warning("KeyboardInterrupt detected")
            print(f"\n\n{term.bold_yellow('⚠️  Interruption detected...')}")
            if trip_in_progress:
                print(term.yellow("🏁 Finishing current trip..."))
                finish_trip()
            logger.info("Exiting application due to keyboard interrupt")
            print(term.bold_green("👋 See you later!"))
            break
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            print(term.bold_red(f"❌ Unexpected error: {e}"))

def main():
    try:
        clear_screen()
        # Check if the terminal supports colors (by examining environment variables (like NO_COLOR or TERM)
        if not term.does_styling: # is terminal capable of displaying ANSI escape sequences (example, \033[31m turns text red)?
            print("Warning: Your terminal doesn't fully support colors. Some visual elements may not display correctly.")
        
        # Check terminal size (if too short, "ctrl+C" message overlaps in welcome screen) 
        if term.height < 24 or term.width < 80:
            print(f"Warning: Terminal size ({term.width}x{term.height}) may be too small. Recommended: 80x24 or larger.")
        
        run_taximeter()
    except Exception as e:
        logger.critical(f"Critical error in main function: {str(e)}", exc_info=True)
    finally:
        logger.info("Application terminated")

if __name__ == "__main__":
    main()