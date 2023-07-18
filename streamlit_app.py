import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('🥣 Breakfast Favorites')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#
# Using pandas to read CSV
#
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Set index to fruit name
my_fruit_list = my_fruit_list.set_index('Fruit')

# Create pick list
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display table
streamlit.dataframe(fruits_to_show)

# New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

def get_fruityvice_data(this_fruit_choice):
  # Using requests to get information about fruits
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  # normalize json
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  # Text entry box
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)    
except URLError as e:
  streamlit.error()

# Snowflake related functions
def get_fruit_load_list():
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit

streamlit.header("View Our Fruit List - Add Your Favorites!")
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
if streamlit.button('Add a Fruit to the List'):
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)

