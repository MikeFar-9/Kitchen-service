# Kitchen Service

## 🧑‍🍳 Overview

**Kitchen Service** is a kitchen management system for restaurants. 
The project helps improve communication among chefs by allowing them to create new dishes, 
organize them by type, and assign responsible chefs for each dish.

Imagine you're a restaurant owner wanting to enhance collaboration and order in your kitchen — this system 
is built exactly for that purpose. 
It streamlines your operations, ensures accountability, and keeps everything organized.

## 🚀 Features

- 🔪 **Cook management** – Create, edit, and remove cooks.
- 🥕 **Ingredient management** – Add, update, and delete ingredients.
- 🍽️ **Dish management** – 
  - Create, update, and remove dishes.
  - Assign chefs to dishes.
  - Specify ingredients and quantities per dish.
  - Add preparation time for each dish.
- 🧠 Dish categorization via types.

## 📦 Technology Stack

- **Backend:** Django 5.2
- **Language:** Python 3.12

## Login
- **username:** bestcook
- **password:** cookbest1234321

## Installation
1. **Clone the repository:** 

git clone https://github.com/MikeFar-9/Kitchen-service.git

## 2. Creating and activating a virtual environment
**For Windows:** 

python -m venv venv
venv\Scripts\activate
 

**For macOS/Linux:** 

python3 -m venv venv
source venv/bin/activate

## 3. Install dependencies
pip install -r requirements.txt

## 4. Apply database migrations
python manage.py migrate
