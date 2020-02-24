#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from fuzzywuzzy import process
import unicodedata
import re
import discord.ext.commands
from discord.ext import commands

# Connect to the local sqlite database `rocbot.sqlite` and generate a list of 
# ship names from the `ship` table
def get_ships():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # Return a list of items instead of 1 item tuples 
    conn.row_factory = lambda cursor, row: row[0]
    # make an sqlite connection object
    c = conn.cursor()
    # creates a variable and assigns the list of ship names to it
    ship_list = c.execute('''SELECT name FROM ship''').fetchall()
    # close the databse connection
    conn.close()
    # return a list of ship names
    return ship_list

# return the ship name from name_list which is a list of ship names 
# extracted from the databases table called ship
def ship_search(find_this):
    # using the class initiated list ship_list find one ship name that 
    # matches the given string as close as possible
    found_this = process.extractOne(find_this, get_ships())
    # fuzzywuzzy returns the name and the ratio so strip the ratio and keep 
    # the ship name
    ship_name = found_this[0]
    # return the ship name as a string
    return ship_name

# Connect to the local sqlite database `rocbot.sqlite` and generate a list of 
# invader names from the invaders table
def get_invaders():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # Return a list of items instead of 1 item tuples 
    conn.row_factory = lambda cursor, row: row[0]
    # make an sqlite connection object
    c = conn.cursor()
    # creates a variable and assigns the list of ship names to it
    invader_list = c.execute('''SELECT name FROM invaders''').fetchall()
    # close the databse connection
    conn.close()
    # return a list of ship names
    return invader_list

def invader_search(find_this):
    if find_this != None:
        # using the class initiated list ship_list find one ship name that 
        # matches the given string as close as possible
        found_this = process.extractOne(find_this, get_invaders())
        # fuzzywuzzy returns the name and the ratio so strip the ratio and keep 
        # the ship name
        invader_name = found_this[0]
        # return the ship name as a string
        return invader_name
    else:
        pass

# strip all non lete
def sanitise_input(input_string):
    words_only = re.sub(r'\W+','', input_string)
    return unicodedata.normalize('NFKD', words_only).encode('ascii', 'ignore').decode('utf8')

def customemoji(self, find_this):
    find_sanitised = sanitise_input(find_this.lower())
    return discord.utils.get(self.bot.emojis, name = find_sanitised)

def embed_pagination(description):
    paginator = commands.Paginator(prefix='', suffix='', max_size=2000)
    for ship_line in description:
        paginator.add_line(ship_line)
    return paginator.pages

def shortcut_obj(arg1):
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # return a class sqlite3.row object which requires a tuple input query
    conn.row_factory = sqlite3.Row
    # make an sqlite connection object
    c = conn.cursor()
    # using a defined view shortcut collect all table info 
    c.execute('select * from shortcut where shortcut =?', (arg1,))
    # return the shortcut object including the required elemnts
    # using shortc instead of sc so not to be confused with 
    # sub command abbrehviations 
    shortc_obj = c.fetchall()
    # close the databse connection
    conn.close()
    # return the sqlite3.cursor object
    return shortc_obj

def sql_dmg_brackets():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # Return a list of items instead of 1 item tuples 
    conn.row_factory = lambda cursor, row: row[0]
    # make an sqlite connection object
    c = conn.cursor()
    # creates a variable and assigns the list of ship names to it
    dmg_obj = c.execute('''SELECT amount FROM ship_damage''').fetchall()
    # close the databse connection
    conn.close()
    # return a list of ship names
    return dmg_obj

def dmg_bracket_list():
    dmg_list = []
    for i in sql_dmg_brackets():
        dmg_list.append(i)
    return dmg_list




33234234234

def sql_arg_list():
    # connect to the sqlite database
    conn = sqlite3.connect('rocbot.sqlite')
    # Return a list of items instead of 1 item tuples 
    conn.row_factory = lambda cursor, row: row[0]
    # make an sqlite connection object
    c = conn.cursor()
    # creates a variable and assigns the list of ship names to it
    dmg_obj = c.execute('''SELECT name FROM shortcut''').fetchall()
    # close the databse connection
    conn.close()
    # return a list of ship names
    return dmg_obj

def arg_parse_list():
    dmg_list = []
    for i in sql_arg_list():
        dmg_list.append(i)
    return dmg_list

def argument_parser(sc, arg1):
    clean_arg1 = sanitise_input(arg1)
    if sc == 'dmg':
        dmg_bracket = process.extractOne(clean_arg1, dmg_bracket_list())
        return dmg_bracket[0]
    else:
        if len(clean_arg1) <= 4:
            shortcut = shortcut_obj(clean_arg1.lower())
            if len(shortcut) > 0:
                return shortcut[0]['name']
        else:
            arg_found = process.extractOne(clean_arg1, arg_parse_list())
            return arg_found[0]

def get_em_colour(arg1):
    embed_colours = {"Shield Breaker": 0x3a77f9, "High Impact": 0xee4529, "Armor Piercing": 0xffb820}
    return embed_colours[arg1]
    