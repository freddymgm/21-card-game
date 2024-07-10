import pydealer
from playsound import playsound
import tkinter as tk
import sys
import cv2
import numpy as np

# Get the screen resolution. Used to centralize items on screen
my_sys = tk.Tk()
SCR_WIDTH = my_sys.winfo_screenwidth()
SCR_HEIGHT = my_sys.winfo_screenheight()


def main():

    # Call functions to create and show deck.
    main_window()
    deck = create_deck()
    msg = "Pick a card on your mind. Do not tell anyone. When done, please press 'Enter'."
    display_text(msg)
    show_deck(deck)
    destroy_window("Deck")

    # Create groups of cards
    groups = create_groups(deck)
    group1, group2, group3 = groups

    # Show groups of cards to user - 3 rounds.
    # Round 1
    round1_groups = show_groups(group1, group2, group3, 1)
    group1, group2, group3 = round1_groups
    destroy_window("Cards Group 1", "Cards Group 2", "Cards Group 3")

    # Round 2
    round2_groups = show_groups(group1, group2, group3, 2)
    group1, group2, group3 = round2_groups
    destroy_window("Cards Group 1", "Cards Group 2", "Cards Group 3")

    # Round 3
    round3_groups = show_groups(group1, group2, group3, 3)
    group1, group2, group3 = round3_groups
    destroy_window("Cards Group 1", "Cards Group 2", "Cards Group 3")

    msg = "We have guessed your card... please press Enter to reveal it!"
    display_text(msg)
    cv2.waitKey(0)
    destroy_window("Message")

    # The user's card, as per the rule of the trick
    playsound('snd/tada.mp3')
    display_text("This is your card!!!")
    yourcard = group2[3]

    fname = str(yourcard).replace(" ","")
    fname = fname.lower()
    image_path = f"img/{fname}.png"

    show_card_image(image_path)

    sys.exit(0)


# Create main window
def main_window():
    
    img = 255 * np.ones((200, 200, 1), dtype=np.uint8)
    
    cv2.namedWindow("Twenty-One Card Trick", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Twenty-One Card Trick", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Twenty-One Card Trick", img)

# Create the deck containing 21 randome cards out of the full deck.
def create_deck():
    d = pydealer.Deck()
    d.shuffle()
    d = d.deal(21)
    return d

def destroy_window(*windows):
    for window in windows:
        cv2.destroyWindow(window)
    

# Function to display a message in an Opencv window
def display_text(s):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    f_scale = 1
    f_thickness = 1
    txt_size = cv2.getTextSize(s, font, f_scale, f_thickness)[0]

    img_width = txt_size[0] + 50
    img_height = txt_size[1] + 50
    
    img = 255 * np.ones((img_height, img_width, 1), dtype=np.uint8)
    
    txt_x = (img_width - txt_size[0]) // 2
    txt_y = (img_height + txt_size[1]) // 2

    cv2.putText(img, s, (txt_x, txt_y), font, f_scale, (0, 0, 0), f_thickness)

    cv2.imshow("Message", img)
    cv2.moveWindow("Message", (SCR_WIDTH - img_width) // 2, 30)



# Show deck of 21 cards to the user
def show_deck(d):
    img_list = []
    rows = 3
    cols = 7

    # Assign the file name and resize the image
    for card in range(len(d)):
        fname = str(d[card]).replace(" ","")
        fname = fname.lower()
        img_path = f"img/{fname}.png"
        img_item = cv2.imread(img_path)
        img_width = int(img_item.shape[1] * 0.5)
        img_height = int(img_item.shape[0] * 0.5)
        img_dim = (img_width, img_height)
        img_resized = cv2.resize(img_item, img_dim, interpolation = cv2.INTER_AREA)

        # Append the list of images
        img_list.append(img_resized)


    # Reshape the array to a 3D array
    image_array = np.array(img_list).reshape(rows, cols, *img_list[0].shape)

    # Horizontally stack each image row in the image array
    row_img = [np.hstack(img_row) for img_row in image_array]

    # Vertically concatenate the image rows
    concat_image = np.vstack(row_img)

    # Display the 21 cards Deck to the user
    cv2.imshow("Deck", concat_image)
    cv2.namedWindow("Deck", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Deck", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Move the window to a viewable position
    cv2.moveWindow("Deck", (SCR_WIDTH - concat_image.shape[1]) // 2, 150)

    # Wait on any key to be pressed
    while True:
        try:
            n = cv2.waitKey(0)

            if n == 13:
                break
            else:
                continue

        except ValueError:
            pass


def create_groups(d):
    g = []
    g1 = []
    g2 = []
    g3 = []

    msg = "Shuffling cards... please wait"
    display_text(msg)
    cv2.waitKey(3000)

    for card in range(len(d)):
        if card >= 0 and card <= 6:
            g1.append(d[card])
        elif card >= 7 and card <= 13:
            g2.append(d[card])
        else:
            g3.append(d[card])

    g = [g1, g2, g3]

    return g


def show_groups(g1, g2, g3, rnd):
    g = []
    newgroup1=[]
    newgroup2=[]
    newgroup3=[]
    img_list1=[]
    img_list2=[]
    img_list3=[]
    i = 0

    for c in range(len(g1)):

        fname = str(g1[c]).replace(" ","")
        fname = fname.lower()
        img_path = f"img/{fname}.png"
        img_item = cv2.imread(img_path)
        img_width = int(img_item.shape[1] * 0.5)
        img_height = int(img_item.shape[0] * 0.5)
        img_dim = (img_width, img_height)
        img_resized = cv2.resize(img_item, img_dim, interpolation = cv2.INTER_AREA)

        if i == 0:
            newgroup1.append(g1[c])
            img_list1.append(img_resized)
            i += 1
        elif i == 1:
            newgroup2.append(g1[c])
            img_list2.append(img_resized)
            i += 1
        elif i == 2:
            newgroup3.append(g1[c])
            img_list3.append(img_resized)
            i = 0


    for c in range(len(g2)):

        fname = str(g2[c]).replace(" ","")
        fname = fname.lower()
        img_path = f"img/{fname}.png"
        img_item = cv2.imread(img_path)
        img_width = int(img_item.shape[1] * 0.5)
        img_height = int(img_item.shape[0] * 0.5)
        img_dim = (img_width, img_height)
        img_resized = cv2.resize(img_item, img_dim, interpolation = cv2.INTER_AREA)

        if i == 0:
            newgroup1.append(g2[c])
            img_list1.append(img_resized)
            i += 1
        elif i == 1:
            newgroup2.append(g2[c])
            img_list2.append(img_resized)
            i += 1
        elif i == 2:
            newgroup3.append(g2[c])
            img_list3.append(img_resized)
            i = 0


    for c in range(len(g3)):

        fname = str(g3[c]).replace(" ","")
        fname = fname.lower()
        img_path = f"img/{fname}.png"
        img_item = cv2.imread(img_path)
        img_width = int(img_item.shape[1] * 0.5)
        img_height = int(img_item.shape[0] * 0.5)
        img_dim = (img_width, img_height)
        img_resized = cv2.resize(img_item, img_dim, interpolation = cv2.INTER_AREA)

        if i == 0:
            newgroup1.append(g3[c])
            img_list1.append(img_resized)
            i += 1
        elif i == 1:
            newgroup2.append(g3[c])
            img_list2.append(img_resized)
            i += 1
        elif i == 2:
            newgroup3.append(g3[c])
            img_list3.append(img_resized)
            i = 0

    g1 = newgroup1
    g2 = newgroup2
    g3 = newgroup3
    concat_image1 = np.hstack(img_list1)
    concat_image2 = np.hstack(img_list2)
    concat_image3 = np.hstack(img_list3)

    if rnd == 1:
        msg = "Please press the key corresponding to your card's group number: 1, 2 or 3"
    elif rnd == 2:
        msg = "Again, please press the key corresponding to your card's group number: 1, 2 or 3"
    elif rnd == 3:
        msg = "For the last time, please press the key corresponding to your card's group number: 1, 2 or 3"

    display_text(msg)

    cv2.imshow("Cards Group 1", concat_image1)
    cv2.imshow("Cards Group 2", concat_image2)
    cv2.imshow("Cards Group 3", concat_image3)

    # Centralize all windows
    cv2.moveWindow("Cards Group 1", (SCR_WIDTH - concat_image1.shape[1]) // 2, 150)
    cv2.moveWindow("Cards Group 2", (SCR_WIDTH - concat_image2.shape[1]) // 2, 350)
    cv2.moveWindow("Cards Group 3", (SCR_WIDTH - concat_image3.shape[1]) // 2, 550)

    # Wait for key from user (1, 2 or 3)
    while True:
        try:
            n = cv2.waitKey(0)

            if n == 49 or n==156:
                g = [g2, g1, g3]
                return g
            elif n == 50 or n==153:
                g = [g1, g2, g3]
                return g
            elif n == 51 or n==155:
                g = [g1, g3, g2]
                return g
        except ValueError:
            pass

def show_card_image(img_path):
    img = cv2.imread(img_path)
    cv2.imshow("Your Card", img)
    cv2.moveWindow("Your Card", (SCR_WIDTH - img.shape[1]) // 2, 210)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main()