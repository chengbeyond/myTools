#AutoIt3Wrapper_UseUpx=n
#include <GUIConstantsEx.au3>
#include <WindowsConstants.au3>
#include <Inet.au3>
#include <Process.au3>

Global $hGUI, $LabelStatus, $ButtonStart, $ButtonExit, $LabelProxy, $LabelProxyStatus
Global $g_bRunning = False
Global $g_bFixing = False

; 设置GUI窗口大小和位置
$GUI_Width = 400
$GUI_Height = 200
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
$ButtonExit = GUICtrlCreateButton("退出", $GUI_Width-110, 100, 100, 30)

; 显示GUI窗口
GUISetState(@SW_SHOW, $hGUI)

; 主循环
While 1
    $msg = GUIGetMsg()
    Switch $msg
        Case $GUI_EVENT_CLOSE,$ButtonExit  ; 修改这里，增加 $ButtonExit 的处理
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
WEnd

Func _Main()
    GUICtrlSetData($LabelStatus, "正在测试网络连接...")
    $bConnected = _IsNetworkConnected()
    If $bConnected Then
        GUICtrlSetData($LabelStatus, "网络连接正常!")
        _CheckProxyAndSetLabel()
    Else
        GUICtrlSetData($LabelStatus, "网络连接失败，正在尝试修复...")
        $g_bFixing = True
        If _FixNetwork() Then
            GUICtrlSetData($LabelStatus, "网络已修复，正在重新测试...")
            If _IsNetworkConnected() Then
                GUICtrlSetData($LabelStatus, "网络连接已恢复!")
               _CheckProxyAndSetLabel()
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
    GUICtrlSetData($ButtonStart, "开始测试") ; 在 _Main 函数末尾恢复按钮文字
EndFunc

Func _IsNetworkConnected()
    ; 尝试访问一个已知可靠的网址
    Local $bConnected = InetGet("http://www.baidu.com", "", 1)
    If @error Then
        Return False
    Else
        Return True
    EndIf
EndFunc

Func _FixNetwork()
    ; 执行网络重置命令
    Local $iRet = RunWait(@ComSpec & " /c netsh winsock reset & netsh int ip reset & ipconfig /release & ipconfig /renew", "", @SW_HIDE)
    If $iRet = 0 Then
        Return True
    Else
        Return False
    EndIf
EndFunc

Func _CheckProxyByInetGet()
    Local $bConnected = InetGet("http://www.baidu.com", "", 1)
    If @error Then
         Local $bConnected2 = InetGet("https://www.google.com", "", 1)
         If @error Then
             Return True ; 可能使用了代理
         Else
              Return False ; 没有使用代理
         EndIf
    Else
         Return False ; 没有使用代理
    EndIf
EndFunc

Func _CheckProxyAndSetLabel()
    if _CheckProxyByInetGet() Then
        GUICtrlSetData($LabelProxyStatus, "可能已启用")
    Else
        GUICtrlSetData($LabelProxyStatus, "未启用")
    EndIf
EndFunc

Func _CheckProxyAndWarn()
    ; 检查是否启用了手动代理
    If _CheckProxyByInetGet() Then
       GUICtrlSetData($LabelStatus, "检测到您可能启用了代理服务器，请手动关闭代理后重试!")
        _CheckProxyAndSetLabel()
        MsgBox(16,"提示","请手动关闭代理服务器后重试！")
    Else
       GUICtrlSetData($LabelStatus, "网络连接失败，请检查网络设置!")
        _CheckProxyAndSetLabel()
    EndIf
EndFunc
