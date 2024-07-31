# QAM Linux Package

This project offers a comprehensive .deb package for Ubuntu 24.04, providing users with a convenient way to view essential system details, including browser information and firewall status.

## Key Features:

* **Easy access to system health:** Quickly gain insights into your system's well-being.
* **Concise presentation:** Focuses on essential system data without clutter.
* **Effortless installation:** Streamlined process for seamless integration into your system.

## Prerequisites:

* Ubuntu 24.04 LTS (Long Term Support)
* Basic familiarity with Git and the command line

## Installation:
### 1. Clone the Repository:

Open a terminal window and navigate to your desired directory. Then, clone the project repository using Git:

```
git clone https://github.com/Kr1sh-Patel/QAM_LinuxPackage.git
```

### 2. Change Directories:

Move into the project directory:

```
cd QAM_LinuxPackage
```

### 3. Make Scripts Executable:

Grant execution permissions to the Python script and the binary executable within the package:

```
chmod +x package-1.0/usr/local/bin/package package.py
```

### 4. Build the `.deb` Package:

Execute the following command to create the `.deb` package:

```
dpkg-deb --build package-1.0
```

This will generate a file named `package-1.0.deb` in the current directory.

### 5. Install the Package (Requires Administrator Privileges):

Use sudo to install the built package with administrator permissions:

```
sudo dpkg -i package-1.0.deb
```

Enter your password (won't be displayed) when prompted.

## Usage:

Once installed, simply run the package command in your terminal to retrieve the system information:

```
package
```
The output will display details about your system, browsers, and firewall status.

## Project Structure:

The project directory holds the following files and directories:

* `package.py`: Python script containing the core functionality.
* `package-1.0.deb`: The generated .deb package.
* `package-1.0/`: Contains the Debian package structure:
* `DEBIAN/`: Stores metadata for the package, including control file.
* `usr/`: Simulated installation directory within the package.
* `local/`: Simulated subdirectory for locally installed files.
* `bin/`: Holds the package executable binary.

## Output Screenshots:
![image](https://github.com/user-attachments/assets/b03773ba-bd1c-4cb6-ab08-2075201b69f3)
![image](https://github.com/user-attachments/assets/13e82736-b42b-4960-8e67-289ae7b600fc)
![image](https://github.com/user-attachments/assets/657d3c24-f168-472d-bdce-0ca087369aa6)

**NOTE:** The above image shows `No browsers found.` in the `BROWSER STATUS` because the package was installed in the VM using a live-server image and not the Graphical User Interface image and no browsers were installed.

## Contributions:

We welcome contributions to this project! Feel free to fork the repository on GitHub, make improvements, and submit pull requests.

This README.md provides a clear, informative guide for users to install and utilize your package effectively. It highlights the value proposition, installation steps, usage instructions, and project structure. Additionally, it encourages contributions to foster collaboration.
