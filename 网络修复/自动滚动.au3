#include <Misc.au3>

Global $g_bScrolling = False

HotKeySet("^9", "StartScrolling") ; Ctrl + 2 ��ʼ����
HotKeySet("^0", "StopScrolling")  ; Ctrl + 3 ֹͣ����

While 1
    If $g_bScrolling Then
        ; ģ�ⰴ�� Page Down ��
        Send("{PGDN}")
        Sleep(2500) ; ���ƹ����ٶȣ���λΪ����
    EndIf
    Sleep(1000) ; ���� CPU ռ�ù���
WEnd

Func StartScrolling()
    $g_bScrolling = True
EndFunc

Func StopScrolling()
    $g_bScrolling = False
EndFunc
