#############
# Path: discord.py
# Author: Jack Fitton
# Date: 01/07/2023
# Description: A discord bot that can play tic tac toe
#############

import discord
import os
import random
from random import randint
import string
from dotenv import load_dotenv
import sqlite3
import json
from PIL import Image, ImageDraw, ImageFont



# Create a font object with the desired size
font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 24)


load_dotenv()





try:
    TOKEN = os.getenv('DISCORD_TOKEN')
except:
    print("Error loading discord token")
    exit(2)

try:
    #try to connect to the database, if it doesn't exist create it
    conn = sqlite3.connect('games.db')
    c = conn.cursor()


    # Create the 'games' table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            game_id TEXT,
            player1 TEXT,
            player2 TEXT,
            x TEXT,
            o TEXT,
            board TEXT,
            turn INTEGER,
            winner TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()

except:
    print("Error connecting to database")
    exit(2)


intents = discord.Intents.all()
client = discord.Client(intents=intents)

async def start_game(player1, player2, game_id, channel):

    if player2 == None:
        player2 = 100

    #check user is not already in a game
    c.execute('''SELECT * FROM games WHERE player1=? OR player2=?''', (player1.id, player1.id))
    if c.fetchone() != None:
        await channel.send("You are already in a game")
        return False
    
    board = [[1,2,3],[4,5,6],[7,8,9]]


    
    # Create a game object, store board as json string
    game = {
        "game_id": game_id,
        "player1": player1.id,
        "player2": player2,
        "x": player1.id,
        "o": player2,
        "board": json.dumps(board),
        "turn": player1.id,
        "winner": 0
    }

    # Send the game object to the database
    #TODO: add sqlite3 database to store game objects against game_id and player_id
    c.execute('''INSERT INTO games (game_id, player1, player2, x, o, board, turn, winner) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (game["game_id"], game["player1"], game["player2"], game["x"], game["o"], str(game["board"]), game["turn"], game["winner"]))
    conn.commit()

    return True




    # Send the game object to the database
    pass

async def end_game(game_id, player_id):
    #delete the game from the database only if the player is in the game
    c.execute('''SELECT * FROM games WHERE game_id=?''', (game_id,))
    game = c.fetchone()
    if game[2] == player_id or game[3] == player_id:
        c.execute('''DELETE FROM games WHERE game_id=?''', (game_id,))
        conn.commit()
        return True
    else:
        return False
    
async def make_move(player_id, move, channel):

    game_id = await get_game_id(player_id)

    # Get the game from the database
    c.execute('''SELECT * FROM games WHERE game_id=?''', (game_id,))
    game = c.fetchone()

    moves = {
        1: [0,0],
        2: [0,1],
        3: [0,2],
        4: [1,0],
        5: [1,1],
        6: [1,2],
        7: [2,0],
        8: [2,1],
        9: [2,2]
    }

    move = int(move)


    board = json.loads(game[6])

    #print(game)

    # Check if the game exists
    if game == None:
        return False

    # Check if it is the players turn
    if game[7] != player_id:
        await channel.send("It is not your turn to play")
        return False
    
    # Check if the move is valid
    if board[moves[move][0]][moves[move][1]] > 9:
        await channel.send("That move is not valid please try again")
        return False

    
    # Make the move
    board[moves[move][0]][moves[move][1]] = player_id


    board = json.dumps(board)


    #update the database
    c.execute('''UPDATE games SET board=? WHERE game_id=?''', (board, game_id))
    conn.commit()

    #change the turn
    changeTurn(game_id)


    #check if the player has won
    player = await checkWin(game_id)

    if player != False:
        c.execute('''UPDATE games SET winner=? WHERE game_id=?''', (player, game_id))
        conn.commit()
        user = await client.fetch_user(int(player))
        await channel.send("Player "+str(user.mention)+" has won the game")
        await end_game(game_id, user.id)
        return True
    



    return True
    
async def get_game_id(player_id):
    #get the game_id from the database
    c.execute('''SELECT * FROM games WHERE player1=? OR player2=?''', (player_id, player_id))
    game = c.fetchone()
    return game[1]

async def genBoard(game_id):

    #make a random filename to avoid overwriting
    filename = game_id+''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    #use pillow to generate an image of the board and return it
    #put numbers 1-9 on the board to represent the moves
    #put an x or o on the board to represent the moves
    
    #get the game from the database
    c.execute('''SELECT * FROM games WHERE game_id=?''', (game_id,))
    game = c.fetchone()

    if game == None:
        return False
    


    board = json.loads(game[6])
    player1 = game[2]
    player2 = game[3]

    cells = {
        player1: "x",
        player2: "o"
    }





    #create a new image
    img = Image.new('RGB', (300, 300), color = (255, 255, 255))

    #draw the lines
    draw = ImageDraw.Draw(img)
    draw.line((100, 0, 100, 300), fill=128)
    draw.line((200, 0, 200, 300), fill=128)
    draw.line((0, 100, 300, 100), fill=128)
    draw.line((0, 200, 300, 200), fill=128)

    #either drawn the number in the cell or put player1 or player2 in the cell depending on the value in the board
    for i in range(3):
        for j in range(3):
            if int(board[i][j]) < 10:
                draw.text((j*100+40, i*100+40), str(board[i][j]), font=font, fill=(0, 0, 0))
            else:
                draw.text((j*100+40, i*100+40), cells[board[i][j]], font=font, fill=(0, 0, 0))
            


    #save the image
    img.save("boards/"+filename+'.png')

    #return the image
    return "boards/"+filename+'.png'

async def checkWin(game_id):
    
        #get the game from the database
        c.execute('''SELECT * FROM games WHERE game_id=?''', (game_id,))
        game = c.fetchone()
    
        board = json.loads(game[6])
    
        #check if there is a winner
        #check the rows
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] != 0:
                return board[i][0]
        #check the columns
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] != 0:
                return board[0][i]
        #check the diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
            return board[0][2]
    
        #check if the board is full
        if 0 not in board[0] and 0 not in board[1] and 0 not in board[2]:
            return "tie"
    
        #if there is no winner return false
        return False
    
async def changeTurn(game_id):

    #get the game from the database
    c.execute('''SELECT * FROM games WHERE game_id=?''', (game_id,))

    game = c.fetchone()
    
    board = json.loads(game[6])

    #see how many moves have been made

    player1 = game[2]
    player2 = game[3]

    #if there are more player1 moves than player2 moves then it is player2's turn
    if board.count(player1) > board.count(player2):
        c.execute('''UPDATE games SET turn=? WHERE game_id=?''', (player2, game_id))
        conn.commit()
        return player2
    
    #if there are more player2 moves than player1 moves then it is player1's turn
    elif board.count(player2) > board.count(player1):
        c.execute('''UPDATE games SET turn=? WHERE game_id=?''', (player1, game_id))
        conn.commit()
        return player1



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    if message.content.startswith('!game'):

        # Get the players
        player1 = message.author
        try:
            player2 = message.mentions[0]
        except:
            player2 = None

        #create game id (5 alphanumeric characters)
        game_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


        # Check if the players are valid
        if player1 == player2:
            await message.channel.send("You can't play against yourself")

        
        elif player2 == None:
            # send message @player1 vs Computer
            await message.channel.send(f"Game starting ({game_id}): {player1.mention} vs Computer")

        
        else:
            # send message @player1 vs @player2
            await message.channel.send(f"Game starting ({game_id}): {player1.mention} vs {player2.mention}")

        # create game
        if await start_game(player1, player2, game_id, message.channel):
            await message.channel.send(file=discord.File(await genBoard(game_id)))
        else:
            #get the game_id from the database
            game_id = await get_game_id(player1.id)
            await message.channel.send(file=discord.File(await genBoard(game_id)))

    if message.content.startswith('!end'):
        try:
            game_id = message.content.split()[1]
            if game_id == "all" and message.author.id == 196664058143965184:
                c.execute('''DELETE FROM games''')
                conn.commit()
                await message.channel.send("Ending all games")
                return
        except:
            await message.channel.send("Please specify a game id")
            return
        
        
        if end_game(game_id, message.author.id):
            await message.channel.send(f"Ending game {game_id}")
        else:
            await message.channel.send(f"You are not in game {game_id}")

    if message.content.startswith('!move'):
        game_id = await get_game_id(message.author.id)
        try:
            move = message.content.split()[1]
        except:
            await message.channel.send("Please specify a move `!move 1` or `!move 2`")
            return

        if await make_move(message.author.id, move, message.channel):
            await message.channel.send(file=discord.File(await genBoard(game_id)))


        





        
client.run(TOKEN)


