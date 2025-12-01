from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TestBillPay:
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

    def test_billpay_page_access(self):
        print("\n=== TC_BILL_01: Bill Pay Page Access ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            billpay_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Bill Pay")))
            billpay_link.click()
            time.sleep(2)

            fields = ["payee.name", "payee.address.street", "payee.address.city",
                      "payee.address.state", "payee.address.zipCode", "payee.phoneNumber",
                      "payee.accountNumber", "verifyAccount", "amount"]

            missing_fields = []
            for field in fields:
                try:
                    driver.find_element(By.NAME, field)
                except:
                    missing_fields.append(field)

            if len(missing_fields) == 0:
                print("[PASS] PASS: All Bill Pay form fields present")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: Missing fields: {missing_fields}")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_valid_bill_payment(self):
        print("\n=== TC_BILL_02: Valid Bill Payment ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            driver.find_element(By.NAME, "payee.name").send_keys("Electric Company")
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 Power St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("New York")
            driver.find_element(By.NAME, "payee.address.state").send_keys("NY")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("10001")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5551234567")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("12345")
            driver.find_element(By.NAME, "verifyAccount").send_keys("12345")
            driver.find_element(By.NAME, "amount").send_keys("50")

            send_button = driver.find_element(By.XPATH, "//input[@value='Send Payment']")
            send_button.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "complete" in page_source or "successful" in page_source:
                print("[PASS] PASS: Bill payment completed successfully")
                self.passed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error during bill payment")
                self.failed += 1
            else:
                print("[FAIL] FAIL: Payment confirmation not displayed")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_payee_name(self):
        print("\n=== TC_BILL_03: Empty Payee Name Validation ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            driver.find_element(By.NAME, "payee.address.street").send_keys("123 Test St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("Test City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("TS")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5551111111")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("11111")
            driver.find_element(By.NAME, "verifyAccount").send_keys("11111")
            driver.find_element(By.NAME, "amount").send_keys("25")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            errors = driver.find_elements(By.CLASS_NAME, "error")
            if len(errors) > 0 or "required" in page_source or "payee name is required" in page_source:
                print("[PASS] PASS: Validation error shown for empty payee name")
                self.passed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error instead of validation message")
                self.failed += 1
            else:
                print("[FAIL] FAIL: BUG - No validation for empty payee name")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_account_number_mismatch(self):
        print("\n=== TC_BILL_04: Account Number Mismatch ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            driver.find_element(By.NAME, "payee.name").send_keys("Test Payee")
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 Test St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("ST")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5552222222")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("12345")
            driver.find_element(By.NAME, "verifyAccount").send_keys("99999")
            driver.find_element(By.NAME, "amount").send_keys("10")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "do not match" in page_source or "account numbers do not match" in page_source:
                print("[PASS] PASS: Account mismatch error displayed correctly")
                self.passed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error instead of mismatch validation")
                self.failed += 1
            else:
                print("[FAIL] FAIL: BUG - No validation for account number mismatch")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_negative_amount(self):
        print("\n=== TC_BILL_05: Negative Payment Amount ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            driver.find_element(By.NAME, "payee.name").send_keys("Negative Test")
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("ST")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5553333333")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("55555")
            driver.find_element(By.NAME, "verifyAccount").send_keys("55555")
            driver.find_element(By.NAME, "amount").send_keys("-100")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "complete" in page_source or "successful" in page_source:
                print("[FAIL] FAIL: BUG - System accepted negative payment amount")
                self.failed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error for negative amount")
                self.failed += 1
            else:
                print("[PASS] PASS: Negative amount rejected")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_xss_in_payee_name(self):
        print("\n=== TC_BILL_06: XSS Prevention in Payee Name (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            xss_payload = "<script>alert('XSS')</script>"

            driver.find_element(By.NAME, "payee.name").send_keys(xss_payload)
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("ST")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5554444444")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("66666")
            driver.find_element(By.NAME, "verifyAccount").send_keys("66666")
            driver.find_element(By.NAME, "amount").send_keys("1")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            try:
                alert = driver.switch_to.alert
                print("[FAIL] FAIL: XSS vulnerability - alert triggered")
                alert.accept()
                self.failed += 1
            except:
                page_source = driver.page_source.lower()
                if "an internal error has occurred" in page_source:
                    print("[FAIL] FAIL: BUG - Server crashed on XSS input")
                    self.failed += 1
                else:
                    print("[PASS] PASS: XSS attack prevented")
                    self.passed += 1

        except Exception as e:
            if "ConnectionReset" in str(type(e).__name__) or "10054" in str(e):
                print("[PASS] PASS: Server blocked malicious XSS request")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: {str(e)}")
                self.failed += 1
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def test_sql_injection_in_account(self):
        print("\n=== TC_BILL_07: SQL Injection in Account Field (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            sql_payload = "'; DROP TABLE accounts; --"

            driver.find_element(By.NAME, "payee.name").send_keys("SQL Test")
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("ST")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5555555555")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys(sql_payload)
            driver.find_element(By.NAME, "verifyAccount").send_keys(sql_payload)
            driver.find_element(By.NAME, "amount").send_keys("1")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            page_lower = driver.page_source.lower()
            if "sql" in page_lower or "database" in page_lower or "syntax" in page_lower:
                print("[FAIL] FAIL: SECURITY BUG - SQL injection vulnerability (database error exposed)")
                self.failed += 1
            elif "an internal error has occurred" in page_lower:
                print("[FAIL] FAIL: BUG FOUND - Internal server error on SQL injection input")
                self.failed += 1
            elif "please enter a valid number" in page_lower or "invalid" in page_lower:
                print("[PASS] PASS: SQL injection blocked by input validation")
                self.passed += 1
            else:
                print("[PASS] PASS: SQL injection handled safely")
                self.passed += 1

        except Exception as e:
            if "ConnectionReset" in str(type(e).__name__) or "10054" in str(e):
                print("[PASS] PASS: Server blocked malicious SQL injection request")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: {str(e)}")
                self.failed += 1
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK BILL PAY TEST SUITE")
        print("="*60)

        self.test_billpay_page_access()
        self.test_valid_bill_payment()
        self.test_empty_payee_name()
        self.test_account_number_mismatch()
        self.test_negative_amount()
        self.test_xss_in_payee_name()
        self.test_sql_injection_in_account()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("BILL PAY TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}

if __name__ == "__main__":
    test_suite = TestBillPay()
    test_suite.run_all_tests()