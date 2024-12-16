#include <MsgBoxConstants.au3>
#include <WinAPI.au3>

; 检查网络连接
Func CheckNetworkConnection()
    Local $result = Ping("www.baidu.com", 1000)
    If $result = 0 Then
        Return False
    Else
        Return True
    EndIf
EndFunc

; 清理 DNS 缓存
Func ClearDNSCache()
    Local $output = Run("ipconfig /flushdns", "", @SW_HIDE)
    If @error Then
        MsgBox($MB_SYSTEMMODAL, "错误", "清理 DNS 缓存失败：" & @error)
    EndIf
EndFunc

; 重置网络
Func ResetNetwork()
    Local $output = Run("netsh winsock reset", "", @SW_HIDE)
    If @error Then
        MsgBox($MB_SYSTEMMODAL, "错误", "重置网络失败：" & @error)
    EndIf
    $output = Run("ipconfig /release", "", @SW_HIDE)
    If @error Then
        MsgBox($MB_SYSTEMMODAL, "错误", "释放 IP 地址失败：" & @error)
    EndIf
    $output = Run("ipconfig /renew", "", @SW_HIDE)
    If @error Then
        MsgBox($MB_SYSTEMMODAL, "错误", "更新 IP 地址失败：" & @error)
    EndIf
EndFunc

; 主函数
Func Main()
    If Not CheckNetworkConnection() Then
        MsgBox($MB_SYSTEMMODAL, "警告", "网络连接不通，尝试修复...")
        ClearDNSCache()
        ResetNetwork()
    Else
        MsgBox($MB_SYSTEMMODAL, "信息", "网络连接正常")
    EndIf
EndFunc

; 运行主函数
Main()
