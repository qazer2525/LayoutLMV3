@echo off
:menu
cls
echo Welcome to LayoutLMV3 model's menu. Done by @qazer25
echo Choose an option:
echo 1. Install
echo 2. Login to HuggingFace
echo 3. Convert_pdf_to_dataset
echo 4. Convert_label_to_layout
echo 5. Training from base
echo 6. Fine-tuning
echo 7. Launch label-studio
echo 8. Compile inference
echo 9. Run inference
echo 0. Exit
set "choice="
set /p choice="Enter the number of your choice: "

if "%choice%" == "1" (
    pip install poetry & poetry install & poetry run pip install label-studio
    pause
    goto menu
) else if "%choice%" == "2" (
    poetry run python .\login.py
    pause
    goto menu
) else if "%choice%" == "3" (
    poetry run python .\Convert_pdf_to_images.py & poetry run python .\create_LMv3_dataset_with_Pytesseract.py
    pause
    goto menu
) else if "%choice%" == "4" (
    poetry run python Label_studio_to_layoutLMV3.py
    pause
    goto menu
)  else if "%choice%" == "5" (
    cd /d ".\src"
    poetry run python train_new.py
    pause
    cd /d ".."
    goto menu
) else if "%choice%" == "6" (
    cd /d ".\src"
    poetry run python train_repo.py
    pause
    cd /d ".."
    goto menu
) else if "%choice%" == "7" (
    echo Spawning 2 cmd windows, do not close until you are done with label studios
    start /min /d ".\files\images" poetry run python simple_http_server.py
    start /min poetry run label-studio
    pause
    goto menu
) else if "%choice%" == "8" (
    cd /d ".\src"
    poetry run python -m nuitka .\inference.py
    cd /d ".."
    pause
    goto menu
) else if "%choice%" == "9" (
    cd /d ".\src"
    poetry run python .\inference.py
    cd /d ".."
    pause
    goto menu
) else if "%choice%" == "0" (
    exit
) else (
    echo Invalid choice. Please try again.
    pause
    goto menu
)