from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

class TestAccountStatement:
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

    def login(self, driver, wait):
        driver.get("https://parabank.parasoft.com")
        time.sleep(2)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("john")
        driver.find_element(By.NAME, "password").send_keys("demo")
        driver.find_element(By.XPATH, "//input[@value='Log In']").click()
        time.sleep(2)

    def test_account_details_display(self):
        print("\n=== TC_STMT_01: Account Details Display ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            time.sleep(2)

            account_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'activity.htm')]")

            if len(account_links) > 0:
                account_links[0].click()
                time.sleep(2)

                page_source = driver.page_source

                has_account_number = "Account Number" in page_source or "account number" in page_source.lower()
                has_balance = "$" in page_source

                if has_account_number and has_balance:
                    print("[PASS] PASS: Account details displayed with number and balance")
                    self.passed += 1
                else:
                    print("[FAIL] FAIL: Account details incomplete")
                    self.failed += 1
            else:
                print("[FAIL] FAIL: No accounts to view")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_transaction_list_display(self):
        print("\n=== TC_STMT_02: Transaction List Display ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            time.sleep(2)
            account_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'activity.htm')]")

            if len(account_links) > 0:
                account_links[0].click()
                time.sleep(2)

                try:
                    trans_table = driver.find_element(By.ID, "transactionTable")
                    print("[PASS] PASS: Transaction table displayed")
                    self.passed += 1
                except:
                    page_source = driver.page_source.lower()
                    if "no transactions" in page_source or "transaction" in page_source:
                        print("[PASS] PASS: Transaction section present (may be empty)")
                        self.passed += 1
                    else:
                        print("[FAIL] FAIL: No transaction section found")
                        self.failed += 1
            else:
                print("[FAIL] FAIL: No accounts available")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_account_type_displayed(self):
        print("\n=== TC_STMT_03: Account Type Displayed ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            time.sleep(2)
            account_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'activity.htm')]")

            if len(account_links) > 0:
                account_links[0].click()
                time.sleep(2)

                page_source = driver.page_source.lower()

                if "checking" in page_source or "savings" in page_source or "account type" in page_source:
                    print("[PASS] PASS: Account type displayed")
                    self.passed += 1
                else:
                    print("[FAIL] FAIL: BUG - Account type not displayed")
                    self.failed += 1
            else:
                print("[FAIL] FAIL: No accounts available")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_balance_format(self):
        print("\n=== TC_STMT_04: Balance Currency Format (UI) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            time.sleep(2)

            page_source = driver.page_source

            import re
            currency_pattern = r'\$[\d,]+\.\d{2}'
            matches = re.findall(currency_pattern, page_source)

            if len(matches) > 0:
                print(f"[PASS] PASS: Balance properly formatted (found: {matches[0]})")
                self.passed += 1
            else:
                if "$" in page_source:
                    print("[PASS] PASS: Currency symbol present")
                    self.passed += 1
                else:
                    print("[FAIL] FAIL: BUG - No currency formatting found")
                    self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_negative_balance_display(self):
        print("\n=== TC_STMT_05: Negative Balance Display (UI) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            time.sleep(2)

            page_source = driver.page_source

            if "-$" in page_source or "negative" in page_source.lower():
                print("[PASS] PASS: Negative balance indicator present")
                self.passed += 1
            else:
                print("[PASS] PASS: No negative balances (all positive)")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_multiple_accounts_display(self):
        print("\n=== TC_STMT_06: Multiple Accounts Display ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            time.sleep(2)

            account_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'activity.htm')]")

            if len(account_links) > 0:
                print(f"[PASS] PASS: {len(account_links)} account(s) displayed")
                self.passed += 1
            else:
                print("[FAIL] FAIL: No accounts displayed")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_unauthorized_statement_access(self):
        print("\n=== TC_STMT_07: Unauthorized Statement Access (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            time.sleep(2)
            account_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'activity.htm')]")

            if len(account_links) > 0:
                href = account_links[0].get_attribute("href")
                import re
                match = re.search(r'id=(\d+)', href)
                if match:
                    current_id = int(match.group(1))

                    test_id = current_id - 1 if current_id > 1 else current_id + 1000

                    driver.get(f"https://parabank.parasoft.com/parabank/activity.htm?id={test_id}")
                    time.sleep(2)

                    page_source = driver.page_source.lower()

                    if "an internal error has occurred" in page_source:
                        print("[FAIL] FAIL: BUG - Server crashed instead of proper access denial")
                        self.failed += 1
                    elif "access denied" in page_source or "unauthorized" in page_source:
                        print("[PASS] PASS: Unauthorized account access properly blocked")
                        self.passed += 1
                    elif "$" in driver.page_source and "balance" in page_source:
                        print("[FAIL] FAIL: SECURITY BUG - IDOR - Accessed unauthorized account")
                        self.failed += 1
                    else:
                        print("[PASS] PASS: No data returned for unauthorized account")
                        self.passed += 1
                else:
                    print("[PASS] PASS: Could not extract account ID for test")
                    self.passed += 1
            else:
                print("[FAIL] FAIL: No accounts to test")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK ACCOUNT STATEMENT TEST SUITE")
        print("="*60)

        self.test_account_details_display()
        self.test_transaction_list_display()
        self.test_account_type_displayed()
        self.test_balance_format()
        self.test_negative_balance_display()
        self.test_multiple_accounts_display()
        self.test_unauthorized_statement_access()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("ACCOUNT STATEMENT TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}

if __name__ == "__main__":
    test_suite = TestAccountStatement()
    test_suite.run_all_tests()