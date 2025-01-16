#RequireAdmin ; 请求管理员权限
#include <GUIConstantsEx.au3>
#include <ProgressConstants.au3>

; 设置GUI窗口大小和位置
$GUI_Width = 300
$GUI_Height = 150
$GUI_X = (@DesktopWidth - $GUI_Width) / 2
$GUI_Y = (@DesktopHeight - $GUI_Height) / 2

; 创建GUI窗口
$hGUI = GUICreate("DNS 清理工具", $GUI_Width, $GUI_Height, $GUI_X, $GUI_Y)

; 创建状态标签
$LabelStatus = GUICtrlCreateLabel("请单击按钮以清理 DNS 缓存", 10, 10, $GUI_Width - 20, 30)

; 创建按钮
$hButton = GUICtrlCreateButton("清理 DNS 缓存", 100, 50, 100, 30)

; 创建进度条
$Progress = GUICtrlCreateProgress(10, 90, $GUI_Width - 20, 20)
GUICtrlSetData($Progress, 0)

; 显示窗口
GUISetState(@SW_SHOW, $hGUI)

; 主循环
While 1
    $nMsg = GUIGetMsg()
    Switch $nMsg
        Case $GUI_EVENT_CLOSE
            Exit
        Case $hButton
            ; 更新状态标签和进度条
            GUICtrlSetData($LabelStatus, "正在清理 DNS 缓存...")
            GUICtrlSetData($Progress, 50)
            Sleep(500) ; 模拟延迟以便用户可以看到进度

            ; 执行清理 DNS 缓存的命令
            Local $iResult = RunWait(@ComSpec & " /c ipconfig /flushdns", "", @SW_HIDE)

            ; 更新进度条
            GUICtrlSetData($Progress, 100)
            Sleep(500) ; 模拟延迟以便用户可以看到进度

            ; 检查命令执行结果并给出提示
            If $iResult = 0 Then
                GUICtrlSetData($LabelStatus, "DNS 缓存已成功清理！")
                MsgBox(64, "提示", "DNS 缓存已成功清理！")
            Else
                GUICtrlSetData($LabelStatus, "清理 DNS 缓存失败，请检查权限或网络设置。")
                MsgBox(16, "错误", "清理 DNS 缅存失败，请检查权限或网络设置。")
            EndIf
    EndSwitch
WEnd