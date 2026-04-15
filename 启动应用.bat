@echo off
chcp 65001 >nul
title AI 数据分析助手
echo.
echo  ========================================
echo     AI 数据分析助手
echo  ========================================
echo.
echo  正在启动...
echo  启动后浏览器会自动打开
echo  关闭时请直接关闭此窗口
echo.
cd /d "%~dp0"
.venv\Scripts\streamlit run app.py --server.headless true
pause
