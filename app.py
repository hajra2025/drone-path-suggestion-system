import streamlit as st
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="m151518949hsxw",
    database="concert_booking"
)

cursor = conn.cursor()

st.title("🎤 Concert Booking System")

# Show concerts
st.subheader("Available Concerts")

cursor.execute("SELECT * FROM concerts")
concerts = cursor.fetchall()

for c in concerts:
    st.write(f"ID: {c[0]} | {c[1]} | {c[2]} | {c[3]} | Rs.{c[4]}")

# Add user
st.subheader("Create User")

name = st.text_input("Name")
email = st.text_input("Email")
password = st.text_input("Password")

if st.button("Add User"):
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )
    conn.commit()
    st.success("User Added!")

# Book tickets
st.subheader("Book Ticket")

user_id = st.number_input("User ID", min_value=1)
concert_id = st.number_input("Concert ID", min_value=1)
tickets = st.number_input("Tickets", min_value=1)

if st.button("Book Now"):
    cursor.execute(
        "INSERT INTO bookings (user_id, concert_id, tickets) VALUES (%s, %s, %s)",
        (user_id, concert_id, tickets)
    )
    conn.commit()
    st.success("Booking Successful!")

# Show bookings
st.subheader("All Bookings")

cursor.execute("""
SELECT b.booking_id, u.name, c.artist, b.tickets
FROM bookings b
JOIN users u ON b.user_id = u.user_id
JOIN concerts c ON b.concert_id = c.concert_id
""")

for b in cursor.fetchall():
    st.write(f"Booking {b[0]} | {b[1]} | {b[2]} | {b[3]} tickets")