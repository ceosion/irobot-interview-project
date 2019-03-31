# Windows PowerShell script for lauching Visual Studio Code in an
# isolated/independent environment. This means that the user data
# and extensions are separate from the main user instance that is
# normally launched when you simply type 'code'.
#
# You can open files in this specific isolated environment by
# using this script again... e.g.
#   ./start-vscode.ps1 file1 file2

# Author: Alex Richard Ford (arf4188@gmail.com)
# Website: http://www.alexrichardford.com
# License: MIT License

$VSCODE = "C:\Users\arf41\AppData\Local\Programs\Microsoft VS Code\Code.exe"
if (-Not (Test-Path $VSCODE)) {
    Write-Error "Visual Studio Code not found at: $VSCODE"
    exit 1
}


& $VSCODE --verbose `
          --user-data-dir ".\.vscode\user-data\" `
          --extensions-dir ".\.vscode\extensions\" `
          ".\arfwiki.code-workspace" `
          $args

