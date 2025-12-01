from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TestUpdateContactInfo:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def create_driver(self):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        return driver, wait

    def login(self, driver, wait):
        driver.get("https://parabank.parasoft.com")
        time.sleep(2)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("john")
        driver.find_element(By.NAME, "password").send_keys("demo")
        driver.find_element(By.XPATH, "//input[@value='Log In']").click()
        time.sleep(2)

    def test_update_page_access(self):
        print("\n=== TC_UPDATE_01: Update Contact Info Page Access ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            update_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Update Contact Info")))
            update_link.click()
            time.sleep(2)

            fields = ["customer.firstName", "customer.lastName", "customer.address.street",
                      "customer.address.city", "customer.address.state", "customer.address.zipCode",
                      "customer.phoneNumber"]

            missing = []
            for field in fields:
                try:
                    driver.find_element(By.ID, field)
                except:
                    missing.append(field)

            if len(missing) == 0:
                print("[PASS] PASS: Update Contact Info page loaded with all fields")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: Missing fields: {missing}")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_form_prepopulated(self):
        print("\n=== TC_UPDATE_02: Form Pre-populated with Current Info ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/updateprofile.htm")
            time.sleep(2)

            first_name = driver.find_element(By.ID, "customer.firstName").get_attribute("value")
            last_name = driver.find_element(By.ID, "customer.lastName").get_attribute("value")

            if first_name and last_name:
                print(f"[PASS] PASS: Form pre-populated (First: {first_name}, Last: {last_name})")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Form not pre-populated with user data")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_valid_update(self):
        print("\n=== TC_UPDATE_03: Valid Contact Info Update ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/updateprofile.htm")
            time.sleep(2)

            phone_field = driver.find_element(By.ID, "customer.phoneNumber")
            phone_field.clear()
            phone_field.send_keys("5559999999")

            update_button = driver.find_element(By.XPATH, "//input[@value='Update Profile']")
            update_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "updated" in page_source or "success" in page_source:
                print("[PASS] PASS: Contact info updated successfully")
                self.passed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error during profile update")
                self.failed += 1
            else:
                print("[FAIL] FAIL: No update confirmation message")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_first_name(self):
        print("\n=== TC_UPDATE_04: Empty First Name Validation ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/updateprofile.htm")
            time.sleep(2)

            first_name = driver.find_element(By.ID, "customer.firstName")
            first_name.clear()

            update_button = driver.find_element(By.XPATH, "//input[@value='Update Profile']")
            update_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            errors = driver.find_elements(By.CLASS_NAME, "error")

            if len(errors) > 0 or "first name is required" in page_source:
                print("[PASS] PASS: Validation error for empty first name")
                self.passed += 1
            elif "updated" in page_source or "success" in page_source:
                print("[FAIL] FAIL: BUG - Profile updated with empty first name")
                self.failed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Internal server error instead of validation")
                self.failed += 1
            else:
                print("[FAIL] FAIL: BUG - No validation for empty first name")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_invalid_zip_code(self):
        print("\n=== TC_UPDATE_05: Invalid Zip Code Format ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/updateprofile.htm")
            time.sleep(2)

            zip_field = driver.find_element(By.ID, "customer.address.zipCode")
            zip_field.clear()
            zip_field.send_keys("ABCDE")

            update_button = driver.find_element(By.XPATH, "//input[@value='Update Profile']")
            update_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Internal server error instead of zip validation")
                self.failed += 1
            elif "updated" in page_source or "success" in page_source:
                print("[FAIL] FAIL: BUG - System accepted invalid zip code (ABCDE)")
                self.failed += 1
            else:
                errors = driver.find_elements(By.CLASS_NAME, "error")
                if len(errors) > 0:
                    print("[PASS] PASS: Invalid zip code rejected with validation error")
                    self.passed += 1
                else:
                    print("[FAIL] FAIL: BUG - No proper validation for invalid zip")
                    self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_xss_in_name_field(self):
        print("\n=== TC_UPDATE_06: XSS in Name Field (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/updateprofile.htm")
            time.sleep(2)

            xss_payload = "<img src=x onerror=alert('XSS')>"

            first_name = driver.find_element(By.ID, "customer.firstName")
            first_name.clear()
            first_name.send_keys(xss_payload)

            update_button = driver.find_element(By.XPATH, "//input[@value='Update Profile']")
            update_button.click()
            time.sleep(2)

            try:
                alert = driver.switch_to.alert
                print("[FAIL] FAIL: XSS vulnerability detected")
                alert.accept()
                self.failed += 1
            except:
                print("[PASS] PASS: XSS attack prevented")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_long_input_boundary(self):
        print("\n=== TC_UPDATE_07: Long Input Boundary Test (UI) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/updateprofile.htm")
            time.sleep(2)

            long_string = "A" * 500

            street = driver.find_element(By.ID, "customer.address.street")
            street.clear()
            street.send_keys(long_string)

            update_button = driver.find_element(By.XPATH, "//input[@value='Update Profile']")
            update_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed on long input (500 chars)")
                self.failed += 1
            elif "updated" in page_source or "success" in page_source:
                print("[PASS] PASS: Long input accepted (no max length restriction)")
                self.passed += 1
            elif "too long" in page_source or "maximum" in page_source:
                print("[PASS] PASS: Long input rejected with validation message")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Unexpected response to long input")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK UPDATE CONTACT INFO TEST SUITE")
        print("="*60)

        self.test_update_page_access()
        self.test_form_prepopulated()
        self.test_valid_update()
        self.test_empty_first_name()
        self.test_invalid_zip_code()
        self.test_xss_in_name_field()
        self.test_long_input_boundary()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("UPDATE CONTACT INFO TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}

if __name__ == "__main__":
    test_suite = TestUpdateContactInfo()
    test_suite.run_all_tests()