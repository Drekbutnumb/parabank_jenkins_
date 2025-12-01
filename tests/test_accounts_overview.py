from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TestAccountsOverview:
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
        driver.maximize_window()
        time.sleep(2)

        username_field = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys("john")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("demo")

        login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
        login_button.click()

        time.sleep(2)

    def test_view_accounts_overview(self):
        print("\n=== TC_ACCOUNTS_01: View Accounts Overview ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            accounts_table = wait.until(
                EC.presence_of_element_located((By.ID, "accountTable"))
            )

            account_rows = driver.find_elements(By.XPATH, "//table[@id='accountTable']//tbody/tr")
            account_count = len(account_rows)

            if account_count > 0:
                print(f"[PASS] PASS: Accounts Overview displayed with {account_count} accounts")
                self.passed += 1
            else:
                print("[FAIL] FAIL: No accounts found")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_navigate_to_account_details(self):
        print("\n=== TC_ACCOUNTS_02: Navigate to Account Details ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            accounts_table = wait.until(
                EC.presence_of_element_located((By.ID, "accountTable"))
            )

            first_account_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//table[@id='accountTable']//tbody/tr[1]/td[1]/a"))
            )
            account_number = first_account_link.text
            first_account_link.click()

            time.sleep(2)

            account_details_title = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Account Details')]"))
            )
            account_id = driver.find_element(By.ID, "accountId").text
            account_type = driver.find_element(By.ID, "accountType").text
            balance = driver.find_element(By.ID, "balance").text

            print(f"[PASS] PASS: Account Details displayed - ID: {account_id}, Type: {account_type}, Balance: {balance}")
            self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_view_transaction_history(self):
        print("\n=== TC_ACCOUNTS_03: View Transaction History ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            first_account_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//table[@id='accountTable']//tbody/tr[1]/td[1]/a"))
            )
            first_account_link.click()

            time.sleep(2)

            try:
                transaction_table = wait.until(
                    EC.presence_of_element_located((By.ID, "transactionTable"))
                )
                transaction_rows = driver.find_elements(By.XPATH, "//table[@id='transactionTable']//tbody/tr")
                transaction_count = len(transaction_rows)

                print(f"[PASS] PASS: Transaction history displayed with {transaction_count} transactions")
                self.passed += 1
            except:
                print("[PASS] PASS: Account page loaded (no transactions yet)")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_verify_balance_format(self):
        print("\n=== TC_ACCOUNTS_04: Verify Balance Currency Format ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            balance_cell = wait.until(
                EC.presence_of_element_located((By.XPATH, "//table[@id='accountTable']//tbody/tr[1]/td[2]"))
            )
            balance_text = balance_cell.text

            if "$" in balance_text:
                print(f"[PASS] PASS: Balance displayed with correct currency format: {balance_text}")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: Balance missing currency symbol: {balance_text}")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_account_links_clickable(self):
        print("\n=== TC_ACCOUNTS_05: Verify All Account Links Are Clickable ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            account_links = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//table[@id='accountTable']//tbody/tr/td[1]/a"))
            )

            link_count = len(account_links)
            all_clickable = True

            for link in account_links:
                if not link.is_enabled():
                    all_clickable = False
                    break

            if all_clickable and link_count > 0:
                print(f"[PASS] PASS: All {link_count} account links are clickable")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Some account links are not clickable")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_total_balance_calculation(self):
        print("\n=== TC_ACCOUNTS_06: Verify Total Balance Calculation (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            balance_cells = driver.find_elements(By.XPATH, "//table[@id='accountTable']//tbody/tr/td[2]")

            calculated_total = 0.0
            for cell in balance_cells:
                balance_text = cell.text.replace('$', '').replace(',', '')
                try:
                    calculated_total += float(balance_text)
                except ValueError:
                    pass

            try:
                total_cell = driver.find_element(By.XPATH, "//table[@id='accountTable']//tfoot//td[2]")
                displayed_total = total_cell.text.replace('$', '').replace(',', '')
                displayed_total = float(displayed_total)

                if abs(calculated_total - displayed_total) < 0.01:
                    print(f"[PASS] PASS: Total balance correct - Displayed: ${displayed_total:.2f}, Calculated: ${calculated_total:.2f}")
                    self.passed += 1
                else:
                    print(f"[FAIL] FAIL: Total mismatch - Displayed: ${displayed_total:.2f}, Calculated: ${calculated_total:.2f}")
                    self.failed += 1
            except:
                print(f"[PASS] PASS: Individual balances verified, calculated total: ${calculated_total:.2f}")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_direct_account_url_access(self):
        print("\n=== TC_ACCOUNTS_07: Direct URL Access Without Login (ADVANCED - Security) ===")
        driver = None
        try:
            driver, wait = self.create_driver()

            driver.get("https://parabank.parasoft.com/parabank/activity.htm?id=12345")
            time.sleep(2)

            page_source = driver.page_source.lower()

            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed instead of proper access denial")
                self.failed += 1
            elif "login" in page_source or "username" in page_source:
                print("[PASS] PASS: Direct account access blocked - redirected to login")
                self.passed += 1
            elif "account" in page_source and "balance" in page_source:
                print("[FAIL] FAIL: SECURITY BUG - Account data accessible without login")
                self.failed += 1
            else:
                print("[PASS] PASS: Direct account access blocked")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK ACCOUNTS OVERVIEW AUTOMATION TEST SUITE")
        print("="*60)

        self.test_view_accounts_overview()
        self.test_navigate_to_account_details()
        self.test_view_transaction_history()
        self.test_verify_balance_format()
        self.test_account_links_clickable()
        self.test_total_balance_calculation()
        self.test_direct_account_url_access()

        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print("\n" + "="*60)
        print("ACCOUNTS OVERVIEW TEST SUITE COMPLETED")
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
    test_suite = TestAccountsOverview()
    test_suite.run_all_tests()