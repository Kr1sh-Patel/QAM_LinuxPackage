import subprocess
import json
import os

def get_certificate_info(cert_path):
    try:
        # Get the subject
        subject_command = f"openssl x509 -in {cert_path} -noout -subject"
        subject_output = subprocess.check_output(subject_command, shell=True).decode().strip()
        subject = subject_output.split("subject=")[-1].strip()

        # Get the thumbprint (SHA-1 fingerprint)
        thumbprint_command = f"openssl x509 -in {cert_path} -noout -fingerprint -sha1"
        thumbprint_output = subprocess.check_output(thumbprint_command, shell=True).decode().strip()
        thumbprint = thumbprint_output.split("Fingerprint=")[-1].replace(":", "").strip()

        return {
            "Subject": subject,
            "Thumbprint": thumbprint
        }
    except subprocess.CalledProcessError as e:
        print(f"Error processing {cert_path}: {e}")
        return None

def main():
    cert_dir = "/etc/ssl/certs/"  # Directory containing certificates
    cert_info_list = []

    for cert_file in os.listdir(cert_dir):
        cert_path = os.path.join(cert_dir, cert_file)
        if os.path.isfile(cert_path):
            cert_info = get_certificate_info(cert_path)
            if cert_info:
                cert_info_list.append(cert_info)

    print(json.dumps(cert_info_list, indent=4))

if __name__ == "__main__":
    main()
