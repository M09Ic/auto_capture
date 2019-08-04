import win32gui, win32ui, win32con, win32api ,win32process
import os,sys,getopt,subprocess

# 调用windows api截图
def window_capture(filename,hwnd):
    # hwnd = win32gui.GetForegroundWindow()
 # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    rect = win32gui.GetWindowRect(hwnd)

    w = rect[2]-rect[0]
    h = rect[3]-rect[1]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)


# 根据pid获取hwnd
def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


opts, args = getopt.getopt(sys.argv[1:], '-t:-p:', ['target','port'])

target = ''
port = ''
for opt_name, opt_value in opts:
    if opt_name in ('-t', '--target'):
        target = opt_value

    if opt_name in ('-p', '--port'):
        port = opt_value




pid = os.getpid()
hwnd = get_hwnds_for_pid(pid)[0]

# 如果存在漏洞则截图
sc = subprocess.Popen('0708detector.exe -t %s -p %s'%(target,port),stdout=subprocess.PIPE)
print('0708detector.exe -t %s -p %s'%(target,port))
flag = 0
while sc.poll() is None:

    line = sc.stdout.readline().strip().decode('utf-8')
    if line != '':
        print(line)
    if 'SERVER IS VULNERABLE' in line:
        flag = 1

if flag == 1:
    window_capture('./img/'+target+'.jpg',hwnd)


