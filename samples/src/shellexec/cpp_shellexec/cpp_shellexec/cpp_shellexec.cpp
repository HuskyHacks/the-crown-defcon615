#include <iostream>
#include <windows.h>
#include <ShellApi.h>

int main()
{
    ShellExecute(0, L"open", L"notepad", L"", NULL, SW_SHOW);
}

