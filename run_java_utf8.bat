@echo off
chcp 65001 >nul
javac -encoding UTF-8 %1.java
java -Dfile.encoding=UTF-8 -Dconsole.encoding=UTF-8 %1

