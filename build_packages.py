import os
import shutil
import subprocess

BASE_DIR = os.path.join(os.getcwd(), "QAM","command_name")

def make_executable(path):
    """Make a file executable (chmod +x)"""
    mode = os.stat(path).st_mode
    os.chmod(path, mode | 0o111)

def main():
    if not os.path.isdir(BASE_DIR):
        print(f"ERROR: Directory {BASE_DIR} not found")
        return

    for file in os.listdir(BASE_DIR):
        if not file.endswith(".py"):
            continue

        pkg_name = file[:-3]
        name = pkg_name.split("_", 1)[0]
        build_dir = f"{name}-1.0"
        debian_dir = os.path.join(build_dir, "DEBIAN")
        bin_dir = os.path.join(build_dir, "usr", "local", "bin")

        #clean up previous build if exists
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)

        #create folder structure
        os.makedirs(debian_dir, exist_ok=True)
        os.makedirs(bin_dir, exist_ok=True)

        #copy file and remove .py extension in target
        src_file = os.path.join(BASE_DIR, file)
        dest_file = os.path.join(bin_dir, name)
        shutil.copy(src_file, dest_file)
        make_executable(dest_file)

        #create DEBIAN/control file
        control_content = f"""Package: {name}
Version: 1.0
Section: base
Priority: optional
Architecture: all
Maintainer: Krish krish@example.com
Description: Installs {file} as a standalone script
"""

        with open(os.path.join(debian_dir, "control"), "w") as f:
            f.write(control_content)

        #build the .deb
        deb_file = f"{name}-1.0.deb"
        print(f"[+] Building Package: {deb_file}")
        subprocess.run(["dpkg-deb", "--build", build_dir, deb_file], check=True)

        #extract the .deb into a folder for verification
        extract_dir = f"{name}-1.0-extracted"
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir, exist_ok=True)

        print(f"[+] Extracting {deb_file} to {extract_dir}")
        subprocess.run(["sudo", "dpkg", "-i", deb_file], check=True)
        subprocess.run(["sudo", "rm", "-rf", build_dir, extract_dir, deb_file], check=True)

    print("\n All packages built and extracted successfully.")        

if __name__ == "__main__":
    main()
