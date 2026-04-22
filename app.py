import pandas as pd 
import streamlit as st


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
pg_Semester_01 = st.Page("views/Semester_01.py", title="1. Semester", icon=":material/school:")
pg_Semester_02 = st.Page("views/Semester_02.py", title="2. Semester", icon=":material/school:")
pg_Semester_03 = st.Page("views/Semester_03.py", title="3. Semester", icon=":material/school:")
pg_Semester_04 = st.Page("views/Semester_04.py", title="4. Semester", icon=":material/school:")
pg_Semester_05 = st.Page("views/Semester_05.py", title="5. Semester", icon=":material/school:")
pg_Semester_06 = st.Page("views/Semester_06.py", title="6. Semester", icon=":material/school:")

pg = st.navigation([pg_home, pg_calculator, pg_viz, pg_Semester_01, pg_Semester_02, pg_Semester_03, pg_Semester_04, pg_Semester_05, pg_Semester_06])
pg.run()
