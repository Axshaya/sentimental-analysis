from django.shortcuts import render
from django.http import HttpResponse
import random;
import openai
import os
import textwrap
import google.generativeai as genai

GOOGLE_API_KEY=''
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

x = []

sentiment = ""

def to_markdown(text):
  text = text.replace('•', '  *')
  return textwrap.indent(text, '', predicate=lambda _: True)


def home(request):
    global x
    length=request.GET.get('length')
    instructions = f""" You are given with a role of a psychiatrist. You will be provided with a sentence delimited within triple backticks or an paragraph and you should analyse the sentiment of the paragraph and tell the emotions of the writer of the paragraph.
    
    - If the sentence is about any context other than sentiment analysis, then you should return Iam designed for sentiment analysis only. This is very important. For example if the sentence is about coding a software, then tell Iam designed for sentiment analysis only.
    
    -sentence = ```{length}```

    -You should not assist them in any other context other than sentiment analysis. you should say Iam designed for sentiment analysis only if the context is not about sentiment analysis.
    
    """
    
    # thepassword = get_completion(instructions)

    response = model.generate_content(instructions)
    result = to_markdown(response.text)
    chatbot_response = result
    sentiment = result
    x.append(chatbot_response)
    return render(request, 'generator/home.html', {'password': chatbot_response })



def password(request):
    global x
    global sentiment
    length=request.GET.get('length')
    instructions = f""" You are given with a role of a psychiatrist. You will be provided with a sentence delimited within triple backticks or an paragraph and you should analyse the sentiment of the paragraph and tell the emotions of the writer of the paragraph.
    
    - If the sentence is about any context other than sentiment analysis, then you should return I dont know. This is very important. For example if the sentence is about coding a software, then tell I dont know.
    
    -sentence = ```{length}```

    -You should not assist them in any other context other than sentiment analysis. you should say I dont know if the context is not about sentiment analysis.
    
    """
    
    # thepassword = get_completion(instructions)

    response = model.generate_content(instructions)
    result = to_markdown(response.text)
    chatbot_response = result
    sentiment = result
    x.append(chatbot_response)

    return render(request, 'generator/home.html', {'password': chatbot_response })

def give_feedback(request):
    global x
    global sentiment

    instructions = f""" You are given with a role of a psychiatrist. You will be provided with a sentence delimited within triple backticks. The sentence sentiments of the user.
    
    - You have to give the feedback to the user and some suggestions for the user to be followed in the future so that he will get a happy mood.
    
    -paragraph = ```{sentiment}```

    -please dont give the array as the response.

    -do not use bold texts.

    -Use only english. seperate lines with line breaks. this is important.

    - Give a single paragraph answer within 100 words. this is very very important.

    """

    response = model.generate_content(instructions)
    result = to_markdown(response.text)
    chatbot_response = result

    return render(request, 'generator/feedback.html', {'password': chatbot_response })


def generate_report(request):
    global x
    global sentiment

    instructions = f""" You are given with a role of a psychiatrist. You will be provided with a array delimited within triple backticks. The array consists of the past sentiment analysis of the user.
    
    - You have to give the overall report to the user based on the past sentiments in the array. consider the array is sorted that is first element in the array is the first sentiment, and the last is the latest sentiment.
    
    -paragraph = ```{x}```

    -please dont give the array as the response.

    -do not use bold texts.

    -Use only english. seperate lines with line breaks. this is important.

    - Give a single paragraph answer within 250 words. this is very very important.

    """

    response = model.generate_content(instructions)
    result = to_markdown(response.text)
    chatbot_response = result
    return render(request, 'generator/about.html', {'password': chatbot_response })



def about(request):
    return render(request,'generator/about.html')

# def get_completion(prompt, model="gpt-3.5-turbo"): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0, # this is the degree of randomness of the model's output
#     )
#     return response.choices[0].message["content"]













