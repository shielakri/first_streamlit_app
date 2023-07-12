import streamlit

streamlit.title('My Parents New Healthy Diner')

streamlit.header('🥣 Breakfast Favorites')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Create pick list
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display table
streamlit.dataframe(my_fruit_list)
