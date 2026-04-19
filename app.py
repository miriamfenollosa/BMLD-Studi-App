import pandas as pd 
import streamlit as st

# Eigener Code
st.title("Hallo, Streamlit!")
st.write ("Dies ist eine einfache Streamlit-App.")


# --- NEW CODE: import and initialize data manager and login manager ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="BMLD_App_DB"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in
# --- END OF NEW CODE ---

# --- CODE UPDATE: load user data from data manager if not already present in session state --
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',                     # The file on switch drive where the data is stored
        initial_value=pd.DataFrame(),   # Initial value if the file does not exist
        parse_dates=['timestamp']       # Parse timestamp as datetime
    )
# --- END OF CODE UPDATE ---

st.set_page_config(page_title="BMI Rechner", page_icon=":material/monitor_weight:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_calculator = st.Page("views/calculator.py", title="BMI-Rechner", icon=":material/calculate:")
pg_viz  = st.Page("views/viz.py",  title="BMI Grafik",  icon=":material/show_chart:")

pg = st.navigation([pg_home, pg_calculator, pg_viz])
pg.run()
