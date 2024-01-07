import subprocess

def write_pytorch_cuda_install_command():
    try:
        result = subprocess.run(['nvcc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            # get cuda version
            cuda_version = result.stdout.split()[18].strip(",").strip(" ").replace(".", "")
            # build command
            pytorch_cuda_install = f"pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu{cuda_version} --upgrade"
            # write command to file
            with open(".\.pytorch_cuda_install_command.txt", "w") as f:
                f.write(pytorch_cuda_install)
        else:
            return False
    except Exception as e:
        print("An error occurred. Maybe you do not have CUDA installed", str(e))
        return False

if __name__ == "__main__":
    write_pytorch_cuda_install_command()
