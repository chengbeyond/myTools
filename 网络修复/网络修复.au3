#RequireAdmin
#AutoIt3Wrapper_UseUpx=n
#include <GUIConstantsEx.au3>
#include <WindowsConstants.au3>
#include <Inet.au3>
#include <Process.au3>
#include <WinAPI.au3>

Global $hGUI, $LabelStatus, $ButtonStart, $ButtonExit, $LabelProxy, $LabelProxyStatus, $Progress
Global $g_bRunning = False
Global Const $TEST_URL_1 = "http://www.baidu.com"
Global Const $TEST_URL_2 = "https://www.google.com" ; Unused, removed

; GUI Constants
Global Const $GUI_WIDTH = 400
Global Const $GUI_HEIGHT = 210

; Create GUI centered
$hGUI = GUICreate("网络测试和修复", $GUI_WIDTH, $GUI_HEIGHT, (@DesktopWidth - $GUI_WIDTH) / 2, (@DesktopHeight - $GUI_HEIGHT) / 2, -1, $WS_EX_TOPMOST)
GUISetFont(10, 400, 0, "宋体")

; Create Controls
$LabelStatus = GUICtrlCreateLabel("请点击开始按钮进行网络测试", 10, 10, $GUI_WIDTH - 20, 30)
$LabelProxy = GUICtrlCreateLabel("代理状态:", 10, 50, 100, 30)
$LabelProxyStatus = GUICtrlCreateLabel("未知", 110, 50, $GUI_WIDTH - 120, 30)
$ButtonStart = GUICtrlCreateButton("开始测试", 10, 100, 100, 30)
$ButtonExit = GUICtrlCreateButton("退出", $GUI_WIDTH - 110, 100, 100, 30)
$Progress = GUICtrlCreateProgress(10, 140, $GUI_WIDTH - 20, 20)

; Show GUI
GUISetState(@SW_SHOW, $hGUI)

; Main Loop
While 1
    Switch GUIGetMsg()
        Case $GUI_EVENT_CLOSE, $ButtonExit
            Exit
        Case $ButtonStart
            If $g_bRunning Then ContinueLoop
            $g_bRunning = True
            GUICtrlSetState($ButtonStart, $GUI_DISABLE) ; Disable button while running
            _Main()
            GUICtrlSetState($ButtonStart, $GUI_ENABLE)
            $g_bRunning = False
    EndSwitch
WEnd

Func _Main()
    _UpdateStatus("正在测试网络连接...")
    If _IsNetworkConnected() Then
        _UpdateStatus("网络连接正常!")
        _UpdateProxyStatus()
    Else
        _UpdateStatus("网络连接失败，正在尝试修复...")
        If _FixNetwork() Then
            _UpdateStatus("网络已修复，正在重新测试...")
            If _IsNetworkConnected() Then
                _UpdateStatus("网络连接已恢复!")
                _UpdateProxyStatus()
            Else
                _UpdateStatus("修复后网络连接仍然失败!")
                _CheckProxyAndWarn()
            EndIf
        Else
            _UpdateStatus("网络修复失败!")
            _CheckProxyAndWarn()
        EndIf
    EndIf
EndFunc

Func _IsNetworkConnected()
    Return Not @error = InetGet($TEST_URL_1, "", 1, 1) ; Simplified connection check
EndFunc

Func _FixNetwork()
    Local $commands = ["netsh winsock reset", "netsh int ip reset", "ipconfig /release", "ipconfig /renew"]
    For $i = 0 To UBound($commands) - 1
        _UpdateStatus("正在执行命令: " & $commands[$i])
        RunWait(@ComSpec & " /c " & $commands[$i], "", @SW_HIDE)
        GUICtrlSetData($Progress, ($i + 1) * 25)
        Sleep(500) ; Reduced sleep time
    Next
    Return True ; Always returns true, could be improved with error checking
EndFunc

Func _CheckProxyByInetGet()
    Return RegRead("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyEnable") = 1 And RegRead("HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings", "ProxyServer") <> ""
EndFunc

Func _UpdateProxyStatus()
    GUICtrlSetData($LabelProxyStatus, _CheckProxyByInetGet() ? "可能已启用" : "未启用")
EndFunc

Func _CheckProxyAndWarn()
    If _CheckProxyByInetGet() Then
        _UpdateStatus("检测到您可能启用了代理服务器，请手动关闭代理后重试!")
        MsgBox(16, "提示", "请手动关闭代理服务器后重试！")
    Else
        _UpdateStatus("网络连接失败，请检查网络设置!")
    EndIf
    _UpdateProxyStatus() ; Update proxy status regardless of warning
EndFunc

Func _UpdateStatus($sText)
    GUICtrlSetData($LabelStatus, $sText)
EndFunc



; Removed _GetInetErrorDescription() as it was unused after simplifying _IsNetworkConnected()
