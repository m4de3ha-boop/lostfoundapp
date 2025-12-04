import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fyndr", layout="centered")

# -----------------------------------------
# SAFE INITIALIZATION
# -----------------------------------------
if "items" not in st.session_state or not isinstance(st.session_state["items"], pd.DataFrame):
    st.session_state["items"] = pd.DataFrame(columns=["Name", "Item", "Claimed"])


df = st.session_state["items"]

# -----------------------------------------
# NAVIGATION
# -----------------------------------------
page = st.sidebar.radio("Navigate", ["Student Portal", "Staff Portal"])


# -----------------------------------------
# STUDENT PORTAL
# -----------------------------------------
if page == "Student Portal":

    st.title("Fyndr - Student Lost & Found")
    st.subheader("Lost Something?")

    name = st.text_input("Your Name")
    lost_item = st.text_input("Lost Item Name")

    if st.button("Search"):
        if df.empty:
            st.warning("No items available yet")
        else:
            matches = df[(df["Item"].str.lower() == lost_item.lower()) & (df["Claimed"] == False)]

            if matches.empty:
                st.error("Nothing found")
            else:
                st.success("Your item was found!")
                st.dataframe(matches)

                # Claim button
                if st.button("Claim Item"):
                    # Mark ALL matching items as claimed
                    idx = matches.index
                    st.session_state["items"].loc[idx, "Claimed"] = True
                    st.success("Item successfully claimed 🎉")

    st.subheader("Available Lost Items")
    available = df[df["Claimed"] == False]
    st.dataframe(available)



# -----------------------------------------
# STAFF PORTAL
# -----------------------------------------
else:

    st.title("👩‍🏫 Staff Panel")
    pwd = st.text_input("Staff Password", type="password")

    if pwd == "admin123":
        st.success("Access granted 🔓")

        st.subheader("Add New Item")

        n = st.text_input("Student Name (enter '-' if unknown)")
        i = st.text_input("Item Name")

        if st.button("Add Item"):
            if not i.strip():
                st.error("Item name required.")
            else:
                new = pd.DataFrame([[n.strip(), i.strip(), False]], columns=df.columns)
                st.session_state["items"] = pd.concat([df, new], ignore_index=True)
                st.success("Item added ✔️")

        st.subheader("All Items")
        st.dataframe(st.session_state["items"])

    elif pwd != "":
        st.error("Wrong password ❌")
