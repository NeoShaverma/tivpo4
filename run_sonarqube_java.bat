@echo off
echo ========================================
echo SonarQube Analysis for Java
echo ========================================
echo.

echo Step 1: Compiling Java files...
javac TodoList.java
if %errorlevel% neq 0 (
    echo ERROR: Failed to compile TodoList.java
    pause
    exit /b 1
)

javac TodoList_with_errors.java
if %errorlevel% neq 0 (
    echo ERROR: Failed to compile TodoList_with_errors.java
    pause
    exit /b 1
)

echo.
echo Step 2: Checking compiled files...
dir *.class
echo.

echo Step 3: Running SonarQube Scanner...
sonar-scanner

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Analysis completed successfully!
    echo Open http://localhost:9000 to view results
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Analysis failed. Check errors above.
    echo ========================================
)

pause

