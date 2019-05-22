#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 17:54:04 2019

@author: carlosponce
"""

class Category(object):
    
    # List of category names
    category_names = []
    categories = []
    
    def __init__(self, name):
        self.name = name
        self.subcategories = []
        self.categories.append(self)
        self.category_names.append(name)
        self.codes = []
    
    def add_sub(self, subcategory):
        if subcategory not in self.subcategories:
            self.subcategories.append(subcategory)
            subcategory.add_supercat(self)
            
    def get_name(self):
        return self.name
    
    def get_subcategories(self):
        return self.subcategories
            
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    
class Subcategory(Category):
    
    category_names = []
    categories = []
    
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
    
    def __init__(self,name):
        Subcategory.__init__(self, name)
        
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
    
    return [categories, subcategories, subcategories2]

categories, subcategories, subcategories2 = load_categories('categories.csv')
#
#print('There are ' +str(len(subcategories2))+ ' subcategories2.')
#
#print(str(len(categories)))
#print()
#print(str(len(subcategories)))
#print()
#print(str(len(subcategories2)))

# Test supercategories
#for i in subcategories:
#    print(i, 'belongs in', i.get_supercat())

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
        
#print(categories[0].__class__.__name__)
        





























