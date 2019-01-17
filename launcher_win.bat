@pip install pandas
@cd .\js
@start cmd /k node index.js
@echo London, Paris, SPb3, Toronto
@echo.
:do
@set /p city="Choose the city: "
:while
@if "%city%" == "London" (goto next) else (goto one)
:one
@if "%city%" == "Paris" (goto next) else (goto two)
:two
@if "%city%" == "SPb3" (goto next) else (goto three)
:three
@if "%city%" == "Toronto" (goto next) else (goto do)
:next
@cd ..\
@cd .\python
@explorer http://localhost:8080
@python main.py %city%
pause
