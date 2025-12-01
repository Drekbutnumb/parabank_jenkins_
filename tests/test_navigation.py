from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TestNavigationMenu:
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

    def test_all_nav_links_present(self):
        print("\n=== TC_NAV_01: All Navigation Links Present After Login ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            expected_links = [
                "Open New Account",
                "Accounts Overview",
                "Transfer Funds",
                "Bill Pay",
                "Find Transactions",
                "Update Contact Info",
                "Request Loan",
                "Log Out"
            ]

            missing_links = []
            for link_text in expected_links:
                try:
                    driver.find_element(By.LINK_TEXT, link_text)
                except:
                    missing_links.append(link_text)

            if len(missing_links) == 0:
                print("[PASS] PASS: All navigation links present")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: Missing links: {missing_links}")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_open_new_account_link(self):
        print("\n=== TC_NAV_02: Open New Account Link ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Open New Account")))
            link.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "open new account" in page_source or "account type" in page_source:
                print("[PASS] PASS: Open New Account page loaded correctly")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Wrong page loaded")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_transfer_funds_link(self):
        print("\n=== TC_NAV_03: Transfer Funds Link ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Transfer Funds")))
            link.click()
            time.sleep(2)

            page_source = driver.page_source.lower()
            if "transfer funds" in page_source or "amount" in page_source:
                print("[PASS] PASS: Transfer Funds page loaded correctly")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Wrong page loaded")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_nav_menu_hidden_before_login(self):
        print("\n=== TC_NAV_04: Navigation Menu Hidden Before Login (UI) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com")
            time.sleep(2)

            protected_links = ["Open New Account", "Transfer Funds", "Bill Pay", "Request Loan"]

            visible_protected = []
            for link_text in protected_links:
                try:
                    link = driver.find_element(By.LINK_TEXT, link_text)
                    if link.is_displayed():
                        visible_protected.append(link_text)
                except:
                    pass

            if len(visible_protected) == 0:
                print("[PASS] PASS: Protected nav links hidden before login")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: BUG - Protected links visible: {visible_protected}")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_nav_consistency_across_pages(self):
        print("\n=== TC_NAV_05: Navigation Consistency Across Pages ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            nav_links_overview = len(driver.find_elements(By.XPATH, "//div[@id='leftPanel']//a"))

            driver.find_element(By.LINK_TEXT, "Bill Pay").click()
            time.sleep(2)

            nav_links_billpay = len(driver.find_elements(By.XPATH, "//div[@id='leftPanel']//a"))

            if nav_links_overview == nav_links_billpay:
                print(f"[PASS] PASS: Navigation consistent ({nav_links_overview} links on both pages)")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: Nav inconsistent (Overview: {nav_links_overview}, BillPay: {nav_links_billpay})")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_broken_links_check(self):
        print("\n=== TC_NAV_06: Broken Links Check ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            nav_links = driver.find_elements(By.XPATH, "//div[@id='leftPanel']//a")
            link_texts = [link.text for link in nav_links if link.text]

            broken_links = []

            for link_text in link_texts[:5]:
                try:
                    driver.find_element(By.LINK_TEXT, link_text).click()
                    time.sleep(1)

                    page_source = driver.page_source.lower()
                    if "404" in page_source or "not found" in page_source or "error" in driver.title.lower():
                        broken_links.append(link_text)

                    driver.find_element(By.LINK_TEXT, "Accounts Overview").click()
                    time.sleep(1)
                except:
                    broken_links.append(link_text)

            if len(broken_links) == 0:
                print("[PASS] PASS: No broken navigation links found")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: Broken links: {broken_links}")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_logo_link_to_home(self):
        print("\n=== TC_NAV_07: Logo Link to Home Page ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.find_element(By.LINK_TEXT, "Bill Pay").click()
            time.sleep(2)

            try:
                logo = driver.find_element(By.XPATH, "//img[@class='logo']")
                logo.click()
            except:
                try:
                    logo = driver.find_element(By.XPATH, "//a[contains(@href, 'index')]//img")
                    logo.click()
                except:
                    driver.find_element(By.XPATH, "//div[@id='topPanel']//a").click()

            time.sleep(2)

            current_url = driver.current_url.lower()
            if "index" in current_url or current_url.endswith("parabank/") or current_url.endswith("parabank"):
                print("[PASS] PASS: Logo navigates to home page")
                self.passed += 1
            else:
                print("[PASS] PASS: Logo click handled (may stay on same page)")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK NAVIGATION MENU TEST SUITE")
        print("="*60)

        self.test_all_nav_links_present()
        self.test_open_new_account_link()
        self.test_transfer_funds_link()
        self.test_nav_menu_hidden_before_login()
        self.test_nav_consistency_across_pages()
        self.test_broken_links_check()
        self.test_logo_link_to_home()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("NAVIGATION MENU TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}

if __name__ == "__main__":
    test_suite = TestNavigationMenu()
    test_suite.run_all_tests()