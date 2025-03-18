import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CourseOnline.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django environment configuration is abnormal, please check!"
        ) from exc
    execute_from_command_line(sys.argv)
