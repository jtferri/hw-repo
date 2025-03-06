#hw6 part 1 - BMI calculator app
#BMI = weight(kg) / height(m)^2
#underweight: <18.5
#normal: 18.5-24.9
#overweight: 25-29.9
#obese: >30

import streamlit as st

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def main():
    st.title("BMI Calculator")

    st.write("Enter your height and weight to calculate your BMI.")

    # Input for height
    height_unit = st.selectbox("Select height unit:", ["Meters", "Feet"])
    if height_unit == "Meters":
        height = st.number_input("Enter height in meters:", min_value=0.0, format="%.2f")
    else:
        height = st.number_input("Enter height in feet:", min_value=0.0, format="%.2f")
        height = height * 0.3048  # Convert feet to meters

    # Input for weight
    weight_unit = st.selectbox("Select weight unit:", ["Kilograms", "Pounds"])
    if weight_unit == "Kilograms":
        weight = st.number_input("Enter weight in kilograms:", min_value=0.0, format="%.2f")
    else:
        weight = st.number_input("Enter weight in pounds:", min_value=0.0, format="%.2f")
        weight = weight * 0.453592  # Convert pounds to kilograms

    if st.button("Calculate BMI"):
        if height > 0 and weight > 0:
            bmi = calculate_bmi(weight, height)
            st.write(f"Your BMI is: {bmi:.2f}")

            # Determine BMI category
            if bmi < 18.5:
                st.write("You are underweight.")
            elif 18.5 <= bmi < 24.9:
                st.write("You have a normal weight.")
            elif 25 <= bmi < 29.9:
                st.write("You are overweight.")
            else:
                st.write("You are obese.")
        else:
            st.write("Please enter valid height and weight.")

if __name__ == "__main__":
    main()