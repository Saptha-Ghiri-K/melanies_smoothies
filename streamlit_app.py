# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
streamlit.title("My Parets New Healthy Diner")


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write(
  """choose the fruits you want in your Smoothie
  """
)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("your favorite fruit is:", option)

name_on_order = st.text_input("Name On Smoothie");
if name_on_order:
    st.write("The name entered in Smoothie :", name_on_order);
cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIt_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe
)

if ingredients_list:
    # st.write(ingredients_list);
    # st.text(ingredients_list);

    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string += x + ' '

    # st.write(ingredients_string);

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order )
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    # st.write(my_insert_stmt)
    # st.write(len(ingredients_list))
    if len(ingredients_list)<=5:
        time_to_insert = st.button("Submit orders")
    
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
    else:
        st.write("***You can add only upto 5 in ingredients***")
