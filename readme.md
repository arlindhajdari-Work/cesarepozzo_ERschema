
# CSV to JSON Conversion Documentation

## Process Overview
This document outlines how we used AI-assisted tools to convert a complex CSV file
(`mergelabelsCesare.csv`) into a structured JSON file (`tiddlers_v2.json`).

## Tools Used
- **Visual Studio Code** (primary code editor)
- **Cody AI** (by Sourcegraph for code analysis and generation)
- **Aider** (AI pair programming tool)

## Workflow Steps

### 1. Data Preparation
- Started with `mergelabelsCesare.csv` containing CRM entity definitions
- CSV structure included:
  - Entity definitions
  - Attribute mappings (Italian/English)
  - Entity relationships under the "Con un entita"/"Con varie entita"

### 2. Prompting Aider 
- We used Aider with openrouter/deepseek/deepseek-chat-v3-0324:free models
- We gave it the following initial prompt:

    "i want to create a json file to import to tiddlywiki with multiple tiddlers, where each tiddler is represented by the entity in the database, the file defines the structure of the database as such: there are the names of the entities, the names of their respective fields, in the second column there are the names of the field as defined in the database, and under the section 'con uno entita' it represented are the 1-to-1 relations, and 'con varie entita' represented are the many-to-many or many-to-one relations, the tiddlers will be used to create an ER schema of the database in tiddlywiki, using tiddlymap. In tiddlymap, the structure for defining nodes(tiddlers) and relations is as follows: 

{
  "title": "tiddlerName",
   "tags": "ENTITY CRM",
  "text": [[relatedTable1]] , [[relatedTable2]] "
  }

where the title is the name of the table, in the text there are the tables which are linked to the title table, and tags are like the ones given in the example . Following this example, generate a json file for the data in the csv file for all of the tables of the database."

- Since the LLM would not generate all the entities at once, we had to ask it to "continue with the others", even this approach resulted ineffective as it eventually started looping/going over the same tables.

- What we did was to extract all of the names of the entities manually  and to pass them in batches to the LLM, which proved significantly faster and more effective.

- However, the LLM was not able to catch all of the relations between the entities and format them appropriately, so, most of them had to be manually entered into the respective json objects. Here is where Cody (the VSCode Extension, Copilot could also work), to insert the relations manually


Key Challenges 

1. LLM was not all too familiar with tiddler syntax, so we had to teach it the proper formatting.
2. The LLM was not able to capture the data for each entity properly, this was also affected by the fact that the CSV file was not properly structured and easily readable.
3. A lot of manual work had to be done to reach the current state of the tiddlywiki, which might not prove effective in the long run.

Future Possible Solutions

1. Implementing the export functionality, which will provide a well structured and easy to understand CSV file of all the modules, or even for specific modules.
2. Automating the tiddler generation by using some sort of script, which takes the CSV as input, and produces the JSON file (This was experimented with, during this process, but proved ineffective due to improper CSV structure)


## Final Output

Generated tiddlers_v2.json containing:

 • 100+ CRM entity definitions
 • Attribute mappings
 • Entity relationships in the 
 • Bilingual text preservation


