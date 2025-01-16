#AutoIt3Wrapper_UseUpx=n
#include <GUIConstantsEx.au3>
#include <WindowsConstants.au3>
#include <Inet.au3>
#include <Process.au3>
#include <WinAPI.au3>

Global $hGUI, $LabelStatus, $ButtonStart, $ButtonExit, $LabelProxy, $LabelProxyStatus, $Progress
Global $g_bRunning = False
Global $g_bFixing = False
Global Const $TEST_URL_1 = "http://www.baidu.com"
Global Const $TEST_URL_2 = "https://www.google.com"

; 设置GUI窗口大小和位置
$GUI_Width = 400
$GUI_Height = 250
$GUI_X = (@DesktopWidth - $GUI_Width) / 2
$GUI_Y = (@DesktopHeight - $GUI_Height) / 2

; 创建GUI窗口
$hGUI = GUICreate("网络测试和修复", $GUI_Width, $GUI_Height, $GUI_X, $GUI_Y, -1, $WS_EX_TOPMOST)
GUISetFont(10, 400, 0, "宋体")

; 创建状态标签
$LabelStatus = GUICtrlCreateLabel("请点击开始按钮进行网络测试", 10, 10, $GUI_Width - 20, 30)

; 创建代理状态标签
$LabelProxy = GUICtrlCreateLabel("代理状态:", 10, 50, 100, 30)
$LabelProxyStatus = GUICtrlCreateLabel("未知", 110, 50, $GUI_Width - 120, 30)

; 创建开始按钮
$ButtonStart = GUICtrlCreateButton("开始测试", 10, 100, 100, 30)

; 创建退出按钮
$ButtonExit = GUICtrlCreateButton("退出", $GUI_Width - 110, 100, 100, 30)

; 创建进度条
$Progress = GUICtrlCreateProgress(10, 140, $GUI_Width - 20, 20)
GUICtrlSetData($Progress, 0)

; 显示GUI窗口
GUISetState(@SW_SHOW, $hGUI)

; 主循环
While 1
    $msg = GUIGetMsg()
    Switch $msg
        Case $GUI_EVENT_CLOSE, $ButtonExit
            Exit
        Case $ButtonStart
            If $g_bRunning Or $g_bFixing Then
                ContinueLoop
            EndIf
            $g_bRunning = True
            GUICtrlSetData($ButtonStart, "测试中...")
            _Main()

            $g_bRunning = False
    EndSwitch
    Sleep(10)
WEnd

Func _Main()
    GUICtrlSetData($LabelStatus, "正在测试网络连接...")
    $bConnected = _IsNetworkConnected()
    If $bConnected Then
        GUICtrlSetData($LabelStatus, "网络连接正常!")
        _UpdateProxyStatus()
    Else
        GUICtrlSetData($LabelStatus, "网络连接失败，正在尝试修复...")
        $g_bFixing = True
        If _FixNetwork() Then
            GUICtrlSetData($LabelStatus, "网络已修复，正在重新测试...")
            If _IsNetworkConnected() Then
                GUICtrlSetData($LabelStatus, "网络连接已恢复!")
                _UpdateProxyStatus()
            Else
                GUICtrlSetData($LabelStatus, "修复后网络连接仍然失败!")
                _CheckProxyAndWarn()
            EndIf
        Else
            GUICtrlSetData($LabelStatus, "网络修复失败!")
            _CheckProxyAndWarn()
        EndIf
        $g_bFixing = False
    EndIf
    GUICtrlSetData($ButtonStart, "开始测试")
EndFunc

Func _IsNetworkConnected()
    Local $bConnected = InetGet($TEST_URL_1, "", 1, 1)
    If @error Then
        GUICtrlSetData($LabelStatus, "网络连接失败: " & _GetInetErrorDescription(@error))
        Return False
    Else
        Return True
    EndIf
EndFunc

Func _FixNetwork()
    GUICtrlSetData($Progress, 0) ; 重置进度条
    ; 执行网络重置命令
    For $i = 1 To 4
        Local $cmd = ""
        Switch $i
            Case 1
                $cmd = "netsh winsock reset"
            Case 2
                $cmd = "netsh int ip reset"
            Case 3
                $cmd = "ipconfig /release"
            Case 4
                $cmd = "ipconfig /renew"
        EndSwitch

        GUICtrlSetData($LabelStatus, "正在执行命令: " & $cmd)
        RunWait(@ComSpec & " /c " & $cmd, "", @SW_HIDE)
        GUICtrlSetData($Progress, $i * 25) ; 更新进度条
        Sleep(1000) ; 添加延迟以便用户可以看到进度
    Next
    Return True
EndFunc

Func _CheckProxyByInetGet()
    ; 使用 WinAPI 读取注册表来获取代理设置
    Local $sProxyEnable = RegRead("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyEnable")
    Local $sProxyServer = RegRead("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyServer")

    If $sProxyEnable = 1 And $sProxyServer <> "" Then
        Return True ; 启用了代理
    Else
        Return False ; 未启用代理
    EndIf
EndFunc

Func _UpdateProxyStatus()
    If _CheckProxyByInetGet() Then
        GUICtrlSetData($LabelProxyStatus, "可能已启用")
    Else
        GUICtrlSetData($LabelProxyStatus, "未启用")
    EndIf
EndFunc

Func _CheckProxyAndWarn()
    If _CheckProxyByInetGet() Then
        GUICtrlSetData($LabelStatus, "检测到您可能启用了代理服务器，请手动关闭代理后重试!")
        _UpdateProxyStatus()
        MsgBox(16, "提示", "请手动关闭代理服务器后重试！")
    Else
        GUICtrlSetData($LabelStatus, "网络连接失败，请检查网络设置!")
        _UpdateProxyStatus()
    EndIf
EndFunc

Func _GetInetErrorDescription($iError)
    Switch $iError
        Case 1
            Return "无法连接到服务器。"
        Case 2
            Return "无法打开文件。"
        Case 3
            Return "无法写入文件。"
        Case 4
            Return "超时。"
        Case 5
            Return "无效的 URL。"
        Case 6
            Return "无法找到主机。"
        Case 7
            Return "无法连接到服务器。"
        Case 8
            Return "无法读取数据。"
        Case 9
            Return "无法写入数据。"
        Case 10
            Return "无法打开文件。"
        Case 11
            Return "无法写入文件。"
        Case 12
            Return "无法读取数据。"
        Case 13
            Return "无法写入数据。"
        Case 14
            Return "无法连接到服务器。"
        Case 15
            Return "无法读取数据。"
        Case 16
            Return "无法写入数据。"
        Case 17
            Return "无法连接到服务器。"
        Case 18
            Return "无法读取数据。"
        Case 19
            Return "无法写入数据。"
        Case Else
            Return "未知错误 (" & $iError & ")"
    EndSwitch
EndFunc
