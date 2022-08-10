# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 15:58:16 2022

@author: behira
"""
# Headers 
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
import pandas as pd
from scipy.io import loadmat 
from PIL import Image
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
# ---------------------------------
class word_cloud_plot:
    
    def __init__(self, path_csv, path_color):
        self.path_csv     = path_csv
        self.path_color   = path_color
    
    def read_dat(self, tsk):
        # load colors
        col = loadmat(self.path_color)
        if tsk == 'EP':
            self.col = col["col"][0]
        elif tsk == 'SJ':
            self.col = col["col"][3]
    
        # Reads 'iES CSV' file
        df = pd.read_csv(self.path_csv) # includes Patien_sAdVerbatimSubjectiveReport
        self.df = df.loc[(df['task'] == tsk) & (df['Tval'] > 1) & (df['Hot_1_OrCold_0_'] == 1)]
            
    def parse_prompt(self):                
        self.comment_words = ""
        # iterate through the csv file
        for val in self.df.Pateint_sAdVerbatimSubjectiveReport:
     
            # typecaste each val to string
            val = str(val)
 
            # split the value
            tokens = val.split()
            
            # Converts each token into lowercase
            for i in range(len(tokens)):
                    tokens[i] = tokens[i].lower()   
                    self.comment_words += " ".join(tokens)+" "
def one_color_func_EP(word = None, font_size = None,
                   position = None, orientation = None,
                   font_path = None, random_state = None):
    
    
    
    if font_size >= 85:
        # This HSL is for the green color
         h = 0
         s = 62
         l = 45
    else:
         h = 29
         s = 62
         l = 0
    return "hsl({}, {}%, {}%)".format(h, s, l) 
   
  

def main(task):
    #
    
    path_csv   = 'data.csv'
    path_color = 'foster_col.mat'
    # create wordcloud object 
    word_cloud_obj = word_cloud_plot(path_csv= path_csv, path_color=path_color)
    # reading data
    word_cloud_obj.read_dat(task)
    
    # parsing the prompt
    word_cloud_obj.parse_prompt()
    
    comment_words = ''
    stopwords = set(STOPWORDS)
    # load oval mask
    mask = np.array(Image.open(r'oval_mask.png'))
    # colors

    if task == 'EP':
        wordcloud = WordCloud(width = 800, height = 800,    
                background_color ='white',
                stopwords = stopwords,
                mask= mask,
                min_font_size = 10,
                max_font_size = 100,
                color_func= one_color_func_EP).generate(word_cloud_obj.comment_words)
        
 
    # plot the WordCloud image                      
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig('word_cloud' + task +'.png')
    plt.show()
   
    
if __name__ == '__main__':
    task = 'EP'
    main(task)
    