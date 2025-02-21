#include <Misc.au3>

Global $g_bScrolling = False

HotKeySet("^9", "StartScrolling") ; Ctrl + 2 开始滚动
HotKeySet("^0", "StopScrolling")  ; Ctrl + 3 停止滚动

While 1
    If $g_bScrolling Then
        ; 模拟按下 Page Down 键
        Send("{PGDN}")
        Sleep(2500) ; 控制滚动速度，单位为毫秒
    EndIf
    Sleep(1000) ; 避免 CPU 占用过高
WEnd

Func StartScrolling()
    $g_bScrolling = True
EndFunc

Func StopScrolling()
    $g_bScrolling = False
EndFunc
