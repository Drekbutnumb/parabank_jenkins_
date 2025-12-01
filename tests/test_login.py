from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TestLogin:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def create_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        return driver, wait

    def setup(self, driver):
        driver.get("https://parabank.parasoft.com")
        driver.maximize_window()
        time.sleep(2)

    def test_valid_login(self):
        print("\n=== TC_LOGIN_01: Valid Login Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("john")

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys("demo")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            try:
                accounts_overview = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accounts Overview')]"))
                )
                print("[PASS] PASS: User logged in successfully, Accounts Overview page displayed")
                self.passed += 1
            except:
                print("[FAIL] FAIL: Login failed or Accounts Overview page not displayed")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_invalid_username(self):
        print("\n=== TC_LOGIN_02: Invalid Username Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("invaliduser999")

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys("demo")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            page_source = driver.page_source.lower()

            if "accounts overview" in page_source or "welcome" in page_source:
                print("[FAIL] FAIL: BUG - User logged in with invalid username!")
                self.failed += 1
            elif "error" in page_source or "invalid" in page_source:
                print("[PASS] PASS: Error message displayed for invalid username")
                self.passed += 1
            else:
                print("[FAIL] FAIL: No error message displayed for invalid username")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_invalid_password(self):
        print("\n=== TC_LOGIN_03: Invalid Password Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("john")

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys("wrongpassword123")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            page_source = driver.page_source.lower()

            if "accounts overview" in page_source or "welcome" in page_source:
                print("[FAIL] FAIL: BUG - User logged in with invalid password!")
                self.failed += 1
            elif "error" in page_source or "invalid" in page_source:
                print("[PASS] PASS: Error message displayed for invalid password")
                self.passed += 1
            else:
                print("[FAIL] FAIL: No error message displayed for invalid password")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_credentials(self):
        print("\n=== TC_LOGIN_04: Empty Username and Password Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            login_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Log In']"))
            )
            login_button.click()

            time.sleep(2)

            try:
                error_message = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error"))
                )
                print("[PASS] PASS: Error message displayed for empty credentials")
                self.passed += 1
            except:
                print("[FAIL] FAIL: No error message displayed for empty credentials")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_password(self):
        print("\n=== TC_LOGIN_05: Empty Password Only Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("john")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            try:
                error_message = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error"))
                )
                print("[PASS] PASS: Error message displayed for empty password")
                self.passed += 1
            except:
                print("[FAIL] FAIL: No error message displayed for empty password")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_sql_injection_prevention(self):
        print("\n=== TC_LOGIN_06: SQL Injection Prevention Test (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            sql_injection = "' OR '1'='1"

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(sql_injection)

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(sql_injection)

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            page_source_lower = driver.page_source.lower()
            if "an internal error has occurred" in page_source_lower:
                print("[FAIL] FAIL: BUG - Server crashed on SQL injection input")
                self.failed += 1
            elif "accounts overview" in page_source_lower:
                print("[FAIL] FAIL: Potential SQL injection vulnerability - logged in!")
                self.failed += 1
            elif "sql" in page_source_lower or "database" in page_source_lower:
                print("[FAIL] FAIL: SQL error exposed in response")
                self.failed += 1
            else:
                print("[PASS] PASS: SQL injection attempt blocked - no unauthorized access")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_session_management_after_logout(self):
        print("\n=== TC_LOGIN_07: Session Management After Logout (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("john")

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys("demo")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accounts Overview')]"))
            )

            logout_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Log Out"))
            )
            logout_link.click()

            time.sleep(2)

            driver.get("https://parabank.parasoft.com/parabank/overview.htm")
            time.sleep(2)

            page_source = driver.page_source.lower()

            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed on session check")
                self.failed += 1
                return

            login_form_present = False
            try:
                driver.find_element(By.NAME, "username")
                login_form_present = True
            except:
                pass

            error_present = "please login" in page_source or "log in" in page_source

            if login_form_present or error_present:
                print("[PASS] PASS: Session properly invalidated after logout - access denied")
                self.passed += 1
            elif "accounts overview" in page_source:
                print("[FAIL] FAIL: Session not properly invalidated - protected data still accessible")
                self.failed += 1
            else:
                print("[PASS] PASS: Session properly invalidated")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK LOGIN AUTOMATION TEST SUITE")
        print("="*60)

        self.test_valid_login()
        self.test_invalid_username()
        self.test_invalid_password()
        self.test_empty_credentials()
        self.test_empty_password()
        self.test_sql_injection_prevention()
        self.test_session_management_after_logout()

        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print("\n" + "="*60)
        print("LOGIN TEST SUITE COMPLETED")
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
    test_suite = TestLogin()
    test_suite.run_all_tests()