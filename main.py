import multiprocessing
import time
import pyautogui, pythoncom
import pyWinhook as pyHook
import queue
import pyscreenshot as ImageGrab
import pydirectinput as pyautogui
import time

class AutoClicker(multiprocessing.Process):
    def __init__(self, queue, interval):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.click_interval = interval

    def run(self):
        while True:
            try:
                task = self.queue.get(block=False)
                if task == "Exit":
                    print("Exiting")
                    self.queue.task_done()
                    break

            except queue.Empty:
                time.sleep(self.click_interval)
                print("Clicking...")
                pyautogui.click()
        return

def OnKeyboardEvent(event):

    key = event.Key

    if key == "F3":
        print("Starting auto clicker")
        # Start consumers
        clicker = AutoClicker(queue, 0.1)
        clicker.start()
    elif key == "F4":
        print("Stopping auto clicker")
        # Add exit message to queue
        queue.put("Exit")
        # Wait for all of the tasks to finish
        queue.join()

    # return True to pass the event to other handlers
    return True

if __name__ == '__main__':
    # Establish communication queues
    queue = multiprocessing.JoinableQueue()
    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    hm.KeyDown = OnKeyboardEvent
    # set the hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()