HR Policies RAG Chatbot

Welcome to the HR Policies RAG Chatbot project! This chatbot uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers about HR policies of EnFuse Solutions.

Table of Contents : 

Overview

Features

Architecture

Setup Instructions

Usage

Technologies Used

Folder Structure

Future Enhancements

Contributing


Overview : 

The HR Policies RAG Chatbot is designed to:

Help employees quickly find and understand HR policies.

Provide reliable and contextually relevant answers by combining document retrieval and generative AI.

Reduce dependency on HR personnel for repetitive queries.

Features : 

Intelligent Query Understanding: Processes natural language questions with advanced NLP techniques.

RAG Framework: Combines retrieval from a document database with a generative AI model for context-aware answers.

Interactive Chat Interface: Provides a user-friendly interface for employees.

Steps

Clone the repository:

git clone <repo-link>
cd hr-policies-rag-chatbot

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

Create a .env file with necessary credentials (API keys, URL, etc.).

Run the frontend:

chainlit run main_1.py

Access the chatbot at http://localhost:3000.

Usage

Upload HR policy documents via the admin interface.

Ask questions in the chatbot interface, e.g., "What is the leave policy?"

Get accurate answers with links to relevant sections in the policy documents.
