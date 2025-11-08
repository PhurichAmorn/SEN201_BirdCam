# BirdCam Flowchart App (openSUSE / WSL)

Hello! Thanks for using the BirdCam Flowchart App.

To run this application on a minimal openSUSE (WSL) environment, you must first install several required system libraries and set file permissions.

This installer will add:
* **graphviz** & **graphviz-gd**: Required to generate flowcharts (and save them as PNGs).
* **libxcb1**: A core graphics library needed to draw the application window.
* **fontconfig**, **libXft2** & **dejavu-fonts**: Required for the system to find and render fonts.

---

## 🖥️ System Requirements

* **Operating System:** openSUSE Leap 15.4 or a compatible Linux distribution.
* **GLIBC Version:** This executable was built on a system with **GLIBC 2.38**. It will **not** run on openSUSE Leap 15.4, which uses **GLIBC 2.31**.
* **Action Required:** To run this application, you must **re-build the executable from its source code on the openSUSE 15.4 system itself.**
* **WSL:** If running on WSL, a version that supports GUI applications is required (e.g., Windows 11).

---

### Instructions

Follow these steps in your terminal to set up and run the application.

1.  **Fix Line Endings (If needed):**
    If you copied these files from Windows, you may need to fix the installer script's line endings.
    ```sh
    sed -i 's/\r$//' install.sh
    ```

2.  **Make Files Executable:**
    You must give both the installer and the app permission to run.
    ```sh
    chmod +x install.sh
    chmod +x BirdCam
    ```

3.  **Run the Installer:**
    Run the installer script to install all dependencies.
    ```sh
    ./install.sh
    ```

4.  **Wait for Installation:**
    The script will ask for your `sudo` password. Wait for it to show "Installation complete."

5.  **Run the App:**
    The installer script will try to start the app automatically. If you want to run it manually later, just type:
    ```sh
    ./BirdCam
    ```