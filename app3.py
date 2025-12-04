import streamlit as st
import utils as utl
import streamlit_authenticator as stauth
from pathlib import Path
from streamlit_option_menu import option_menu


# On intègre un CSS personnalisé
css_path = Path(__file__).parent / "streamlit.css"
if css_path.exists():
    with open(css_path, encoding="utf-8") as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
else:
    st.warning(f"CSS file not found at: {css_path}")

# Def des données des comptes utilisateurs
lesDonneesDesComptes = {
    'usernames': {
        'utilisateur': {
            'name': 'utilisateur',
            'password': 'utilisateurMDP',
            'email': 'utilisateur@gmail.com',
            'failed_login_attemps': 0,  # Sera géré automatiquement
            'logged_in': False,          # Sera géré automatiquement
            'role': 'utilisateur'
        },
        'root': {
            'name': 'root',
            'password': 'rootMDP',
            'email': 'thoms.constantin@gmail.com',
            'failed_login_attemps': 0,
            'logged_in': False,
            'role': 'admin'
        }
    }
}
# Initialisation de l'authentificateur
authenticator = stauth.Authenticate(
    lesDonneesDesComptes,
    'some_cookie_name',
    'cookie name',
    30,
)

# Login
authenticator.login()

# Initialize session state for welcome message
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False


def page1():
    # Je créé trois colonnes pour centrer le contenu
    lay_gauche, lay_centre, lay_droit = st.columns([1, 20, 1])

    # Put title and main image in the central column
    with lay_centre:
        # Use the same centered layout as the image row (spacers + 3 middle columns)
        st.title("Bienvenu sur l'app la plus impressionante du monde !")
        sp_left_main, main_col1, main_col2, main_col3, sp_right_main = st.columns([1, 3, 3, 3, 1])
        with main_col2:
            st.image("https://i.imgflip.com/4it6fe.png", use_container_width=True)

        # Three small images in a centered row: add outer spacers so the trio is centered
        spacer_left, img_col1, img_col2, img_col3, spacer_right = st.columns([1, 3, 3, 3, 1])
        with img_col1:
            st.image("https://millennialshow.com/wp-content/uploads/2015/07/Screen-Shot-2015-07-07-at-10.56.46-AM.png", use_container_width=True)
        with img_col2:
            st.image("https://media.makeameme.org/created/impressive-very-impressive-5b42f7.jpg", use_container_width=True)
        with img_col3:
            st.image("https://media.makeameme.org/created/very-impressive-effort.jpg", use_container_width=True)

        # Final centered image
        sp_left_bis, main_bis_1, main_bis_2, main_bis_3, sp_right_bis = st.columns([1, 3, 3, 3, 1])
        with main_bis_2:
            st.markdown('<div class="main-bis-text">Êtes-vous impressionné(e) ? Je sais...</div>', unsafe_allow_html=True)
            st.image("https://media.makeameme.org/created/yes-i-am-57c7f98c58.jpg", use_container_width=True)
        
        
def page2():
    st.write("Un petit test pour du multipage app")
    st.image("https://media.makeameme.org/created/impressive-2y23ct.jpg", width=600)

def page3():
    st.write("Un autre petit test pour du multipage app")
    st.image("https://i.pinimg.com/564x/56/b9/a9/56b9a962f481a4212bce3f82b151433d.jpg", width=600)

# Def des pages pour la navigation
pages = [
    st.Page(page1, icon="🚨", title="Home"),
    st.Page(page2, icon="🔥", title="Page 2 Test"),
    st.Page(page3, icon="🔥", title="Page 3 Test"),
]
# Setup de la navigation
current_page = st.navigation(pages=pages, position="hidden")
st.set_page_config(layout="wide")

# Setup du menu
num_cols_menu = max(len(pages) + 1, 8)
columns_menu = st.columns(num_cols_menu, vertical_alignment="bottom")
columns_menu[0].write("**Menu de l'App Impressionante**")
for col, page in zip(columns_menu[1:-1], pages):
    col.page_link(page, icon=page.icon)
# J'ajoute le bouton logout tout à droite du menu si l'utilisateur est connecté
if st.session_state["authentication_status"]:
    with columns_menu[-1]:
        authenticator.logout("Se déconnecter", "main")
# Fin setup menu

# On ajoute un petit titre en haut à gauche de la page pour rappeler sur quelle page on est
st.title(f"{current_page.icon} {current_page.title}")

if st.session_state["authentication_status"]:
    # Show welcome message only once after login
    if not st.session_state.welcome_shown:
        if st.session_state["name"] == "root":
            st.success(f"Bienvenue {st.session_state['name']} (admin) sur l'app impressionante !")
        else:
            st.success(f"Bienvenue {st.session_state['name']} sur l'app impressionante !")
        st.session_state.welcome_shown = True
elif st.session_state["authentication_status"] is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect")
    st.session_state.welcome_shown = False  # Reset when login fails
elif st.session_state["authentication_status"] is None:
    st.warning("Les champs username et mot de passe doivent être remplis")
    st.session_state.welcome_shown = False  # Reset when not logged in

# Permet de lancer la page active pour du multipage    

current_page.run()
