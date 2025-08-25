from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pymongo
from urllib.parse import quote_plus
import certifi
import os

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Heritage Virtual Guide",
    layout="wide",
    page_icon="🏛️"
)

# ===================== CUSTOM DARK CSS =====================
dark_css = """
<style>
/* Background */
.stApp {
    background: linear-gradient(to right, #0f0f0f, #1a1a1a);
    font-family: 'Georgia', serif;
    color: #e0d5c0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #121212;
    color: #e0d5c0;
}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
    color: #f0c674;
}

/* Titles */
h1, h2, h3 {
    color: #f0c674;
    font-weight: bold;
    text-align: center;
    text-shadow: 1px 1px 4px #000;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(145deg, #f0c674, #d4a017);
    color: black;
    border-radius: 10px;
    padding: 8px 20px;
    border: none;
    font-weight: bold;
}
.stButton>button:hover {
    background: linear-gradient(145deg, #d4a017, #b8860b);
    color: white;
}

/* Forms */
.stTextInput>div>div>input {
    border-radius: 8px;
    border: 1px solid #f0c674;
    padding: 6px;
    background-color: #222;
    color: #f5f5f5;
}
.stTextInput>div>label {
    font-weight: bold;
    color: #f0c674;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 30px;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    font-weight: bold;
    color: #e0d5c0;
}
.stTabs [aria-selected="true"] {
    border-bottom: 3px solid #f0c674 !important;
    color: #f0c674 !important;
}

/* Cards */
.card {
    background: #1c1c1c;
    border: 1px solid #f0c674;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 2px 4px 15px rgba(0,0,0,0.6);
}
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

# ===================== DATABASE CONFIG =====================
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "indranilsamanta2003")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "indu94070@2003")
MONGODB_CLUSTER = os.getenv("MONGODB_CLUSTER", "clusterheritage.aedeqma.mongodb.net")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "heritage_db")

@st.cache_resource
def init_connection():
    try:
        username = quote_plus(MONGODB_USERNAME)
        password = quote_plus(MONGODB_PASSWORD)
        
        # Updated connection string with proper SSL configuration
        connection_string = f"mongodb+srv://{username}:{password}@{MONGODB_CLUSTER}/{MONGODB_DATABASE}?retryWrites=true&w=majority&appName=Clusterheritage"
        
        # Connect with enhanced SSL configuration
        client = pymongo.MongoClient(
            connection_string,
            tls=True,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=False,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            serverSelectionTimeoutMS=30000,
            retryWrites=True
        )
        
        # Test the connection with a simple command
        client.admin.command('ping')
        st.sidebar.success("✅ Connected to MongoDB successfully!")
        return client
    except Exception as e:
        st.sidebar.error(f"❌ MongoDB connection failed: {str(e)}")
        # Provide troubleshooting tips
        st.sidebar.info("""
        💡 Troubleshooting Tips:
        1. Check if your IP is whitelisted in MongoDB Atlas
        2. Verify your database user has proper permissions
        3. Ensure your credentials are correct
        4. Try connecting with MongoDB Compass to test your connection
        """)
        return None

client = init_connection()
if client:
    db = client[MONGODB_DATABASE]
    users_collection = db.users
else:
    class DummyCollection:
        def find_one(self, *args, **kwargs): 
            return None
        def insert_one(self, *args, **kwargs): 
            return {"inserted_id": "demo_id"}
    users_collection = DummyCollection()
    st.warning("⚠️ Running in demo mode without database connection. Some features may be limited.")

# ===================== AUTH =====================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None

def login_user(username, password):
    if not client:
        # Demo mode - accept any non-empty credentials
        return bool(username and password)
    user = users_collection.find_one({"username": username, "password": password})
    return user is not None

def signup_user(username, password, email):
    if not client:
        # Demo mode - always succeed for non-empty credentials
        if not username or not password or not email:
            return False, "All fields are required"
        return True, "User created successfully! (Demo mode)"
    if users_collection.find_one({"username": username}):
        return False, "Username already exists"
    users_collection.insert_one({"username": username, "password": password, "email": email})
    return True, "User created successfully!"

# ===================== UI =====================
if not st.session_state.authenticated:
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab1:
        st.subheader("Login to Your Guide")
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login")
            if login_submitted:
                if login_user(login_username, login_password):
                    st.session_state.authenticated = True
                    st.session_state.username = login_username
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

    with tab2:
        st.subheader("Create an Account")
        with st.form("signup_form"):
            signup_username = st.text_input("Choose a Username")
            signup_email = st.text_input("Email")
            signup_password = st.text_input("Choose a Password", type="password")
            signup_submitted = st.form_submit_button("Sign Up")
            if signup_submitted:
                success, message = signup_user(signup_username, signup_password, signup_email)
                if success:
                    st.success(message)
                else:
                    st.error(message)

else:
    st.sidebar.title(f"🌟 Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

    st.title("🏛️ Heritage Virtual Guide")
    st.markdown("<p style='text-align:center; font-size:18px; color:#f0c674;'>Discover the history and stories behind the world's greatest heritage sites.</p>", unsafe_allow_html=True)

    tab_home, tab_search, tab_upload = st.tabs(["🏠 Home", "🔍 Search", "🖼️ Upload Image"])

    with tab_home:
        st.header("✨ Featured Heritage Sites")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div class='card'><h3>Taj Mahal</h3><p>India's iconic symbol of love and Mughal architecture.</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='card'><h3>Great Pyramids</h3><p>Ancient wonders of Egypt standing tall for millennia.</p></div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div class='card'><h3>Colosseum</h3><p>Rome's grand amphitheater showcasing gladiatorial glory.</p></div>", unsafe_allow_html=True)

    with tab_search:
        st.header("🔍 Search Heritage")
        search_query = st.text_input("Ask about any heritage site:")
        if search_query:
            st.success(f"📖 Search results for: {search_query} will appear here.")

    with tab_upload:
        st.header("🖼️ Explore by Image")
        uploaded_file = st.file_uploader("Upload an image of a heritage site", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.info("AI analysis results will appear here after backend integration.")