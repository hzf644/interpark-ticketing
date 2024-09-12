# VPN
# 增加计时
# 从列表选择
# 支持多人
# 侧边分区无判断余票
# 谷歌浏览器
import re
import sys
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from info1 import *

target_url = ""


def Booking():
    # 点击预订
    while True:
        time.sleep(0.1)
        try:
            driver.find_element(By.CSS_SELECTOR,
                                'body > div > div > div.wrap_Pinfo > div.bak > div.Py_Time > div.Date_Select > div.btn_Booking > img').click()
            handles = driver.window_handles
            if len(handles) > 1:
                wait = WebDriverWait(driver, 1)  # 等待最多10秒
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                driver.switch_to.window(handles[1])
                if driver.current_url != 'https://gpoticket.globalinterpark.com/Global/Play/Book/BookMain.asp' and not driver.current_url.startswith("https://tickets.interpark.com/"):
                    driver.close()
                    driver.switch_to.window(handles[0])
                    if driver.current_url != target_url:
                        driver.get(target_url)
                else:
                    break
        except:
            pass
    index = 1
    while True:
        current_url = driver.current_url
        if not current_url.startswith("https://tickets.interpark.com/"):
            Date()
            while True:
                driver.switch_to.frame("ifrmSeat")
                div_element = driver.find_element(By.ID, "divRecaptchaWrap")
                display_style = driver.execute_script("return document.getElementById('divRecaptchaWrap').style.display;")
                if display_style == "none":
                    driver.switch_to.parent_frame()
                    break
                else:
                    driver.switch_to.parent_frame()
                    time.sleep(1)
            ChooseSeat()
            Price()
            InputInfo()
            Pay()
            break
        else:
            print(f"等待中({index})")
            index += 1
            time.sleep(2)


def Date():
    while True:
        time.sleep(0.1)
        try:
            driver.switch_to.frame("ifrmBookStep")
            driver.find_elements(By.ID, 'CellPlayDate')[0].click()
            break
        except:
            driver.switch_to.parent_frame()
    driver.switch_to.parent_frame()
    while True:
        try:
            driver.find_element(By.ID, 'LargeNextBtnImage').click()
            break
        except:
            time.sleep(0.1)


def ChooseSeat():
    """
<area shape="poly" coords="332,275,391,277,392,288,388,304,382,325,330,290" onfocus="this.blur()" href="javascript:GetBlockSeatList('', '', '007')" onmouseover="javascript:EventBlockOver(this, '007')" onmouseout="javascript:EventBlockOut(this, '007')" alt="007Side" title="007Side">
<area shape="poly" coords="144,249,201,262,201,272,201,284,141,286,141,266" onfocus="this.blur()" href="javascript:GetBlockSeatList('', '', '114')" onmouseover="javascript:EventBlockOver(this, '114')" onmouseout="javascript:EventBlockOut(this, '114')">
<area shape="rect" coords="395,277,455,340" onfocus="this.blur()" href="javascript:GetBlockSeatList('', '', '208')" onmouseover="javascript:EventBlockOver(this, '208')" onmouseout="javascript:EventBlockOut(this, '208')" alt="208Side" title="208Side">
<area shape="rect" coords="276,368,347,425" onfocus="this.blur()" href="javascript:GetBlockSeatList('', '', '212')" onmouseover="javascript:EventBlockOver(this, '212')" onmouseout="javascript:EventBlockOut(this, '212')">
<img id="NextStepImage" src="//ticketimage.globalinterpark.com/ticketimage/Global/Play/onestop/G2001/btn_seat_confirm.gif" alt="">
<area shape="rect" coords="326,188,387,277" onfocus="this.blur()" href="javascript:GetBlockSeatList('', '', '004')" onmouseover="javascript:EventBlockOver(this, '004')" onmouseout="javascript:EventBlockOut(this, '004')" alt="004Side" title="004Side">
<area shape="rect" coords="396,132,470,357" onfocus="this.blur()" href="javascript:GetBlockSeatList('', '', '207')" onmouseover="javascript:EventBlockOver(this, '207')" onmouseout="javascript:EventBlockOut(this, '207')" alt="207Side
[Seating P] 100 seat(s)" title="207Side
[Seating P] 100 seat(s)">

/html/body/table/tbody/tr/td/span[3]
/html/body/table/tbody/tr/td/span[8]
//*[@id="TmgsTable"]/tbody/tr/td/map/area[23]
//*[@id="TmgsTable"]/tbody/tr/td/table[2]/tbody/tr/td/map/area[6]
/html/body/table/tbody/tr/td/table[2]/tbody/tr/td/map/area[6]
//*[@id="TmgsTable"]/tbody/tr/td/map[1]/area[25]
/html/body/table/tbody/tr/td/map[1]/area[25]

<span class="SeatN" id="Seats" name="Seats" style="background-color:#A0D53F;" title="[스탠딩 R석] -E구역 입장번호-116" onclick="SelectSeat(this,'5','','E구역 입장번호','116','012')" value="N"><!----></span>
<span class="SeatR"><!----></span>
"""
    ifbreak = False
    while True:
        time.sleep(0.1)
        try:
            driver.switch_to.frame("ifrmSeat")
            side_selects = driver.find_elements(By.XPATH, "//span[@class='select']")
            for area in side_selects:
                match = re.search(r'(\d+)\s*seat\b', area.text)
                if match:
                    seats = int(match.group(1))
                    if seats > 0:
                        area.click()
                        while True:
                            try:
                                driver.find_element(By.XPATH, "//a[contains(@href, 'javascript:fnBlockSeatUpdate')]").click()
                                break
                            except:
                                time.sleep(0.1)
                        while True:
                            try:
                                driver.switch_to.frame("ifrmSeatDetail")
                                available = driver.find_elements(By.XPATH, "//span[@class='SeatN']")
                                if len(available) > 0:
                                    available[0].click()
                                    ifbreak = True
                                    break
                            except:
                                driver.switch_to.parent_frame()
                                time.sleep(0.2)
                if ifbreak:
                    break
            if ifbreak:
                break
            else:
                print("oops！票已被抢光")
                sys.exit(0)
        except:
            pass
    driver.switch_to.parent_frame()
    driver.find_element(By.ID, "NextStepImage").click()
    time.sleep(0.2)


# 选择价格
def Price():
    while True:
        try:
            driver.switch_to.parent_frame()
            driver.switch_to.frame("ifrmBookStep")
            select = driver.find_element(By.NAME, "SeatCount")
            select.find_element(By.XPATH, ".//option[@value='1']").click()
            driver.switch_to.parent_frame()
            driver.find_element(By.ID, "SmallNextBtnImage").click()
            break
        except:
            time.sleep(0.1)


def InputInfo():
    """
<iframe id="ifrmBookStep" name="ifrmBookStep" src="" width="637" height="493" frameborder="0" scrolling="no" title="예매정보 선택 페이지"></iframe>

<input class="txt1" id="PhoneNo" style="width: 90%;" type="text" value="">
<input class="txt1" id="HpNo" style="width: 90%;" type="text" value="">
<select id="SNSChannel"><option value="" class="lang" title="Select">Select</option><option value="SN001">WhatsApp</option><option value="SN002">LINE</option><option value="SN003">KakaoTalk</option><option value="SN004">WeChat</option><option value="SN005">Facebook</option><option value="SN006">Telegram</option></select>
<input class="txt1" id="SNSID" style="width: 50%;" type="text" value="" maxlength="30">

<img src="//ticketimage.globalinterpark.com/ticketimage/Global/Play/onestop/G2001/btn_next_02.gif" id="SmallNextBtnImage" alt="">
    """
    while True:
        try:
            driver.switch_to.parent_frame()
            driver.switch_to.frame("ifrmBookStep")
            driver.find_element(By.ID, "PhoneNo").send_keys(PhoneNo)
            select_element = driver.find_element(By.ID, "SNSChannel")
            from selenium.webdriver.support.ui import Select
            select = Select(select_element)
            select.select_by_visible_text("WeChat")
            driver.find_element(By.ID, "SNSID").send_keys(WeChatID)
            # 下一步
            driver.switch_to.parent_frame()
            driver.find_element(By.ID, "SmallNextBtnImage").click()
            break
        except:
            time.sleep(0.1)


def Pay():
    while True:
        try:
            driver.find_element(By.ID, "SmallNextBtnImage").click()
            break
        except:
            time.sleep(0.1)
    while True:
        try:
            driver.switch_to.frame("ifrmBookStep")
            driver.find_element(By.ID, "CancelAgree").click()
            driver.find_element(By.ID, "CancelAgree2").click()
            driver.switch_to.parent_frame()
            driver.find_element(By.ID, "LargeNextBtnImage").click()
            break
        except:
            time.sleep(0.1)

    handle = None
    while True:
        time.sleep(0.2)
        handles = driver.window_handles
        if len(handles) == 3:
            handle = handles[-1]
            break
    driver.switch_to.window(handle)
    while True:
        try:
            driver.find_element(By.XPATH, "//span[./img[@alt='UnionPay']]").click()
            driver.find_element(By.ID, "unioncardnoTmp").send_keys(credit_card)
            driver.find_element(By.ID, "btnNext").click()
            break
        except:
            time.sleep(0.1)


if __name__ == '__main__':
    args = sys.argv
    target_url = args[1]
    # 浏览器配置对象
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # 打开浏览器
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)
    times = 0
    while True:
        try:
            driver.switch_to.frame("product_detail_area")
            bookingGuide = driver.find_elements(By.XPATH, "//*[@id='bookingGuideLayer']/button")
            if bookingGuide:
                bookingGuide[0].click()
            driver.find_element(By.CSS_SELECTOR,
                                'body > div > div > div.wrap_Pinfo > div.bak > div.Py_Time > div.Date_Select > div.btn_Booking > img')
            break
        except:
            time.sleep(0.2)
            times += 1
            if times >= 100:
                times = 0
                print("尚未开票，刷新页面")
                driver.refresh()
    Booking()
