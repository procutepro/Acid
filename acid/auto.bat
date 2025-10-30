@echo off
:: =========================
:: Acid Auto-Build & Upload
:: =========================

echo Cleaning old builds...
rmdir /s /q dist
rmdir /s /q build
rmdir /s /q frogfast.egg-info

echo Building new version...
python -m build

echo Uploading to PyPI...
twine upload dist\*

echo Done! Acid should now be live with the new version.
pause
