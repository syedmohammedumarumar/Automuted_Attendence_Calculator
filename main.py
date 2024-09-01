from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Hey Mitsian Calculate Your Attendance")

try:
    # Get registration number and password from user input
    reg_no = input("Enter your registration number: ")
    password = input("Enter your password: ")

    # Set Chrome options (headless mode is turned off so user can see the process)
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-extensions')
    options.add_argument('--log-level=3')
    # Comment out or remove the headless option
    # options.add_argument('--headless')  # Disable headless mode
    options.add_argument('--disable-gpu')  # Disable GPU usage (optional but recommended)
    options.add_argument('--window-size=1920,1080')  # Set window size (important)

    # Install ChromeDriver and set up the service
    service = Service(ChromeDriverManager().install())

    # Initialize WebDriver with options
    driver = webdriver.Chrome(service=service, options=options)

    # Open the college website and log in
    driver.get("http://www.mitsims.in/home.jsp")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "studentLink"))).click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "studentForm")))
    form = driver.find_element(By.ID, "studentForm")
    form.find_element(By.ID, "inputStuId").send_keys(reg_no)
    form.find_element(By.ID, "inputPassword").send_keys(password)
    form.find_element(By.ID, "studentSubmitButton").click()

    # Wait for some time to check if login was successful
    time.sleep(5)

    # Check if login was successful
    if "Invalid login" in driver.page_source:  # Change the text based on the actual error message on the site
        if "incorrect registration number" in driver.page_source.lower():
            print("The registration number is incorrect. Please try again.")
        elif "incorrect password" in driver.page_source.lower():
            print("The password is incorrect. Please enter the correct password.")
        else:
            print("Login failed. Please check your credentials and try again.")
    else:
        # Proceed with attendance calculation if login is successful

        # Extract the student name using the ID 'studentName'
        student_name = driver.find_element(By.ID, "studentName").text

        # Add a delay to ensure the attendance page is fully loaded
        time.sleep(10)

        # Use JavaScript to extract percentages
        script = """
            var percentages = [];
            var elements = document.getElementsByClassName('x-form-display-field');
            for (var i = 0; i < elements.length; i++) {
                var text = elements[i].innerText.trim();
                if (text && text.includes('.')) {  // Check if the text is a percentage
                    percentages.push(parseFloat(text));
                }
            }
            return percentages;
        """

        # Execute JavaScript in the browser context
        percentage_values = driver.execute_script(script)

        # Filter out None values
        percentage_values = [p for p in percentage_values if p is not None]

        # Print valid floating-point percentages found
        print(f"The subjects' attendance percentages are: {percentage_values}")

        # Calculate and print the average attendance percentage
        if percentage_values:
            total_percentage = sum(percentage_values) / len(percentage_values)
            print(f"Hey {student_name}, your total attendance percentage is: {total_percentage:.2f}%")
        else:
            print("No valid attendance percentages found. (You may have entered the wrong registration number or password. Please check!)")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Automatically close the browser after displaying the result
    driver.quit()

# Wait for user input before closing
input("Press Enter to exit...")
