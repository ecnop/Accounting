#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 16:11:44 2019

@author: carlosponce
"""
# Function to create the accounts dictionary
# Accounts dictionary maps account abbreviation to its full name for money pro
def load_acc_dic(file):
    f = open(file, 'r')
    f.readline() # ignore header
    dic = {}
    for line in f:
        split = line.rstrip().split(',')
        if split[0] != '':
            dic[split[0]] = [split[1],split[2]]
    f.close()
    print('Loaded ' + str(len(dic)) + ' accounts...')
    return dic
    
# Function to create the dictionaries for categories, subcategories, subcategories2
# Category dictionary maps the first word in lower case of a category to its
# full name with proper capitalization
# The subcategory dictionary maps the first word in lower case of a subcategory
# to a list, whose entries are, in order: full name, category
# The subcategory2 dictionary maps the first word in lower case of a subcategory2
# to a list, whose entires are, in order: full name, category, subcategory

# Classes to contain the categories and subcategories and be able to manipulate
# the information in a more versatile way
    
class Category(object):
    
    # List of category names
    category_names = []
    categories = []
    categories_first_lower = {} # maps first lower case word in name to its category
    
    def __init__(self, name):
        self.name = name
        self.subcategories = []
        self.categories.append(self)
        self.category_names.append(name)
        self.codes = []
        self.name_lower = name.split()[0].lower()
        self.categories_first_lower[self.name_lower] = self
    
    def add_sub(self, subcategory):
        if subcategory not in self.subcategories:
            self.subcategories.append(subcategory)
            subcategory.add_supercat(self)
            
    def get_name(self):
        return self.name
    
    def get_all_names(self):
        return self.category_names
    
    def get_num_words(self):
        split = self.name.split()
        return len(split)
    
    def get_subcategories(self):
        return self.subcategories
    
    def get_all_lower(self):
        return self.categories_first_lower.keys()
            
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    
class Subcategory(Category):
    
    category_names = []
    categories = []
    categories_first_lower = {}
    
    def __init__(self,name):
        Category.__init__(self, name)
        self.supercat = 0 # this is not really needed, but w/e
        
    def add_supercat(self, supercat):
        self.supercat = supercat
        
    def get_supercat(self):
        return self.supercat
    
class Subcategory2(Subcategory):
    
    category_names = []
    categories = []
    categories_first_lower = {}
    
    def __init__(self,name):
        Subcategory.__init__(self, name)
        
    def add_sub(self, subcategory):
        raise ValueError('Subcategory2 elements cannot have a subcategory. At least not yet.')
        
def is_in(categories, word):
    # Returns true if the lower case of the word is in the lower case first word 
    # list for the category list
    return word.lower() in categories[0].get_all_lower()

def find_cat(word, categories):
    # Returns the category given a word and the list of categories
    # it assumes the word is in the categories_first_lower list for the respective category
    return categories[0].__class__.categories_first_lower[word.lower()]
    
def find_cat_and_numwords(word, categories):
    # Returns a tuple:
    # First value is the category's name given a word and the list of categories
    # it assumes the word is in the categories_first_lower list for the respective category
    # Second value is the amount of words in the category's name
    category = categories[0].__class__.categories_first_lower[word.lower()] # Goes into the dic of categories_first_lower and gets the category from it
    a = category
    b = category.get_num_words()
    return (a, b)

def find_cat_and_numwords_within_supercategory(word, supercategory):
    # Returns a tuple:
    # First value is the category's name given a word and the category it must belong to.
    # It tries to find the word within the category, if it can't find it it means that the 
    # subcat is not part of that cat and raises a ValueError. Assumes word is a category that exists, but may not be within the supercategory
    # Second value is the amount of words in the category's name
    category = supercategory.get_subcategories()[0].__class__.categories_first_lower[word.lower()] # Goes into the dic of categories_first_lower and gets the category from it
    if category not in supercategory.get_subcategories():
        raise ValueError('Subcategory \"' + str(category) + '\" not found within category \"' + str(supercategory) + '\"')
    else:
        a = category
        b = category.get_num_words()
        return (a, b)

def extend(ext, split_line, current_index):
    # Returns ext if extending the current index by ext on the split_line list 
    # doens't raise an Index Error. Returns 0 otherwise
    try:
        a = split_line[current_index + ext]
        a = 0
        ext += a
    except IndexError:
        ext = 0
    return ext

# Function to load the categories from the categories file into instances of those
# categories
def load_categories(file):
    categories = []
    subcategories = []
    subcategories2 = []
    
    f = open(file, 'r')
    f.readline() # Ignore header
    for line in f:
        split = line.rstrip().split(',')
        a = split[0]
        b = split[1]
        c = split[2]
#        d = split[3]
        if a not in Category.category_names:
            category = Category(a)
            categories.append(category)
        else:
            for i in Category.categories:
                if i.get_name() == a:
                    category = i
        
        if b not in Subcategory.category_names:
            subcategory = Subcategory(b)
            subcategories.append(subcategory)
        else:
            for i in Subcategory.categories:
                if i.get_name() == b:
                    subcategory = i
        
        if c not in Subcategory2.category_names and c != '':
            subcategory2 = Subcategory2(c)
            subcategories2.append(subcategory2)
        else:
            for i in Subcategory2.categories:
                if i.get_name() == c:
                    subcategory2 = i
        
        category.add_sub(subcategory)
        if c != '':
            subcategory.add_sub(subcategory2)
        
    f.close()
    
    print('Loaded ' + str(len(categories)) + ' Categories, ' +
                      str(len(subcategories)) + ' Subcategories, ' +
                      str(len(subcategories2)) + ' Subcategories2...')
    
    return [categories, subcategories, subcategories2]

# Functions to print the categories with their respective subcategories, to check
# that the categories have been loaded correctly
def printout(categories):
    for i in categories:
        if i.get_subcategories() != []:
            for j in i.get_subcategories():
                if j.get_subcategories() != []:
                    for k in j.get_subcategories():
                        print(str(i)+', '+str(j)+', '+str(k))
                else:
                    print(str(i)+', '+str(j))
        else:
            print(i)
                
#printout(categories)
            
def printnice(categories):
    # categories is the list of main categories
    # First, create a list of lists of all the data to make into columns
    data = []
    
    for i in categories:
        if i.get_subcategories() != []:
            for j in i.get_subcategories():
                if j.get_subcategories() != []:
                    for k in j.get_subcategories():
                        data.append([i.get_name(),j.get_name(),k.get_name()])
                else:
                    data.append([i.get_name(),j.get_name(),''])
        else:
            data.append(i.get_name(),'','')
    
    def get_max_len_cols(array):
        ans = []
        min_val = min(len(row) for row in array)
        for i in range(min_val):
            a = max(len(str(row[i])) for row in array)
            ans.append(a)
        return ans    
        
    max_lens = get_max_len_cols(data)
    
    for row in data:
        for i in range(len(max_lens)):
            print(row[i].ljust(max_lens[i]), end='  ')
        print()
    
#printnice(categories)

class Entry(object):
    
    def __init__(self, day, line, categories_lists, accounts): # categories is the list of cats, subcats, sub2
        self.day = day
        self.category = ''
        self.subcategory = ''
        self.subcategory2 = ''
        self.account = ''
        self.amount = 0
        self.description = ''
        self.description_short = ''
        
        def fill(line, categories_lists, accounts):
            categories = categories_lists[0]
            subcategories = categories_lists[1]
            subcategories2 = categories_lists[2]
            
            split = line.split()
            self.amount = split[0] # amount is always the first info
            word = 1 # counter for the word in the line/entry
            if split[word] in accounts:
                self.description_short = ' '.join(split[(2):])
                self.account = accounts[split[word]][0] #accounts is a dic that maps the abbreviation to a list of the name of the account 
                                                        # and how it appears (or should appear) in the note entries
                ext = len(accounts[split[word]][1].split())
                word += ext
#                print(ext, word, split[word])
                if is_in(categories, split[word]):
                    self.category, ext = find_cat_and_numwords(split[word], categories)
                    word += extend(ext, split, word)
                    if is_in(subcategories, split[word]):
                        self.subcategory, ext = find_cat_and_numwords_within_supercategory(split[word], self.category)
                        word += extend(ext, split, word)
                        if is_in(subcategories2, split[word]) and self.subcategory.get_subcategories() != []: # Added the and statement so that adding words to the description that match a subcategory2 doesn't screw te algorithm:
                            self.subcategory2, ext = find_cat_and_numwords_within_supercategory(split[word], self.subcategory)
                            word += extend(ext, split, word)
                elif is_in(subcategories, split[word]):
                    self.subcategory, ext = find_cat_and_numwords(split[word], subcategories)
                    self.category = find_cat(split[word], subcategories).get_supercat()
                    word += extend(ext, split, word)
                    if is_in(subcategories2, split[word]) and self.subcategory.get_subcategories() != []: # Added the and statement so that adding words to the description that match a subcategory2 doesn't screw te algorithm
                        self.subcategory2, ext = find_cat_and_numwords_within_supercategory(split[word], self.subcategory)
                        word += extend(ext, split, word)
                elif is_in(subcategories2, split[word]):
                    self.subcategory2, ext = find_cat_and_numwords(split[word], subcategories2)
                    self.subcategory = find_cat(split[word], subcategories2).get_supercat()
                    self.category = find_cat(split[word], subcategories2).get_supercat().get_supercat()
                    word += extend(ext, split, word)
            else:
                self.description_short = ' '.join(split[(1):])
                if is_in(categories, split[word]):
                    self.category, ext = find_cat_and_numwords(split[word], categories)
                    word += extend(ext, split, word)
                    if is_in(subcategories, split[word]):
                        self.subcategory, ext = find_cat_and_numwords_within_supercategory(split[word], self.category)
                        word += extend(ext, split, word)
                        if is_in(subcategories2, split[word]) and self.subcategory.get_subcategories() != []: # Added the and statement so that adding words to the description that match a subcategory2 doesn't screw te algorithm:
                            self.subcategory2, ext = find_cat_and_numwords_within_supercategory(split[word], self.subcategory)
                            word += extend(ext, split, word)
                elif is_in(subcategories, split[word]):
                    self.subcategory, ext = find_cat_and_numwords(split[word], subcategories)
                    self.category = find_cat(split[word], subcategories).get_supercat()
                    word += extend(ext, split, word)
                    if is_in(subcategories2, split[word]) and self.subcategory.get_subcategories() != []: # Added the and statement so that adding words to the description that match a subcategory2 doesn't screw te algorithm
                        self.subcategory2, ext = find_cat_and_numwords_within_supercategory(split[word], self.subcategory)
                        word += extend(ext, split, word)
                elif is_in(subcategories2, split[word]):
                    self.subcategory2, ext = find_cat_and_numwords(split[word], subcategories2)
                    self.subcategory = find_cat(split[word], subcategories2).get_supercat()
                    self.category = find_cat(split[word], subcategories2).get_supercat().get_supercat()
                    word += extend(ext, split, word)
                        
            self.description = ' '.join(split[1:])
        
        fill(line, categories_lists, accounts)
            
    def get_category(self):
        return self.category
    
    def get_subcategory(self):
        return self.subcategory
    
    def get_subcategory2(self):
        return self.subcategory2
    
    def get_day(self):
        return self.day
    
    def get_account(self):
        return self.account
    
    def get_amount(self):
        return self.amount
    
    def get_categories(self):
        if self.subcategory2 == '':
            if self.subcategory == '':
                cat = self.category.get_name()
            else:
                cat = self.category.get_name() + ' : ' + self.subcategory.get_name()
        else:
            cat = self.category.get_name() + ' : ' + self.subcategory.get_name() + ' : ' + self.subcategory2.get_name()
        return cat
    
    def __str__(self):
        return self.day + ' ' + self.amount + ' ' + self.description + '; ' + self.get_categories()
    
    def __repr__(self):
        return str(self)
        
## Testing the Entry class
#accounts_file = 'acc_dic.csv'
#categories_file = 'categories.csv'
#accounts = load_acc_dic(accounts_file)
#categories = load_categories(categories_file)
#
#line = '25.55 cmb skin care this is a test'
#
##print(categories)
#
#entry = Entry('3', line, categories, accounts)
#
#print(entry)
#print('day =',entry.get_day())
#print('amount =', entry.get_amount())
#print('account =', entry.get_account())
#print('category =', entry.get_category())
#print('subcategory =', entry.get_subcategory())
#print('subcategory2 =', entry.get_subcategory2())

## Print categories and categories[0]
#print(categories)
#print()
#print(categories[0])
#print()

# Function to process the information and create the entries that we'll use to
# print whatever we need
def get_entries(inFile, categories, accounts): # categories is a list of categories, subcategories, sub2

    f_input = open(inFile, 'r')

    lines = []
    
    # List of entries
    entries = []
    
    # Read the file and put each line into a list
    for line in f_input:
        lines.append(line.rstrip())
    
    for line in lines:
        if len(line) == 0:
            continue
        if line[-1] == ':':
            day = line[:-1]
            continue
        entries.append(Entry(day, line, categories, accounts))

    f_input.close()
    
    # Return the list of entries
    return entries

### Test the get_entries method
## Load the accounts dictionary and the categories csv
#accounts_file = 'acc_dic.csv'
#categories_file = 'categories.csv'
#
#accounts = load_acc_dic(accounts_file)
#categories = load_categories(categories_file)
#
## Define the entry file
#inFile = 'Test input.txt'
#
### Print categories and categories[0]
##print(categories)
##print()
##print(categories[0])
##print()
#
## Load the entries into a list of entries
#entries = get_entries(inFile, categories, accounts)
#
## Test the results
#for entry in entries:
#    print(entry)


## Funtion that creates a csv output for google sheets
def write():
    # Load the accounts dictionary and the categories csv
    accounts_file = 'acc_dic.csv'
    categories_file = 'categories.csv'
    
    accounts = load_acc_dic(accounts_file)
    categories = load_categories(categories_file)
    
    # Define the entry file and output files
    inFile = 'Evernote.txt'
    outSheets = 'sheets.csv'
    outMoney = 'money.csv'
    separator = ','
    
    # Get the entries from the input file
    entries = get_entries(inFile, categories, accounts)
    
    # Create a sheets.csv with the appropriate format
    f_sheets = open(outSheets,'w+')
    for entry in entries:
        f_sheets.write(entry.day + separator +
                       entry.amount + separator +
                       entry.description_short + separator +
                       str(entry.category) + separator + 
                       str(entry.subcategory) + separator + 
                       str(entry.subcategory2) + separator +
                       entry.account + "\n")
    
    f_sheets.close()
    
    
    # Now print into the money file
    f_money = open(outMoney,'w+')
    
    # Print the header for the money file
    header = 'Date,Amount,Account,Amount received,Account (to),Balance,' \
                + 'Category,Description,Transaction Type,Agent\n'
    f_money.write(header)
    
    for entry in entries:
        # Establish what is going to be printed in the category column
        if entry.subcategory2 != '':
            if entry.subcategory.get_name() == 'Groceries':
                category = 'Groceries: ' + str(entry.subcategory2)
            else:                
                category = str(entry.category) + ': ' + str(entry.subcategory2)
        else:
            category = str(entry.category) + ': ' + str(entry.subcategory)
        # Print the entries according to the money format
        f_money.write(entry.day + separator + # Day
                       entry.amount + separator + # Amount
                       entry.account + separator + # Account
                       '' + separator + # Amount received
                       '' + separator + # Account (to)
                       '' + separator + # Balance
                       category + separator + # Category in a custom format according to above if
                       entry.description_short + separator + # Description for the money output
                       'Expense' + separator + # Transaction Type should always be Expense until I try to incorporate Income
                       '' + "\n") # Agent
    
    f_money.close()

    print('Wrote a total of ' + str(len(entries)) + ' entries into ' + outSheets + ' and ' + outMoney)
    


if __name__ == '__main__':
    
    # Create the sheets and money csv
    write()
    
    # Printout the categories to check them
#    categories = load_categories('categories.csv')[0]
#    printnice(categories)















                
                
    
    
    
    
    



