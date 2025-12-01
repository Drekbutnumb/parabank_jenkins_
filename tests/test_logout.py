from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TestLogout:
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

    def test_logout_link_visible(self):
        print("\n=== TC_LOGOUT_01: Logout Link Visible After Login ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            try:
                logout_link = driver.find_element(By.LINK_TEXT, "Log Out")
                if logout_link.is_displayed():
                    print("[PASS] PASS: Logout link visible after login")
                    self.passed += 1
                else:
                    print("[FAIL] FAIL: Logout link not visible")
                    self.failed += 1
            except:
                print("[FAIL] FAIL: Logout link not found")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_successful_logout(self):
        print("\n=== TC_LOGOUT_02: Successful Logout ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log Out")))

            logout_link.click()
            time.sleep(2)

            try:
                login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
                print("[PASS] PASS: Logout successful, redirected to login page")
                self.passed += 1
            except:
                print("[FAIL] FAIL: Not redirected to login page after logout")
                self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_protected_page_after_logout(self):
        print("\n=== TC_LOGOUT_03: Protected Page Access After Logout ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log Out")))
            logout_link.click()
            time.sleep(2)

            driver.get("https://parabank.parasoft.com/parabank/overview.htm")
            time.sleep(2)

            page_source = driver.page_source.lower()

            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Server crashed instead of proper redirect")
                self.failed += 1
            else:
                try:
                    driver.find_element(By.NAME, "username")
                    print("[PASS] PASS: Protected page redirects to login after logout")
                    self.passed += 1
                except:
                    if "log in" in page_source:
                        print("[PASS] PASS: Access denied to protected page")
                        self.passed += 1
                    else:
                        print("[FAIL] FAIL: SECURITY BUG - Protected page accessible after logout")
                        self.failed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_back_button_after_logout(self):
        print("\n=== TC_LOGOUT_04: Back Button After Logout (SESSION) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/overview.htm")
            time.sleep(2)

            logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log Out")))
            logout_link.click()
            time.sleep(2)

            driver.back()
            time.sleep(2)

            page_source = driver.page_source.lower()

            if "accounts overview" in page_source and "$" in driver.page_source:
                print("[FAIL] FAIL: SECURITY BUG - Session restored after back button")
                self.failed += 1
            else:
                print("[PASS] PASS: Session not restored after back button")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_logout_link_not_visible_before_login(self):
        print("\n=== TC_LOGOUT_05: Logout Link Hidden Before Login (UI) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            driver.get("https://parabank.parasoft.com")
            time.sleep(2)

            logout_links = driver.find_elements(By.LINK_TEXT, "Log Out")

            if len(logout_links) == 0:
                print("[PASS] PASS: Logout link correctly hidden before login")
                self.passed += 1
            else:
                visible = any(link.is_displayed() for link in logout_links)
                if visible:
                    print("[FAIL] FAIL: BUG - Logout link visible before login")
                    self.failed += 1
                else:
                    print("[PASS] PASS: Logout link exists but hidden")
                    self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_multiple_logout_clicks(self):
        print("\n=== TC_LOGOUT_06: Multiple Logout Clicks ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log Out")))
            logout_link.click()
            time.sleep(1)

            try:
                logout_link2 = driver.find_element(By.LINK_TEXT, "Log Out")
                logout_link2.click()
                time.sleep(1)

                print("[PASS] PASS: Multiple logout handled gracefully")
                self.passed += 1
            except:
                print("[PASS] PASS: Logout link not available after logout")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_session_cookie_cleared(self):
        print("\n=== TC_LOGOUT_07: Session Cookie Cleared After Logout (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            cookies_before = driver.get_cookies()
            session_cookies_before = [c for c in cookies_before if 'session' in c['name'].lower() or 'jsession' in c['name'].lower()]

            logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log Out")))
            logout_link.click()
            time.sleep(2)

            cookies_after = driver.get_cookies()
            session_cookies_after = [c for c in cookies_after if 'session' in c['name'].lower() or 'jsession' in c['name'].lower()]

            if len(session_cookies_before) > 0:
                if len(session_cookies_after) == 0:
                    print("[PASS] PASS: Session cookies cleared after logout")
                    self.passed += 1
                elif session_cookies_before[0].get('value') != session_cookies_after[0].get('value'):
                    print("[PASS] PASS: Session cookie invalidated (value changed)")
                    self.passed += 1
                else:
                    print("[FAIL] FAIL: SECURITY BUG - Session cookie not cleared")
                    self.failed += 1
            else:
                print("[PASS] PASS: No session cookies found (may use different mechanism)")
                self.passed += 1

        except Exception as e:
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK LOGOUT FUNCTIONALITY TEST SUITE")
        print("="*60)

        self.test_logout_link_visible()
        self.test_successful_logout()
        self.test_protected_page_after_logout()
        self.test_back_button_after_logout()
        self.test_logout_link_not_visible_before_login()
        self.test_multiple_logout_clicks()
        self.test_session_cookie_cleared()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("LOGOUT FUNCTIONALITY TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}

if __name__ == "__main__":
    test_suite = TestLogout()
    test_suite.run_all_tests()