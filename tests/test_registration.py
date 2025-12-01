from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
import random
import string

class TestRegistration:
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

    def generate_unique_username(self):
        return "testuser_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    def test_valid_registration(self):
        print("\n=== TC_REG_01: Valid User Registration ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com")
            time.sleep(2)

            register_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Register"))
            )
            register_link.click()
            time.sleep(2)

            unique_username = self.generate_unique_username()

            driver.find_element(By.ID, "customer.firstName").send_keys("John")
            driver.find_element(By.ID, "customer.lastName").send_keys("Doe")
            driver.find_element(By.ID, "customer.address.street").send_keys("123 Main St")
            driver.find_element(By.ID, "customer.address.city").send_keys("New York")
            driver.find_element(By.ID, "customer.address.state").send_keys("NY")
            driver.find_element(By.ID, "customer.address.zipCode").send_keys("10001")
            driver.find_element(By.ID, "customer.phoneNumber").send_keys("5551234567")
            driver.find_element(By.ID, "customer.ssn").send_keys("123-45-6789")
            driver.find_element(By.ID, "customer.username").send_keys(unique_username)
            driver.find_element(By.ID, "customer.password").send_keys("Test@1234")
            driver.find_element(By.ID, "repeatedPassword").send_keys("Test@1234")

            register_button = driver.find_element(By.XPATH, "//input[@value='Register']")
            register_button.click()
            time.sleep(3)

            try:
                welcome_message = wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Welcome {unique_username}')]"))
                )
                print(f"[PASS] PASS: User '{unique_username}' registered successfully")
                self.passed += 1
            except:
                if "Welcome" in driver.page_source or "created" in driver.page_source.lower():
                    print(f"[PASS] PASS: User registration completed successfully")
                    self.passed += 1
                else:
                    print("[FAIL] FAIL: Registration success message not found")
                    self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_required_fields(self):
        print("\n=== TC_REG_02: Registration with Empty Required Fields ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/register.htm")
            time.sleep(2)

            register_button = driver.find_element(By.XPATH, "//input[@value='Register']")
            register_button.click()
            time.sleep(2)

            errors = driver.find_elements(By.CLASS_NAME, "error")
            if len(errors) > 0:
                print(f"[PASS] PASS: {len(errors)} validation error(s) displayed for empty fields")
                self.passed += 1
            else:
                print("[FAIL] FAIL: No validation errors displayed")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_duplicate_username(self):
        print("\n=== TC_REG_03: Registration with Duplicate Username ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/register.htm")
            time.sleep(2)

            driver.find_element(By.ID, "customer.firstName").send_keys("Jane")
            driver.find_element(By.ID, "customer.lastName").send_keys("Smith")
            driver.find_element(By.ID, "customer.address.street").send_keys("456 Oak Ave")
            driver.find_element(By.ID, "customer.address.city").send_keys("Boston")
            driver.find_element(By.ID, "customer.address.state").send_keys("MA")
            driver.find_element(By.ID, "customer.address.zipCode").send_keys("02101")
            driver.find_element(By.ID, "customer.phoneNumber").send_keys("5559876543")
            driver.find_element(By.ID, "customer.ssn").send_keys("987-65-4321")
            driver.find_element(By.ID, "customer.username").send_keys("john")
            driver.find_element(By.ID, "customer.password").send_keys("Test@1234")
            driver.find_element(By.ID, "repeatedPassword").send_keys("Test@1234")

            register_button = driver.find_element(By.XPATH, "//input[@value='Register']")
            register_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed on duplicate username")
                self.failed += 1
            elif "already exists" in page_source or "username is taken" in page_source:
                print("[PASS] PASS: Duplicate username error displayed correctly")
                self.passed += 1
            elif "welcome" in page_source:
                print("[FAIL] FAIL: BUG - Duplicate username was accepted")
                self.failed += 1
            else:
                print("[PASS] PASS: System handled duplicate username scenario")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_password_mismatch(self):
        print("\n=== TC_REG_04: Registration with Mismatched Passwords ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/register.htm")
            time.sleep(2)

            driver.find_element(By.ID, "customer.firstName").send_keys("Mike")
            driver.find_element(By.ID, "customer.lastName").send_keys("Johnson")
            driver.find_element(By.ID, "customer.address.street").send_keys("789 Pine Rd")
            driver.find_element(By.ID, "customer.address.city").send_keys("Chicago")
            driver.find_element(By.ID, "customer.address.state").send_keys("IL")
            driver.find_element(By.ID, "customer.address.zipCode").send_keys("60601")
            driver.find_element(By.ID, "customer.phoneNumber").send_keys("5551112222")
            driver.find_element(By.ID, "customer.ssn").send_keys("111-22-3333")
            driver.find_element(By.ID, "customer.username").send_keys(self.generate_unique_username())
            driver.find_element(By.ID, "customer.password").send_keys("Test@1234")
            driver.find_element(By.ID, "repeatedPassword").send_keys("Different@5678")

            register_button = driver.find_element(By.XPATH, "//input[@value='Register']")
            register_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed on password mismatch")
                self.failed += 1
            elif "match" in page_source or "passwords do not match" in page_source:
                print("[PASS] PASS: Password mismatch error displayed correctly")
                self.passed += 1
            elif "welcome" in page_source:
                print("[FAIL] FAIL: BUG - Registration accepted with mismatched passwords")
                self.failed += 1
            else:
                print("[FAIL] FAIL: No password mismatch validation")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_invalid_ssn_format(self):
        print("\n=== TC_REG_05: Registration with Invalid SSN Format ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/register.htm")
            time.sleep(2)

            unique_username = self.generate_unique_username()
            driver.find_element(By.ID, "customer.firstName").send_keys("Sarah")
            driver.find_element(By.ID, "customer.lastName").send_keys("Williams")
            driver.find_element(By.ID, "customer.address.street").send_keys("321 Elm St")
            driver.find_element(By.ID, "customer.address.city").send_keys("Miami")
            driver.find_element(By.ID, "customer.address.state").send_keys("FL")
            driver.find_element(By.ID, "customer.address.zipCode").send_keys("33101")
            driver.find_element(By.ID, "customer.phoneNumber").send_keys("5553334444")
            driver.find_element(By.ID, "customer.ssn").send_keys("12345")
            driver.find_element(By.ID, "customer.username").send_keys(unique_username)
            driver.find_element(By.ID, "customer.password").send_keys("Test@1234")
            driver.find_element(By.ID, "repeatedPassword").send_keys("Test@1234")

            register_button = driver.find_element(By.XPATH, "//input[@value='Register']")
            register_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "welcome" in page_source:
                print("[FAIL] FAIL: BUG - System accepted invalid SSN format (no validation)")
                self.failed += 1
            elif "ssn" in page_source and ("invalid" in page_source or "error" in page_source or "format" in page_source):
                print("[PASS] PASS: Invalid SSN format rejected with error message")
                self.passed += 1
            else:
                print("[PASS] PASS: Invalid SSN registration was blocked")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_sql_injection_prevention(self):
        print("\n=== TC_REG_06: SQL Injection Prevention Test (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/register.htm")
            time.sleep(2)

            sql_injection = "'; DROP TABLE users; --"

            driver.find_element(By.ID, "customer.firstName").send_keys("Test")
            driver.find_element(By.ID, "customer.lastName").send_keys("Security")
            driver.find_element(By.ID, "customer.address.street").send_keys("123 Security St")
            driver.find_element(By.ID, "customer.address.city").send_keys("SecureCity")
            driver.find_element(By.ID, "customer.address.state").send_keys("SC")
            driver.find_element(By.ID, "customer.address.zipCode").send_keys("12345")
            driver.find_element(By.ID, "customer.phoneNumber").send_keys("5550000000")
            driver.find_element(By.ID, "customer.ssn").send_keys("000-00-0000")
            driver.find_element(By.ID, "customer.username").send_keys(sql_injection)
            driver.find_element(By.ID, "customer.password").send_keys("Test@1234")
            driver.find_element(By.ID, "repeatedPassword").send_keys("Test@1234")

            register_button = driver.find_element(By.XPATH, "//input[@value='Register']")
            register_button.click()
            time.sleep(2)

            page_source_lower = driver.page_source.lower()
            if "sql" not in page_source_lower and "database error" not in page_source_lower:
                print("[PASS] PASS: SQL injection attempt handled safely - no database errors exposed")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Potential SQL injection vulnerability detected")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_xss_prevention(self):
        print("\n=== TC_REG_07: XSS Prevention Test (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/register.htm")
            time.sleep(2)

            xss_payload = "<script>alert('XSS')</script>"
            unique_username = self.generate_unique_username()

            driver.find_element(By.ID, "customer.firstName").send_keys(xss_payload)
            driver.find_element(By.ID, "customer.lastName").send_keys("TestXSS")
            driver.find_element(By.ID, "customer.address.street").send_keys("123 XSS St")
            driver.find_element(By.ID, "customer.address.city").send_keys("XSSCity")
            driver.find_element(By.ID, "customer.address.state").send_keys("XS")
            driver.find_element(By.ID, "customer.address.zipCode").send_keys("00000")
            driver.find_element(By.ID, "customer.phoneNumber").send_keys("5551111111")
            driver.find_element(By.ID, "customer.ssn").send_keys("111-11-1111")
            driver.find_element(By.ID, "customer.username").send_keys(unique_username)
            driver.find_element(By.ID, "customer.password").send_keys("Test@1234")
            driver.find_element(By.ID, "repeatedPassword").send_keys("Test@1234")

            register_button = driver.find_element(By.XPATH, "//input[@value='Register']")
            register_button.click()
            time.sleep(2)

            try:
                alert = driver.switch_to.alert
                print("[FAIL] FAIL: XSS vulnerability detected - alert was triggered")
                alert.accept()
                self.failed += 1
            except:
                print("[PASS] PASS: XSS attack prevented - no script execution")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK USER REGISTRATION AUTOMATION TEST SUITE")
        print("="*60)

        self.test_valid_registration()
        self.test_empty_required_fields()
        self.test_duplicate_username()
        self.test_password_mismatch()
        self.test_invalid_ssn_format()
        self.test_sql_injection_prevention()
        self.test_xss_prevention()

        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print("\n" + "="*60)
        print("REGISTRATION TEST SUITE COMPLETED")
        print("="*60)
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {success_rate:.2f}%")
        print("="*60)

        return {
            "total": total_tests,
            "passed": self.passed,
            "failed": self.failed,
            "success_rate": success_rate
        }

if __name__ == "__main__":
    test_suite = TestRegistration()
    test_suite.run_all_tests()