import re
import pandas as pd
from nltk.corpus import stopwords
import os

# creating stopwords list using nltk package
stop_words = stopwords.words("english")


# function for creating dataframe of comments from files such as .csv, .xlsx and .txt
def get_comments_from_file(path):

    # If file name ends with .csv read using pandas
    if re.search("\.csv$", path):
        comments = pd.read_csv(path)
        comments.columns = ["comment"]
    
    # same with excel file
    elif re.search("\.xlsx$", path):
        comments = pd.read_excel(path)
        comments.columns = ["comment"]

    # file name ending with .txt file
    elif re.search("\.txt$", path):
        with open(path, "r") as f:
            text = f.read()
            # Assuming comments are separated using newline character
            text_comments = text.split("\n")
            comments = pd.DataFrame({"comment":text_comments})
    return comments


# Function for getting profanity score of the comment
def get_profanity_score(bad_words, comments_file_path):
    
    # Here I am assuming racial slur / bad words are provided in list/tuple format.
    # If provided comments is path to the file then call get_comments_from_file() function or I am assuming they are list/tuple.
    if type(comments_file_path) == str:
        try:
            if os.path.isfile(comments_file_path):
                data = get_comments_from_file(comments_file_path)
            else:
                return f"{comments_file_path} file doesn't exist"
        except:
            return f"There is an encoding or other error in file path"
    else:
        data = pd.DataFrame({"comment":comments_file_path})
    
    # looping through comments
    i = 0
    for comment in data["comment"]:
        # changing comments to lower case
        comment = comment.lower()
        count = 0   # represets total no. of racial slurs or bad words present in comments

        for word in bad_words:
            word = word.lower()
            # using regex to find racial slurs or bad words present in comments
            count = len(re.findall(word, comment)) + count
        
        # cleaning comment 
        comment = re.sub("[^a-z']", " ", comment)
        comment = re.sub("\s+", " ", comment)
        comment = comment.split()

        # removing stopwords
        cleaned_comment = []
        for word in comment:
            if word not in stop_words:
                cleaned_comment.append(word)
        
        # genarating profanity score which lies in 0-1 
        # 0 means comment is not profane and 1 means all words are racial slurs or bad words
        score = count / len(cleaned_comment)

        # saving score in dataframe
        data.loc[i,"Profanity_score"] = score
        i += 1

        # returning the comments with profanity score
    return data


if __name__ == "__main__":
    bw = ["badword1", "badword2", "badword3", "badword4", "badword5"]
    obj = get_profanity_score(bw, "Comments_File.txt")
    print(obj)
