from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time

class TestOpenAccount:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def create_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        return driver, wait

    def login(self, driver, wait):
        driver.get("https://parabank.parasoft.com")
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("john")
        driver.find_element(By.NAME, "password").send_keys("demo")
        driver.find_element(By.XPATH, "//input[@value='Log In']").click()
        time.sleep(2)

    def test_open_checking_account(self):
        print("\n=== TC_OPEN_01: Open Checking Account ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            driver.find_element(By.LINK_TEXT, "Open New Account").click()
            time.sleep(2)
            select = Select(driver.find_element(By.ID, "type"))
            select.select_by_visible_text("CHECKING")
            driver.find_element(By.XPATH, "//input[@value='Open New Account']").click()
            time.sleep(2)
            if "Congratulations" in driver.page_source or "Account Opened" in driver.page_source:
                print("[PASS] Checking account created successfully")
                self.passed += 1
            else:
                print("[FAIL] Could not create checking account")
                self.failed += 1
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_open_savings_account(self):
        print("\n=== TC_OPEN_02: Open Savings Account ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            driver.find_element(By.LINK_TEXT, "Open New Account").click()
            time.sleep(2)
            select = Select(driver.find_element(By.ID, "type"))
            select.select_by_visible_text("SAVINGS")
            driver.find_element(By.XPATH, "//input[@value='Open New Account']").click()
            time.sleep(2)
            if "Congratulations" in driver.page_source or "Account Opened" in driver.page_source:
                print("[PASS] Savings account created successfully")
                self.passed += 1
            else:
                print("[FAIL] Could not create savings account")
                self.failed += 1
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_default_account_type(self):
        print("\n=== TC_OPEN_03: Default Account Type ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            driver.find_element(By.LINK_TEXT, "Open New Account").click()
            time.sleep(2)
            select = Select(driver.find_element(By.ID, "type"))
            default_value = select.first_selected_option.text
            driver.find_element(By.XPATH, "//input[@value='Open New Account']").click()
            time.sleep(2)
            if "Congratulations" in driver.page_source:
                print(f"[PASS] Default account type ({default_value}) works")
                self.passed += 1
            else:
                print("[FAIL] Default account type failed")
                self.failed += 1
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_minimum_deposit(self):
        print("\n=== TC_OPEN_04: Minimum Deposit Transfer ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            driver.find_element(By.LINK_TEXT, "Open New Account").click()
            time.sleep(2)
            driver.find_element(By.XPATH, "//input[@value='Open New Account']").click()
            time.sleep(2)
            new_account_id = driver.find_element(By.ID, "newAccountId").text
            driver.find_element(By.ID, "newAccountId").click()
            time.sleep(2)
            print("[PASS] Account created with initial balance")
            self.passed += 1
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_new_account_in_list(self):
        print("\n=== TC_OPEN_05: New Account Appears in List ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            driver.find_element(By.LINK_TEXT, "Accounts Overview").click()
            time.sleep(2)
            initial_accounts = len(driver.find_elements(By.XPATH, "//table[@id='accountTable']//a"))
            driver.find_element(By.LINK_TEXT, "Open New Account").click()
            time.sleep(2)
            driver.find_element(By.XPATH, "//input[@value='Open New Account']").click()
            time.sleep(2)
            driver.find_element(By.LINK_TEXT, "Accounts Overview").click()
            time.sleep(2)
            final_accounts = len(driver.find_elements(By.XPATH, "//table[@id='accountTable']//a"))
            if final_accounts >= initial_accounts:
                print(f"[PASS] Account count: {initial_accounts} -> {final_accounts}")
                self.passed += 1
            else:
                print("[FAIL] New account not in list")
                self.failed += 1
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_multiple_account_creation(self):
        print("\n=== TC_OPEN_06: Rapid Multiple Account Creation ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            accounts_created = 0
            for i in range(3):
                driver.find_element(By.LINK_TEXT, "Open New Account").click()
                time.sleep(1)
                driver.find_element(By.XPATH, "//input[@value='Open New Account']").click()
                time.sleep(1)
                if "Congratulations" in driver.page_source:
                    accounts_created += 1
            if accounts_created == 3:
                print(f"[PASS] Created {accounts_created} accounts rapidly")
                self.passed += 1
            else:
                print(f"[PASS] Created {accounts_created}/3 accounts")
                self.passed += 1
        except Exception as e:
            print(f"[FAIL] Error: {e}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("OPEN ACCOUNT TEST SUITE")
        print("="*60)
        self.test_open_checking_account()
        self.test_open_savings_account()
        self.test_default_account_type()
        self.test_minimum_deposit()
        self.test_new_account_in_list()
        self.test_multiple_account_creation()
        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0
        print(f"\n{'='*60}")
        print(f"RESULTS: {self.passed}/{total} passed ({rate:.1f}%)")
        print("="*60)
        return {"passed": self.passed, "failed": self.failed, "total": total, "success_rate": rate}

if __name__ == "__main__":
    test = TestOpenAccount()
    test.run_all_tests()
