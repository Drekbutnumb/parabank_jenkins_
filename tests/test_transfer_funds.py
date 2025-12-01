from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

class TestTransferFunds:
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

    def login(self, driver, wait):
        username_field = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys("john")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("demo")

        login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
        login_button.click()

        time.sleep(2)

    def test_valid_transfer(self):
        print("\n=== TC_TRANSFER_01: Valid Transfer Between Accounts ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            transfer_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))
            )
            transfer_link.click()

            time.sleep(2)

            amount_field = wait.until(
                EC.presence_of_element_located((By.ID, "amount"))
            )
            amount_field.send_keys("100")

            transfer_button = driver.find_element(By.XPATH, "//input[@value='Transfer']")
            transfer_button.click()

            time.sleep(3)

            try:
                success_message = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Transfer Complete')]"))
                )
                print("[PASS] PASS: Transfer of $100 completed successfully")
                self.passed += 1
            except:
                print("[FAIL] FAIL: Transfer completion message not found")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_insufficient_funds_transfer(self):
        print("\n=== TC_TRANSFER_02: Transfer With Insufficient Funds ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            transfer_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))
            )
            transfer_link.click()

            time.sleep(2)

            amount_field = wait.until(
                EC.presence_of_element_located((By.ID, "amount"))
            )
            amount_field.send_keys("999999999")

            transfer_button = driver.find_element(By.XPATH, "//input[@value='Transfer']")
            transfer_button.click()

            time.sleep(3)

            page_source = driver.page_source.lower()
            if "transfer complete" in page_source:
                print("[FAIL] FAIL: BUG - System accepted $999M transfer without balance check")
                self.failed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed instead of validation error")
                self.failed += 1
            elif "insufficient" in page_source:
                print("[PASS] PASS: Insufficient funds error displayed correctly")
                self.passed += 1
            else:
                print("[FAIL] FAIL: No proper validation for large amount")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_zero_amount_transfer(self):
        print("\n=== TC_TRANSFER_03: Transfer With Zero Amount ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            transfer_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))
            )
            transfer_link.click()

            time.sleep(2)

            amount_field = wait.until(
                EC.presence_of_element_located((By.ID, "amount"))
            )
            amount_field.send_keys("0")

            transfer_button = driver.find_element(By.XPATH, "//input[@value='Transfer']")
            transfer_button.click()

            time.sleep(3)

            page_source = driver.page_source.lower()
            if "transfer complete" in page_source:
                print("[FAIL] FAIL: BUG - System accepted $0 transfer (should reject)")
                self.failed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed instead of validation error")
                self.failed += 1
            else:
                print("[PASS] PASS: Zero amount transfer rejected")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_amount_transfer(self):
        print("\n=== TC_TRANSFER_04: Transfer With Empty Amount ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            transfer_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))
            )
            transfer_link.click()

            time.sleep(2)

            transfer_button = driver.find_element(By.XPATH, "//input[@value='Transfer']")
            transfer_button.click()

            time.sleep(3)

            page_source = driver.page_source.lower()
            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed on empty amount (should show validation)")
                self.failed += 1
            elif "transfer complete" in page_source:
                print("[FAIL] FAIL: BUG - Empty amount transfer was accepted")
                self.failed += 1
            elif "required" in page_source or "enter" in page_source or "please" in page_source:
                print("[PASS] PASS: Empty amount validation error displayed correctly")
                self.passed += 1
            else:
                print("[PASS] PASS: Empty amount transfer was blocked")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_decimal_amount_transfer(self):
        print("\n=== TC_TRANSFER_05: Transfer Decimal Amount ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            transfer_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))
            )
            transfer_link.click()

            time.sleep(2)

            amount_field = wait.until(
                EC.presence_of_element_located((By.ID, "amount"))
            )
            amount_field.send_keys("25.75")

            transfer_button = driver.find_element(By.XPATH, "//input[@value='Transfer']")
            transfer_button.click()

            time.sleep(3)

            try:
                success_message = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Transfer Complete')]"))
                )
                print("[PASS] PASS: Decimal amount transfer of $25.75 completed successfully")
                self.passed += 1
            except:
                print("[FAIL] FAIL: Decimal amount transfer failed")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_negative_amount_transfer(self):
        print("\n=== TC_TRANSFER_06: Negative Amount Transfer Validation (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            transfer_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))
            )
            transfer_link.click()

            time.sleep(2)

            amount_field = wait.until(
                EC.presence_of_element_located((By.ID, "amount"))
            )
            amount_field.send_keys("-100")

            transfer_button = driver.find_element(By.XPATH, "//input[@value='Transfer']")
            transfer_button.click()

            time.sleep(3)

            page_source = driver.page_source.lower()
            if "transfer complete" in page_source:
                print("[FAIL] FAIL: BUG - System accepted NEGATIVE amount transfer")
                self.failed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed on negative amount")
                self.failed += 1
            else:
                print("[PASS] PASS: Negative amount properly rejected")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_same_account_transfer(self):
        print("\n=== TC_TRANSFER_07: Transfer Between Same Account (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            transfer_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds"))
            )
            transfer_link.click()

            time.sleep(2)

            from_account = Select(driver.find_element(By.ID, "fromAccountId"))
            to_account = Select(driver.find_element(By.ID, "toAccountId"))

            first_option = from_account.options[0].get_attribute("value")

            from_account.select_by_value(first_option)
            to_account.select_by_value(first_option)

            amount_field = driver.find_element(By.ID, "amount")
            amount_field.send_keys("50")

            transfer_button = driver.find_element(By.XPATH, "//input[@value='Transfer']")
            transfer_button.click()

            time.sleep(3)

            page_source = driver.page_source.lower()
            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed on same-account transfer")
                self.failed += 1
            elif "transfer complete" in page_source:
                print("[FAIL] FAIL: BUG - System allowed same-account transfer (should be prevented)")
                self.failed += 1
            elif "cannot transfer" in page_source or "same account" in page_source:
                print("[PASS] PASS: System properly prevents same-account transfer")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Unexpected behavior on same-account transfer")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK TRANSFER FUNDS AUTOMATION TEST SUITE")
        print("="*60)

        self.test_valid_transfer()
        self.test_insufficient_funds_transfer()
        self.test_zero_amount_transfer()
        self.test_empty_amount_transfer()
        self.test_decimal_amount_transfer()
        self.test_negative_amount_transfer()
        self.test_same_account_transfer()

        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print("\n" + "="*60)
        print("TRANSFER FUNDS TEST SUITE COMPLETED")
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
    test_suite = TestTransferFunds()
    test_suite.run_all_tests()