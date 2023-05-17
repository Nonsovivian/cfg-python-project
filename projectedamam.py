import requests
import csv
import pandas as pd


# function for searching the edamam API recipes based on user specified search term and dish type
def query_recipe_api(ingredient, want_quick_recipes, type_of_dish):
    app_id = '9998b3db'
    app_key = '90ba3a3c5c54c0c001a42780546f2a12'
    # if user has said they only want quick recipes than include filter in API request for max time of 45 minutes
    if want_quick_recipes:
        time = '45'
        result = requests.get('https://api.edamam.com/search?q={}&app_id={}&app_key={}&time={}&dishType={}&to=20'.format(ingredient, app_id, app_key, time, type_of_dish))
    else:
        result = requests.get('https://api.edamam.com/search?q={}&app_id={}&app_key={}&dishType={}&to=20'.format(ingredient, app_id, app_key, type_of_dish))

    data = result.json()
    # return list of recipes from API
    return data['hits']


# function for asking the user to specify search terms, then calls function to query recipe API
# and saves the results to a CSV
def new_recipe_search():
    ingredient = input('Enter an ingredient/food item to search for in the recipe database: ')

    time_check = input('Would you like to only see quick recipes (45 minutes or less)? y/n: ')
    if time_check.lower() == 'yes' or time_check.lower() == 'y':
        want_quick_recipes = True
    else:
        want_quick_recipes = False

    type_of_dish = input('What type of dish would you like to search for?:'
                         'starter/main course/desserts? ')
    while type_of_dish.lower() != 'starter' and type_of_dish.lower() != 'main course' and type_of_dish.lower() != 'desserts':
        type_of_dish = input('Sorry we did not recognise that. Please enter starter, main course or desserts ')

    recipe_results = query_recipe_api(ingredient, want_quick_recipes, type_of_dish)

    # if no recipe results from search flag this to the user, otherwise loop through recipes and write
    # them to a csv
    if len(recipe_results) == 0:
        print('Sorry we did not find any recipes with that ingredient/food item.')
    else:
        with open('recipe_results.csv', 'w+') as csv_file:
            field_names = ['label', 'yield', 'totalTime', 'url', 'ingredientLines']
            spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names, extrasaction='ignore')
            spreadsheet.writeheader()

            for result in recipe_results:
                recipe = result['recipe']
                recipe['ingredientLines'] = ';'.join(recipe['ingredientLines'])
                spreadsheet.writerow(recipe)


# Function that reads recipe CSV and returns it as a data frame with sorted and renamed columns
def tidy_recipe_csv():
    recipe_data_frame = pd.read_csv('recipe_results.csv')
    recipe_data_frame = recipe_data_frame.sort_values(by=['yield'])
    recipe_data_frame = recipe_data_frame.reset_index(drop=True)
    recipe_data_frame = recipe_data_frame.rename(columns={'label': 'Recipe', 'yield': 'Serves', 'totalTime': 'Minutes', 'ingredientLines': 'Ingredients'})
    recipe_data_frame.to_csv('recipe_results.csv')
    return recipe_data_frame


# function that if user wants, adds ingredients for specified recipe to a text file called shopping_list.txt
def update_shopping_list(recipe_data_frame):
    add_shopping_list = input('Would you like to add any of ingredients for these recipes to your shopping list? y/n ')

    if add_shopping_list.lower() == 'yes' or add_shopping_list.lower() == 'y':
      print()
      recipe_id = int(input('Please enter the id of the recipe (in the first column) you would like to add to your weekly plan: '))
      # get the specific recipe based on index then get the ingredients and change them to a list
      selected_recipe = recipe_data_frame.iloc[recipe_id]
      ingredients_to_add = selected_recipe['Ingredients'].split(';')

      # open text file and then loop through ingredients, appending each one to the text file, then close
      shopping_list = open('shopping_list.txt', 'a')
      for ingredient in ingredients_to_add:
        shopping_list.write(ingredient + '\n')
      shopping_list.close()
      print('Your shopping list has been updated')


# call functions
new_recipe_search()
recipe_df = tidy_recipe_csv()
print()
print('Please see the details of the recipe_results.csv from your recipe search ')
print()
update_shopping_list(recipe_df)
