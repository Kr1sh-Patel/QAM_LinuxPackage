import subprocess
import json
import os

def get_certificate_info(cert_path):
    try:
        command = f"openssl x509 -in {cert_path} -noout -subject -fingerprint -sha1"
        output = subprocess.check_output(command, shell=True).decode().strip()

        subject, thumbprint = None, None
        for line in output.splitlines():
            if line.startswith("subject="):
                subject = line.split("subject=")[-1].strip()
            elif line.startswith("sha1 Fingerprint=") or line.startswith("SHA1 Fingerprint="):
                thumbprint = line.split("=")[-1].replace(":", "").strip()

        if subject and thumbprint:
            return {
                "Subject": subject,
                "Thumbprint": thumbprint
            }
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error processing {cert_path}: {e}")
        return None

def main():
    cert_dir = "/etc/ssl/certs/"  # Directory containing certificates
    cert_info_list = []

    for cert_file in os.listdir(cert_dir):
        cert_path = os.path.join(cert_dir, cert_file)
        if os.path.isfile(cert_path) and cert_file.endswith((".pem", ".crt")):
            cert_info = get_certificate_info(cert_path)
            if cert_info:
                cert_info_list.append(cert_info)

    print(json.dumps(cert_info_list, indent=4))

if __name__ == "__main__":
    main()
