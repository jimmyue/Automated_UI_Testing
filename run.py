#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Created on 2026年2月11日
@author: jimmy
'''
# npm.taobao.org/mirrors/chromedriver/
import unittest
import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from htmltestreport import HTMLTestReport
from dotenv import load_dotenv
from my_common import weixin
from pathlib import Path
import ddddocr

#设置环境变量
env_path = './my_common/.env'
load_dotenv(dotenv_path=env_path)


class WAYS(unittest.TestCase):
	@classmethod
	def setUpClass(self): #在所有用例执行前，执行一次
		base_dir = Path(__file__).parent
		self.screenshot_dir = base_dir / 'ScreenShot'
		# 确保目录存在
		self.screenshot_dir.mkdir(exist_ok=True)
		# 清理旧截图
		for file in self.screenshot_dir.glob('*'):
			if file.is_file():
				file.unlink()
				print(f"已删除: {file}")

		#实例化微信通知
		self.wx=weixin.WeChat()
		self.wx.send_text('每日点检正在执行中...请执行完后查看截图\n图片依次为：智库、智见、达示、LaneAi、一汽大众、上汽集团、上汽通用、广汽本田、DMS、威尔森官网、GN、长安海外配置、汽车流通协会、终端支持查询')
		#验证码识别登录重试次数、等待时间
		self.max_retries=5
		self.retry_delay =2

	def setUp(self): #在每个用例执行前，执行一次
		#分布式驱动模式
		options = webdriver.ChromeOptions() # EdgeOptions / FirefoxOptions
		options.add_argument('--headless')
		self.driver = webdriver.Remote(command_executor='http://10.10.22.74:4444/wd/hub', options=options)  #分布式selenium
		self.driver.implicitly_wait(12) #隐形等待
		#本地浏览器模式
		# options = webdriver.ChromeOptions()
		# self.driver=webdriver.Chrome(options=options)	

	def test_iways_login(self):
		'''
		智库-登录
		'''
		username=os.getenv("IWAYS_USERNAME")
		password=os.getenv('IWAYS_PASSWORD')
		url=os.getenv('IWAYS_URL')
		self.driver.get(url)
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		##################IWAYS-登录############################
		time.sleep(1)
		self.find_element('CSS_SELECTOR','#root > div > div > header > div.header-container > div > div.header-user-panel__btn.header-user-panel__btn--plain > span').click()
		time.sleep(1)
		for i in range(8):
			self.find_element('CSS_SELECTOR','#rightSide > ul > li.active').click()
		time.sleep(1)
		self.find_element('CSS_SELECTOR','#rightSide > div > div.footer > div.other-login-type > a:nth-child(1)').click()
		time.sleep(1)
		self.find_element('XPATH','//*[@id="rightSide"]/div/div[1]/div[1]/input').send_keys(username)
		self.find_element('XPATH','//*[@id="rightSide"]/div/div[1]/div[2]/input').send_keys(password+Keys.RETURN)
		checkbox = self.find_element('CLASS_NAME', 'ways-checkbox-input')
		if not checkbox.is_selected():
			checkbox.click()
		self.find_element('CSS_SELECTOR','#rightSide > div > div.form > div.form-item.login > button').click()
		self.takephono('iways','login')
		time.sleep(1)
		words=self.find_element('CSS_SELECTOR', "a.ways-dropdown-link.ways-dropdown-trigger").text
		if 'itways_test' in words:
			print('登录正常')
		else:
			self.wx.send_text('智库登录异常，请查看图片核查')
		self.assertIn('itways_test',words)	
		# self.driver.get(url+"/sales-volume-analysis/wholeMarket")
		# self.takephono('iways','sales')
		# self.driver.get(url+"/price-monitor-analysis/price-analysis/overview")
		# self.takephono('iways','price')
		# self.driver.get(url+"/model-conf/overview")
		# self.takephono('iways','config')

	def test_iev_login(self):
		'''
		智见-登录
		'''
		username=os.getenv("IEV_USERNAME")
		password=os.getenv('IEV_PASSWORD')
		url=os.getenv('IEV_URL')
		self.driver.get(url)
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		#####################登录##############################
		self.find_element('CSS_SELECTOR','#__next > div > section.Header_wrapper__VaBF4 > div > div.Header_profileWrapper__jmjBt > a').click()
		for i in range(8):
			self.find_element('CSS_SELECTOR','#__next > div > section.login_wrapper__ZpTp8 > main > div > div.LoginPanel_header__y3MJq > div.LoginPanel_title__MpUYD > svg').click()
		time.sleep(1)
		self.find_element('CSS_SELECTOR','#__next > div > section.login_wrapper__ZpTp8 > main > div > div.LoginPanel_tab__rvk4Y > div:nth-child(2)').click()
		time.sleep(1)
		username_box=self.find_element('CSS_SELECTOR','#__next > div > section.login_wrapper__ZpTp8 > main > div > div.LoginPanel_form__eW071 > div:nth-child(1) > span > input')
		for char in username: #maxlength="13"需特殊处理
			username_box.send_keys(char)
			time.sleep(0.1)
		self.find_element('CSS_SELECTOR','#__next > div > section.login_wrapper__ZpTp8 > main > div > div.LoginPanel_form__eW071 > div:nth-child(2) > span > input').send_keys(password+Keys.RETURN)
		checkbox = self.find_element('CLASS_NAME', 'ant-checkbox-input')
		if not checkbox.is_selected():
			checkbox.click()
		self.find_element('CSS_SELECTOR','#__next > div > section.login_wrapper__ZpTp8 > main > div > div.LoginPanel_form__eW071 > div.LoginPanel_loginBtn__5Ypip > button > span').click()
		self.takephono('iev','login')
		time.sleep(1)
		words=self.find_element('CSS_SELECTOR', "#__next > div > section.Header_wrapper__VaBF4 > div > div.Header_profileWrapper__jmjBt > div > div.jsx-976186373.Header_username__6NY_3").text
		if 'IT' in words:
			print('登录正常')
		else:
			self.wx.send_text('智见登录异常，请查看图片核查')
		self.assertIn('IT',words)	

	def test_daas_login(self):
		'''
		达示-登录
		'''
		username=os.getenv("DAAS_USERNAME")
		password=os.getenv('DAAS_PASSWORD')
		url=os.getenv('DAAS_URL')
		self.driver.get(url)
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		#####################登录##############################
		self.find_element('CSS_SELECTOR','body > div:nth-child(9) > div > div.ant-modal-wrap.ant-modal-centered > div > div.ant-modal-content > div > div > img.close-icon').click()
		time.sleep(1)
		self.find_element('CSS_SELECTOR','#__layout > section > header > div.daas-header__login > div.header-right > div.button').click()
		time.sleep(1)
		self.find_element('XPATH',"//div[text()='密码登录']").click()
		self.find_element('XPATH',"//input[@placeholder='手机号/用户名']").send_keys(username)
		self.find_element('XPATH',"//input[@placeholder='请输入密码']").send_keys(password+Keys.RETURN)
		checkbox = self.find_element('CLASS_NAME', 'ant-checkbox-input')
		if not checkbox.is_selected():
			checkbox.click()
		self.find_element('XPATH',"//button[contains(@class, 'login-button')]").click()
		self.takephono('daas','login')
		time.sleep(1)
		words=self.find_element('XPATH',"/html/body/div[1]/div/section/header/div[3]/div[2]/div[5]/div/div/div[1]").text
		if 'lizouhuan' in words:
			print('登录正常')
		else:
			self.wx.send_text('达示登录异常，请查看图片核查')
		self.assertIn('lizouhuan',words)	

	def test_ai_login(self):
		'''
		LANEAI-登录
		'''
		username=os.getenv("AI_USERNAME")
		password=os.getenv('AI_PASSWORD')
		url=os.getenv('AI_URL')
		self.driver.get(url)
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		#####################登录##############################
		self.find_element('XPATH','//*[@id="react-joyride-step-0"]/div/div/div/div[3]/button').click()
		time.sleep(1)
		self.find_element('CSS_SELECTOR',"button.bg-primary").click()
		time.sleep(1)
		self.find_element('XPATH','//*[@id="new-chat-dialog"]/div/div[1]/form/div[3]/div[4]/div/div/span').click()
		time.sleep(1)
		self.find_element('ID',"username").send_keys(username)
		self.find_element('ID',"password").send_keys(password+Keys.RETURN)
		checkbox = self.find_element('ID', 'aggree')
		if not checkbox.is_selected():
			checkbox.click()
		self.find_element('XPATH','//*[@id="new-chat-dialog"]/div/div[1]/form/div[3]/button/span').click()
		self.takephono('ai','login')
		time.sleep(1)
		words=self.find_element('XPATH','//*[@id="root"]/div[1]/main/div[1]/div/div/a').text
		if '产品介绍' in words:
			print('登录正常')
		else:
			self.wx.send_text('LANGAI登录异常，请查看图片核查')
		self.assertIn('产品介绍',words)	
		# self.find_element('XPATH','//*[@id="chat-input"]').send_keys('今天天气怎么样？')
		# time.sleep(1)
		# self.find_element('XPATH','//*[@id="chat-submit"]/span').click()
		# self.takephono('ai','ask')
		# words=self.find_element('XPATH',"//div[@role='article']").text
		# self.assertIn('天气',words)	

	def test_faw_login(self):
		'''
		一汽大众-登录
		'''
		username=os.getenv("FAW_USERNAME")
		password=os.getenv('FAW_PASSWORD')
		url=os.getenv('FAW_URL')
		self.driver.get(url)
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		#####################登录##############################
		time.sleep(1)
		self.find_element('ID',"username").send_keys(username)
		self.find_element('ID',"password").send_keys(password+Keys.RETURN)
		self.takephono('faw','login')
		time.sleep(1)
		words=self.find_element('XPATH',"//div[@class='appname']").text
		if '价量分析系统' in words:
			print('登录正常')
		else:
			self.wx.send_text('一汽大众登录异常，请查看图片核查')
		self.assertIn('价量分析系统',words)	

	def test_saic_login(self):
		'''
		上汽集团-登录
		'''
		username=os.getenv("SAIC_USERNAME")
		password=os.getenv('SAIC_PASSWORD')
		url=os.getenv('SAIC_URL')
		self.driver.get(url)
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		#####################登录##############################
		time.sleep(1)
		for attempt in range(1, self.max_retries + 1): #登录重试
			print(f"【上汽集团】🔄 第 {attempt} 次登录尝试...")
			try:
				element=self.find_element('ID',"yanZhengMa")
				img_bytes = element.screenshot_as_png
				ocr = ddddocr.DdddOcr(show_ad=False)
				auth_code = ocr.classification(img_bytes)
				time.sleep(0.3)		
				self.find_element('ID',"login_username").send_keys(username)
				self.find_element('ID',"login_password").send_keys(password)
				self.find_element('ID',"login_authCode").send_keys(auth_code+Keys.RETURN)
				time.sleep(1)
				current_url = self.driver.current_url
				if current_url!=url: #通过URL判断是否登录成功
					break
				else:
					input_username=self.find_element('ID',"login_username")
					input_username.click()
					input_username.send_keys(Keys.CONTROL, 'a')  # 全选
					input_username.send_keys(Keys.DELETE)        # 删除
					input_password=self.find_element('ID',"login_password")
					input_password.click()
					input_password.send_keys(Keys.CONTROL, 'a')  # 全选
					input_password.send_keys(Keys.DELETE)        # 删除
					input_code=self.find_element('ID',"login_authCode")
					input_code.click()
					input_code.send_keys(Keys.CONTROL, 'a')  # 全选
					input_code.send_keys(Keys.DELETE)        # 删除
					time.sleep(self.retry_delay+attempt)
					continue
			except Exception as e:
				print(f"【上汽集团】⚠️ 登录过程异常: {str(e)}")
				if attempt == self.max_retries:
					raise
		self.takephono('saic','login')
		time.sleep(1)
		words=self.find_element('XPATH','//*[@id="header"]/div/div/div[4]/ul/li/a/span').text
		if '2023' in words:
			print('登录正常')
		else:
			self.wx.send_text('上汽集团登录异常，请查看图片核查')
		self.assertIn('2023',words)	

	def test_sgm_login(self):
		'''
		SGM-登录
		'''
		username=os.getenv("SGM_USERNAME")
		password=os.getenv('SGM_PASSWORD')
		url=os.getenv('SGM_URL')
		self.driver.get(url)
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		##################IWAYS-登录############################
		time.sleep(1)
		self.find_element('ID','j_username').send_keys(username)
		self.find_element('ID','j_password').send_keys(password + Keys.RETURN)
		time.sleep(1)
		if '系统登录' in self.driver.title:
			self.find_element('XPATH','//*[@id="Button1"]').click()
		time.sleep(1)
		if '密码过期提醒' in self.driver.title:
			self.find_element('XPATH','//*[@id="authenForm"]/fieldset/div/div[2]/button[2]').click()
		time.sleep(1)
		if '信息补充提醒' in self.driver.title:
			self.find_element('XPATH','//*[@id="ignore"]').click()
		self.takephono('sgm','login')
		time.sleep(1)
		words = self.driver.current_url
		if 'mos1.sgms.saic-gm.com' in words:
			print('登录正常')
		else:
			self.wx.send_text('上汽通用登录异常，请查看图片核查')
		self.assertIn('mos1.sgms.saic-gm.com',words)	

	def test_honda_login(self):
		'''
		广汽本田-登录
		'''
		username=os.getenv("HONDA_USERNAME")
		password=os.getenv('HONDA_PASSWORD')
		url=os.getenv('HONDA_URL')
		sales_url=os.getenv('HONDA_SALES_URL')
		self.driver.get(url)
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		#####################登录##############################
		time.sleep(1)
		for attempt in range(1, self.max_retries + 1): #登录重试
			print(f"【广汽本田】🔄 第 {attempt} 次登录尝试...")
			try:
				element=self.find_element('ID',"s-canvas")
				img_bytes = element.screenshot_as_png
				ocr = ddddocr.DdddOcr(show_ad=False)
				auth_code = ocr.classification(img_bytes)
				time.sleep(0.3)		
				self.find_element('ID',"username").send_keys(username)
				self.find_element('ID',"password").send_keys(password)
				self.find_element('ID',"code").send_keys(auth_code+Keys.RETURN)
				time.sleep(1)
				current_url = self.driver.current_url
				if current_url!=url: #通过URL判断是否登录成功
					break
				else:
					input_username=self.find_element('ID',"username")
					input_username.click()
					input_username.send_keys(Keys.CONTROL, 'a')  # 全选
					input_username.send_keys(Keys.DELETE)        # 删除
					input_password=self.find_element('ID',"password")
					input_password.click()
					input_password.send_keys(Keys.CONTROL, 'a')  # 全选
					input_password.send_keys(Keys.DELETE)        # 删除
					input_code=self.find_element('ID',"code")
					input_code.click()
					input_code.send_keys(Keys.CONTROL, 'a')  # 全选
					input_code.send_keys(Keys.DELETE)        # 删除
					time.sleep(self.retry_delay+attempt)
					continue
			except Exception as e:
				print(f"【广汽本田】⚠️ 登录过程异常: {str(e)}")
				if attempt == self.max_retries:
					raise

		self.takephono('honda','login')
		time.sleep(1)
		words = self.driver.current_url
		if 'miap.ghac.cn/manf' in words:
			print('登录正常')
		else:
			self.wx.send_text('广汽本田登录异常，请查看图片核查')
		self.assertIn('miap.ghac.cn/manf',words)	


	def test_dms_login(self):
		'''
		DMS-登录
		'''
		username=os.getenv("DMS_USERNAME")
		password=os.getenv('DMS_PASSWORD')
		url=os.getenv('DMS_URL')
		self.driver.get(url)
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		##################IWAYS-登录############################
		self.find_element('ID','username').send_keys(username)
		self.find_element('ID','password').send_keys(password + Keys.RETURN)
		time.sleep(3)
		self.find_element('CSS_SELECTOR','#pillswithdropdowns > div > div > div.nav-collapse.collapse.navbar-inverse-collapse.pillswithdropdowns > ul > li > a').click()
		time.sleep(1)
		self.takephono('dms','login')
		time.sleep(1)
		words=self.find_element('XPATH',"//a[contains(text(), 'dlrstest')]").text
		if 'dlrstest' in words:
			print('登录正常')
		else:
			self.wx.send_text('DMS登录异常，请查看图片核查')
		self.assertIn('dlrstest',words)	

	def test_no_login_url(self):
		'''
		不用登录系统
		'''
		#智库
		self.driver.get(os.getenv('WAYS_URL'))
		self.driver.set_window_size(1920,1080) #浏览器分辨率设置
		time.sleep(1)
		self.takephono('ways','dashboard')
		#GN
		self.driver.get(os.getenv('GN_URL'))
		time.sleep(6)
		self.takephono('gn','dashboard')
		#海外配置
		self.driver.get(os.getenv('GN_OVERSEAS_URL'))
		self.takephono('gn_overseas','dashboard')
		#汽车流通协会
		self.driver.get(os.getenv('CADA_URL'))
		self.takephono('cada','dashboard')
		#汽车流通协会
		self.driver.get(os.getenv('TERMINAL_URL'))
		self.takephono('terminal','dashboard')

	def takephono(self,name,row):#截图
		time.sleep(6)
		file_name='./ScreenShot/'+name+'_'+row+'.png'
		self.driver.save_screenshot(file_name)
		print(file_name+' 截图成功！')

	def find_element(self,type,element):#定位元素方法封装
		try:
			if type=='CSS_SELECTOR':
				do=WebDriverWait(self.driver, 10, 0.2).until( EC.presence_of_element_located((By.CSS_SELECTOR,element)) )
			elif type=='XPATH':
				do=WebDriverWait(self.driver, 10, 0.2).until( EC.presence_of_element_located((By.XPATH,element)) )
			elif type=='ID':
				do=WebDriverWait(self.driver, 10, 0.2).until( EC.presence_of_element_located((By.ID,element)) )
			elif type=='NAME':
				do=WebDriverWait(self.driver, 10, 0.2).until( EC.presence_of_element_located((By.NAME,element)) )
			elif type=='CLASS_NAME':
				do=WebDriverWait(self.driver, 10, 0.2).until( EC.presence_of_element_located((By.CLASS_NAME,element)) )
			elif type=='TAG_NAME':
				do=WebDriverWait(self.driver, 10, 0.2).until( EC.presence_of_element_located((By.TAG_NAME,element)) )
			elif type=='LINK_TEXT':
				do=WebDriverWait(self.driver, 10, 0.2).until( EC.presence_of_element_located((By.LINK_TEXT,element)) )
			elif type=='PARTIAL_LINK_TEXT':
				do=WebDriverWait(self.driver, 10, 0.2).until( EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,element)) )
			else:
				print('定位元素方法错误！')
			return do
		except Exception as e:
			raise

	def tearDown(self): #在每个用例执行后，执行一次
		#退出浏览器
		time.sleep(1)
		self.driver.quit()

	@classmethod
	def tearDownClass(self): #在所有用例执行后，执行一次
		iways_pic=[
			['智库登录截图','./ScreenShot/iways_login.png'],
			['智见登录截图','./ScreenShot/iev_login.png'],
			['达示登录截图','./ScreenShot/daas_login.png'],
			['LaneAi登录截图','./ScreenShot/ai_login.png'],
			['一汽大众登录截图','./ScreenShot/faw_login.png'],
			['上汽集团登录截图','./ScreenShot/saic_login.png'],
			['上汽通用登录截图','./ScreenShot/sgm_login.png'],
			['广汽本田登录截图','./ScreenShot/honda_login.png'],
			['DMS登录截图','./ScreenShot/dms_login.png'],
			['威尔森官网截图','./ScreenShot/ways_dashboard.png'],
			['GN截图','./ScreenShot/gn_dashboard.png'],
			['长安海外配置截图','./ScreenShot/gn_overseas_dashboard.png'],
			['汽车流通协会截图','./ScreenShot/cada_dashboard.png'],
			['终端支持查询截图','./ScreenShot/terminal_dashboard.png'],
		]
		# 发送核查图片到微信
		for pic in iways_pic:
			try:
				if os.path.exists(pic[1]):
					mediaid=self.wx.upload_media(pic[1])
					# 图文发送
					# self.wx.send_mpnews(mediaid,pic[0],'请查看图片，核查系统是否正常！')
					# 图片发送
					self.wx.send_image(mediaid)
				else:
					text=pic[0]+'，文件不存在！'
					print(text)
					#self.wx.send_text(text)
			except:
				print(str(e))

def findAllFile(base):#获取文件夹下所有文件
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f
	
if __name__ == "__main__":
	suite = unittest.TestSuite()
	suite.addTest(WAYS("test_iways_login")) 
	suite.addTest(WAYS("test_iev_login"))
	suite.addTest(WAYS("test_daas_login"))
	suite.addTest(WAYS("test_ai_login"))
	suite.addTest(WAYS("test_faw_login"))
	suite.addTest(WAYS("test_saic_login"))
	suite.addTest(WAYS("test_sgm_login"))
	suite.addTest(WAYS("test_honda_login"))
	suite.addTest(WAYS("test_dms_login"))
	suite.addTest(WAYS("test_no_login_url"))
	now = time.strftime("%Y%m%d", time.localtime(time.time()))
	file_path = "./Result/index.html"
	file_result = open(file_path, 'wb')
	HTMLTestReport(file_path,'UI自动化测试报告','每日系统点检UI测试').run(suite)
	file_result.close()
