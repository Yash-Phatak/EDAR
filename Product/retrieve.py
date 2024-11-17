from pymongo import MongoClient
import json
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from datetime import datetime  # Correct import
# Replace with your MongoDB cloud connection string
client = MongoClient("mongodb+srv://adityagautam1911:pB71om2iNw5yEWmi@cluster0.frx2v.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

def summarize_text(text, sentence_count=2):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)  # Number of sentences in summary
    return ' '.join(str(sentence) for sentence in summary)

def retrieve_recent_data():
    # Access a specific database
    db = client["news_db"]
    # Access a specific collection within the database
    collection = db["articles"]
    # Retrieve documents from the collection
    documents = collection.find()
    # Create a list to hold each document as a dictionary
    documents_list = []
    # Process each document in the cursor
    for doc in documents:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string for JSON compatibility
        # Convert any datetime fields to strings
        for key, value in doc.items():
            if isinstance(value, datetime):  # Check for datetime type
                doc[key] = value.isoformat()  # Convert datetime to ISO format string
        
        documents_list.append(doc)  # Append the dictionary to the list
    # Save the list of dictionaries to a JSON file
    with open("data/retrieve.json", "w") as file:
        json.dump(documents_list, file, indent=4)
    print("Data saved to retrieve json")

def preprocess_scraped_data():
    with open('data/retrieve.json','r') as file:
        data = json.load(file)
    updated_data = [] # updated json
    for item in data:
        _id = item.get('_id')
        title = item.get('title')
        content = item.get('content')

        #Summarise the content 
        if content=="No content found" or content=="":
            summary = ""
        else:
            summary = summarize_text(content)
        new_item = {
            "_id":_id,
            "text": title + summary
        }
        updated_data.append(new_item)

    with open('data/summarized_data.json','w') as file:
        json.dump(updated_data,file,indent=4)
    print("data saved.")


