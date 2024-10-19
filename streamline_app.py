# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie.
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The Name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect("Choose up to 5 ingredients!:", my_dataframe, max_selections=5)

#st.dataframe(data=my_dataframe, use_container_width=True)
if ingredients_list:
    #st.write(ingredients_list)
    ingredients_string = ''
    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    submit_button = st.button('Submit Order')
    
    #view the SQL statement that will be used via the Streamlit app. 
    #Good for troubleshooting and you can run it in Snowflake.
    #st.write(my_insert_stmt)
    #st.stop
    
    if submit_button:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered!' + " " + name_on_order, icon="✅")
