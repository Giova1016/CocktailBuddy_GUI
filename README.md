# CocktailBuddy App

This project is a working prototype for a GUI integrated with databases using the SQLite3 Python module.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)

## Introduction

This is a project made for a computer engineering course. The project's purpose was to create a working GUI for the idea we came up with during the course, in our case a Mocktail suggesting application based on user preferences.
This project helped us learn how to create a working GUI and integrate SQLite databases to improve it further.

## Features

In this app, users can:
- Register and log in with their saved credentials.
- Select their desired preferences from a list of mocktail flavors along with levels of preferred sweetness/bitterness.
- Be shown a list of Beverages, from a database with 34 different mocktails, that meet their preferences or at least some of them. 

## Installation

To install the project you can follow this guide:
- It is required for you to have a working Python interpreter, you can download it in the official website or from the Microsoft store.
- Once that is done, I recommend you change the directory to the one you would like to clone this repository, preferably an easy-to-access one like the Desktop.
- This can be done very easily, just like the following examples:

In a machine with Linux or in the Windows PowerShell, you can go to the terminal and type: 

```
cd directory
```
- Next, make a Python virtual environment with the following command.

```
python<version> -m venv <virtual-environment-name>
```

- Here is an example of what it would look like if you were to do it on a Linux machine and make a new directory.

```bash
cd Desktop
mkdir Project
cd Project
python -m venv env
```

- Next, you can copy and paste the following commands into your terminal in the same order they are written.
- Clone the repository

```bash
git clone https://github.com/Giova1016/CocktailBuddyAppDownload.git
```

- Navigate to the project directory

```bash
cd CocktailBuddyApp
```

- Install the required dependencies

```bash
pip install -r requirements.txt
```
- Lastly you can run the .py file conrainkng the code with rhe following command
```
python<version> <file_name>.py
```

## Contributing
I want to thank my friend [@Omar-Torres11](https://github.com/Omar-Torres11) for helping me write some of the code for this project. You were an amazing help during the time we spent making this GUI.
