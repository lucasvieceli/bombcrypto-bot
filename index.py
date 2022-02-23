# -*- coding: utf-8 -*-    
from src.logger import logger, loggerMapClicked, loggerRegisterBcoin, getLastBcoinDate
from src.date import dateFormatted
from cv2 import cv2
from os import listdir
from random import randint
from random import random
import numpy as np
import mss
import pyautogui
import time
import sys
import yaml
import subprocess
import pyperclip

if sys.platform != 'linux' and sys.platform != 'linux2':
    import pygetwindow

# Load config file.
stream = open("config.yaml", 'r')
c = yaml.safe_load(stream)
ct = c['threshold']
ch = c['home']
pause = c['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = pause
pyautogui.FAILSAFE = False

cat = """
                                                _
                                                \`*-.
                                                 )  _`-.
                                                .  : `. .
                                                : _   '  \\
                                                ; *` _.   `*-._
                                                `-.-'          `-.
                                                  ;       `       `.
                                                  :.       .        \\
                                                  . \  .   :   .-'   .
                                                  '  `+.;  ;  '      :
                                                  :  '  |    ;       ;-.
                                                  ; '   : :`-:     _.`* ;
                                               .*' /  .*' ; .*`- +'  `*'
                                               `*-*   `*-*  `*-*'
=========================================================================
========== 💰 Have I helped you in any way? All I ask is a tip! 🧾 ======
========== ✨ Faça sua boa ação de hoje, manda aquela gorjeta! 😊 =======
=========================================================================
======================== vvv BCOIN BUSD BNB vvv =========================
============== 0xbd06182D8360FB7AC1B05e871e56c76372510dDf ===============
=========================================================================
===== https://www.paypal.com/donate?hosted_button_id=JVYSC6ZYCNQQQ ======
=========================================================================

>>---> Press ctrl + c to kill the bot.

>>---> Some configs can be found in the config.yaml file."""




def get_linux_bombcrypto_windows():
    stdout = (subprocess.Popen("xdotool search --name Bombcrypto", shell=True,stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip())
    windows = stdout.split('\n')
    return windows

def activate_linux_window(window_id):
    subprocess.Popen(f"xdotool windowactivate {window_id}", shell=True)


def addRandomness(n, randomn_factor_size=None):
    """Returns n with randomness
    Parameters:
        n (int): A decimal integer
        randomn_factor_size (int): The maximum value+- of randomness that will be
            added to n

    Returns:
        int: n with randomness
    """

    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    # logger('{} with randomness -> {}'.format(int(n), randomized_n))
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)


def remove_suffix(input_string, suffix):
    """Returns the input_string without the suffix"""

    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images(dir_path='./targets/'):
    """ Programatically loads all images of dir_path as a key:value where the
        key is the file name without the .png suffix

    Returns:
        dict: dictionary containing the loaded images as key:value pairs.
    """

    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets


def loadHeroesToSendHome():
    """Loads the images in the path and saves them as a list"""
    file_names = listdir('./targets/heroes-to-send-home')
    heroes = []
    for file in file_names:
        path = './targets/heroes-to-send-home/' + file
        heroes.append(cv2.imread(path))

    print('>>---> %d heroes that should be sent home loaded' % len(heroes))
    return heroes





def show(rectangles, img = None):
    """ Show an popup with rectangles showing the rectangles[(x, y, w, h),...]
        over img or a printSreen if no img provided. Useful for debugging"""

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)





def clickBtn(img, timeout=3, threshold = ct['default']):
    """Search for img in the scree, if found moves the cursor over it and clicks.
    Parameters:
        img: The image that will be used as an template to find where to click.
        timeout (int): Time in seconds that it will keep looking for the img before returning with fail
        threshold(float): How confident the bot needs to be to click the buttons (values from 0 to 1)
    """

    logger(None, progress_indicator=True)
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(img, threshold=threshold)

        if(len(matches)==0):
            has_timed_out = time.time()-start > timeout
            continue

        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True

    return False

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:,:,:3]

def positions(target, threshold=ct['default'],img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll():

    commoms = positions(images['commom-text'], threshold = ct['commom'])
    if (len(commoms) == 0):
        commoms = positions(images['rare-text'], threshold = ct['rare'])
        if (len(commoms) == 0):
            commoms = positions(images['super_rare-text'], threshold = ct['super_rare'])
            if (len(commoms) == 0):
                commoms = positions(images['epic-text'], threshold = ct['epic'])
                if (len(commoms) == 0):
                    return
    x,y,w,h = commoms[len(commoms)-1]
#
    moveToWithRandomness(x,y,1)

    if not c['use_click_and_drag_instead_of_scroll']:
        pyautogui.scroll(-c['scroll_size'])
    else:
        pyautogui.dragRel(0,-c['click_and_drag_amount'],duration=1, button='left')


def clickButtons():
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    # print('buttons: {}'.format(len(buttons)))
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
        if hero_clicks > 20:
            logger('too many hero clicks, try to increase the go_to_work_btn threshold')
            return
    return len(buttons)

def isHome(hero, buttons):
    y = hero[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            # if send-home button exists, the hero is not home
            return False
    return True

def isWorking(bar, buttons):
    y = bar[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True

def clickGreenBarButtons():
    # ele clicka nos q tao trabaiano mas axo q n importa
    offset = 140

    green_bars = positions(images['green-bar'], threshold=ct['green_bar'])
    logger('🟩 %d green bars detected' % len(green_bars))
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])
    logger('🆗 %d buttons detected' % len(buttons))


    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        logger('🆗 %d buttons with green bar detected' % len(not_working_green_bars))
        logger('👆 Clicking in %d heroes' % len(not_working_green_bars))

    # se tiver botao com y maior que bar y-10 e menor que y+10
    hero_clicks_cnt = 0
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        moveToWithRandomness(x+offset+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1
        hero_clicks_cnt = hero_clicks_cnt + 1
        if hero_clicks_cnt > 20:
            logger('⚠️ Too many hero clicks, try to increase the go_to_work_btn threshold')
            return
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)

def clickFullBarButtons():
    offset = 100
    full_bars = positions(images['full-stamina'], threshold=ct['default'])
    buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    not_working_full_bars = []
    for bar in full_bars:
        if not isWorking(bar, buttons):
            not_working_full_bars.append(bar)

    if len(not_working_full_bars) > 0:
        logger('👆 Clicking in %d heroes' % len(not_working_full_bars))

    for (x, y, w, h) in not_working_full_bars:
        moveToWithRandomness(x+offset+(w/2),y+(h/2),1)
        pyautogui.click()
        global hero_clicks
        hero_clicks = hero_clicks + 1

    return len(not_working_full_bars)

def goToHeroes():
    if clickBtn(images['go-back-arrow']):
        global login_attempts
        login_attempts = 0

    #TODO tirar o sleep quando colocar o pulling
    time.sleep(1)
    clickBtn(images['hero-icon'])
    time.sleep(randint(1,3))

def goToGame():
    # in case of server overload popup
    clickBtn(images['x'])
    # time.sleep(3)
    clickBtn(images['x'])

    clickBtn(images['treasure-hunt-icon'])

def refreshHeroesPositions():

    logger('🔃 Refreshing Heroes Positions')
    clickBtn(images['go-back-arrow'])
    clickBtn(images['treasure-hunt-icon'])

    # time.sleep(3)
    clickBtn(images['treasure-hunt-icon'])

def login():
    global login_attempts
    logger('😿 Checking if game has disconnected')

    if login_attempts > 3:
        logger('🔃 Too many login attempts, refreshing')
        login_attempts = 0
        pyautogui.hotkey('ctrl','f5')
        return
        
    if clickBtn(images['accept-checkbox'], timeout = 10):
        clickBtn(images['accept-button'])

    if clickBtn(images['connect-wallet'], timeout = 10):
        clickBtn(images['login'])
    
        logger('🎉 Connect wallet button detected, logging in!')
        login_attempts = login_attempts + 1
        #TODO mto ele da erro e poco o botao n abre
        # time.sleep(10)

        if clickBtn(images['select-wallet-2'], timeout=15):
            # sometimes the sign popup appears imediately
            login_attempts = login_attempts + 1
            # print('sign button clicked')
            # print('{} login attempt'.format(login_attempts))
            if clickBtn(images['treasure-hunt-icon'], timeout = 15):
                # print('sucessfully login, treasure hunt btn clicked')
                login_attempts = 0
            return
            # click ok butto

    if clickBtn(images['ok'], timeout=5):
        pass
        # time.sleep(15)
        # print('ok button clicked')



def sendHeroesHome():
    if not ch['enable']:
        return
    heroes_positions = []
    for hero in home_heroes:
        hero_positions = positions(hero, threshold=ch['hero_threshold'])
        if not len (hero_positions) == 0:
            #TODO maybe pick up match with most wheight instead of first
            hero_position = hero_positions[0]
            heroes_positions.append(hero_position)

    n = len(heroes_positions)
    if n == 0:
        print('No heroes that should be sent home found.')
        return
    print(' %d heroes that should be sent home found' % n)
    # if send-home button exists, the hero is not home
    go_home_buttons = positions(images['send-home'], threshold=ch['home_button_threshold'])
    # TODO pass it as an argument for both this and the other function that uses it
    go_work_buttons = positions(images['go-work'], threshold=ct['go_to_work_btn'])

    for position in heroes_positions:
        if not isHome(position,go_home_buttons):
            print(isWorking(position, go_work_buttons))
            if(not isWorking(position, go_work_buttons)):
                print ('hero not working, sending him home')
                moveToWithRandomness(go_home_buttons[0][0]+go_home_buttons[0][2]/2,position[1]+position[3]/2,1)
                pyautogui.click()
            else:
                print ('hero working, not sending him home(no dark work button)')
        else:
            print('hero already home, or home full(no dark home button)')





def refreshHeroes():
    logger('🏢 Search for heroes to work')

    goToHeroes()

    if c['select_heroes_mode'] == "full":
        logger('⚒️ Sending heroes with full stamina bar to work', 'green')
    elif c['select_heroes_mode'] == "green":
        logger('⚒️ Sending heroes with green stamina bar to work', 'green')
    else:
        logger('⚒️ Sending all heroes to work', 'green')

    buttonsClicked = 1
    empty_scrolls_attempts = 5

    while(empty_scrolls_attempts >= 0):
        if c['select_heroes_mode'] == 'full':
            buttonsClicked = clickFullBarButtons()
        elif c['select_heroes_mode'] == 'green':
            buttonsClicked = clickGreenBarButtons()
        else:
            buttonsClicked = clickButtons()

        clickFullBarButtons()

        sendHeroesHome()

        #if buttonsClicked == 0:
        empty_scrolls_attempts = empty_scrolls_attempts - 1
        scroll()
        time.sleep(2)
    logger('💪 {} heroes sent to work'.format(hero_clicks))
    goToGame()

def getDigitsBcoin():
    img = printSreen()
    d = images
    digits = []
    search = ['0','1','2','3','4','5','6','7','8','9', 'ponto']
    for i in search: 

        p = positions(d[i],img=img,threshold=0.95)
        for (x, y, w, h) in p:
            if x > 0:
                if i == 'ponto':
                    dig = '.'
                else:
                    dig = i

                digits.append({'digit':dig  ,'x':x})
	
    def getX(e):
        return e['x']
        
    if not len (digits) == 0:
        digits.sort(key=getX)
        digits.pop()
        r = list(map(lambda x : x['digit'],digits))
        return(''.join(r))
    else:
        return ''
def getIdMetamask():
    logger('Get id metamask')
    clickBtn(images['metamask'])
    clickBtn(images['copy'], 15)
    id = pyperclip.paste()
    
    buttons = positions(images['metamask'], threshold=ct['default'])
    
    if(len(buttons)>0):
        x =  buttons[0][0]
        y = buttons[0][1]
        
        moveToWithRandomness( x-400,y +100,1)
        pyautogui.click()
    
    time.sleep(2)
    if not len(id) > 10:
        return 0

    
    return id

def registerBcoin(idMeta):
    hour = dateFormatted('%H')
    minu = dateFormatted('%M')
    current_date = dateFormatted('%Y-%m-%d')
    last_date = getLastBcoinDate(idMeta)

    
    if last_date < current_date and hour == '01':

    	logger('Registering last bcoin')

    	clickBtn(images['chest'])
    	time.sleep(8)


    	digits = getDigitsBcoin()
    	loggerRegisterBcoin(digits, idMeta)
    	
    	logger(digits)
    	clickBtn(images['x'])

def checkChest():
    img = printSreen()
    chest1 = len(positions(images['chest1'],img=img,threshold=0.8))
    chest2 = len(positions(images['chest2'],img=img,threshold=0.8))
    chest3 = len(positions(images['chest3'],img=img,threshold=0.8))
    chest4 = len(positions(images['chest4'],img=img,threshold=0.8))
    chest5 = len(positions(images['chest5'],img=img,threshold=0.8))

    logger('Báu Comum: %d' % chest1)
    logger('Báu Marrom: %d' % chest2)
    logger('Báu Roxo: %d' % chest3)
    logger('Báu Amarelo: %d' % chest4)
    logger('Báu Azul: %d' % chest4)

    if chest1 == 1 and chest2 == 0 and chest3 == 0 and chest4 == 0 and chest5 == 0:
        pyautogui.hotkey('ctrl','f5')
        time.sleep(10)
        login()


def activeWindow(currentWindow):
    if sys.platform == 'linux' or sys.platform == 'linux2':
        activate_linux_window(currentWindow["window"])
    else:
        currentWindow["window"].activate()

def main():
    """Main execution setup and loop"""
    # ==Setup==
    global hero_clicks
    global login_attempts
    global last_log_is_progress
    hero_clicks = 0
    login_attempts = 0
    last_log_is_progress = False

    global images
    images = load_images()

    if ch['enable']:
        global home_heroes
        home_heroes = loadHeroesToSendHome()
    else:
        print('>>---> Home feature not enabled')
    print('\n')

    print(cat)
    time.sleep(7)
    t = c['time_intervals']

    windows = []
 
    if sys.platform == 'linux' or sys.platform == 'linux2':
        bombcryptoWindows = get_linux_bombcrypto_windows()
    else:
        bombcryptoWindows = pygetwindow.getWindowsWithTitle('Bombcrypto')

    #  Aqui ele percorre as janelas que estiver escrito bombcrypto
    for window in bombcryptoWindows:
        windows.append({
            "window": window,
            "login": 0,
            "heroes": 0,
            "new_map": 0,
            "check_for_captcha": 0,
            "refresh_heroes": time.time(),
             "register_bcoin": 0,
             "check_chest": 0,
             "metamask_id": '0'
        })



 

    if len(windows) >= 1:
        print('>>---> %d windows with the name bombcrypto were found' % len(windows))

        login()
        return
        while True:
            for currentWindow in windows:
                activeWindow(currentWindow)
          


                time.sleep(2)
                now = time.time()
                
                if currentWindow["metamask_id"] ==  '0':
                  
                    currentWindow["metamask_id"] = getIdMetamask()
                    
                if now - currentWindow["login"] > addRandomness(t['check_for_login'] * 60):
                  
                    sys.stdout.flush()
                    currentWindow["login"] = now
                    login()

                if now - currentWindow["register_bcoin"] >  60 and currentWindow["metamask_id"] != '0':
                  
                    currentWindow["register_bcoin"] = now
                    registerBcoin(currentWindow["metamask_id"])
               
                if now - currentWindow["heroes"] > addRandomness(t['send_heroes_for_work'] * 60):
                
                    currentWindow["heroes"] = now
                    refreshHeroes()

                if now - currentWindow["new_map"] > t['check_for_new_map_button']:
                    
                    currentWindow["new_map"] = now

                    if clickBtn(images['new-map']):
                        loggerMapClicked()


                if now - currentWindow["refresh_heroes"] > addRandomness( t['refresh_heroes_positions'] * 60):
                   
                    currentWindow["refresh_heroes"] = now
                    refreshHeroesPositions()

                #clickBtn(teasureHunt)
                logger(None, progress_indicator=True)

                sys.stdout.flush()

                time.sleep(1)
    else:
        print('>>---> No window with the name bombcrypto was found')


if __name__ == '__main__':



    main()


#cv2.imshow('img',sct_img)
#cv2.waitKey()

# colocar o botao em pt
# soh resetar posiçoes se n tiver clickado em newmap em x segundos


