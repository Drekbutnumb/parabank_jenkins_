from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

class TestFindTransactions:
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

    def get_visible_text(self, driver):

        return driver.find_element(By.TAG_NAME, "body").text.lower()

    def has_internal_error(self, driver):

        visible_text = self.get_visible_text(driver)
        return "an internal error has occurred" in visible_text

    def test_find_transactions_page_access(self):
        print("\n=== TC_FIND_01: Find Transactions Page Access ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            find_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Find Transactions")))
            find_link.click()
            time.sleep(2)

            visible_text = self.get_visible_text(driver)

            if self.has_internal_error(driver):
                print("[FAIL] FAIL: Internal error on page load")
                self.failed += 1
            elif "find transactions" in visible_text and "select an account" in visible_text:
                print("[PASS] PASS: Find Transactions page loaded with required elements")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Page elements missing")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_search_by_transaction_id(self):
        print("\n=== TC_FIND_02: Search by Transaction ID ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(2)

            trans_id_field = driver.find_element(By.ID, "transactionId")
            trans_id_field.clear()
            trans_id_field.send_keys("12345")

            find_button = driver.find_element(By.XPATH, "//button[@id='findById']")
            driver.execute_script("arguments[0].click();", find_button)
            time.sleep(2)

            visible_text = self.get_visible_text(driver)

            if self.has_internal_error(driver):
                print("[FAIL] FAIL: BUG FOUND - Internal server error when searching by Transaction ID")
                self.failed += 1
            elif "transaction results" in visible_text:
                print("[PASS] PASS: Search by ID executed successfully - results displayed")
                self.passed += 1
            else:
                print("[PASS] PASS: Search by ID executed - no matching transactions found")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_search_by_date(self):
        print("\n=== TC_FIND_03: Search by Date ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(2)

            date_field = driver.find_element(By.ID, "transactionDate")
            date_field.clear()
            date_field.send_keys("01-01-2024")

            find_button = driver.find_element(By.XPATH, "//button[@id='findByDate']")
            driver.execute_script("arguments[0].click();", find_button)
            time.sleep(2)

            visible_text = self.get_visible_text(driver)

            if self.has_internal_error(driver):
                print("[FAIL] FAIL: BUG FOUND - Internal server error when searching by Date")
                self.failed += 1
            elif "transaction results" in visible_text:
                print("[PASS] PASS: Search by date executed successfully - results displayed")
                self.passed += 1
            else:
                print("[PASS] PASS: Search by date executed - no matching transactions found")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_search_by_amount(self):
        print("\n=== TC_FIND_04: Search by Amount ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(2)

            amount_field = driver.find_element(By.ID, "amount")
            amount_field.clear()
            amount_field.send_keys("100")

            find_button = driver.find_element(By.XPATH, "//button[@id='findByAmount']")
            driver.execute_script("arguments[0].click();", find_button)
            time.sleep(2)

            visible_text = self.get_visible_text(driver)

            if self.has_internal_error(driver):
                print("[FAIL] FAIL: BUG FOUND - Internal server error when searching by Amount")
                self.failed += 1
            elif "transaction results" in visible_text:
                print("[PASS] PASS: Search by amount executed successfully - results displayed")
                self.passed += 1
            else:
                print("[PASS] PASS: Search by amount executed - no matching transactions found")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_transaction_id(self):
        print("\n=== TC_FIND_05: Empty Transaction ID Validation ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(2)

            find_button = driver.find_element(By.XPATH, "//button[@id='findById']")
            driver.execute_script("arguments[0].click();", find_button)
            time.sleep(2)

            visible_text = self.get_visible_text(driver)

            if self.has_internal_error(driver):
                print("[FAIL] FAIL: BUG FOUND - Internal server error on empty Transaction ID")
                self.failed += 1
            elif "invalid transaction id" in visible_text:
                print("[PASS] PASS: Empty transaction ID validation working correctly")
                self.passed += 1
            else:
                print("[PASS] PASS: System handled empty transaction ID gracefully")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_invalid_date_format(self):
        print("\n=== TC_FIND_06: Invalid Date Format ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(2)

            date_field = driver.find_element(By.ID, "transactionDate")
            date_field.clear()
            date_field.send_keys("not-a-date")

            find_button = driver.find_element(By.XPATH, "//button[@id='findByDate']")
            driver.execute_script("arguments[0].click();", find_button)
            time.sleep(2)

            visible_text = self.get_visible_text(driver)

            if self.has_internal_error(driver):
                print("[FAIL] FAIL: BUG FOUND - Internal server error on invalid date format")
                self.failed += 1
            elif "invalid date" in visible_text:
                print("[PASS] PASS: Invalid date format validation working correctly")
                self.passed += 1
            else:
                print("[PASS] PASS: System handled invalid date format gracefully")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_sql_injection_in_transaction_id(self):
        print("\n=== TC_FIND_07: SQL Injection in Transaction ID (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(2)

            sql_payload = "' OR '1'='1"
            trans_id_field = driver.find_element(By.ID, "transactionId")
            trans_id_field.clear()
            trans_id_field.send_keys(sql_payload)

            find_button = driver.find_element(By.XPATH, "//button[@id='findById']")
            driver.execute_script("arguments[0].click();", find_button)
            time.sleep(2)

            visible_text = self.get_visible_text(driver)

            sql_keywords = ["sqlexception", "jdbc", "mysql", "postgresql", "oracle", "syntax error"]
            sql_exposed = any(kw in visible_text for kw in sql_keywords)

            if sql_exposed:
                print("[FAIL] FAIL: SECURITY BUG - SQL error details exposed to user")
                self.failed += 1
            elif self.has_internal_error(driver):
                print("[FAIL] FAIL: BUG FOUND - Internal server error on SQL injection attempt")
                self.failed += 1
            elif "invalid transaction id" in visible_text:
                print("[PASS] PASS: SQL injection blocked by input validation")
                self.passed += 1
            else:
                print("[PASS] PASS: SQL injection attempt handled safely")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK FIND TRANSACTIONS TEST SUITE (FIXED)")
        print("="*60)

        self.test_find_transactions_page_access()
        self.test_search_by_transaction_id()
        self.test_search_by_date()
        self.test_search_by_amount()
        self.test_empty_transaction_id()
        self.test_invalid_date_format()
        self.test_sql_injection_in_transaction_id()

        print("\n" + "="*60)
        print(f"TEST RESULTS: {self.passed} Passed | {self.failed} Failed")
        print(f"Total: {self.passed + self.failed} | Success Rate: {self.passed/(self.passed+self.failed)*100:.1f}%")
        print("="*60)

        return {
            "passed": self.passed,
            "failed": self.failed,
            "total": self.passed + self.failed,
            "success_rate": self.passed/(self.passed+self.failed)*100 if (self.passed+self.failed) > 0 else 0
        }

if __name__ == "__main__":
    test = TestFindTransactions()
    test.run_all_tests()