# from sklearn.tree import DecisionTreeClassifier
# import pandas as pd 


# music_data=pd.read_csv("music.csv")
# x=music_data.drop(columns=['genre'])


# print(music_data)
def something(n):
    if n%2 !=0:
        return("weird")
    elif n%2==0 and n>=2 and n<=5:
        return ("Not Weird")
    elif n%2==0 and n>=6 and n<=20:
        return("Weird")
    elif n%2==0 and n>20:
        return("Not weird")


print(something(9))