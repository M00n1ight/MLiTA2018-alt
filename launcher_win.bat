@pip install pandas
@cd .\js
@start cmd /k node index.js
@echo London, Paris, SPb3, Toronto
@echo.
@set /p city="Choose the city: "
@cd ..\
@cd .\python
@explorer http://localhost:8080
@python main.py %city%
pause
