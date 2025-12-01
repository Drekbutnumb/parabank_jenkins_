from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TestForgotLoginInfo:
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

    def test_forgot_login_link_access(self):
        print("\n=== TC_FORGOT_01: Forgot Login Link Access ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com")
            time.sleep(2)

            forgot_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Forgot login info?")))
            forgot_link.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "customer lookup" in page_source or "find your login" in page_source:
                print("[PASS] PASS: Forgot Login page accessible")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Forgot Login page not loaded correctly")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_all_fields_present(self):
        print("\n=== TC_FORGOT_02: All Required Fields Present ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/lookup.htm")
            time.sleep(2)

            fields = ["firstName", "lastName", "address.street", "address.city",
                      "address.state", "address.zipCode", "ssn"]

            missing = []
            for field in fields:
                try:
                    driver.find_element(By.ID, field)
                except:
                    missing.append(field)

            if len(missing) == 0:
                print("[PASS] PASS: All lookup fields present")
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

    def test_valid_lookup(self):
        print("\n=== TC_FORGOT_03: Valid Customer Lookup ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/lookup.htm")
            time.sleep(2)

            driver.find_element(By.ID, "firstName").send_keys("John")
            driver.find_element(By.ID, "lastName").send_keys("Doe")
            driver.find_element(By.ID, "address.street").send_keys("123 Main St")
            driver.find_element(By.ID, "address.city").send_keys("New York")
            driver.find_element(By.ID, "address.state").send_keys("NY")
            driver.find_element(By.ID, "address.zipCode").send_keys("10001")
            driver.find_element(By.ID, "ssn").send_keys("123-45-6789")

            find_button = driver.find_element(By.XPATH, "//input[@value='Find My Login Info']")
            find_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "internal error" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error during lookup")
                self.failed += 1
            elif "username" in page_source and "password" in page_source:
                print("[PASS] PASS: Lookup returned credentials")
                self.passed += 1
            elif "not found" in page_source or "could not" in page_source:
                print("[PASS] PASS: Lookup executed - user not found (expected for test data)")
                self.passed += 1
            else:
                print("[FAIL] FAIL: No proper lookup result returned")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_fields_validation(self):
        print("\n=== TC_FORGOT_04: Empty Fields Validation ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/lookup.htm")
            time.sleep(2)

            find_button = driver.find_element(By.XPATH, "//input[@value='Find My Login Info']")
            find_button.click()
            time.sleep(2)

            errors = driver.find_elements(By.CLASS_NAME, "error")
            if len(errors) > 0:
                print(f"[PASS] PASS: {len(errors)} validation error(s) displayed")
                self.passed += 1
            else:
                print("[FAIL] FAIL: BUG - No validation errors for empty form")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_invalid_user_lookup(self):
        print("\n=== TC_FORGOT_05: Non-existent User Lookup ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/lookup.htm")
            time.sleep(2)

            driver.find_element(By.ID, "firstName").send_keys("NonExistent")
            driver.find_element(By.ID, "lastName").send_keys("User")
            driver.find_element(By.ID, "address.street").send_keys("999 Fake St")
            driver.find_element(By.ID, "address.city").send_keys("Nowhere")
            driver.find_element(By.ID, "address.state").send_keys("XX")
            driver.find_element(By.ID, "address.zipCode").send_keys("00000")
            driver.find_element(By.ID, "ssn").send_keys("000-00-0000")

            find_button = driver.find_element(By.XPATH, "//input[@value='Find My Login Info']")
            find_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed instead of user not found error")
                self.failed += 1
            elif "not found" in page_source or "could not" in page_source:
                print("[PASS] PASS: Proper error for non-existent user")
                self.passed += 1
            else:
                print("[FAIL] FAIL: BUG - No error message for invalid user")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_sql_injection_in_ssn(self):
        print("\n=== TC_FORGOT_06: SQL Injection in SSN Field (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/lookup.htm")
            time.sleep(2)

            sql_payload = "' OR '1'='1"

            driver.find_element(By.ID, "firstName").send_keys("Test")
            driver.find_element(By.ID, "lastName").send_keys("User")
            driver.find_element(By.ID, "address.street").send_keys("123 St")
            driver.find_element(By.ID, "address.city").send_keys("City")
            driver.find_element(By.ID, "address.state").send_keys("ST")
            driver.find_element(By.ID, "address.zipCode").send_keys("12345")
            driver.find_element(By.ID, "ssn").send_keys(sql_payload)

            find_button = driver.find_element(By.XPATH, "//input[@value='Find My Login Info']")
            find_button.click()
            time.sleep(2)

            page_lower = driver.page_source.lower()
            if "cloudflare" in page_lower or "verify you are human" in page_lower:
                print("[PASS] PASS: Security system (Cloudflare) blocked malicious request")
                self.passed += 1
            elif "username" in page_lower and "password" in page_lower and "sql" not in page_lower:
                print("[FAIL] FAIL: Potential SQL injection - credentials returned")
                self.failed += 1
            elif "an internal error has occurred" in page_lower:
                print("[FAIL] FAIL: BUG - Server crashed on SQL injection input")
                self.failed += 1
            elif "sql" in page_lower or "database" in page_lower or "exception" in page_lower:
                print("[FAIL] FAIL: SQL error exposed")
                self.failed += 1
            else:
                print("[PASS] PASS: SQL injection handled safely")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_sensitive_data_exposure(self):
        print("\n=== TC_FORGOT_07: Sensitive Data Exposure Check (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com/parabank/lookup.htm")
            time.sleep(2)

            driver.find_element(By.ID, "firstName").send_keys("John")
            driver.find_element(By.ID, "lastName").send_keys("Smith")
            driver.find_element(By.ID, "address.street").send_keys("123 St")
            driver.find_element(By.ID, "address.city").send_keys("City")
            driver.find_element(By.ID, "address.state").send_keys("ST")
            driver.find_element(By.ID, "address.zipCode").send_keys("12345")
            driver.find_element(By.ID, "ssn").send_keys("123456789")

            find_button = driver.find_element(By.XPATH, "//input[@value='Find My Login Info']")
            find_button.click()
            time.sleep(2)

            page_source = driver.page_source

            if "Password:" in page_source or "password:" in page_source.lower():
                print("[FAIL] FAIL: SECURITY BUG - Password displayed in plain text")
                self.failed += 1
            else:
                print("[PASS] PASS: Password not exposed in plain text")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK FORGOT LOGIN INFO TEST SUITE")
        print("="*60)

        self.test_forgot_login_link_access()
        self.test_all_fields_present()
        self.test_valid_lookup()
        self.test_empty_fields_validation()
        self.test_invalid_user_lookup()
        self.test_sql_injection_in_ssn()
        self.test_sensitive_data_exposure()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("FORGOT LOGIN INFO TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}

if __name__ == "__main__":
    test_suite = TestForgotLoginInfo()
    test_suite.run_all_tests()