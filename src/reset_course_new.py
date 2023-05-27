import pyautogui
import time
import pyperclip

def reset_course_new(link: str, us_id: str) -> bool:
    print("reset course function called")
    pyautogui.moveTo(217, 737)
    time.sleep(2)
    pyautogui.click(button='left')
    time.sleep(2)
    pyautogui.write(link)
    time.sleep(5)
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.moveTo(530, 453)
    time.sleep(2)
    pyautogui.click(button='left')
    time.sleep(2)
    pyautogui.write(us_id)
    time.sleep(3)
    pyautogui.press('tab')
    time.sleep(1)
    # pyautogui.write("alwaysbetraining2004")
    # time.sleep(2)
    pyautogui.moveTo(660, 582)
    time.sleep(2)
    pyautogui.click(button='left')
    time.sleep(7)
    pyautogui.hotkey('ctrl', 'shift', 'i')
    time.sleep(2)
    pyautogui.moveTo(160, 481)
    time.sleep(2)
    pyautogui.click(button='left')
    time.sleep(1)
    pyautogui.moveTo(68, 684)
    time.sleep(2)
    pyautogui.click(button='left')
    time.sleep(1)
    pyperclip.copy("""let dropdownBtns = document.querySelectorAll(
                ".ud-btn.ud-btn-large.ud-btn-link.ud-heading-md.js-panel-toggler.accordion-panel-module--panel-toggler--1RjML"
                );         

                dropdownBtns.forEach((dropdownBtn) => {
                // If is not expanded, then expand it.
                if (dropdownBtn.getAttribute("aria-expanded") === "false") {
                    dropdownBtn.click();
                }
                });
    let inputCheckBoxes = document.querySelectorAll(
            ".curriculum-item-link--progress-toggle--1CMcg.ud-toggle-input-container.ud-text-sm"
            );

            inputCheckBoxes.forEach((inputCheckBox) => {
            // If checked, then uncheck it.
            if(inputCheckBox.textContent.indexOf(" complete") !== -1) {
                inputCheckBox.click()
            }
            });

    """)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(7)
    pyautogui.moveTo(1349, 5)
    time.sleep(2)
    pyautogui.click(button='left')
    time.sleep(3)
    print("course reset done")
    return True


def main():
    reset_course_new("https://www.udemy.com/course/deeplearning/learn/lecture/6743222#overview","engage@fischerjordan.com")
    x,y=pyautogui.position()
    print(x,y)

if __name__ == "__main__":
    main()
